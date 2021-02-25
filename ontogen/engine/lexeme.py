from ontograph.Frame import Frame
from ontograph.Space import Space
from ontograph import graph
from ontoagent.utils.common import AnchoredObject
from typing import List, Union
from collections import OrderedDict
import re


class Lexeme(AnchoredObject):
    @classmethod
    def build(cls, ldict: OrderedDict) -> "Lexeme":
        sense = ldict["SENSE"].split("-")
        sense_num = re.findall(r"\d*\Z", sense[1])[0]
        space = Lexeme.next_available_space("LEX")

        name = f"@LEX.{sense[0]}.{sense_num}"
        if name in graph:
            return Lexeme(graph[name])
        else:
            anchor = Frame(name)
            l = Lexeme(anchor)
            l.set_space(space)
            l.__populate(ldict)
            return l

    @classmethod
    def from_frame(cls, frame: Union[Frame, str]) -> "Lexeme":
        frame = frame.id if isinstance(frame, Frame) else frame
        if frame in graph:
            return Lexeme(graph[frame])
        else:
            return None

    @classmethod
    def next_available_space(cls, header: str = None) -> Space:
        if header is None:
            header = "LEX"

        spaces = list(graph)
        spaces = filter(lambda space: space.name.startswith(header + "#"), spaces)
        spaces = map(lambda space: int(space.name.replace(header + "#", "")), spaces)
        spaces = list(spaces)

        next = 1 if len(spaces) == 0 else max(spaces) + 1
        return Space(header + "#" + str(next))

    def word(self):
        return self.anchor["WORD"].singleton()

    def cat(self):
        return self.anchor["CAT"].singleton()

    def root(self) -> Frame:
        return self.anchor["ROOT"].singleton()

    def set_root(self, root: Frame):
        self.anchor["ROOT"] = root

    def elements(self) -> List[Frame]:
        return list(self.anchor["HAS-ELEMENT"])

    def add_element(self, element: Frame):
        self.anchor["HAS-ELEMENT"] += element
        self.add_constituent(element)

    def get_element(self, name: Union[str, Frame]) -> Union[Frame, None]:
        if isinstance(name, Frame):
            name = name.id.split(".")[1]
        for element in self.elements():
            if name in element.id:
                return element
        return None

    def constituents(self) -> List[Frame]:
        return list(self.anchor["HAS-CONSTITUENT"])

    def add_constituent(self, constituent: Frame):
        self.anchor["HAS-CONSTITUENT"] += constituent

    def resolve_pointer(self, pointer: str) -> Union[Frame, None]:
        pointer = re.sub("[?^]", "", str(pointer))
        for element in self.elements():
            if element["ROOT"] == pointer:
                return element
        return None

    def space(self) -> Space:
        return Space(self.anchor["SPACE"].singleton().replace("@", "", 1))

    def set_space(self, space: Union[str, Space]):
        if isinstance(space, Space):
            space = "@" + space.name
        self.anchor["SPACE"] = space

    def debug(self) -> dict:
        out = {}
        for constituent in self.constituents():
            results = {}
            for slot in constituent.slots():
                results[slot.property] = slot.debug()
            out[constituent.id] = results
        return out

    @staticmethod
    def is_pointer(s: str) -> bool:
        if "^" in s or "$" in s:
            return True
        else:
            return False

    ##############################################################
    # -----------------------  INTERNAL  ----------------------- #
    ##############################################################

    def __populate(self, content: OrderedDict):
        self.__process_metadata(content)
        self.__process_syn_struc(content["SYN-STRUC"])
        self.__process_sem_struc(content["SEM-STRUC"])

    def __process_metadata(self, content: OrderedDict):
        # def __set_metadata(_id: str, _content: Union[OrderedDict, list, str]):
        #     # TODO - Do typechecking
        #     self.anchor[_id] = _content

        for item in content.keys():
            if item != "SYN-STRUC" and item != "SEM-STRUC":
                # __set_metadata(item, content[item])
                # TODO - Do typechecking
                self.anchor[item] = content[item]

    def __process_syn_struc(self, syn_struc):
        def __build_element(_id: str, _content: OrderedDict) -> Frame:
            elem = Frame(f"@{self.space().name}.{_id}.?")
            for key in _content.keys():
                elem[key] = _content[key]
            # if elem is pp, do something here
            # elem["ROOT"] = _content["ROOT"]
            # elem["CAT"]  = _content["CAT"]
            self.add_element(elem)
            return elem

        root_elem = OrderedDict({"ROOT": syn_struc["ROOT"], "CAT": syn_struc["CAT"]})
        elements = [__build_element("ROOT", root_elem)]
        self.set_root(self.get_element("ROOT"))
        for item in syn_struc.keys():
            if isinstance(
                syn_struc[item], OrderedDict
            ):  # if item != "ROOT" and item != "CAT":
                elements.append(__build_element(item, syn_struc[item]))
            else:
                self.root()[item]

    def __process_sem_struc(self, sem_struc):
        def __process_concept(name: str, concept: OrderedDict, element: str = "ROOT"):
            element_sem = Frame(f"@{self.space().name}.{element}_SEM.?")
            element_sem["SEM"] = name
            self.add_constituent(element_sem)
            for relation in concept.keys():
                if isinstance(concept[relation], OrderedDict):
                    if self.is_pointer(concept[relation]):
                        pass
                    else:
                        if self.is_pointer(concept[relation]["VALUE"]):
                            element = self.resolve_pointer(concept[relation]["VALUE"])
                            if element is not None:
                                element_sem[relation] = element
                        else:
                            element_sem[relation] = concept[relation["VALUE"]]
            self.root()["SEM"] = element_sem

        if isinstance(sem_struc, str):
            pass
        elif isinstance(sem_struc, OrderedDict):
            for item in sem_struc.keys():
                if self.is_pointer(item):
                    (f"pointer: {item}")

                if item == "MODALITY":
                    pass
                else:
                    __process_concept(item, sem_struc[item], element="ROOT")
