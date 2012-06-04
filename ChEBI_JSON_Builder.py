#!/usr/bin/python
# Ian Daniher - 2012.06.01
# Beerware

import gzip
import json
import urllib
import io

# get ChEBI database from the European Bioinformatics Institute 

#sdfFullText = gzip.open("./ChEBI_complete.sdf.gz").read()
virtualsdfgz = io.BytesIO(urllib.urlopen("ftp://ftp.ebi.ac.uk/pub/databases/chebi/SDF/ChEBI_complete.sdf.gz").read())
sdfFullText = gzip.GzipFile(fileobj=virtualsdfgz, mode="rb").read()

## start parsing SDF

# split string by "$$$$", the SD file segmenter 
sdfFullText = sdfFullText.split("$$$$")

# normalize Molfile data to match formatting for the rest of the file
sdfFullText = ["\n> <Molfile>\n"+item for item in sdfFullText]

# subsegment by looking for "\n> <tag>" 
sdfFullText = [item.split("\n> <") for item in sdfFullText]

# clean up subsegments
stripNewlines = lambda inList: [ item.strip("\n") for item in inList ] 
sdfFullText = map(stripNewlines, sdfFullText)

# split subsegments into key-value pairs
listToTuples = lambda inList: [ string.split('>\n') for string in inList ]
sdfFullText = map(listToTuples, sdfFullText)

# trim off first (garbage/empty) object
sdfFullText = [item[1:-1] for item in sdfFullText]

# split the values into lists by newline
tupleSplitter = lambda inList: dict([ (item[0], item[1].split('\n')) if item[0] != "Molfile" else item for item in inList])
sdfFullText = map(tupleSplitter, sdfFullText)

# define a resliant type normalizer for the chemical key-value groups
def typeChemical(d):
	for key in d.keys():
		if len(d[key]) == 1:
			if key in ['ChEBI ID', 'ChEBI Name', 'InChI', 'InChIKey', 'Formulae', 'Definition', 'SMILES', 'Secondary ChEBI ID', 'IUPAC Names']:
				d[key] = d[key][0]
			elif key in ['Charge', 'Star']:
				d[key] = int(d[key][0])
			elif key in ['Mass']:
				d[key] = float(d[key][0])
	return d
# normalize types
sdfFullText = [typeChemical(d) for d in sdfFullText][0:-1]

# write a gzip'ed JSON dump of the shiny and well-formatted ChEBI database to file
gzip.open("ChEBI_complete.json.gz", 'w').write(json.dumps(sdfFullText, indent=1))
