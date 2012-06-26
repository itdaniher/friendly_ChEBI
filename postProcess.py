import chemkit
import json
import gzip
import re


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
		if type(molfile) in [str, unicode]:
			molfile = molfile.splitlines()
		count = [bool(re.search("^ *[0-9]+ *[0-9]+ .*", item)) for item in molfile].index(True)
		if count < 3:
			molfile.insert(0, '')
			return normalizeMolfile(molfile)
		elif count > 3:
			molfile.pop(0)
			return normalizeMolfile(molfile)
		else:
			molfile[0:3] = ['']*3
			return '\n'.join(molfile)
			
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
	results = json.loads(moleculeFile.writeString())
	if 'name' in results.keys():
		del results['name']
	compound.update(results)
	del compound['molfile']
	if 'formulae' in compound.keys():
		del compound['formulae']
	return compound

if __name__ == "__main__":
	compounds = json.loads(gzip.open('ChEBI_complete.json.gz').read())
	import time
	start = time.time()
	compounds = [addInfo(compound) for compound in compounds]
	print time.time() - start
	print compounds[0]
