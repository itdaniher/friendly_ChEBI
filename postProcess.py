import time
import chemkit
import json
import gzip
import re
import random
import os

def lowerKeys(x):
	""" convert all keys in the provided dictionary to lowercase """
	if isinstance(x, list):
		return [lowerKeys(v) for v in x]
	if isinstance(x, dict):
		return dict((k.lower(), lowerKeys(v)) for k, v in x.iteritems())
	return x


def addImplicitHydrogens(molecule):
	""" iterate through atoms in the molecule and add hydrogens to atoms not matching their expected valence """
	atoms = molecule.atoms()
	for atom in atoms:
		if atom.neighbors():
			position = atom.neighbors()[0].position()
			while atom.valence() < atom.element().expectedValence():
				hydrogen = molecule.addAtom("H")
				hydrogen.setPosition(position.x()+random.random(), position.y()+random.random(), position.z()+random.random())
				molecule.addBond(atom, hydrogen)

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

chunk = lambda l, x: [l[i:i+x] for i in xrange(0, len(l), x)]
		

def addInfo(compound):
	""" process raw json element to chemjson and add molecular geometry """
	compound = lowerKeys(compound)
	if compound["chebi name"] + ".json" in os.listdir("./compounds"):
		print compound["chebi name"] + " already processed!"
		return json.loads(open("compounds/"+compound["chebi name"]+".json").read())
	moleculeFile = chemkit.MoleculeFile()
	moleculeFile.setFormat("sdf")
	molfile = normalizeMolfile(compound["molfile"])
	moleculeFile.readString(molfile)
	moleculeFile.setFormat("cjson")
	print "starting", compound['chebi name'], '~', sum(json.loads(moleculeFile.writeString())['atoms']['elements'])*2
	if 'charge' not in compound.keys() or compound['charge'] == 0: 
		addImplicitHydrogens(moleculeFile.molecule())
	start = time.time()
	chemkit.CoordinatePredictor.eliminateCloseContacts(moleculeFile.molecule())
	chemkit.MoleculeGeometryOptimizer.optimizeCoordinates(moleculeFile.molecule())
	print '\t', round(time.time()-start, 4)
	compound.update(json.loads(moleculeFile.writeString()))
	del compound['molfile']
	if 'formulae' in compound.keys():
		del compound['formulae']
#	moleculeFile.setFormat("cml")
#	moleculeFile.write("compounds/"+compound["chebi name"]+".cml")
	open("compounds/"+compound["chebi name"]+".json", "w").write(json.dumps(compound))
	return compound

if __name__ == "__main__":
	compounds = json.loads(gzip.open('ChEBI_complete.json.gz').read())
	compounds = [addInfo(compound) for compound in compounds]
	gzip.open('ChEBI_complete.json.gz', 'w').write(json.dumps(compounds))
