from ontogen.knowledge.lexicon import Lexicon, Sense
from ontogen.knowledge.ontology import Ontology
from ontogen.engine.candidate import RealizationCandidate
from ontogen.config import OntoGenConfig

from typing import Any, List, Union

import ast
import re


class oTMR:
    def __init__(
        self, config: OntoGenConfig, ontology: Ontology = None, lexicon: Lexicon = None
    ):
        self.config = config
        self.ontology = ontology if ontology is not None else self.config.ontology()
        self.lexicon = lexicon if lexicon is not None else self.config.lexicon()
        self.frames = {}
        self.root = None

    def next_frame_for_concept(self, concept: str) -> "TMRFrame":
        instance = 0

        for f in self.frames.values():
            if f.concept == concept:
                instance = max(instance, f.instance)

        instance += 1

        frame = TMRFrame(concept, instance)
        self.frames[frame.frame_id()] = frame

        return frame

    def remove_frame(self, frame: "TMRFrame"):
        frame_id = frame.frame_id()

        self.frames.pop(frame_id)
        for frame in self.frames.values():
            for property, fillers in list(frame.properties.items()):
                if frame_id in fillers:
                    frame.properties[property].remove(frame_id)

    def items(self):
        for k, v in self.frames.items():
            yield k, v

    def constructions(self):
        return [f.list_constructions() for _, f in self.frames.items()]

    def root(self):
        return {self.root: self.frames[self.root]}

    def set_root(self, frame_id: str):
        self.root = frame_id

    def set_ontology(self, ontology: Ontology):
        self.ontology = ontology

    def set_lexicon(self, lexicon: Lexicon):
        self.lexicon = lexicon

    def to_dict(self) -> dict:
        return {"frames": list(map(lambda f: f.to_dict(), self.frames.values()))}

    @classmethod
    def instance(cls, config: OntoGenConfig, tmr_dict: dict) -> "oTMR":
        otmr = oTMR(config=config)
        out = []
        found_ids = set()
        built_ids = set()

        def _convert_frame(frame_id: str, contents: dict):
            if "concept" in contents:
                contents["INSTANCE-OF"] = contents["concept"]
            frame_id = _fix_frame_id(frame_id).split(".")
            built_ids.add(f"{frame_id[0]}.{frame_id[1]}")

            frame = otmr.next_frame_for_concept(frame_id[0])

            properties_to_ignore = [
                "is-in-subtree",
                "preference",
                "sem-preference",
                "sent-word-ind",
                "token",
                "coref",
            ]

            if "concept" in contents.keys():
                contents["CONCEPT"] = contents.pop("concept")

            for _slot_id, _slot in contents.items():
                if _slot_id in properties_to_ignore:
                    continue

                if _slot_id == "MP":
                    # TODO - RUN KNOWN MPs HERE , for now just add them to otmr
                    for mp in _slot:
                        frame.add_filler(_slot_id, mp)
                    continue

                if not isinstance(_slot, list):
                    _slot = [_slot]

                for _filler in _slot:
                    if _slot_id != "INSTANCE-OF":
                        filler = _convert_value(_slot_id, _filler)
                        frame.add_filler(_slot_id, filler)
                    else:
                        frame.add_filler(_slot_id, f"@ONT.{_filler}")

            return frame

        def _fix_frame_id(frame: str):
            # if frame is a *-concept, ground the reference.
            #       *-concepts are concepts like the SPEAKER, INTERLOCUTOR, and VEHICLE-IN-QUESTION

            if frame[0] == "*" and frame[-1] == "*":
                frame_id = f"{frame}.?"  # TODO: DO CORRECT INDEXING
                found_ids.add(frame_id)
                return frame_id
            else:  # NOTE: HACK TO MAKE FRAMES LIKE HUMAN-1 and HUMAN.1 work...
                if "." not in frame:
                    instance = re.findall(r"-([0-9]+)$", frame)[0]
                    frame_id = re.sub(r"-[0-9]+$", ".%s" % instance, frame)
                    frame_id = f"{frame_id}"
                    found_ids.add(frame_id)
                    return frame_id
                else:
                    found_ids.add(frame)
                    return frame

        def _convert_value(_property, value):
            if isinstance(value, str):
                # TODO - check for ontology existence
                if _property.upper() in [
                    "AGENT",
                    "BENEFICIARY",
                    "THEME",
                    "INSTRUMENT",
                    "MODALITY",
                    "SCOPE",
                    "ATTRIBUTED-TO",
                    "DESTINATION",
                    "DOMAIN",
                    "INSTANCE-OF",
                    "RANGE",
                ]:
                    return _fix_frame_id(value)
                return f"{value}"
            return value

        for key in tmr_dict.keys():
            if key.lower() == key:
                continue
            out.append(_convert_frame(key, tmr_dict[key]))

        return otmr

    def __iter__(self):
        for _, v in self.frames.items():
            yield v

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.frames[item]
        if isinstance(item, TMRFrame):
            return self.frames[item.frame_id()]

    def __contains__(self, item):
        if isinstance(item, str):
            return item in self.frames
        if isinstance(item, TMRFrame):
            return item.frame_id() in self.frames
        return False

    def __eq__(self, other):
        if isinstance(other, oTMR):
            return self.frames == other.frames
        return super().__eq__(other)


