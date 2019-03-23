"""
Usage:
    search.py [options] (KEYWORDS...)

Options:
    --max_count COUNT   Maximum number of results to return. [default: 10]
    --postfix_glob G    Use provided keyword as start of query. Appends G. [default: *]
    --sort_by NAME      Sort results by this field name. Can be charge/formula/mass/name/InChI/SMILES [default: mass]
    --index PATH        Specify path to the index made by ChEBI_Indexer.py. [default: index]
    --prefix_glob G     Preface keyword with G for glob searching.
    --no_glob           Disables globbing.
"""
from docopt import docopt as magic_docopt

import sys
import os

from whoosh.index import open_dir
from whoosh.qparser import QueryParser, FuzzyTermPlugin

magic_docopt()
if not os.path.isdir(arguments.index):
    raise FileNotFoundError("can't find the ChEBI index")

assert arguments.sort_by in "charge/formula/mass/name/InChI/SMILES".split("/")

ix = open_dir(arguments.index)

searcher = ix.searcher()
parser = QueryParser("name", ix.schema)
keyword_sequence = " ".join(arguments.KEYWORDS)

# no special commands
if keyword_sequence.islower() and all([keyword.isalpha() for keyword in keyword_sequence]):
    if not arguments.no_glob and len(arguments.KEYWORDS) == 1:
        keyword_sequence = ("*" if arguments.prefix_glob else "") + keyword_sequence + arguments.postfix_glob

query = parser.parse(keyword_sequence)
results = searcher.search(query, limit=int(arguments.max_count or 10), sortedby=arguments.sort_by)
print(results)
for result in results:
    print(result)
