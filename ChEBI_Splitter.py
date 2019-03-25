__doc__ = f"""
Usage:
    {__file__} [options]

Options:
    --input_file CHEBIJSON  Input JSON object. (compressed or not) [default: ChEBI_complete.json]
    --split_count COUNT     Number of lines per output file. [default: 5000]
    --output_dir DIR        Output directory to place JSON line files in. [default: chebi_split]
"""
import gzip
import sys
import mmap
import json
import os.path
from docopt import magic
import glob

magic()
os.makedirs(arguments.output_dir, mode=0o755, exist_ok=True)

if not os.path.exists(arguments.input_file):
    arguments["input_file"] = glob.glob("ChEBI_complete.json*")[0]

print(f"splitting: {arguments.input_file}")
with open(arguments.input_file, "rb") as f:
    mapped = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
    if arguments.input_file.endswith('.gz'):
        input_file = gzip.GzipFile(mode="r", fileobj=mapped)
    else:
        input_file = mapped
    i = 0
    f = None
    split_count = int(arguments.split_count or 5000)
    split_index = 0
    break_count = 0
    while True:
        line = input_file.readline()
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
