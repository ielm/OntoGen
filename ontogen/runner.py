from ontogen.engine.semantics.compiler import SemanticCompiler
from ontogen.engine.preprocessor import Preprocessor
from ontogen.engine.report import Report
from ontogen.engine.otmr import oTMR
from ontogen.knowledge.ontology import Ontology
from ontogen.knowledge.lexicon import Lexicon
from ontogen.config import OntoGenConfig

from typing import Union

import json
import sys
import ast


class OntoGenRunner:
    def __init__(
        self, config: OntoGenConfig, ontology: Ontology = None, lexicon: Lexicon = None
    ):
        self.config = config if config is not None else OntoGenConfig()
        self.ontology = ontology if ontology is not None else self.config.ontology()
        self.lexicon = lexicon if lexicon is not None else self.config.lexicon()

    def run_from_file(self, file: str):
        f = open(file, "r")
        otmrs = json.load(f)
        print("\n Loaded", len(otmrs), "oTMRs.\n")
        f.close()

        return [self.run(t) for t in otmrs]

    def run(self, otmr: Union[oTMR, dict]):
        if isinstance(otmr, dict):
            otmr = oTMR.instance(self.config, otmr)
            otmr.set_ontology(self.ontology)
            otmr.set_lexicon(self.lexicon)

        report = Report(self.config, otmr)

        # Preprocess - resolve any MPs and reference frames
        pp = Preprocessor(self.config).run(otmr)  # r: preprocessed otmr
        _ = SemanticCompiler(self.config, self.ontology, self.lexicon).run(pp)

        # Generate Sentences for Viable Candidates

        # Select the Best Candidate Utterance

        return Report


if __name__ == "__main__":
    arguments = sys.argv

    if len(arguments) < 2 or (
        len(arguments) == 2 and arguments[1].startswith("config=")
    ):
        print("Correct usage: runner.py tmr_index")
        print("Optional config parameter: runner.py config=ontogen.yml tmr_index")

    arguments = arguments[1:]

    config = OntoGenConfig()
    if arguments[0].startswith("config="):
        config_file = arguments[1].replace("config=", "")
        config = OntoGenConfig().from_file(config_file)
        arguments = arguments[1:]

    with open("tests/resources/sample-TMRs.txt", "r") as file:
        data = file.read()
        tmrs = ast.literal_eval(data)

    tmr_index = int(arguments[0])
    temp = tmrs[tmr_index]["results"][0]["TMR"]
    tmr = {"sentence": tmrs[tmr_index]["sentence"], "tmr": {}}

    for key in temp.keys():
        if key.lower() == key:
            # print(f"---skipping--- {key}: \t {temp[key]}")
            continue  # Skip non-frame elements
        tmr["tmr"][key] = temp[key]

    # == DEV PRINTS == #
    # print(f"TMR FOR: {tmr['sentence']}")
    # pprint(tmr["tmr"])
    # print(f"\n{'-'*80}\n")

    config.load_knowledge()
    runner = OntoGenRunner(
        config,
    )
    results = runner.run(tmr["tmr"])
