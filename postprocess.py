import chemkit
from pprint import pprint
import json
import gzip
import ast

compounds = json.loads(gzip.open('ChEBI_complete.json.gz').read())

def lower_keys(x):
	if isinstance(x, list):
		return [lower_keys(v) for v in x]
	if isinstance(x, dict):
		return dict((k.lower(), lower_keys(v)) for k, v in x.iteritems())
	return x


def addImplicitHydrogens(molecule):
	atoms = molecule.atoms()
	for atom in atoms:
		while atom.valence() < atom.element().expectedValence():
			hydrogen = molecule.addAtom("H")
			molecule.addBond(atom, hydrogen)

def addInfo(compound):
	def normalizeMolfile(molfile):
		if molfile[0:4].count('\n') > 1:
			return normalizeMolfile(molfile[1::])
		if molfile[0:4].count('\n') < 1:
			return normalizeMolfile('\n'+molfile)
		else:
			return molfile
	compound = lower_keys(compound)
	f = chemkit.MoleculeFile()
	f.setFormat("sdf")
	molfile = normalizeMolfile(compound["molfile"])
	f.readString(molfile)
	f.setFormat("cjson")
	if 'charge' not in compound.keys() or compound['charge'] == 0: 
		addImplicitHydrogens(f.molecule())
	chemkit.CoordinatePredictor.predictCoordinates(f.molecule())
	chemkit.MoleculeGeometryOptimizer.optimizeCoordinates(f.molecule())
	results = f.writeString()
	results = ast.literal_eval(results)
	if 'name' in results.keys():
		del results['name']
	compound.update(results)
	del compound['molfile']
	if 'formulae' in compound.keys():
		del compound['formulae']
	return compound

compounds = [addInfo(compound) for compound in compounds]
