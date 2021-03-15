from ontogen.engine.candidate import RealizationCandidate
from ontogen.engine.otmr import oTMR
from ontogen.config import OntoGenConfig

from typing import List


class Report:
    def __init__(self, config: OntoGenConfig, otmr: oTMR):
        self.config = config
        self.candidates: List[RealizationCandidate] = []
        self.otmr = otmr

    def to_dict(self) -> dict:
        return {
            "config": self.config.to_dict(),
            "candidates": list(map(lambda s: s.to_dict(), self.candidates)),
        }
