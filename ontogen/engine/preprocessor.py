from ontogen.engine.otmr import oTMR
from ontogen.config import OntoGenConfig


class Preprocessor:
    def __init__(self, config: OntoGenConfig):
        self.config = config

    def run(self, otmr: oTMR) -> oTMR:

        self.resolve_explicit_references(otmr)

        return otmr

    def resolve_explicit_references(self, otmr: oTMR):
        # print([e for e in otmr])
        pass
