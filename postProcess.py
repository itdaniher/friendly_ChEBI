import chemkit
from pprint import pprint
import json
import gzip
import ast

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
		if molfile[0:4].count('\n') > 1:
			return normalizeMolfile(molfile[1::])
		if molfile[0:4].count('\n') < 1:
			return normalizeMolfile('\n'+molfile)
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
	chemkit.CoordinatePredictor.predictCoordinates(moleculeFile.molecule())
	chemkit.MoleculeGeometryOptimizer.optimizeCoordinates(moleculeFile.molecule())
	results = ast.literal_eval(moleculeFile.writeString())
	if 'name' in results.keys():
		del results['name']
	compound.update(results)
	del compound['molfile']
	if 'formulae' in compound.keys():
		del compound['formulae']
	return compound

compounds = [addInfo(compound) for compound in compounds[0:1]]
print compounds
