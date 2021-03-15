from collections import OrderedDict
from dataclasses import dataclass
from ontomem.frame import Frame
from ontomem.memory import MemoryManager
from typing import List, Union

import re


# The lexicon is a heavy wrapper around the OntoMem memory.
# It takes lexicon frames and converts them (as needed) into Word and Sense object instances which are cached
# in the lexicon instance.
# As the analysis task writes temporary (per-sentence) lexicon senses from the syntax, those senses are parsed
# from the lisp input and stored in the lexicon instance - not in the OntoMem memory; consequently, they are
# "forgotten" when the next sentence runs (the lexicon instance is remade).
class Lexicon(object):

    _null_sense = None

    @classmethod
    def null_sense(cls) -> "Sense":
        if Lexicon._null_sense is None:
            Lexicon._null_sense = Sense(
                "NULL", "", SynStruc(OrderedDict()), SemStruc({}), []
            )
        return Lexicon._null_sense

    def __init__(self):
        self.sense_cache = {}

    def sense(self, id: str) -> "Sense":
        # If the requested id is nulled, return the singleton null sense.
        # TODO: replace this detection with a check for the explicit null sense flag
        if not re.findall("-[A-Z]+[0-9]+$", id):
            return Lexicon.null_sense()

        if id not in self.sense_cache:
            lexword = Frame("LEX-WORD")

            # Find all slots that are SENSE=id
            slots = MemoryManager.memory.slots_by_filler[id]
            slots = filter(lambda s: s[-1] == "SENSE", slots)

            # Find all frames that own those slots that are isa=LEX-WORD
            frames = map(lambda s: Frame(s[0]), slots)
            frames = filter(lambda f: f.isa(lexword), frames)
            frames = list(frames)

            # Find all frames that fit the desired POS
            pos = [re.findall(r"(\w+?)(\d+)", id.split("-")[-1])[0]][0][0]
            frames = [f for f in frames if pos in str(f).split(".", 1)[-1]]

            # There should be exactly one (if it is defined)
            if len(frames) == 0:
                raise Exception("Unknown lexical sense %s." % id)
            if len(frames) > 1:
                raise Exception("More than one match found for lexical sense %s." % id)

            # Parse the frame into a sense, and cache it
            frame = frames[0]
            s = Sense.from_frame(frame)
            self.sense_cache[id] = s

        return self.sense_cache[id]

    def add_sense(self, sense: "Sense"):
        self.sense_cache[sense.id] = sense

    def to_str(self) -> str:
        s = ""
        for k, sense in self.sense_cache.items():
            s += f"\n{k}"
            s += sense.to_str()
        return s


class Sense(object):
    @classmethod
    def parse_lisp(cls, lisp: list) -> "Sense":
        id = lisp[0]

        pos = None
        synstruc: list = None
        semstruc: list = None
        meaning_procedures: list = []

        for e in lisp:
            if type(e) != list:
                continue
            if e[0] == "CAT":
                pos = e[1]
            elif e[0] == "SYN-STRUC":
                synstruc = e[1]
            elif e[0] == "SEM-STRUC":
                semstruc = e[1:]
            elif e[0] == "MEANING-PROCEDURES":
                meaning_procedures = e[1:]

        def parse_synstruc(l: list, d: OrderedDict) -> OrderedDict:
            if l is None:
                return d

            for e in l:
                if type(e[1]) == str:
                    d[e[0]] = e[1]
                elif type(e[1]) == list:
                    d[e[0]] = parse_synstruc(e[1], type(d)())
            return d

        def parse_semstruc(l: list) -> dict:
            semstruc = {}
            for e in l:
                head = e[0]
                semstruc[head] = {}
                for p in e[1:]:
                    property = p[0]
                    filler = p[1]
                    if type(filler) == list:
                        filler = {filler[0]: filler[1]}
                    semstruc[head][property] = filler

            return semstruc

        def parse_meaning_procedures(l: list) -> list:
            mps = []
            for mp in l:
                mps.append(MeaningProcedure(mp))

            return mps

        synstruc: OrderedDict = parse_synstruc(synstruc, OrderedDict())
        semstruc: dict = parse_semstruc(semstruc)
        meaning_procedures: list = parse_meaning_procedures(meaning_procedures)

        return Sense(
            id, pos, SynStruc(synstruc), SemStruc(semstruc), meaning_procedures
        )

    @classmethod
    def from_frame(cls, frame: Frame) -> "Sense":
        id = frame["SENSE"].singleton()
        pos = frame["CAT"].singleton()
        synstruc = SynStruc(frame["SYN-STRUC"].singleton())
        semstruc = SemStruc(frame["SEM-STRUC"].singleton())
        meaning_procedures = list(
            map(
                lambda mp: MeaningProcedure(mp), frame["MEANING-PROCEDURES"].singleton()
            )
        )

        sense = Sense(id, pos, synstruc, semstruc, meaning_procedures)
        return sense

    def __init__(
        self,
        id: str,
        pos: str,
        synstruc: "SynStruc",
        semstruc: "SemStruc",
        meaning_procedures: List["MeaningProcedure"],
    ):
        self.id = id
        self.pos = pos
        self.synstruc = synstruc
        self.semstruc = semstruc
        self.meaning_procedures = meaning_procedures

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "pos": self.pos,
            "synstruc": self.synstruc.to_dict(),
            "semstruc": self.semstruc.to_dict(),
        }

    def to_str(self) -> str:
        # s = f"\tid: {self.id}\n\tpos: {self.pos}\n\tsynstruc: {self.synstruc.to_str()}\n\tsemstruc: {self.semstruc.to_str()}"
        s = f"\n\tid: {self.id}\n"
        s += f"\tpos: {self.pos}\n"
        s += f"\tsynstruc: {self.synstruc.to_str()}\n"
        s += f"\tsemstruc: {self.semstruc.to_str()}"
        return s

    def __repr__(self):
        return f"{self.id}"


