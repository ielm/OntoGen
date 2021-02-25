from ontoagent.engine.module import (
    OntoAgentModuleRepository,
    OntoAgentModuleBlueprint,
    OntoAgentRenderingModule,
)
from ontoagent.knowledge.ontology import OntologyOntoLangLoader
from ontoagent.knowledge.loader import KnowledgeLoader
from ontoagent.service.service import OntoAgentModuleService
from ontoagent.engine.xmr import XMR
from ontoagent.agent import Agent
from ontogen.engine.otmr import oTMR
from ontogen.ontogen_runner import OntoGenRunner

from ontograph.drivers.SQLiteDriver import SQLiteDriver
from ontograph.Frame import Frame
from ontograph import graph

from pprint import pprint
from typing import Union

import unittest
import ast


class OntoGenTestCase(unittest.TestCase):
    def setUp(self):
        with open("resources/sample-TMRs.txt", "r") as file:
            data = file.read()
            self.tmrs = ast.literal_eval(data)

        # Uncomment to get TMR index numbers
        # for i, tmr in enumerate(results):
        #     print(f"{i}\t{tmr['sentence']}")

    """ 
    For now, use the following simple sentences in the test set: 
         0. Make a left.
         2. Can you please make a left?
         4. Could you please make a left?
     
         9. Make a slight left.
         12. Can you make a slight left?
         13. Could you please make a slight left?
         
         18. Make a left turn.
         
         36. Make a left at the bridge.
    """

    def test_default(self):
        generator = OntoGenRunner()

        tmr_index = 3
        temp = self.tmrs[tmr_index]["results"][0]["TMR"]

        tmr = {"sentence": self.tmrs[tmr_index]["sentence"], "tmr": {}}

        for key in temp.keys():
            if key.lower() == key:
                continue  # Skip non-frame elements
            # out += _convert_frame(key, temp[key]) + "\n"
            tmr["tmr"][key] = temp[key]

        # == DEV PRINTS == #
        print(f"TMR FOR: {tmr['sentence']}")
        pprint(tmr["tmr"])
        print(f"\n{'-'*80}\n")

        generator.run(tmr)
