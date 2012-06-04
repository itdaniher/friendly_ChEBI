#!/usr/bin/python
import json, gzip, pymongo

chebi = json.loads(gzip.open("ChEBI_complete.json.gz").read())

connection = pymongo.Connection("mongodb://localhost")
db = connection.chemicals
[db.chebi.insert(obj) for obj in chebi]
