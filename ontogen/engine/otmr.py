# Local Package Imports
from ontogen.utils.common import AnchoredObject

# OntoGraph Imports
from ontograph_ontolang.OntoLang import OntoLang
from ontograph.Identifier import Identifier
from ontograph.Focus import Focus
from ontograph.Frame import Frame
from ontograph.Space import Space
from ontograph import graph
from ontograph.Query import (
    AndComparator,
    ExistsComparator,
    InSpaceComparator,
    Query,
    SelectPipeline,
)

# Python Package Imports
from typing import Generic, TypeVar, Union
from collections import OrderedDict
from pprint import pprint
from enum import Enum

import time
import json
import re

RAW = TypeVar("RAW")

SPEECH_ACTS = ["REQUEST-ACTION", "REQUEST-INFO"]


class oTMR(AnchoredObject):
    class Status(Enum):
        RAW = "RAW"  # The oTMR represents raw output that hasn't been processed
        ISSUED = "ISSUED"  # The oTMR represents output that has not yet been rendered
        RENDERED = "RENDERED"  # The oTMR represents output that has been rendered

    class Priority(Enum):
        LOW = "LOW"
        ASAP = "ASAP"
        INTERRUPT = "INTERRUPT"

    @classmethod
    def instance(
        cls,
        tmr_type: Union[str, Frame] = "@ONT.OTMR",
        root_type: Union[None, str, Frame] = "@ONT.SPEECH-ACT",
        originator: Union[None, str, Frame] = None,
        space: Union[None, str, Space] = None,
        raw: Union[None, str] = None,
        priority: Priority = Priority.ASAP,
        speaker: Union[None, str, Frame] = None,
        listener: Union[None, str, Frame] = None,
    ) -> "oTMR":

        # Build the oTMR frame
        if isinstance(tmr_type, Frame):
            tmr_type = tmr_type.id
        name = Identifier.parse(tmr_type)[1]
        frame = Frame("@IO.%s.?" % name).add_parent(tmr_type)
        otmr = cls(frame)

        # Reserve the oTMR space
        # if space is None:
        space = oTMR.next_available_space(header=name)
        otmr.set_space(space)

        # If a root type was provided, make an instance of it and assign it to the root; otherwise
        # make a default placeholder root
        if root_type is not None:
            if isinstance(root_type, Frame):
                root_type = root_type.id
            root_name = Identifier.parse(root_type)[1]
            root = space.frame("@.%s.?" % root_name).add_parent(root_type)
            otmr.set_root(root)
        else:
            root = space.frame("@.ALL.?").add_parent("@ONT.ALL")
            root["PLACEHOLDER"] = True
            otmr.set_root(root)

        # Assign any originator provided
        if originator is not None:
            otmr.set_originator(originator)

        # Assign any raw data provided
        if raw is not None:
            otmr.set_raw(raw)
            otmr.set_status(oTMR.Status.RAW)
        else:
            otmr.set_status(oTMR.Status.ISSUED)

        otmr.set_priority(priority)
        otmr.set_timestamp(time.time_ns())

        if speaker is not None:
            otmr.set_speaker(speaker)
        if listener is not None:
            otmr.set_listener(listener)

        return otmr

    @classmethod
    def instance_from_dict(
        cls,
        input_dict: Union[dict, OrderedDict] = None,
        priority: Priority = Priority.ASAP,
    ) -> "oTMR":

        # Make input_dict elements frames and anchor to graph
        out = dict_to_frames(input_dict["tmr"])

        # print(input_dict["tmr"])

        # Get oTMR root and check for multiple roots
        root = [el for el in out if ("TMR-ROOT" in el or el.name() in SPEECH_ACTS)]
        if len(root) > 1:
            # consolidate roots
            raise ValueError("oTMR cannot have multiple roots")
        elif len(root) < 1:
            raise ValueError("oTMR must have a root")

        # Create oTMR anchor
        frame = Frame(f"@IO.OTMR.?").add_parent("@ONT.OTMR")
        otmr = cls(frame)

        root = root[0]
        otmr.set_root(root)

        space = root.space()
        otmr.set_space(space)

        otmr.set_status(oTMR.Status.ISSUED)
        otmr.set_priority(priority)
        otmr.set_timestamp(time.time_ns())
        otmr.set_speaker(root["AGENT"].singleton())
        otmr.set_listener(root["BENEFICIARY"].singleton())

        return otmr

    @classmethod
    def next_available_space(cls, header: str = "OTMR") -> Space:
        spaces = list(graph)
        spaces = filter(lambda space: space.name.startswith(header + "#"), spaces)
        spaces = map(lambda space: int(space.name.replace(header + "#", "")), spaces)
        spaces = list(spaces)

        next = 1 if len(spaces) == 0 else max(spaces) + 1
        return Space(header + "#" + str(next))

    def space(self) -> Space:
        return Space(self.anchor["SPACE"].singleton().replace("@", "", 1))

    def set_space(self, space: Space):
        space = "@" + space.name
        self.anchor["SPACE"] = space

    def root(self) -> Frame:
        return self.anchor["ROOT", Focus(inh=Focus.Inh.LOC)].singleton()

    def set_root(self, root: Frame):
        try:
            cur_root = self.root()
            if True in cur_root["PLACEHOLDER"]:
                cur_root.delete()
        except:
            pass

        self.anchor["ROOT"] = root

    def originator(self) -> Union[None, Frame]:
        try:
            return self.anchor["ORIGINATOR", Focus(inh=Focus.Inh.LOC)].singleton()
        except:
            return None

    def set_originator(self, originator: Frame):
        self.anchor["ORIGINATOR"] = originator

    def raw(self) -> Union[None, RAW]:
        try:
            return self.anchor["RAW"].singleton()
        except:
            return None

    def set_raw(self, raw: RAW):
        self.anchor["RAW"] = raw

    def status(self) -> "oTMR.Status":
        try:
            return self.anchor["STATUS"].singleton()
        except:
            return oTMR.Status.RAW

    def set_status(self, status: "oTMR.Status"):
        self.anchor["STATUS"] = status

    def priority(self) -> "oTMR.Priority":
        try:
            return self.anchor["PRIORITY"].singleton()
        except:
            return oTMR.Priority.ASAP

    def set_priority(self, priority: "oTMR.Priority"):
        self.anchor["PRIORITY"] = priority

    def timestamp(self) -> int:
        return self.anchor["TIMESTAMP"].singleton()

    def set_timestamp(self, timestamp: int):
        self.anchor["TIMESTAMP"] = timestamp

    def speaker(self) -> Union[None, Frame]:
        try:
            return self.root()["AGENT"].singleton()
        except:
            return None

    def set_speaker(self, speaker: Union[str, Frame]):
        if isinstance(speaker, str):
            speaker = Frame(speaker)
        self.root()["AGENT"] = speaker

    def listener(self) -> Union[None, Frame]:
        try:
            return self.root()["BENEFICIARY"].singleton()
        except:
            return None

    def set_listener(self, listener: Union[str, Frame]):
        if isinstance(listener, str):
            listener = Frame(listener)
        self.root()["BENEFICIARY"] = listener

    def debug(self):
        # print(self.anchor.id:)
        pprint({self.anchor.id: self.root().debug()})
        # for element in self.root():
        # print(element)


