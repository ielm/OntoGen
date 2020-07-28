from typing import Union

from ontoagent.engine.xmr import TMR
from ontograph.Identifier import Identifier

from ontogen.lexicalize import lexicalize
from ontogen.realize import realize
from ontogen.schema import select_schema

from ontograph import graph


def generate(input: Union[str, TMR] = None):
    if input is None:
        raise TypeError("Can't generate from nothing.")

    # Handle input cases
    handled_input = handle_input(input)

    # If input is a correct TMR
    if isinstance(handled_input, TMR):

        # Select a satisfactory schema
        speech_act = handled_input.root().id.split(".")[1].replace("-", "_")
        schema = select_schema(speech_act, handled_input)

        # Lexicalize schema elements
        schema = lexicalize(schema, handled_input)

        # Realize utterance with SimpleNLG
        realization = realize(schema)

        # Wrap realized utterance in a SpeechSignal
        speech_signal = realization
        # speech_signal = to_signal(realization)
        # if debug:
        #     print(speech_signal)

        return speech_signal

    # If input is a literal string
    elif isinstance(handled_input, str):
        # Wrap input in a SpeechSignal
        print(handled_input)
        return handled_input

    else:
        raise TypeError("Something went wrong.")


def handle_input(input: Union[str, TMR] = None):
    if isinstance(input, str):
        if input[0] == "@":
            parsed = Identifier.parse(input)
            parsed_id = f"@{parsed[0]}.{parsed[1]}.{parsed[2]}"
            if (parsed_id in graph) and (parsed[1] == "TMR"):
                input = TMR(graph[parsed_id])
            else:
                raise TypeError("Input must be a pointer to a TMR.")
        else:
            # Do literal string stuff here.
            pass

    return input
