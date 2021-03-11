from ontogen.engine.analysis import Analysis
from ontogen.engine.construction import generate_cx_combinations, CombinationBuilder
from ontogen.engine.otmr import oTMR
from ontogen.config import OntoGenConfig


from typing import Union, List

import json
import sys


class OntoGenRunner:

    def __init__(self, config: OntoGenConfig):
        self.config = config

    def run_from_file(self, file: str):
        f = open(file, "r")
        tmrs = json.load(f)
        print("\n Loaded", len(tmrs), "TMRs.\n")
        f.close()

        return [self.run(t) for t in tmrs]



    def run(self, otmr: Union[oTMR, dict]):
        # Only ever runs one sentence at a time
        log = OntoGenLogger(self.config)

        # if not isinstance(otmr, oTMR):
            # otmr = oTMR.instance_from_dict(tmr)

        # Preprocess
        # I was thinking that here is where situational MPs can be run
        # pp = Preprocessor(self.config).run(otmr)

        # Generate Candidate Construction Combinations
        # combinations = CombinationBuilder(self.config).run(pp)
        # combinations = generate_cx_combinations(otmr)

        # Prune Candidate Combinations

        # Generate Sentences for Viable Candidates

        # Select the Best Candidate Utterance
        pass


if __name__ == '__main__':
    arguments = sys.argv

    if len(arguments) < 2 or (len(arguments) == 2 and arguments[1].startswith("config=")):
        print("Correct usage: runner.py \"Input text here.\"")
        print("Optional config parameter: runner.py config=ontosem.yml \"Input text here.\"")

    arguments = arguments[1:]

    config = OntoGenConfig()
    if arguments[0].startswith("config="):
        config_file = arguments[0].replace("config=", "")
        config = OntoGenConfig().from_file(config_file)
        arguments = arguments[1:]

    sentence = arguments[0]

    config.load_knowledge()
    runner = OntoGenmRunner(config)
    results = runner.run([sentence])

    for frame in results.sentences[0].semantics[0].basic_tmr.frames.values():
        print(frame.frame_id())
        for p, fillers in frame.properties.items():
            print("--%s = %s" % (p, ",".join(map(lambda f: str(f), fillers))))
    print("----")
    print("SCORE: %f" % results.sentences[0].semantics[0].score)
    print("SCORING:")
    for score in results.sentences[0].semantics[0].scores:
        print("-- %s" % score)

    print(json.dumps(results.to_dict(), indent=2))