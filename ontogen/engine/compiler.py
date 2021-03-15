from ontogen.engine.otmr import oTMR, TMRFrame
from ontogen.engine.candidate import RealizationCandidate, ConstructionCandidate
from ontogen.knowledge.ontology import Ontology
from ontogen.knowledge.lexicon import Lexicon
from ontogen.config import OntoGenConfig

from json import loads, dumps
from typing import Tuple


class CandidateCompiler:
    def __init__(
        self, config: OntoGenConfig, ontology: Ontology = None, lexicon: Lexicon = None
    ):
        self.config = config
        self.ontology = ontology if ontology is not None else self.config.ontology()
        self.lexicon = lexicon if lexicon is not None else self.config.lexicon()

    def run(self, otmr: oTMR):
        lex = self.lexicalize(otmr)
        candidates = list(self.compile_candidates(*lex))
        return candidates
        # return None

    def lexicalize(self, otmr: oTMR, local: bool = False):
        sem_matches = []
        for key, tmrframe in otmr.items():
            temp_matches = self.sem_search(tmrframe, True)
            matches = []
            for temp_sense in temp_matches:
                sense = self.lexicon.sense(temp_sense["SENSE"])
                self.lexicon.add_sense(sense)
                matches.append({sense.id: ConstructionCandidate(sense, key)})
            sem_matches.append(matches)
        return sem_matches

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

    @staticmethod
    def sem_search(tmrframe: TMRFrame, local: bool = False):
        concept = tmrframe.frame_id().split(".")[1]
        temp = []
        # temp = LexiconAPI().sem_search(concept) # careful with this...
        if local:
            from ontogen.knowledge.local.lexicon import Lexicon as L

            found = []
            for lemma, lexemes in L.items():
                for instance, lexeme in lexemes.items():
                    if concept in lexeme["SEM-STRUC"]:
                        lexeme["SENSE"] = instance
                        lexeme["WORD"] = instance.split("-")[0]
                        found.append(lexeme)
            temp.extend(found)

        seen = []
        res = {}
        for temp_sense in temp:
            temp_sense = loads(dumps(temp_sense))
            if temp_sense["SENSE"] in seen:
                # print(temp_sense)
                # for t in res:
                #     if t["SENSE"] == temp_sense["SENSE"]:
                #         # print(t)

                #         pass
                res[temp_sense["SENSE"]] = temp_sense
            else:
                seen.append(temp_sense["SENSE"])
                # res.append(temp_sense)
                res[temp_sense["SENSE"]] = temp_sense

        # TODO - add tighter selectional constraints for construction candidates

        return res

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
