from ontograph_ontolang.OntoLang import OntoLang, OntoLangScript, OntoLangTransformer
from typing import Type
import sys


class OntoGenOntoLang(OntoLang):

    cached_processors = {}

    def __init__(self):
        super().__init__()
        self.resources.insert(0, ("ontogen.resources", "ontogen.lark"))

    def get_transformer_type(self):
        return OntoGenOntoLangTransformer

    def load_knowledge(self, package: str, resource: str):
        from pkgutil import get_data

        input: str = get_data(package, resource).decode("ascii")

        if package + "." + resource in OntoGenOntoLang.cached_processors:
            processors = OntoGenOntoLang.cached_processors[package + "." + resource]
        else:
            processors = self.parse(input)
            OntoGenOntoLang.cached_processors[package + "." + resource] = processors

        script = OntoLangScript()
        for p in processors:
            p.run_with_script(script=script)


class OntoGenOntoLangTransformer(OntoLangTransformer):
    def clazz(self, matches) -> Type:
        index = matches[0].rfind(".")
        module = matches[0][0:index]
        clazz = matches[0][index + 1 :]
        __import__(module)

        return getattr(sys.modules[module], clazz)
