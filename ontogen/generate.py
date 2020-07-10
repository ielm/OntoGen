# sys imports
from collections import OrderedDict
from typing import Union
from pprint import pprint

# library imports
from ontoagent.engine.xmr import TMR
from ontograph.Identifier import Identifier
from lex.lexicon import Lexicon
from ont.ontology import Ontology
from schema.repository import Repo
from schema.schema import Schema
from nlglib.realisation.simplenlg.realisation import Realiser

# package imports
from ontogen.lexicalize import lexicalize
from ontogen.realize import realize
from ontogen.ontolang import OntoGenOntoLang
from ontogen.schema import select_schema

from ontograph import graph



def generate(input: Union[str, TMR]=None, debug: bool = False):

    if input is None:
        raise TypeError("Can't generate from nothing.")
    if debug: 
        print(list(map(lambda c: (c.id, c.debug()), tmr.constituents())))       

    # schema = input(input)
    input = handle_input(input)
    if isinstance(input, Schema):
        if debug: 
            print(list(map(lambda c: (c.id, c.debug()), schema.constituents())))
        pass
    elif isinstance(input, str):  # will just be a string for now, will convert to signal later
        print(input)
        if debug: 
            print(f"Printing literal string: {input}")
        exit()
    else:
        raise TypeError("Something went wrong.")
        # exit()

    schema = lexicalize(input, tmr)
    if debug: 
        print(list(map(lambda c: (c.id, c.debug()), schema.constituents())))
    
    realization = realize(schema)
    if debug: 
        print(realization)

    speech_signal = to_signal(realization)
    if debug:
        print(speech_signal)

    return speech_signal

def handle_input(input: Union[str, TMR] = None):

    if isinstance(input, str):
        # check if input is a frame id
        # id? check if frame exists
        #   frame? get tmr 
        #   not frame? raise error
        # not id? check if str is a literal generation string
        #   literal? wrap in speech signal and send to effector
        # nothing worth the time?
        #   do nothing and figure out how to tell the agent "don't know what you meant so i did nothing"
        
        if input[0] == "@":  # is input a TMR pointer
            parsed = Identifier.parse(input)
            id = f"@{parsed[0]}.{parsed[1]}.{parsed[2]}"
            if (id in graph) and (parsed[1]=="TMR"):
                input = TMR(graph[id])
                return input
            else:
                raise TypeError("Input must be a pointer to a TMR.")
        else: # is input a literal string
            pass

    if isinstance(input, TMR):
        speech_act = tmr.root().id.split(".")[1].replace("-", "_")
        schema = select_schema(speech_act, tmr)
        return schema

    return None








