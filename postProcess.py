import chemkit
from pprint import pprint
import json
import gzip
import ast
import re

compounds = json.loads(gzip.open('ChEBI_complete.json.gz').read())

def lowerKeys(x):
	""" convert all keys in the provided dictionary to lowercase """
	if isinstance(x, list):
		return [lowerKeys(v) for v in x]
	if isinstance(x, dict):
		return dict((k.lower(), lowerKeys(v)) for k, v in x.iteritems())
	return x


def addImplicitHydrogens(molecule):
	""" iterate through atoms in the molecule and add hydrogens 
	to atoms not matching their expected valence """
	atoms = molecule.atoms()
	for atom in atoms:
		while atom.valence() < atom.element().expectedValence():
			hydrogen = molecule.addAtom("H")
			molecule.addBond(atom, hydrogen)

def addInfo(compound):
	""" process raw json element to chemjson and add molecular geometry """
	def normalizeMolfile(molfile):
		count = [bool(re.search("^ *[0-9]+ *[0-9]+ .*", item)) for item in molfile.splitlines()].index(True)
		if count < 3:
			return normalizeMolfile('\n'+molfile)
		if count > 3:
			return normalizeMolfile(molfile[1::])
		else:
			return molfile
	compound = lowerKeys(compound)
	moleculeFile = chemkit.MoleculeFile()
	moleculeFile.setFormat("sdf")
	molfile = normalizeMolfile(compound["molfile"])
	moleculeFile.readString(molfile)
	moleculeFile.setFormat("cjson")
	if 'charge' not in compound.keys() or compound['charge'] == 0: 
		addImplicitHydrogens(moleculeFile.molecule())
#	chemkit.CoordinatePredictor.predictCoordinates(moleculeFile.molecule())
#	chemkit.MoleculeGeometryOptimizer.optimizeCoordinates(moleculeFile.molecule())
	results = ast.literal_eval(moleculeFile.writeString())
	if 'name' in results.keys():
		del results['name']
	compound.update(results)
	del compound['molfile']
	if 'formulae' in compound.keys():
		del compound['formulae']
	return compound

i = 1
for compound in compounds[i::]:
	print i
	addInfo(compound)
	i += 1
