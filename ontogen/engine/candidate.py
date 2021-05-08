from ontogen.knowledge.lexicon import Sense
from typing import Tuple

import uuid


class RealizationCandidate:
    # TODO: realization candidates should suggest the dependency constraints for the cx_candidates

    def __init__(self, senses: Tuple["ConstructionCandidate"]):
        self.id = str(uuid.uuid4())
        self.constructions = senses
        self.constraints = []
        self.scores = []
        self.score = 0.0

    def to_dict(self):
        return {
            "id": self.id,
            "constructions": self.constructions,
            "constraints": self.constraints,
            "scores": self.scores,
            "score": self.score,
        }

    def to_str(self):
        s = f"\nRealization Candidate #{self.id}"
        for cx in self.constructions:
            s += f"\n{cx.to_str()}"
        return s

    def __iter__(self):
        for construction in self.constructions: 
            yield construction

    def __repr__(self):
        return f"R#{self.id[:4]} -> {self.constructions}"


class ConstructionCandidate:
    def __init__(self, sense: Sense, tmr_anchor: str):
        self.id = sense.id
        self.sense = sense
        self.tmr_anchor = tmr_anchor
        self.score = 0.0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "pos": self.sense.pos,
            "tmr_anchor": self.tmr_anchor,
            "synstruc": self.sense.synstruc.to_dict(),
            "semstruc": self.sense.semstruc.to_dict(),
        }

    def to_str(self, indent: int = 4) -> str:
        s = f"\n{' '*(indent)}v{'-'*10}\n"
        s += f"{' '*(indent)}  id:         \t{self.id}\n"
        s += f"{' '*(indent)}\tpos:        \t{self.sense.pos}\n"
        s += f"{' '*(indent)}\ttmr_anchor: \t{self.tmr_anchor}\n"
        s += f"{' '*(indent)}\tsynstruc:   \t{self.sense.synstruc.to_str(indent*6)}\n"
        s += f"{' '*(indent)}\tsemstruc:   \t{self.sense.semstruc.to_str(indent*6)}\n"
        s += f"{' '*(indent)}^{'-'*10}"

        return s

    def __repr__(self):
        return repr(self.sense)
