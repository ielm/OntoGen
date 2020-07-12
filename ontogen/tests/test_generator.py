from unittest import TestCase
from pathlib import Path
import os

from ontoagent.engine.xmr import TMR
from ontograph.Frame import Frame
from ontograph_ontolang.OntoLang import OntoLang
from schema.api import SchemaAPI
from schema.schema import Schema
from pymongo import MongoClient

from ontogen.generate import generate, handle_input, handle_schema_selection
from ontogen.schema import select_schema


from ontograph import graph


ROOT_DIR = Path(f"{os.path.abspath(__file__)}").parent.parent


class GeneratorTestCase(TestCase):

    def setUp(self):
        import schema.management
        import os

        schema.management.DATABASE = "unittest"
        os.environ[schema.management.REPO_ACTIVE] = "unittest"

    def tearDown(self):
        MONGO_HOST = "localhost"
        MONGO_PORT = 27017
        DATABASE = "unittest"

        client = MongoClient(MONGO_HOST, MONGO_PORT)
        client.drop_database(DATABASE)

    def test_input_id(self):
        tmr_id = "@TEST.TMR.1"
        tmr = TMR(Frame(tmr_id))
        self.assertTrue(tmr_id in graph)

        test_input = handle_input(tmr_id)
        self.assertTrue(isinstance(test_input, TMR))

    def test_input_string(self):
        string = "This is a test string."
        test_input = handle_input(string)
        self.assertTrue(isinstance(test_input, str))

    def test_input_tmr(self):
        tmr = TMR.instance()
        tmr_id = tmr.anchor.id
        self.assertTrue(tmr_id in graph)

        test_input = handle_input(tmr)
        self.assertTrue(isinstance(test_input, TMR))
        
    def test_select_schema(self):
        with open(f"{ROOT_DIR}/tests/resources/gettheredblock.knowledge", "r") as f:
            s = f.read()
            OntoLang().run(s)
            f.close()

        tmr = TMR.instance(root_type="@ONT.REQUEST_ACTION")
        tmr.set_root(Frame("@TMR1.REQUEST_ACTION.1"))
        test_input = handle_input(tmr)
        speech_act = tmr.root().id.split(".")[1].replace("-", "_")
        test_schema = select_schema(speech_act, tmr)

        self.assertTrue(isinstance(test_input, TMR))
        self.assertTrue(isinstance(test_schema, Schema))
        self.assertEqual(test_schema.root().name(), tmr.root().name())

    def test_lexicalization(self):
        pass

    def test_realization(self):
        pass

    def test_generation(self):
        pass

