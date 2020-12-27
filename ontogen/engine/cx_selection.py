import json

from pprint import pprint

from typing import List
from collections import OrderedDict


def boostrap_speech_act_cxs() -> dict:
    data = OrderedDict
    with open("../knowledge/constructions/speech-acts-lexicon.json", "r") as file:
        data = json.load(file, object_pairs_hook=OrderedDict)
    return data


def get_cx_by_speech_act(cxs: dict = None, speech_act: str = None) -> List:
    if not cxs:
        cxs = boostrap_speech_act_cxs()
    if not speech_act:
        raise ValueError("Cannot query constructions with empty speech act.")

    # TODO: THERE SHOULD BE DEEPER SELECTIONAL CONSTRAINTS
    return [c for _, c in cxs.items() if speech_act in c["SEM-STRUC"].keys()]


if __name__ == "__main__":
    sa = "REQUEST-ACTION"
    cxs = get_cx_by_speech_act(speech_act=sa)
    print(f"There are {len(cxs)} cxs for {sa}:")
    i = 1
    for c in cxs: 
    	print(f"\t{i}. {c['SENSE']}\t->  {c['EX']}")
    	i += 1
