from pymongo.database import Database

from ontogen.knowledge.lexicon.lexicon import Lexicon as L

from typing import Union
from pprint import pprint


def sem_search(concept: str = None, lexicon: dict = L):

    found = {}

    for lemma, lexemes in lexicon.items():
        for instance, lexeme in lexemes.items():
            if concept in lexeme["SEM-STRUC"]:
                found[instance] = lexeme

    return found


if __name__ == "__main__":
    # want to make sure that the agent can parse the lexicon and find all constructions
    # and lexemes that match a semantic head.

    # sem_search("REQUEST-ACTION")

    lexemes = sem_search("TURN-VEHICLE-LEFT")
    pprint(lexemes)
