from ontoagent.engine.xmr import TMR
from ontograph.Frame import Frame
from schema.schema import Schema
from lex.lexicon import Lexicon
from lex.lexeme import Lexeme


def get_tmr_element(schema_element: Frame, tmr: TMR):
    if is_speech_act(schema_element):
        if tmr.root().id.split(".")[1].replace("-", "_") in schema_element.id:
            return tmr.root()

    elif "SUBJECT" in schema_element.id:
        return tmr.root()["BENEFICIARY"].singleton()

    elif "HEAD" in schema_element.id:
        return tmr.root()["THEME"].singleton()

    elif "DIRECTOBJECT" in schema_element.id:
        root = tmr.root()["THEME"].singleton()
        return root["THEME"].singleton()

    return None


def lexicalize(schema: Schema = None, tmr: TMR = None) -> Schema:
    if schema is None:
        raise TypeError("Schema can not be None")

    if tmr is None:
        raise TypeError("TMR can not be None")

    for element in schema.elements():
        if "LEX" in element:
            continue
        else:
            if "TMR_ELEMENT" in element:
                elemid = (
                    element["TMR_ELEMENT"]
                    .singleton()
                    .id.split(".")[1]
                    .replace("-", "_")
                )
                if element["TMR_ELEMENT"].singleton().id == "@SELF.AGENT.1":
                    element["LEX"] = Lexeme.build(Lexicon().get_sense("I-N1")).anchor
                elif elemid not in schema.root().id:  # if element is not root
                    print(f"Further lexicalization needed for: {elemid}")

    return schema