def dict_to_frames(tmr: Union[OrderedDict, dict], anchor_to_graph: bool = True) -> str:
    inverses = (
        Query(
            AndComparator([InSpaceComparator("ONT"), ExistsComparator(slot="INVERSE")])
        )
        .flatten()
        .filter(str)
        .select(SelectPipeline.Column.FILLER)
        .start()
    )

    found_ids = set()
    built_ids = set()

    out = ""

    space = oTMR.next_available_space()

    default_index = 0

    def _fix_frame_id(frame: str) -> str:
        # if frame is a *-concept, ground the reference.
        #       *-concepts are concepts like the SPEAKER, INTERLOCUTOR, and VEHICLE-IN-QUESTION

        if frame[0] == "*" and frame[-1] == "*":
            frame_id = frame.strip("*")
            frame_id = f"@{space.name}.{frame_id}.35?"  # TODO: DO CORRECT INDEXING

            found_ids.add(frame_id)

            return frame_id
        else:
            instance = re.findall(r"-([0-9]+)$", frame)[0]
            frame_id = re.sub(r"-[0-9]+$", ".%s?" % instance, frame)
            frame_id = f"@{space.name}.{frame_id}"

            found_ids.add(frame_id)

            return frame_id

    def _convert_value(_property, value):
        if isinstance(value, str):
            # if "HUMAN" in value:
            #     value = f"@{space.name}.HUMAN.1?"
            #     found_ids.add(value)
            #     return value
            # if "ROBOT" in value:
            #     value = f"@{space.name}.ROBOT.1?"
            #     found_ids.add(value)
            #     return value
            if Frame(f"@ONT.{_property.upper()}") ^ Frame("@ONT.RELATION"):
                return _fix_frame_id(value)

            # TODO - check for ontology existence
            if _property.upper() in [
                "AGENT",
                "BENEFICIARY",
                "THEME",
                "INSTRUMENT",
                "MODALITY",
                "SCOPE",
                "ATTRIBUTED-TO",
                "DESTINATION",
                "DOMAIN",
                "INSTANCE-OF",
                "RANGE",
            ]:
                return _fix_frame_id(value)
            return f'"{value}"'
        return value

    def _convert_frame(frame: str, contents: dict) -> str:
        if "concept" in contents:
            contents["INSTANCE-OF"] = contents["concept"]

        frame_id = _fix_frame_id(frame)
        built_ids.add(frame_id)

        properties = ["IS-A @ONT.%s;" % contents["INSTANCE-OF"]]

        for k in contents.keys():
            if k.lower() == k:
                continue
            if k.lower() in inverses:
                continue

            if k == "MP":
                # RUN KNOWN MPs HERE
                continue

            values = contents[k]
            if not isinstance(values, list):
                values = [values]
            for value in values:
                if k != "INSTANCE-OF":
                    properties.append("%s %s;" % (k, _convert_value(k, value)))
                else:
                    properties.append("INSTANCE-OF @ONT.%s;" % value)

        return "%s = {\n%s\n};" % (
            frame_id,
            "\n".join(map(lambda p: "\t" + p, properties)),
        )

    for key in tmr.keys():
        if key.lower() == key:
            continue  # Skip non-frame elements
        print(key)

        out += _convert_frame(key, tmr[key]) + "\n"

    for found_id in found_ids.difference(built_ids):
        isa = re.findall(r"\.(.*)\.", found_id)[0]
        out += "%s = { IS-A @ONT.%s; };\n" % (found_id, isa)

    frame_output = []
    if anchor_to_graph:
        return OntoLang().run(out)  # TODO: convert to str or fix return val
    else:
        return out
