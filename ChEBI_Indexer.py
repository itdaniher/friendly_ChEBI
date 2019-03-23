"""
Usage:
    ChEBI_Indexer.py [options] [JSON_LINE_FILES...]

Options:
    --index PATH    Location of folder to store index. [default: index]
"""

from whoosh.fields import Schema, TEXT, ID, STORED, NUMERIC
import whoosh.index as index
import sys, mmap, json
import os.path
from docopt import docopt as magic_docopt

magic_docopt()

chebi = Schema(
    ChEBI=NUMERIC(int, 32, signed=False, stored=True),
    InChI=TEXT(stored=True),
    SMILES=TEXT(stored=True),
    mass=NUMERIC(float, 32, stored=True),
    charge=NUMERIC(int, 32, signed=True, stored=True),
    formula=TEXT(stored=True),
    name=TEXT(stored=True),
)

if os.path.exists(arguments.index):
    ix = index.open_dir(arguments.index)
else:
    os.mkdir(arguments.index)
    ix = index.create_in(arguments.index, chebi)

if not arguments.JSON_LINE_FILES:
    import glob
    arguments["JSON_LINE_FILES"] = glob.glob("chebi_split/*.json")

writer = ix.writer(limitmb=512)


json_keys = [
    "Synonyms",
    "ChEBI ID",
    "SMILES",
    "Star",
    "Definition",
    "Charge",
    "KEGG COMPOUND Database Links",
    "PubChem Database Links",
    "Mass",
    "IUPAC Names",
    "ChEBI Name",
    "InChIKey",
    "IntEnz Database Links",
    "Molfile",
    "Rhea Database Links",
    "Monoisotopic Mass",
    "InChI",
    "CAS Registry Numbers",
    "Secondary ChEBI ID",
    "Formulae",
]

import sqlite3 as sql
import json
import time
import collections


class ChEBIDatastore(object):
    def __init__(self, db_name="chebi_v0.db"):
        self.conn = sql.connect(db_name)
        init_table = "CREATE TABLE IF NOT EXISTS chebi_table (ChEBI INT, name TEXT, mass REAL, charge INT, InChI TEXT, SMILES TEXT, formula TEXT)"
        self.conn.execute(init_table)
        create_index = "CREATE INDEX IF NOT EXISTS chebi_index ON chebi_table (ChEBI ASC)"
        self.conn.execute(create_index)
        self.conn.commit()
        self.cursor = self.conn.cursor()

    def get_chebi_id(self, startid):
        selector = "SELECT * FROM chebi_table WHERE ChEBI IS %d" % (startid)
        samples = self.cursor.execute(selector)
        return [x for x in samples]

    def get_chebi_name(self, name):
        selector = "SELECT * FROM chebi-table WHERE name LIKE %s" % (name)
        samples = self.cursor.execute(selector)
        return [x for x in samples]

    def add_chebi(self, entity):
        inserter = "INSERT INTO chebi_table VALUES(?, ?, ?, ?, ?, ?, ?)"
        data = [x for x in entity.values()]
        print(data)
        self.cursor.executemany(inserter, [data])
        return self.conn.commit()


if __name__ == "__main__":
    datastore = ChEBIDatastore()
    for JL_FILE in arguments.JSON_LINE_FILES:
        with open(JL_FILE, "r+") as f:
            data = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
            i = 0
            while True:
                line = data.readline()
                if len(line.strip()) < 1:
                    break
                res = json.loads(line.decode("utf-8"))
                try:
                    # assert res['SMILES'].lower().count('c') < 9
                    out = collections.OrderedDict()
                    out["ChEBI"] = int(res["ChEBI ID"].split(":")[-1])
                    out["name"] = res["ChEBI Name"].lower()
                    out["mass"] = res["Mass"]
                    out["charge"] = res["Charge"]
                    out["InChI"] = res["InChI"]
                    out["SMILES"] = res["SMILES"]
                    out["formula"] = res["Formulae"]
                    if type(out["formula"]) == list:
                        out["formula"] = [x for x in out["formula"] if ("h2o" in x.lower()) or ("." in x)][0]
                    i += 1
                except Exception as e:
                    out = None
                    pass
                if out != None:
                    writer.add_document(**out)
                    datastore.add_chebi(out)
    writer.commit()
