from pkg_resources import resource_listdir
from pkgutil import get_data
from typing import List, Union
import re

# from ontoagent.utils.analysis import TextAnalyzer
from ontoagent.engine.xmr import TMR
from ontograph.Frame import Frame
from ontograph.Query import (
    AndComparator,
    ExistsComparator,
    InSpaceComparator,
    Query,
    SelectPipeline,
)

from ontograph import graph


def is_speech_act(elem: Union[str, Frame]):
    """
    Determine if a given element is a speech act. 

    TODO: 
        [] - Update speech act list
        [] - Do ontological lookup rather than string matching
    """
    speech_acts = ["REQUEST-ACTION", "REQUEST-INFO", "INFORM"]
    s = elem.id if isinstance(elem, Frame) else elem
    return True if True in list(map(lambda sa: sa in s, speech_acts)) else False


def get_tmr_element(schema_element: Frame, tmr: TMR):
    """
        Get respective TMR element for a given schema element.

        TODO: 
            [] - Update rules for element matching
        """

    # Hard rules for which Schema elements match which TMR elements.
    if is_speech_act(schema_element):
        if tmr.root().id.split(".")[1].replace("-", "_") in schema_element.id:
            return tmr.root()
    elif "SUBJECT" in schema_element.id:
        return tmr.root()["THEME"].singleton()["AGENT"].singleton()
    elif "HEAD" in schema_element.id:
        return tmr.root()["THEME"].singleton()
    elif "DIRECTOBJECT" in schema_element.id:
        root = tmr.root()["THEME"].singleton()
        return root["THEME"].singleton()
    elif "OBJECT" in schema_element.id:
        root = tmr.root()["THEME"].singleton()
        return root["DESTINATION"].singleton()
    return None


def dict_to_signal(tmr: dict):
    ontosem = ontosem_to_ontolang(tmr["results"][0])
    # print(ontosem)
    # analyzer.cache(tmr["OriginalSentence"], ontosem)
    # tmr = analyzer.to_signal(tmr["OriginalSentence"])

    return tmr


def cache_tmrs():
    cache_package = "demo.tmr_cache"

    tmrs = map(
        lambda f: (cache_package, f),
        filter(lambda f: f.endswith(".knowledge"), resource_listdir(cache_package, "")),
    )
    tmrs = map(lambda t: get_data(t[0], t[1]).decode("utf-8"), tmrs)

    def extract_utterances(tmr: str) -> List[str]:
        results = []
        lines = tmr.split("\n")
        for line in lines:
            if line.startswith("// Text:"):
                results.append(line.replace("// Text:", "").strip())
        return results

    tmrs = map(lambda t: (extract_utterances(t), t), tmrs)

    tmr_dict = {}
    for tmr in tmrs:
        for utterance in tmr[0]:
            analyzer.cache(utterance, tmr[1])
            tmr_dict[utterance] = analyzer.to_signal(utterance)

    return tmr_dict


def ontosem_to_ontolang(_tmr: dict) -> str:
    tmr = _tmr["TMR"]

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

    def _fix_frame_id(frame: str) -> str:
        instance = re.findall(r"-([0-9]+)$", frame)[0]
        frame_id = re.sub(r"-[0-9]+$", ".%s?" % instance, frame)
        frame_id = "@[TMR].%s" % frame_id

        found_ids.add(frame_id)
        return frame_id

    def _convert_value(_property, value):
        if isinstance(value, str):
            if "HUMAN" in value:
                value = "@[TMR].HUMAN.1?"
                found_ids.add(value)
                return value
            if "ROBOT" in value:
                value = "@[TMR].ROBOT.1?"
                found_ids.add(value)
                return value
            if Frame("@ONT.%s" % _property.upper()) ^ Frame("@ONT.RELATION"):
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
            return '"%s"' % value
        return value

    def _convert_frame(frame: str, contents: dict) -> str:
        frame_id = _fix_frame_id(frame)
        built_ids.add(frame_id)
        properties = ["IS-A @ONT.%s;" % contents["INSTANCE-OF"]]
        for k in contents.keys():
            if k.lower() == k:
                continue
            if k.lower() in inverses:
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

        out += _convert_frame(key, tmr[key]) + "\n"

    for found_id in found_ids.difference(built_ids):
        isa = re.findall(r"\.(.*)\.", found_id)[0]
        out += "%s = { IS-A @ONT.%s; };\n" % (found_id, isa)

    return out
