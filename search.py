import sys
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
import urllib.parse

ix = open_dir("chebi_index")

results = None
searcher = ix.searcher()
parser = QueryParser("name", ix.schema)
query = parser.parse(" ".join(sys.argv[1:]))
print(query)
results = searcher.search(query, limit=None)
print(results)

for result in sorted(results, key=lambda x: x['mass'])[0:10]:
    print(result)
