from pprint import pprint

from schema.schema import Schema
from nlglib.realisation.simplenlg.realisation import Realiser
from nlglib.microplanning import *


realizer = Realiser(host="nlg.kutlak.info", port=40000)


def realize(schema: Schema = None):
    if schema.anchor["EX"] == "Get the red block.":
        subj_head = Noun(schema.tokenize_element(schema.subject()).capitalize())
        subject = NP(subj_head, ",")
        head = Verb(schema.tokenize_element(schema.head()).lower())
        head = VP(head)
        objekt = Noun(schema.tokenize_element(schema.directobject()).lower())
        objekt = NP("the", objekt)
        objekt.premodifiers.append("red")
        p = Clause(subject=subject, predicate=head, objekt=objekt)
        p["TENSE"] = "PRESENT"
        p.features["FORM"] = "IMPERATIVE"
        return realizer(p)

    elif schema.anchor["EX"] == "Where do I turn?":
        whadv = Adverb(schema.tokenize_element(schema.adv()).capitalize())
        aux = Auxiliary(schema.tokenize_element(schema.aux()).lower())
        subject = Noun(schema.tokenize_element(schema.subject()).capitalize())
        head = Verb(schema.tokenize_element(schema.head()).lower())
        head = VP(head)
        p = Clause(subject=subject, predicate=head)
        p["INTERROGATIVE_TYPE"] = "WHERE"
        return realizer(p)
