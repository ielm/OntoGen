from ontogen.engine.otmr import oTMR, TMRFrame
from ontogen.engine.candidate import RealizationCandidate, ConstructionCandidate
from ontogen.engine.report import Report
from ontogen.knowledge.ontology import Ontology
from ontogen.knowledge.lexicon import *
from ontogen.config import OntoGenConfig
from lex.api import LexiconAPI

from typing import Tuple, List
from enum import Enum
from pprint import pprint

SPECIAL_FRAMES = ["MEANING-PROCEDURE", "REQUEST-ACTION"]


class CandidateCompiler:
    class MatchAlgo(Enum):
        EXACT = "EXACT"
        PARENT = "PARENT"
        FUZZY = "FUZZY"

    def __init__(
        self, config: OntoGenConfig, ontology: Ontology = None, lexicon: Lexicon = None
    ):
        self.config = config
        self.ontology = ontology if ontology is not None else self.config.ontology()
        self.lexicon = lexicon if lexicon is not None else self.config.lexicon()

    def run(self, report: Report):
        lex = self.lexicalize(report.get_otmr())
        candidates = list(self.compile_candidates(*lex))
        report.set_candidates(candidates)

    def lexicalize(self, otmr: oTMR, local: bool = False):
        sem_matches = []
        # print({p: v for p, v in otmr.items()}.keys())

        for key, tmrframe in otmr.items():
            # TODO: instead of ignoring special frames, run procedures to make sure
            #       that they don't need to be lexicalized and run meaning procedures
            if tmrframe.concept in SPECIAL_FRAMES:
                continue
            temp_matches = self.sem_search(tmrframe, local)
            matches = []
            for temp_sense in temp_matches:
                matches.append({temp_sense.id: ConstructionCandidate(temp_sense, key)})
            sem_matches.append(matches)
        return [fm for fm in sem_matches if fm]

    def compile_candidates(self, *candidates, repeat=1):
        # ((<tmr element candidates>), (<...>), (<...>)) -> ((<combination>), (<...>), ...)
        pools = [tuple(pool) for pool in candidates] * repeat
        result = [[]]
        for pool in pools:
            result = [x + [y] for x in result for y in pool]
        for prod in result:
            compatible, combination = self.check_basic_compatibility(prod)
            if compatible:
                yield RealizationCandidate(combination)

    def sem_search(self, tmrframe: TMRFrame, local: bool = False):
        # concept = tmrframe.frame_id().split(".")[1]
        concept = tmrframe.get_concept()
        temp_senses = [
            self.lexicon.sense(s["SENSE"]) for s in LexiconAPI().sem_search(concept)
        ]
        if local:
            from ontogen.knowledge.local.lexicon import Lexicon as LocalLexicon

            found = []
            for lemma, lexemes in LocalLexicon.items():
                for instance, lexeme in lexemes.items():
                    if concept in lexeme["SEM-STRUC"]:
                        lexeme["SENSE"] = instance
                        lexeme["WORD"] = instance.split("-")[0]
                        found.append(lexeme)
            temp_senses.extend(found)

        pre_length = len(temp_senses)
        res = self.cull_senses(tmrframe, temp_senses, CandidateCompiler.MatchAlgo.EXACT)
        print(f"{tmrframe.frame_id()}: {pre_length} -> {len(res)}")
        # return [s for _, s in res.items()]
        return res

    # Match algorithm can be one of: EXACT, PARENT, FUZZY.
    # TODO:
    #       [] - Create objects for each of the match algos that runs that algo
    #       [] - change matching_algo type to MATCH_ALGO
    def cull_senses(
        self, tmr_frame: TMRFrame, temp_senses: list, match_algo: "MatchAlgo"
    ) -> List[ConstructionCandidate]:
        seen = []
        res = []
        for temp_sense in temp_senses:
            if temp_sense.id in seen:
                continue
            else:
                seen.append(temp_sense.id)
                if not self.check_sem_struc_values(tmr_frame, temp_sense):
                    continue
                res.append(temp_sense)
        return res

    @staticmethod
    def check_sem_struc_values(frame: TMRFrame, sense: Sense):
        def match_head(prop, elem):
            _match = True
            for p, v in prop.items():
                if p in elem.contents:
                    continue
                else:
                    _match = False
            return _match

        print_skip_warning = False
        skipped_elems = []
        properties = {}

        for key, val in frame.get_properties():
            if key.lower() == key:
                continue  # Skip non-frame elements
            if key in ["CONCEPT", "INSTANCE-OF", "TIME"]:
                continue  # Skip util elements
            properties[key] = val

        for element in sense.semstruc.elements():
            if isinstance(element, SemStruc.Head):
                if match_head(properties, element):
                    return True
            if (
                isinstance(element, SemStruc.Variable)
                or isinstance(element, SemStruc.Sub)
                or isinstance(element, SemStruc.RefSem)
            ):
                # print_skip_warning = True  # UNCOMMENT THIS LINE IF YOU WANT TO SEE THE SKIPPED ELEMENTS
                skipped_elems.append(element)

        if print_skip_warning:
            print(f"Warning: skipping sem variable resolution for now: {skipped_elems}")

        return False

    @staticmethod
    def check_basic_compatibility(input_combination: list) -> Tuple[bool, tuple]:
        """
        returns true and the corrected combination if compatible, else return false and
        annotated combination detailing why it wasn't compatible.
        """
        combination = [_v for _c in input_combination for _, _v in _c.items()]
        # for cx in combination:
        #     combination.append(cx)

        return True, tuple(combination)
