from ontogen.engine.otmr import oTMR

from lex.lexicon import Lexicon
from ont.ontology import Ontology
from ontograph import graph

from ontogen.knowledge.lexstuff.utils import sem_search
from ontogen.engine.construction import CombinationBuilder

from typing import Union
from collections import OrderedDict

import json


"""
OntoGen is the NLG service module for OntoAgent. 

It is run as an isolated service module which takes input as a GET request an API 
call. There are two input forms for OntoGen, both via the service API: 
    - OntoGen is sent a full oTMR as a JSON structure, OR
    - OntoGen is sent the OntoGraph Frame ID of the oTMR anchor already in shared 
      memory. 

OntoGen will then follow the generation pipeline and return the generated text per 
the specified return type, which can be:
    - A JSON structure containing the input oTMR with the generated text in the "raw"
      field, OR
    - An OntoGraph Frame ID of the input oTMR anchor, with the "raw" field modified 
      in memory by OntoGen. 
"""


class OntoGenRunner:
    def __init__(
        self,
        log: int = 0,
        dc: int = 0,
        dmp: int = 0,
        return_one_result: int = 0,
        is_robot: int = 0,
        robot_args: dict = None,
    ):
        self.log = log  # log process and results
        self.dc = dc  # display constraint matches
        self.dmp = dmp  # display meaning procedure
        self.return_one_result = return_one_result  # return a single generation result
        self.is_robot = is_robot
        self.robot_args = robot_args if robot_args is not None else {}

    def run(self, otmr: Union[oTMR, OrderedDict, dict, str], debug: bool = False):
        if isinstance(otmr, str):
            # check if it's a frame id and create an otmr from the frame, else raise
            # value error
            pass
        # if isinstance(otmr, dict): # Check for instance type later.

        # TODO: COMBINE MULTIPLE INSTANCE ELEMENTS LIKE REQUEST_ACTION}
        # otmr = self.__process_tmr(otmr)
        # pprint(otmr)

        tmrobj = oTMR.instance_from_dict(otmr)
        print(tmrobj.debug())
        # for item in tmrobj:
        #     print(item.debug())
        # print(tmrobj.root()["AGENT"].singleton().id)

        # self.build_candidate_combinations(otmr)

        """ 
            Will not worry about converting to oTMR yet, this is for the future. Just 
            get the damn thing working first. 
        """
        # if isinstance(otmr, OrderedDict):
        #     # convert otmr to oTMR
        #     otmr = oTMR.instance_from_dict(otmr)
        #     pprint(otmr.root().debug())

        return otmr["sentence"]  # TODO: GET REAL RETURNED VALUE

    # @staticmethod
    # def build_candidate_combinations(otmr):
    #     # Find candidate constructions for each frame in otmr
    #     sem_matches = {}
    #     num_items = 0
    #     for key, element in otmr["tmr"].items():
    #         concept = key.rsplit("-", 1)[0]
    #         sem_matches[concept] = sem_search(concept)
    #         num_items += 1

    #     # [[<candidates for tmr frame #1>], [<...frame #2>], [<...frame #3>], ...]
    #     temp_candidates = []
    #     for key1, _element in sem_matches.items():
    #         # print(key1)
    #         temp_element = []
    #         for key2, _candidate in _element.items():
    #             # print("\t", key2)
    #             # print(_candidate.keys())
    #             temp_element.append({key2: _candidate})
    #         temp_candidates.append(temp_element)

    #     res = list(combine_candidates(*temp_candidates))
    #     return res

    def __process_tmr(otmr):
        pass


if __name__ == "__main__":
    with open("knowledge/sample_otmrs/Could_you_get_the_red_block.json", "r") as file:
        print(file)
        data = json.load(file, object_pairs_hook=OrderedDict)

    OntoGenRunner().run(data)
