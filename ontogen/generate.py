from typing import Union

from ontoagent.engine.xmr import TMR
from ontograph.Identifier import Identifier

from ontogen.lexicalize import lexicalize
from ontogen.realize import realize
from ontogen.schema import select_schema

from ontograph import graph


def generate(input: Union[str, TMR]=None, debug: bool = False):

    if input is None:
        raise TypeError("Can't generate from nothing.")
    if debug: 
        print(list(map(lambda c: (c.id, c.debug()), tmr.constituents())))       

    # schema = input(input)
    handled_input = handle_input(input)
    if isinstance(handled_input, TMR):
        if debug: 
            print(handled_input.root().id)

        schema = handle_schema_selection(handled_input)

        schema = lexicalize(schema, handled_input)
        if debug:
            print(list(map(lambda c: (c.id, c.debug()), schema.constituents())))

        realization = realize(schema)
        if debug:
            print(realization)

        speech_signal = realization
        # speech_signal = to_signal(realization)
        # if debug:
        #     print(speech_signal)

        return speech_signal

    elif isinstance(handled_input, str):  # will just be a string for now, will convert to signal later
        print(handled_input)
        if debug: 
            print(f"Printing literal string: {handled_input}")
        exit()

    else:
        raise TypeError("Something went wrong.")


def handle_input(input: Union[str, TMR] = None):

    if isinstance(input, str):
        if input[0] == "@":  # is input a TMR pointer
            parsed = Identifier.parse(input)
            parsed_id = f"@{parsed[0]}.{parsed[1]}.{parsed[2]}"
            if (parsed_id in graph) and (parsed[1] == "TMR"):
                input = TMR(graph[parsed_id])
            else:
                raise TypeError("Input must be a pointer to a TMR.")
        else:  # is input a literal string
            pass

    return input


def handle_schema_selection(tmr: TMR):
    if isinstance(tmr, TMR):
        speech_act = tmr.root().id.split(".")[1].replace("-", "_")
        schema = select_schema(speech_act, tmr)
        return schema
    return None






