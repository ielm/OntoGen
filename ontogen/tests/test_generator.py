from unittest import TestCase

from ontoagent.engine.xmr import TMR
from ontograph.Frame import Frame

from ontogen.generate import generate, handle_input

from ontograph import graph


class GeneratorTestCase(TestCase):
    def test_input_id(self):
        tmr_id = "@TEST.TMR.1"
        tmr = TMR(Frame(tmr_id))
        self.assertTrue(tmr_id in graph)

        test_input = handle_input(tmr_id)


    def test_lexicalization(self):
        pass

    def test_realization(self):
        pass

    def test_generation(self):
        pass

    # def test_demo():
 #        # tmr = get_tmr("WeHaveArrived.json")
 #        tmr = get_tmr("GetTheRedBlock.json")
 #        tmr = dict_to_signal(tmr)
 #        utterance = Generator().generate(tmr, debug=False)
 #        print(utterance)