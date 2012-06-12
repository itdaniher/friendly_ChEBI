import pymongo
from pprint import pprint

connection = pymongo.Connection('localhost')
db = connection.chemicals

findCompound = lambda regex: list(db.chebi.find({'$or':[{'ChEBI Name':regex},{'IUPAC Names':regex},{'Synonyms':regex}]}))
pprint(findCompound("ethane")[0])
