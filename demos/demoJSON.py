import json, gzip, pymongo

chebi = json.loads(gzip.open("ChEBI_complete.json.gz").read())
chebi = chebi[0:-1]

for obj in chebi:
	if 'Synonyms' in obj.keys():
		if 'FOOF' in obj['Synonyms']:
			obj['Molfile']
