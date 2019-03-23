__doc__ = f"""
Usage:
    {__file__} [JSON_LINE_GZ] [options]

Options:
    --split_count COUNT     Number of lines per output file. [default: 5000]
    --output_dir DIR        Output directory to place JSON line files in. [default: chebi_split]
"""
import gzip
import sys
import mmap
import json
import os.path
from docopt import docopt as magic_docopt

magic_docopt()
os.makedirs(arguments.output_dir, mode=0o755, exist_ok=True)
if not arguments.JSON_LINE_GZ:
    arguments["JSON_LINE_GZ"] = "ChEBI_complete.json.gz"
with open(arguments.JSON_LINE_GZ, "r+") as f:
    mapped = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
    gzfile = gzip.GzipFile(mode="r", fileobj=mapped)
    i = 0
    f = None
    split_count = int(arguments.split_count or 5000)
    split_index = 0
    break_count = 0
    while True:
        line = gzfile.readline()
        if line.strip():
            chebi_id, json_text = line.decode("utf-8").strip().split("\t")
            if int(chebi_id) > split_index:
                f = open(f"{arguments.output_dir}/chebi-{split_index}+{split_count}.json", "w")
                split_index += split_count
            f.write(json_text.strip() + "\n")
        else:
            break_count += 1
        if break_count > 20:
            break
