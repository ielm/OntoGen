from ontograph.Frame import Frame
from ontograph import graph
from lex.lexicon import Lexicon
from ont.ontology import Ontology

from ontogen.utils.oTMR import oTMR


from pprint import PrettyPrinter, pprint

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

    def run(self, otmr: oTMR, debug: bool = False):
        return "oTMR successfully input!"
