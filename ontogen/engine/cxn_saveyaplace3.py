import json

from pprint import pprint

from typing import List, Tuple, Union
from collections import OrderedDict
from lex.lexicon import Lexicon
from ontogen.utils.common import AnchoredObject

from ontograph.Frame import Frame
from ontograph.Space import Space
from ontograph import graph

import inspect
import re

# two classes, a combination and a construction
# a combination will contain the set of candidate constructions and ways to manipulate,
#   and iterate through them. They will also contain a global varmap similar to the
#   local construction varmap, but will assist in filling the "slots" dynamically. This
#   will be the primary unit that is passed around the first part of ontogen until it's
#   passed to simplenlg for realization.
# a construction then will basically be a wrapper around the lexical entry and contain
#   the local variable mappings so that varmaps don't have to be computed again
#   downstream.


class Construction(AnchoredObject):
    """
    What do I want a construction to be?
      in short, it's really about the variable links for the local (construction-level)
      skeleton. This means that the information about the construction is readily
      available without having to inspect the raw data because it's preprocessed on
      initialization.

    So what should a construction include?

    """

       # def __init__(self, _id, _raw, _tmr_anchor=None):
    #     self.id = _id
    #     self.raw = _raw
    #     self.varmap = {}
    #     self.tmr_anchor = _tmr_anchor

    #     # Set object attributes
    #     for _k in self.raw:
    #         # print(_k)
    #         setattr(self, _k.lower().replace("-", "_"), self.raw[_k])

    def __init__(self, anchor: Frame, _id: str = None, _cdict: dict = None):
        self.raw_id = _id
        self.raw_data = _cdict

        for _k in _cdict:
            setattr(self, _k.lower().replace("-", "_"), _cdict[_k])

        super().__init__(anchor)

    @classmethod
    def build(cls, _id, _cdict, tmr_anchor=None) -> "Construction":
        cxn = _id.split("-")
        cxn_num = re.findall(r"\d*\Z", cxn[1])[0]
        space = Construction.next_available_space("CXN")
        name = f"@{space.name}.{cxn[0]}.{cxn_num}"

        if name in graph:
            return Construction(graph[name])
        else:
            anchor = Frame(name)
            c = Construction(anchor, _id, _cdict)
            c.set_space(space)
            c.__populate(_cdict)
            return c

    @classmethod
    def next_available_space(cls, header: str = None) -> Space:
        if header is None:
            header = "CXN"

        spaces = list(graph)
        spaces = filter(lambda space: space.name.startswith(header + "#"), spaces)
        spaces = map(lambda space: int(space.name.replace(header + "#", "")), spaces)
        spaces = list(spaces)

        next = 1 if len(spaces) == 0 else max(spaces) + 1
        return Space(header + "#" + str(next))

    def cat(self):
        return self.anchor["CAT"].singleton()

    def root(self) -> Frame:
        return self.anchor["ROOT"].singleton()

    def set_root(self, root: Frame):
        self.anchor["ROOT"] = root

    def elements(self) -> List[Frame]:
        return list(self.anchor["HAS-ELEMENT"])

    def add_element(self, element: Frame):
        self.anchor["HAS-ELEMENT"] += element
        self.add_constituent(element)

    def get_element(self, name: Union[str, Frame]) -> Union[Frame, None]:
        if isinstance(name, Frame):
            name = name.id.split(".")[1]
        for element in self.elements():
            if name in element.id:
                return element
        return None

    def varmap(self):
        return self.anchor["VARMAP"].singleton()

    def constituents(self) -> List[Frame]:
        return list(self.anchor["HAS-CONSTITUENT"])

    def add_constituent(self, constituent: Frame):
        self.anchor["HAS-CONSTITUENT"] += constituent

    def resolve_pointer(self, pointer: str) -> Union[Frame, None]:
        pointer = re.sub("[?^]", "", str(pointer))
        for element in self.elements():
            if element["ROOT"] == pointer:
                return element
        return None

    def space(self) -> Space:
        return Space(self.anchor["SPACE"].singleton().replace("@", "", 1))

    def set_space(self, space: Union[str, Space]):
        if isinstance(space, Space):
            space = "@" + space.name
        self.anchor["SPACE"] = space

    def debug(self) -> dict:
        out = {}
        for slot in self.anchor:
            results = {}
            for facet in slot.facets():
                results[facet.property] = facet.debug()
            out[slot.property] = results
        return out

    @staticmethod
    def is_pointer(s: str) -> bool:
        if "^" in s or "$" in s:
            return True
        else:
            return False

    def __build_varmap(self):

        varmap = Frame(f"@{self.space().name}.VARMAP.?")

        _0_LITERALS = [
            "ROOT",
            "CAT",
            "ROOT-WORD",
            "TENSE",
            "USE-EXAMPLE-BINDING",
            "TYPE",
        ]
        _0_temp = {}

        def __build_element(_id: str, _content: OrderedDict) -> Frame:
            elem = Frame(f"@{self.space().name}.{_id}.?")
            for key in _content.keys():
                elem[key] = _content[key]
            self.add_element(elem)
            return elem


        # * = SYN; ^ = SEM; & = TMR
        for element in self.syn_struc:
            elem = Frame(f"@{self.space().name}.{element}.?")

            if element in _0_LITERALS:  # if element is the root element
                _0_temp[f"*{element}"] = self.syn_struc[element]

            if (  # if element is an allocated variable
                "ROOT" in self.syn_struc[element]
                and self.syn_struc[element]["ROOT"] not in varmap
            ):
                # e = __build_element(element, syn_struc[element])

                # varmap[self.syn_struc[element]["ROOT"]] = {
                #     f"*{ek}": ev for ek, ev in self.syn_struc[element].items()
                # }
                varmap[self.syn_struc[element]["ROOT"]] = __build_element(
                    self.syn_struc[element]["ROOT"], self.syn_struc[element]
                )

        # varmap["$VAR0"] = _0_temp
        varmap["$VAR0"] = __build_element("$VAR0", _0_temp)

        if isinstance(self.sem_struc, str):
            varmap["$VAR0"] = {"^ISA": {self.sem_struc}}
        elif isinstance(self.sem_struc, dict):
            for element in self.sem_struc:
                if "^$VAR" in element:
                    vm_index = element[-1]
                    for xk, xv in self.sem_struc[element].items():  # fmt: skip
                        if f"$VAR{vm_index}" not in varmap:
                            varmap[f"$VAR{vm_index}"] = {}
                        varmap[f"$VAR{vm_index}"][f"^{xk}"] = xv
                else:
                    if f"$VAR0" not in varmap:
                        varmap["$VAR0"] = {}
                    varmap["$VAR0"][f"^{element}"] = self.sem_struc[element]

        self.anchor["VARMAP"] = varmap

    def __populate(self, content: OrderedDict):
        for item in content.keys():
            if item != "SYN-STRUC" and item != "SEM-STRUC":
                self.anchor[item] = content[item]

        # self.__process_syn_struc(content["SYN-STRUC"])
        # self.__process_sem_struc(content["SEM-STRUC"])
        self.__build_varmap()

    def __process_syn_struc(self, syn_struc):
        # def __build_element(_id: str, _content: OrderedDict) -> Frame:
        #     elem = Frame(f"@{self.space().name}.{_id}.?")
        #     for key in _content.keys():
        #         elem[key] = _content[key]
        #     self.add_element(elem)
        #     return elem

        root_elem = OrderedDict({"ROOT": syn_struc["ROOT"], "CAT": syn_struc["CAT"]})
        elements = [__build_element("ROOT", root_elem)]
        self.set_root(self.get_element("ROOT"))
        for item in syn_struc.keys():
            if isinstance(
                syn_struc[item], OrderedDict  # if item != "ROOT" and item != "CAT":
            ):
                elements.append(__build_element(item, syn_struc[item]))
            else:
                self.root()[item]

    def __process_sem_struc(self, sem_struc):
        def __process_concept(name: str, concept: OrderedDict, element: str = "ROOT"):
            element_sem = Frame(f"@{self.space().name}.{element}_SEM.?")
            element_sem["SEM"] = name
            self.add_constituent(element_sem)
            for relation in concept.keys():
                if isinstance(concept[relation], OrderedDict):
                    if self.is_pointer(concept[relation]):
                        pass
                    else:
                        if self.is_pointer(concept[relation]["VALUE"]):
                            element = self.resolve_pointer(concept[relation]["VALUE"])
                            if element is not None:
                                element_sem[relation] = element
                        else:
                            element_sem[relation] = concept[relation["VALUE"]]
            self.root()["SEM"] = element_sem

        if isinstance(sem_struc, str):
            pass
        elif isinstance(sem_struc, OrderedDict):
            for item in sem_struc.keys():
                if self.is_pointer(item):
                    (f"pointer: {item}")

                if item == "MODALITY":
                    pass
                else:
                    __process_concept(item, sem_struc[item], element="ROOT")


