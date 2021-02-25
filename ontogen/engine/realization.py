from simplenlg.framework import *
from simplenlg.lexicon import *
from simplenlg.realiser.english import *
from simplenlg.phrasespec import *
from simplenlg.features import *


def main():
	# Test SimpleNLG factories
    lexicon = Lexicon.getDefaultLexicon()
    nlgfactory = NLGFactory(lexicon)
    realizer = Realiser(lexicon)


if __name__ == "__main__":
    main()
