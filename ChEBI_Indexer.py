from whoosh.fields import Schema, TEXT, ID, STORED, NUMERIC

chebi = Schema(ChEBI=NUMERIC(int, 32, signed=False), InChI=TEXT(stored=True), SMILES=TEXT(stored=True), mass=NUMERIC(float, 32), charge=NUMERIC(int, 32, signed=True), formula=TEXT(stored=True), name=TEXT(stored=True))

import os.path
from whoosh.index import create_in

if not os.path.exists("chebi_index"):
    os.mkdir("chebi_index")

ix = create_in("chebi_index", chebi)

writer = ix.writer(limitmb=192)

import sys, mmap, json

json_keys = ['Synonyms', 'ChEBI ID', 'SMILES', 'Star', 'Definition', 'Charge', 'KEGG COMPOUND Database Links', 'PubChem Database Links', 'Mass', 'IUPAC Names', 'ChEBI Name', 'InChIKey', 'IntEnz Database Links', 'Molfile', 'Rhea Database Links', 'Monoisotopic Mass', 'InChI', 'CAS Registry Numbers', 'Secondary ChEBI ID', 'Formulae']

import sqlite3 as sql
import json
import time
import collections

class ChEBIDatastore(object):

    def __init__(self, db_name = 'chebi_v0.db'):
        self.conn = sql.connect(db_name)
        init_table = 'CREATE TABLE IF NOT EXISTS chebi_table (ChEBI INT, name TEXT, mass REAL, charge INT, InChI TEXT, SMILES TEXT, formula TEXT)'
        self.conn.execute(init_table)
        create_index = 'CREATE INDEX IF NOT EXISTS chebi_index ON chebi_table (ChEBI ASC)'
        self.conn.execute(create_index)
        self.conn.commit()
        self.cursor = self.conn.cursor()

    def get_measurement_vectors(self, start = 0, stop = -1):
        if stop == -1:
            stop = time.time()
        selector = 'SELECT * FROM readings WHERE Timestamp BETWEEN %s AND %s' % (
            str(start), str(stop))
        samples = self.cursor.execute(selector)
        labels = 'timestamp sensor_uid units value'.split()
        values = dict(zip(labels, zip(*samples)))
        values['units'] = [unit_list[unit] for unit in values['units']]
        return values

    def add_chebi(self, entity):
        inserter = "INSERT INTO ChEBI VALUES(?, ?, ?, ?, ?, ?, ?)"
        data = [x for x in entity.values()]
        print(data)
        self.cursor.executemany(inserter, [data])
        return self.conn.commit()

datastore = ChEBIDatastore() 
with open(sys.argv[1], 'r+') as f:
    data = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
    i = 0
    while True:
        line = data.readline()
        if len(line.strip()) < 1:
            break
        res = json.loads(line.decode('utf-8'))
        try:
            assert res['SMILES'].lower().count('c') < 4
            out = collections.OrderedDict() 
            out['ChEBI'] = int(res['ChEBI ID'].split(':')[-1])
            out['name'] = res['ChEBI Name'].lower()
            out['mass'] = res['Mass']
            out['charge'] = res['Charge']
            out['InChI']= res['InChI']
            out['SMILES'] = res['SMILES']
            out['formula'] = res['Formulae']
            if (type(out['formula']) == list):
                out['formula'] = [x for x in out['formula'] if ('h2o' in x.lower()) or ('.' in x)][0]
            writer.add_document(**out)
            datastore.add_chebi(out)
            i += 1
        except Exception as e:
            pass
    writer.commit()