def combine_candidates(*candidates, repeat=1):
    # ((<tmr element candidates>), (<...>), (<...>)) -> ((<combination>), (<...>), ...)
    pools = [tuple(pool) for pool in candidates] * repeat
    result = [[]]
    for pool in pools:
        result = [x + [y] for x in result for y in pool]
    for prod in result:
        compatible, combination = check_basic_compatability(prod)
        if compatible:
            yield tuple(combination)



def check_basic_compatability(input_combination: list) -> Tuple[bool, dict]:
    """
    returns true and the corrected combination if compatible, else return false and
    annotated combination detailing why it wasn't compatible.
    """

    # build the syn-struc template for each candidate with each other candidate
    #     - first by part of speech

    # Reduce input list of candidates to single dictionary
    flat = {_k: _v for _c in input_combination for _k, _v in _c.items()}
    candidate_ids = [_x for _x in flat.keys()]  # list of candidate

    combination = {}
    for c_id, c_raw in flat.items():
        c = Construction.build(c_id, c_raw)

        # combination[c_id] = Construction(c_id, c_raw)

        # aa = inspect.getmembers(combination[c_id], lambda a:not(inspect.isroutine(a)))
        # pprint([a for a in aa if not(a[0].startswith('__') and a[0].endswith('__'))])

        # print()

    # for c_id, cx in combination.items():
    # others = [c for c in combination if c != c_id]

    # Build variable structs for each candidate in the combination
    # for c_id, current in flat.items():
    #     others = [c for c in flat if c != c_id]
    #     # determine variables for current cstruct
    #     # fill variable struct with existing members, and set flag for downstream
    #     #     processing if there are not enough members available, or just decide to
    #     #     not use it at all and fail compatability check

    #     # alias main strucs
    #     synstruc = current["SYN-STRUC"]
    #     synstruc = current["SYN-STRUC"]

    #     varmap = {"$VAR0": {}}

    #     _var0_keys = ["ROOT", "CAT", "ROOT-WORD", "TENSE", "USE-EXAMPLE-BINDING", "TYPE"]
    #     for element in synstruc:
    #         if element in _var0_keys:
    #             varmap["$VAR0"][element] = synstruc[element]

    #         if "ROOT" in synstruc[element] and synstruc[element]["ROOT"] not in varmap:
    #             varmap[synstruc[element]["ROOT"]] = synstruc[element]

    # pprint(synstruc)
    # pprint(varmap)

    # for element in struc
    # for syn_elem in current["SYN-STRUC"].keys():
    #     print(syn_elem)

    # print()
    # print("\n\n")

    return True, input_combination  # TODO: replace with true checking and return