# SynStruc is a simple object wrapper for now; an ordered dict matching the database representation is sufficient
# as the semantic analyzer doesn't current use the synstruc.
class SynStruc(object):
    def __init__(self, data: OrderedDict):
        self.data = data

    def to_dict(self) -> dict:
        return self.data

    def to_str(self) -> str:
        s = ""
        for k, v in self.data.items():
            s += f"\n\t\t{k}: {v}"
        return s

    def __eq__(self, other):
        if isinstance(other, SynStruc):
            return self.data == other.data
        return super().__eq__(other)


# For now, SemStruc will be a simple object wrapper; this will be improved in the near future.
class SemStruc(object):

    MPS = {
        "FIND-NOUN-ATTRIBUTE",
        "APPLY-COUNT-NP",
        "ABSOLUTE-TIME",
        "SEEK-SPONSOR-IN-TEXT",
        "PASS-THROUGH-MEANING",
        "INCREASE-IN-VALUE",
        "FIND-ANCHOR-SPEAKER",
        "APPLY-MEANING",
        "FIND-ANCHOR-PLACE",
        "SEEK-CONTEXTUAL-SPONSOR",
        "FIND-ANCHOR-TIME",
        "REQUEST-INFO-TRACE",
        "EVALUATED-ACCORDINT-TO",
        "COMBINE-TIME",
        "CALCULATE-QUOTIENT",
        "COREF",
        "COMBINE-AMOUNT",
    }

    IEQS = {"=", ">", "<", "><", ">=<", ">=", "<=", "OR", "NOT"}

    @dataclass
    class Head:
        concept: str = "ALL"
        contents: dict = None

    @dataclass
    class Sub:
        index: int
        concept: str = "ALL"
        contents: dict = None

    @dataclass
    class RefSem:
        index: int
        semstruc: "SemStruc" = None

    @dataclass
    class Variable:
        index: int
        contents: dict = None

    def __init__(self, data: Union[dict, list, str]):
        if data == "":
            data = {}
        if isinstance(data, str):
            data = {data: {}}
        if isinstance(data, list):
            data = {data[0]: {}}

        self.data = data

    def elements(
        self,
    ) -> List[
        Union["SemStruc.Head", "SemStruc.Sub", "SemStruc.RefSem", "SemStruc.Variable"]
    ]:
        results = []

        sub_index = 0
        for k, v in self.data.items():
            if k.startswith("REFSEM"):
                index = int(k.replace("REFSEM", ""))
                results.append(SemStruc.RefSem(index, SemStruc(v)))
                continue
            if k.startswith("^$VAR"):
                index = int(k.replace("^$VAR", ""))
                results.append(SemStruc.Variable(index, v))
                continue

            # TODO: Here, if k is not a concept, probably should error, skip, or output some sort of "other"
            if sub_index == 0:
                results.append(SemStruc.Head(k, v))
                sub_index += 1
            else:
                results.append(SemStruc.Sub(sub_index, k, v))
                sub_index += 1

        return results

    def head(self) -> Union["SemStruc.Head", None]:
        for e in self.elements():
            if isinstance(e, SemStruc.Head):
                return e

        return None

    def subs(self) -> List["SemStruc.Sub"]:
        return list(filter(lambda e: isinstance(e, SemStruc.Sub), self.elements()))

    def refsems(self) -> List["SemStruc.RefSem"]:
        return list(filter(lambda e: isinstance(e, SemStruc.RefSem), self.elements()))

    def variables(self) -> List["SemStruc.Variable"]:
        return list(filter(lambda e: isinstance(e, SemStruc.Variable), self.elements()))

    def to_dict(self) -> dict:
        return self.data

    def to_str(self) -> str:
        s = ""
        for k, v in self.data.items():
            s += f"\n\t\t{k}: {v}"
        return s

    def __repr__(self):
        return repr(self.data)

    def __eq__(self, other):
        if isinstance(other, SemStruc):
            return self.data == other.data
        return super().__eq__(other)


class MeaningProcedure(object):
    def __init__(self, data: List[Union[str, List[str]]]):
        if len(data) == 0:
            data = ["UNKNOWN-MP"]
        self.data = data

    def name(self) -> str:
        return self.data[0]

    def parameters(self) -> List[Union[str, List[str]]]:
        return self.data[1:]

    def __eq__(self, other):
        if isinstance(other, MeaningProcedure):
            return self.data == other.data
        return super().__eq__(other)
