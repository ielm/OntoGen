from typing import Union
import random

from ontoagent.engine.xmr import TMR
from ontograph.Frame import Frame
from schema.repository import Repo
from schema.schema import Schema
from lex.lexicon import Lexicon
from lex.lexeme import Lexeme

from ontogen.wordcache import WordCache
from ontogen.utils import is_speech_act, get_tmr_element

speech_acts = ["REQUEST-ACTION", "REQUEST-INFO", "INFORM"]
features = ["MOOD", "SET"]


def select_schema(speech_act: str, tmr: Union[TMR, None]):
    """
    Select a schema given an input oTMR. 

    TODO: 
        [] - Add schema selection tests
        [] - If multiple schemata are left over, choose one at random (for now.)
        [] - 
    """

    # Get initial schema candidate list
    schemata = Repo().get_cat(cat=speech_act)
    # schemata = {}

    # Build each schema candidate
    for key in schemata.keys():
        s = Schema.build(schemata[key])
        s = link_tmr(s, tmr)
        schemata[key] = s

    if tmr is not None:
        # Get head verb from the TMR and get initial lexeme candidate list
        tmr_head = tmr.root()["THEME"].singleton()
        tmr_head_candidates = Lexicon().sem_search(tmr_head.id.split(".")[1])

        # tmr_head_candidates = [l for l in tmr_head_candidates if l['CAT'] != ]

        # Lexicalize schema heads
        schema_candidates = []
        for key in schemata.keys():  # For each schema in schemata

            # Get the head of the schema
            schema = schemata[key]
            schema_head = schema.element("HEAD")

            # Get potential lexeme candidates for the schema head
            tmr_head_candidates = [
                l for l in tmr_head_candidates
                if l["CAT"] == schema_head["CAT"].singleton()
            ]

            # Add tmr_head to the tmr_element slot of the schema head
            schema.add_tmr_element("HEAD", tmr_head)

            # Intersect schema head with tmr_head_candidates
            schema_head_candidates = schema.intersect(schema_head, tmr_head_candidates)

            # Add schema to candidate list if its head has lexical candidates
            if schema_head_candidates:
                schema_candidates.append(schema)

        # A single schema has been selected
        if len(schema_candidates) == 1:
            return schema_candidates[0]

        # No schemata have been selected
        elif not schema_candidates:
            return None

        # System cannot choose a single schema
        else:
            return random.choice(schema_candidates)  # Choose a random one


def link_tmr(schema: Schema, tmr: TMR) -> Schema:
    """
    Link each Schema element with its respective TMR element. 
    """

    for element in schema.elements():
        # Get TMR element for each Schema element
        tmr_element = get_tmr_element(element, tmr)

        # If a TMR element has been found
        if tmr_element is not None:
            # Update tmr_element slot for the respective Schema element
            element["TMR_ELEMENT"] = tmr_element

            # Get element id
            elemid = (
                element["TMR_ELEMENT"].singleton().id.split(".")[1].replace("-", "_")
            )

            # Lexicalize element if element is not root (Speech Act)
            if elemid not in schema.root().id:
                # If element realization is cached in WordCache
                if elemid in WordCache:
                    # Do word selection and stuff here. NOTE: THIS WILL BE MOVED
                    wordtag = WordCache[elemid][0]
                    if "@" in wordtag:
                        word = Lexeme.from_frame(wordtag)
                        element["LEX"] = word.anchor
                    else:
                        parts = wordtag.split("-")
                        if len(parts) > 1:
                            word = Lexeme.build(Lexicon().get_sense(wordtag))
                            element["LEX"] = word.anchor
                        else:
                            element["LEX"] = wordtag

        elif "ROOT-WORD" in element:
            word = Lexeme.build(Lexicon().get_sense(element["ROOT-WORD"].singleton()))
            element["LEX"] = word.anchor

    return schema