def prune_combinations(combinations: list) -> list:

    verified = []

    for combo in combinations:
        print()
        if check_basic_compatability(combo):
            verified.append(combo)

    return verified


def test_prune_combinations(combinations: list, limit=1) -> list:

    verified = []

    for combo in combinations[:limit]:
        if check_basic_compatability(combo):
            verified.append(combo)

    return verified


def boostrap_speech_act_cxs() -> dict:
    data = OrderedDict
    with open("../knowledge/constructions/speech-acts-lexicon.json", "r") as file:
        data = json.load(file, object_pairs_hook=OrderedDict)
    return data


def get_cx_by_speech_act(cxs: dict = None, speech_act: str = None) -> List:
    if not cxs:
        cxs = boostrap_speech_act_cxs()
    if not speech_act:
        raise ValueError("Cannot query constructions with empty speech act.")

    # TODO: THERE SHOULD BE DEEPER SELECTIONAL CONSTRAINTS
    return [c for _, c in cxs.items() if speech_act in c["SEM-STRUC"].keys()]


if __name__ == "__main__":
    sa = "REQUEST-ACTION"
    cxs = get_cx_by_speech_act(speech_act=sa)
    print(f"There are {len(cxs)} cxs for {sa} in the local cx repo:")
    i = 1
    for c in cxs:
        print(f"\t{i}.\t{c['SENSE']}     \t->  {c['EX']}")
        i += 1

    lcxs = Lexicon().sem_search(sa)

    j = 1
    print(f"There are {len(lcxs)} cxs for {sa} in the Lexicon:")
    for lc in lcxs:
        print(f"\t{j}.\t{lc['SENSE']}    \t->  {lc['EX']}")
        j += 1