from ontogen.config import OntoGenConfig
from ontogen.engine.otmr import oTMR
from lex.lexicon import Lexicon

from typing import List, Tuple
from collections import OrderedDict

import json


# two structures, a combination and a construction
# a combination will contain the set of candidate constructions and ways to manipulate,
#   and iterate through them. They will also contain a global varmap similar to the
#   local construction varmap, but will assist in filling the "slots" dynamically. This
#   will be the primary unit that is passed around the first part of ontogen until it's
#   passed to simplenlg for realization.
# a construction then will basically be a wrapper around the lexical entry and contain
#   the local variable mappings so that varmaps don't have to be computed again
#   downstream.


class Construction:
    def __init__(self, _id, _raw, _tmr_anchor=None):
        self.id = _id
        self.raw = _raw
        self.varmap = {}
        self.tmr_anchor = _tmr_anchor

        # Set Construction attributes
        attrs = [  # available attributes
            "CAT",
            "DEF",
            "EX",
            "COMMENTS",
            "TMR-HEAD",
            "SYN-STRUC",
            "SEM-STRUC",
            "OUTPUT-SYNTAX",
            "MEANING-PROCEDURES",
            "EXAMPLE-BINDINGS",
            "EXAMPLE-DEPS",
            "SYNONYMS",
            "HYPONYMS",
        ]
        for _k in self.raw:
            if _k in attrs:
                # print(_k)
                setattr(self, _k.lower().replace("-", "_"), self.raw[_k])

        self.__build_varmap()

    def __build_varmap(self):
        _0_LITERALS = [
            "ROOT",
            "CAT",
            "ROOT-WORD",
            "TENSE",
            "USE-EXAMPLE-BINDING",
            "TYPE",
        ]
        _0_temp = {}

        # _ = SYN; ^ = SEM
        for element in self.syn_struc:
            if element in _0_LITERALS:  # if element is the root element
                _0_temp[f"_{element}"] = self.syn_struc[element]

            if (  # if element is an allocated variable
                "ROOT" in self.syn_struc[element]
                and self.syn_struc[element]["ROOT"] not in self.varmap
            ):
                self.varmap[self.syn_struc[element]["ROOT"]] = {
                    f"_{ek}": ev for ek, ev in self.syn_struc[element].items()
                }

        self.varmap["$VAR0"] = _0_temp

        if isinstance(self.sem_struc, str):
            self.varmap["$VAR0"] = {"^ISA": {self.sem_struc}}
        elif isinstance(self.sem_struc, dict):
            for element in self.sem_struc:
                if "^$VAR" in element:
                    vm_index = element[-1]
                    for xk, xv in self.sem_struc[element].items():  # fmt: skip
                        if f"$VAR{vm_index}" not in self.varmap:
                            self.varmap[f"$VAR{vm_index}"] = {}
                        self.varmap[f"$VAR{vm_index}"][f"^{xk}"] = xv
                else:
                    if f"$VAR0" not in self.varmap:
                        self.varmap["$VAR0"] = {}
                    self.varmap["$VAR0"][f"^{element}"] = self.sem_struc[element]


class CombinationBuilder:
    def __init__(self, config: OntoGenConfig):
        self.config = config

    def run(self, otmr: oTMR):
        # Find candidate constructions for each frame in otmr
        sem_matches = {}
        num_items = 0
        for key, element in otmr["tmr"].items():
            concept = key.rsplit("-", 1)[0]
            sem_matches[concept] = sem_search(concept)
            num_items += 1

        # [[<candidates for tmr frame #1>], [<...frame #2>], [<...frame #3>], ...]
        temp_candidates = []
        for key1, _element in sem_matches.items():
            temp_element = []
            for key2, _candidate in _element.items():
                temp_element.append({key2: _candidate})
            temp_candidates.append(temp_element)

        res = list(self.combine_candidates(*temp_candidates))
        return res

    def combine_candidates(self, *candidates, repeat=1):
        # ((<tmr element candidates>), (<...>), (<...>)) -> ((<combination>), (<...>), ...)
        pools = [tuple(pool) for pool in candidates] * repeat
        result = [[]]
        for pool in pools:
            result = [x + [y] for x in result for y in pool]
        for prod in result:
            compatible, combination = self.check_basic_compatibility(prod)
            if compatible:
                yield tuple(combination)
            # else:
            # add compatability check to log

    @staticmethod
    def check_basic_compatibility(input_combination: list) -> Tuple[bool, list]:
        """
        returns true and the corrected combination if compatible, else return false and
        annotated combination detailing why it wasn't compatible.
        """

        # Reduce input list of candidates to single dictionary
        flat = {_k: _v for _c in input_combination for _k, _v in _c.items()}
        candidate_ids = [_x for _x in flat.keys()]  # list of candidate

        combination = {}
        combination_list = []  # TODO: fix combination return
        for c_id, c_raw in flat.items():
            combination[c_id] = Construction(c_id, c_raw)
            # print(c_id)
            # pprint(combination[c_id].varmap)

        return True, combination_list  # TODO: replace with true checking and return

    @staticmethod
    def prune_combinations(combinations: list) -> list:

        verified = []

        for combo in combinations:
            print()
            if check_basic_compatibility(combo):
                verified.append(combo)

        return verified

    @staticmethod
    def test_prune_combinations(combinations: list, limit=1) -> list:

        verified = []

        for combo in combinations[:limit]:
            if check_basic_compatibility(combo):
                verified.append(combo)

        return verified


def boostrap_speech_act_cxs() -> dict:
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
