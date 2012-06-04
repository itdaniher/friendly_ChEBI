from re import compile as rec
import pymongo
db = pymongo.Connection("localhost")
chebi = db.chemicals.chebi
chebi.find_one({'Synonyms':rec('FOOF')})['Molfile']
