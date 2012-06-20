import pymongo
import sys

from pprint import pprint

connection = pymongo.Connection('localhost')
db = connection.chemicals

findCompound = lambda regex: list(db.chebi.find({'$or':[{'ChEBI Name':regex},{'IUPAC Names':regex},{'Synonyms':regex}]}))
pprint(findCompound(sys.argv[1])[0])
