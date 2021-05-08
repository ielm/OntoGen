from ontogen.engine.preprocessor import Preprocessor
from ontogen.engine.compiler import CandidateCompiler
from ontogen.engine.realizer import Realizer
from ontogen.engine.report import Report
from ontogen.engine.otmr import oTMR
from ontogen.knowledge.ontology import Ontology
from ontogen.knowledge.lexicon import Lexicon
from ontogen.config import OntoGenConfig

# from simplenlg.framework import *  # TODO - make sure imports are right

from typing import Union
from pprint import pprint

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

    def run(self, input_otmr: Union[oTMR, dict]):
        if isinstance(input_otmr, dict):
            otmr = oTMR.instance(self.config, input_otmr)
            otmr.set_ontology(self.ontology)
            otmr.set_lexicon(self.lexicon)

        # Create report for config, otmr, and candidates
        report = Report(self.config, otmr)

        # Print oTMR to console
        ignore_print_frames = ["MEANING-PROCEDURE"]
        pprint(
            [
                v.to_dict()
                for k, v in report.get_otmr().items()
                if v.concept not in ignore_print_frames
            ]
        )
        print(f"\n{'-' * 80}\n")

        # Preprocess - resolve any MPs and reference frames
        Preprocessor(self.config).run(report)

        print("Candidate Reduction:")
        # Select and compile candidate constructions
        CandidateCompiler(self.config, self.ontology, self.lexicon).run(report)

        # Print selected Realization Candidates
        print("\nRealization Candidates:")
        pprint(report.get_candidates())

        print("\nRealizations:")
        # Generate Sentences for Viable Candidates
        for realization_candidate in report.get_candidates():
            Realizer(self.config).run(realization_candidate)

        # Select the Best Candidate Utterance

        return report


if __name__ == "__main__":

    # Handle argument parsing
    arguments = sys.argv
    if len(arguments) < 2 or (
        len(arguments) == 2 and arguments[1].startswith("config=")
    ):
        print("Correct usage: runner.py tmr_index")
        print("Optional config parameter: runner.py config=ontogen.yml tmr_index")
    arguments = arguments[1:]

    # Build config with argument values
    config = OntoGenConfig()
    if arguments[0].startswith("config="):
        config_file = arguments[1].replace("config=", "")
        config = OntoGenConfig().from_file(config_file)
        arguments = arguments[1:]

    # # Read sample TMRs from file
    # with open("../tests/resources/driving_tmrs.txt", "r") as file:
    #     data = file.read()
    #     tmrs = ast.literal_eval(data)

    # tmr_index = int(arguments[0])
    # temp = tmrs[tmr_index]["results"][0]["TMR"]
    # tmr = {"sentence": tmrs[tmr_index]["sentence"], "tmr": {}}

    # for key in temp.keys():
    #     if key.lower() == key:
    #         # print(f"---skipping--- {key}: \t {temp[key]}")
    #         continue  # Skip non-frame elements
    #     tmr["tmr"][key] = temp[key]

    with open("../tests/resources/simple_tmrs.txt", "r") as file:
        data = file.read()
        tmrs = ast.literal_eval(data)

    tmr_index = int(arguments[0])
    tmr = tmrs[tmr_index]

    # == DEV PRINTS == #
    print(f"TMR FOR: {tmr['sentence']}")
    # pprint(tmr["tmr"])
    print(f"{'-'*80}\n")

    # Load knowledge and build OntoGen runner with config
    config.load_knowledge()
    runner = OntoGenRunner(
        config,
    )

    # Run OntoGen runner
    results = runner.run(tmr["tmr"])
