import chemkit
from pprint import pprint
import json
import gzip
import traceback

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
	try:
		f = chemkit.MoleculeFile()
		f.setFormat("sdf")
		molfile = compound["Molfile"][1::]
		f.readString(molfile)
		f.setFormat("cjson")
		if 'Charge' not in compound.keys() or compound['Charge'] == 0: 
			addImplicitHydrogens(f.molecule())
		#chemkit.CoordinatePredictor.predictCoordinates(f.molecule())
		#chemkit.MoleculeGeometryOptimizer.optimizeCoordinates(f.molecule())
		compound.update(json.loads(f.writeString()))
		del compound['Molfile']
		del compound['Formulae']
		compound = lower_keys(compound)
		return compound
	except Exception:
		traceback.print_exc()
		print compound
compounds = [addInfo(compound) for compound in compounds]
