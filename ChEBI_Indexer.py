"""
Usage:
    ChEBI_Indexer.py [options] [JSON_LINE_FILES...]

Options:
    --index PATH    Location of folder to store index. [default: index]
"""

import sqlite3 as sql
import json
import time
import collections

from whoosh.fields import Schema, TEXT, STORED, NUMERIC
import whoosh.index as index
import sys
import mmap
import os.path
from docopt import docopt as magic_docopt

magic_docopt()

chebi = Schema(
    ChEBI=NUMERIC(int, 32, signed=False, stored=True),
    InChI=STORED,
    InChIKey=TEXT(stored=True),
    SMILES=TEXT(stored=True),
    mass=NUMERIC(float, 32, stored=True),
    charge=NUMERIC(int, 32, signed=True, stored=True),
    formula=TEXT(stored=True),
    names=TEXT(stored=True),
    CAS=TEXT(stored=True),
    definition=STORED
)

if os.path.exists(arguments.index):
    ix = index.open_dir(arguments.index)
else:
    os.mkdir(arguments.index)
    ix = index.create_in(arguments.index, chebi)

if not arguments.JSON_LINE_FILES:
    import glob
    arguments["JSON_LINE_FILES"] = glob.glob("chebi_split/*.json")

writer = ix.writer(procs=2, limitmb=512, multisegment=True)


class ChEBIDatastore(object):
    def __init__(self, db_name="chebi_v0.db"):
        self.conn = sql.connect(db_name)
        init_table = "CREATE TABLE IF NOT EXISTS chebi_table (ChEBI INT, names TEXT, mass REAL, charge INT, InChI TEXT, InChIKey TEXT, SMILES TEXT, formula TEXT, CAS TEXT, definition TEXT)"
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
        inserter = "INSERT INTO chebi_table VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        data = [x for x in entity.values()]
        self.cursor.executemany(inserter, [data])
        return self.conn.commit()


if __name__ == "__main__":
    datastore = ChEBIDatastore()
    for JL_FILE in arguments.JSON_LINE_FILES:
        with open(JL_FILE, "r+") as f:
            data = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
            while True:
                line = data.readline()
                if len(line.strip()) < 1:
                    break
                res = json.loads(line.decode("utf-8"))
                try:
                    out = {}
                    out["ChEBI"] = res["ChEBI ID"]
                    out["names"] = "; ".join([res["ChEBI Name"], *res.get("IUPAC Names", []), *res.get("Synonyms", [])])
                    out["mass"] = res["Mass"]
                    out["charge"] = res["Charge"]
                    out["InChI"] = "".join(res.get("InChI", ""))
                    out["InChIKey"] = "".join(res.get("InChIKey",""))
                    out["SMILES"] = res["SMILES"][0]
                    out["formula"] = " ".join(res.get("Formulae",[]))
                    out["definition"] = res.get("Definition", "")
                    out["CAS"] = " ".join(res.get("CAS Registry Numbers",[]))
                    writer.add_document(**out)
                    if not datastore.get_chebi_id(out["ChEBI"]):
                        datastore.add_chebi(out)
                except:
                    pass
    writer.commit()
