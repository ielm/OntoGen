from ontogen.engine.otmr import oTMR
from ontogen.engine.report import Report
from ontogen.config import OntoGenConfig
from ontogen.utils.common import SPEECH_ACTS


class Preprocessor:
    def __init__(self, config: OntoGenConfig):
        self.config = config

    def run(self, report: Report) -> oTMR:
        report.set_otmr(self.consolidate_equivalent_frames(report.get_otmr()))
        report.set_otmr(self.resolve_explicit_references(report.get_otmr()))

    def consolidate_equivalent_frames(self, otmr: oTMR):
        # if two meta frames refer to the same thing (e.g., two REQ-ACT frames in an
        # oTMR), consolidate them into one frame.

        seen = {}

        for frame in otmr:
            # print(type(frame))
            frame_id_elements = frame.frame_id().split(".")
            # print(frame_id_elements)
            if not frame_id_elements[1] in seen:
                seen[frame_id_elements[1]] = [frame]

        # if 2 contentful frames (e.g., two HUMAN frames) refer to the same referent,
        # consolidate them into one frame. If they don't refer to the same referent,
        # do nothing

        return otmr

    def resolve_explicit_references(self, otmr: oTMR):
        # resolve *-references
        return otmr
