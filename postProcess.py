import time
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
	chunk = lambda l, x: [l[i:i+x] for i in xrange(0, len(l), x)]
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
	start = time.time()
	chemkit.CoordinatePredictor.predictCoordinates(moleculeFile.molecule())
	chemkit.MoleculeGeometryOptimizer.optimizeCoordinates(moleculeFile.molecule())
	results = json.loads(moleculeFile.writeString())
	duration = time.time()-start
	if 'name' in results.keys():
		del results['name']
	compound.update(results)
	del compound['molfile']
	if 'formulae' in compound.keys():
		del compound['formulae']
	print round(duration, 4), compound['chebi name']
	return compound

if __name__ == "__main__":
	compounds = json.loads(gzip.open('ChEBI_complete.json.gz').read())
	compounds = [addInfo(compound) for compound in compounds[0:100]]
