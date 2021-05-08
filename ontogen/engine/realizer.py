from ontogen.engine.candidate import RealizationCandidate, ConstructionCandidate
from ontogen.config import OntoGenConfig

from simplenlg.framework import *
from simplenlg.lexicon import *
from simplenlg.realiser.english import *
from simplenlg.phrasespec import *
from simplenlg.features import *

from pprint import pprint


"""
This is a wrapper around pySimpleNLG to eliminate redundant naming between SimpleNLG
and OntoGen. 
"""
class Realizer:
    def __init__(self, config: OntoGenConfig):
        self.lexicon = Lexicon.getDefaultLexicon()
        self.nlgfactory = NLGFactory(self.lexicon)
        self.realizer = Realiser(self.lexicon)

    def run(self, realization_candidate: RealizationCandidate):
        # s1 = self.nlgfactory.createSentence("my dog is happy")
        # output = self.realizer.realiseSentence(s1)

        # print(output)
        # out = self.nlgfactory.createClause()

        # out.setSubject(realization_candidate.subject())

        # if len(realization_candidate.constructions) == 3:
        #     cxs = [c for c in realization_candidate.constructions]
        #     # print(cxs[0].sense.id.split('-')[0])
        #     vphrase = self.nlgfactory.createVerbPhrase(cxs[0].sense.id.split('-')[0].lower())
        #     out.setVerb(vphrase)
        #     # out.setSubject(cxs[2].sense.id.split('-')[0])
        #     obj = self.nlgfactory.createNounPhrase(cxs[2].sense.id.split('-')[0].lower())
        #     out.setObject(obj)
        #     iobj = self.nlgfactory.createNounPhrase(cxs[1].sense.id.split('-')[0].lower())
        #     out.setIndirectObject(iobj)
        #
        # print(self.realizer.realiseSentence(out))

        cxs = [c for c in realization_candidate.constructions]
        verb = cxs[0].sense.id.split('-')[0].lower()
        directobject = cxs[1].sense.id.split('-')[0].lower()
        indirectobject = cxs[2].sense.id.split('-')[0].lower()

        schema = f"{verb} the {directobject} to the {indirectobject}.".capitalize()

        print(schema)
        # print()
        # for cx_candidate in realization_candidate:
        #     pprint(cx_candidate.to_dict())


        pass


# def main():
#     # Test SimpleNLG factories
#     lexicon = Lexicon.getDefaultLexicon()
#     nlgfactory = NLGFactory(lexicon)
#     realizer = Realiser(lexicon)

#     s1 = nlgfactory.createSentence("my dog is happy")

#     output = realizer.realiseSentence(s1)

#     print(output)


if __name__ == "__main__":
    realizer = Realizer()
    realizer.run()