from ontoagent.engine.signal import TMR
from schema.repository import Repo
from schema.schema import Schema
from lex.lexicon import Lexicon
from typing import Union

speech_acts = ["REQUEST-ACTION", "REQUEST-INFO", "INFORM"]
features = ["MOOD", "SET"]


def select_schema(speech_act: str, tmr: Union[TMR, None]):
    # Get schema list and build Schemata
    repo = Repo().get_cat(cat=speech_act)
    schemata = {}

    for key in repo.keys():
        s = Schema.build(repo[key], tmr)
        schemata[key] = s

    if tmr is not None:
        # Get head verb from the TMR and get initial lexeme candidate list
        tmr_head = tmr.root()["THEME"].singleton()
        tmr_head_candidates = Lexicon().sem_search(tmr_head.id.split(".")[1])

        # tmr_head_candidates = [l for l in tmr_head_candidates if l['CAT'] != ]

        # Lexicalize schema heads
        schema_candidates = []
        for key in schemata.keys():
            schema = schemata[key]
            schema_head = schema.element('HEAD')
            tmr_head_candidates = [l for l in tmr_head_candidates if l['CAT'] == schema_head["CAT"].singleton()]

            schema.add_tmr_element('HEAD', tmr_head)
            schema_head_candidates = schema.intersect(schema_head,
                                                      tmr_head_candidates)
            if schema_head_candidates:
                schema_candidates.append(schema)
        if len(schema_candidates) == 1:
            return schema_candidates[0]
        elif schema_candidates == []:
        	return None
        else:
            return schema_candidates