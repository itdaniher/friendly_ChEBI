"""
Usage:
    search.py --field_help
    search.py [options] (KEYWORDS...)

Options:
    --search FIELD      Column to search. [default: names]
    --max_count COUNT   Maximum number of results to return. [default: 10]
    --sort_by FIELD     Sort results by this field name. [default: mass]
    --postfix_glob G    Use provided keyword as start of query. Appends G. [default: *]
    --prefix_glob G     Preface keyword with G for glob searching.
    --no_glob           Disables globbing.
    --index PATH        Specify path to the index made by ChEBI_Indexer.py. [default: index]
    --field_help        Returns available fieldnames for searching and sorting.
"""
from docopt import docopt as magic_docopt

import sys
import os

from whoosh.fields import TEXT
from whoosh.qparser import QueryParser, FuzzyTermPlugin

magic_docopt()

from whoosh.index import open_dir
if not os.path.isdir(arguments.index):
    raise FileNotFoundError("can't find the ChEBI index")

ix = open_dir(arguments.index)

INDEXED_FIELDS = [field_name for field_name in ix.schema.names() if ix.schema[field_name].indexed]
TEXT_FIELDS = [field_name for field_name in ix.schema.names() if isinstance(ix.schema[field_name], TEXT)]

if arguments.field_help:
    print(f"Sortable fields: {', '.join(INDEXED_FIELDS)}")
    print(f"Searchable fields: {', '.join(TEXT_FIELDS)}")
    quit()

if arguments.sort_by not in INDEXED_FIELDS:
    raise ValueError(f"Invalid sort field: {arguments.sort_by} not found.")

if arguments.search not in TEXT_FIELDS:
    raise ValueError(f"Invalid search field: {arguments.search} not found.")

searcher = ix.searcher()
parser = QueryParser(arguments.search, ix.schema)
keyword_sequence = " ".join(arguments.KEYWORDS)

# no special commands
if keyword_sequence.islower() and all([keyword.isalpha() for keyword in keyword_sequence]):
    if not arguments.no_glob and len(arguments.KEYWORDS) == 1:
        keyword_sequence = ("*" if arguments.prefix_glob else "") + keyword_sequence + arguments.postfix_glob

query = parser.parse(keyword_sequence)
results = searcher.search(query, limit=int(arguments.max_count), sortedby=arguments.sort_by)
print(results)
for result in results:
    print(result)