class TMRFrame:
    def __init__(
        self,
        concept: str,
        instance: int,
    ):
        self.concept = concept
        self.instance = instance
        self.properties = {}
        self.resolutions = set()  # List of ids that this frame resolves to
        self.senses = []

    def get_concept(self):
        return self.concept

    def get_properties(self):
        for k, v in self.properties.items():
            yield k, v

    def add_filler(self, property: str, filler: Any) -> "TMRFrame":
        if property not in self.properties:
            self.properties[property] = []
        self.properties[property].append(filler)

        return self

    def remove_filler(self, property: str, filler: Any) -> "TMRFrame":
        if property not in self.properties:
            return self
        self.properties[property].remove(filler)
        if len(self.properties[property]) == 0:
            del self.properties[property]

        return self

    def fillers(self, property: str) -> List[Any]:
        if property not in self.properties:
            return []
        return self.properties[property]

    def frame_id(self) -> str:
        return f"@TMR.{self.concept}.{self.instance}"

    def add_sense(self, sense: Union[Sense, str]):
        if isinstance(sense, str):
            self.senses.append(self.lexicon.sense(sense))
        elif isinstance(sense, Sense):
            self.senses.append(sense)

    def senses(self):
        return [c for c in self.senses]

    def to_dict(self) -> dict:
        return {
            "id": self.frame_id(),
            "concept": self.concept,
            "instance": self.instance,
            "properties": self.properties,
            "resolutions": list(self.resolutions),
        }

    def __repr__(self):
        return self.frame_id()

    def __eq__(self, other):
        if isinstance(other, TMRFrame):
            return self.concept == other.concept and self.instance == other.instance
        return super().__eq__(other)


if __name__ == "__main__":

    with open("../../tests/resources/sample-TMRs.txt", "r") as file:
        data = file.read()
        tmrs = ast.literal_eval(data)

    tmr_index = 3
    temp = tmrs[tmr_index]["results"][0]["TMR"]

    tmr = {"sentence": tmrs[tmr_index]["sentence"], "tmr": {}}

    for key in temp.keys():
        if key.lower() == key:
            continue  # Skip non-frame elements
        # out += _convert_frame(key, temp[key]) + "\n"
        tmr["tmr"][key] = temp[key]

    # # == DEV PRINTS == #
    # print(f"TMR No: {tmrs[tmr_index]['sent-num']}")
    print(f"TMR FOR: {tmr['sentence']}\n")
    # pprint(tmr["tmr"])
    # print(f"\n{'-'*80}\n")

    # otmr = oTMRBuilder(config=OntoGenConfig()).run(tmr["tmr"])
    otmr = oTMR.instance(tmr["tmr"])
    # pprint(otmr.to_dict())
    # for k in otmr:
    # print(type(otmr[k]))
