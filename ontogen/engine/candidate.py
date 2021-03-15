from ontogen.config import OntoGenConfig
from ontogen.knowledge.lexicon import Sense


class RealizationCandidate:
    """
    Whereas OntoSem deals with TMR candidates, OntoGen deals with realization
    candidates. This means that the primary objective is to linearize the syn and
    sem maps of the tmrframe construction candidates.
    """

    def __init__(self, *senses: ConstructionCandidate):
        self.id = str(uuid.uuid4())
        self.constructions = senses
        self.constraints = []
        self.scores = []
        self.score = 0.0


class ConstructionCandidate:
    def __init__(self, sense: Sense, tmr_anchor: str):
        self.id = sense.id
        self.sense = sense
        self.tmr_anchor = tmr_anchor
        self.score = 0.0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "pos": self.pos,
            "tmr_anchor": self.tmr_anchor,
            "synstruc": self.sense.synstruc.to_dict(),
            "semstruc": self.sense.semstruc.to_dict(),
        }

    def to_str(self, indent: int = 4) -> str:
        s = f"\n{' '*indent}id:     \t{self.id}\n"
        s += f"{' '*indent}pos:     \t{self.sense.pos}\n"
        s += f"{' '*indent}tmr_anchor: \t{self.tmr_anchor}\n"
        s += f"{' '*indent}synstruc:\t{self.sense.synstruc.to_str()}\n"
        s += f"{' '*indent}semstruc:\t{self.sense.semstruc.to_str()}"
        return s

    def __repr__(self):
        return repr(self.sense)
