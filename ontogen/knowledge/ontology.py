from ontomem.exceptions import SingletonError
from ontomem.frame import Frame
from ontomem.memory import MemoryManager
from typing import Dict, Set, Union


# The ontology is a lightweight wrapper around the OntoMem memory.
# It provides direct access to OntoMem frames, and some convenience methods.
# The analysis task doesn't currently write any data to the ontology, so this simple interface is fine.
class Ontology(object):
    def concept(self, name: str) -> Frame:
        name = name.upper()
        if name not in MemoryManager.memory.frames:
            raise Exception("Unknown concept %s." % name)
        return Frame(name)

    def common_ancestors(self, a: str, b: str) -> Set[str]:
        a_ancestors = set(map(lambda f: f.concept, self.concept(a).ancestors()))
        b_ancestors = set(map(lambda f: f.concept, self.concept(b).ancestors()))

        ancestors = a_ancestors.intersection(b_ancestors)
        return ancestors

    def distance_to_ancestor(self, descendant: str, ancestor: str) -> Union[int, None]:
        if descendant == ancestor:
            return 0

        ancestor = self.concept(ancestor)

        def _find_ancestor(start: Frame, distance: int) -> Union[int, None]:
            distances = []
            for parent in start.parents():
                if parent == ancestor:
                    return distance + 1
                d = _find_ancestor(parent, distance + 1)
                if d is None:
                    continue
                distances.append(d)

            if len(distances) == 0:
                return None

            return min(distances)

        result = _find_ancestor(self.concept(descendant), 0)
        return result

    def relations(self) -> Set[str]:
        descendants = set(
            map(lambda f: f.concept, self.concept("RELATION").descendants())
        )
        descendants.add("RELATION")
        return descendants

    def inverses(self) -> Dict[str, str]:
        relation = self.concept("RELATION")
        relations = relation.descendants()
        relations.add(relation)

        inv = {}
        for r in relations:
            try:
                inv[r["INVERSE"].singleton()] = r.concept
            except SingletonError:
                inv["%s-INVERSE" % r.concept] = r.concept

        return inv
