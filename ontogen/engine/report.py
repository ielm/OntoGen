from ontogen.engine.candidate import RealizationCandidate
from ontogen.engine.otmr import oTMR
from ontogen.config import OntoGenConfig

from typing import List


class Report:
    def __init__(self, config: OntoGenConfig, otmr: oTMR):
        self.config = config
        self.candidates: List[RealizationCandidate] = []
        self.otmr = otmr

    def set_config(self, config: OntoGenConfig):
        self.config = config

    def get_config(self) -> OntoGenConfig:
        return self.config

    def set_candidates(self, candidates: List[RealizationCandidate]):
        self.candidates = candidates

    def get_candidates(self) -> List[RealizationCandidate]:
        return self.candidates

    def set_otmr(self, otmr: oTMR):
        self.otmr = otmr

    def get_otmr(self) -> oTMR:
        return self.otmr

    # def to_dict(self) -> dict:
    #     return {
    #         "config": self.config.to_dict(),
    #         "otmr": self.otmr.to_dict(),
    #         "candidates": list(map(lambda s: s.to_dict(), self.candidates)),
    #     }

    def to_dict(self) -> dict:
        return {
            "config": self.config.to_dict(),
            "otmr": self.otmr.to_dict(),
            "candidates": f"Length of candidate list is: {len(list(map(lambda s: s.to_dict(), self.candidates)))}",
        }
