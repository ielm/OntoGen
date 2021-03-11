from ontogen.knowledge.lexicon import Lexicon
from ontogen.knowledge.ontology import Ontology
from ontomem.memory import MemoryManager

import os
import yaml


class OntoGenConfig:

    @classmethod
    def from_file(cls, filename: str) -> 'OntoGenConfig':
        with open(filename, "r") as config_file:
            config_dict = yaml.load(config_file, Loader=yaml.FullLoader)
            return OntoGenConfig(
                ontosyn_mem=config_dict["ontosyn-mem-file"],
                ontosyn_lexicon=config_dict["ontosyn-lex-file"],
                corenlp_host=config_dict["corenlp-host"],
                corenlp_port=config_dict["corenlp-port"],
                knowledge_file=config_dict["knowledge-file"],
                semantics_mp_mem=config_dict["semantics-mp-mem-file"]
            )

    def __init__(self,
                 ontosyn_mem: str=None,
                 ontosyn_lexicon: str=None,
                 corenlp_host: str=None,
                 corenlp_port: int=None,
                 knowledge_file: str=None,
                 semantics_mp_mem: str=None
                 ):
        self.ontosyn_mem = self.parameter_environment_or_default(ontosyn_mem, "ONTOSYN-MEM-FILE", "build/ontosem2-new4.mem")
        self.ontosyn_lexicon = self.parameter_environment_or_default(ontosyn_lexicon, "ONTOSYN-LEX-FILE", "ontosyn/lisp/lexicon.lisp")
        self.corenlp_host = self.parameter_environment_or_default(corenlp_host, "CORENLP_HOST", "localhost")
        self.corenlp_port = int(self.parameter_environment_or_default(corenlp_port, "CORENLP_PORT", 9002))
        self.knowledge_file = self.parameter_environment_or_default(knowledge_file, "KNOWLEDGE-FILE", "build/knowledge.om")
        self.semantics_mp_mem = self.parameter_environment_or_default(semantics_mp_mem, "SEMANTICS-MP-MEM-FILE", "build/post-basic-semantic-MPs.mem")
    
    def parameter_environment_or_default(self, parameter, env_var: str, default):
        if parameter is not None:
            return parameter
        if env_var in os.environ:
            return os.environ[env_var]
        return default

    def load_knowledge(self):
        MemoryManager.load_memory(self.knowledge_file)

    # Generates a new Ontology object from the available knowledge
    def ontology(self) -> Ontology:
        return Ontology()

    # Generates a new Lexicon object from the available knowledge
    def lexicon(self) -> Lexicon:
        return Lexicon()

    def to_dict(self) -> dict:
        return {
            "ontosyn-mem": self.ontosyn_mem,
            "ontosyn-lexicon": self.ontosyn_lexicon,
            "corenlp-host": self.corenlp_host,
            "corenlp-port": self.corenlp_port,
            "knowledge-file": self.knowledge_file,
            "semantics-mp-mem": self.semantics_mp_mem
        }