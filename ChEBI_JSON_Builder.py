"""
Usage:
    {__file__} [options]

Options:
    --input F    Input SDF file from EBI. [default: ChEBI_complete.sdf.gz]
    --split_count COUNT     Number of lines per output file. [default: 5000]
    --output_dir DIR        Output directory to place JSON line files in. [default: chebi_split]
"""
import os
import mmap
import gzip
import json
import urllib
from docopt import magic

magic()


def typeChemical(d):
    for key, value in d.items():
        if len(value) == 1:
            if key == "ChEBI ID":
                d[key] = int(value[0].split(":")[-1])
            elif key in ["Charge", "Star"]:
                d[key] = int(value[0])
            elif key in ["Mass", "Monoisotopic Mass"]:
                d[key] = float(value[0])
            elif key in ["ChEBI Name", "Definition"]:
                d[key] = value[0]
    if len(d):
        return (d["ChEBI ID"], dict(sorted(d.items())))

entries = []
os.makedirs(arguments.output_dir, mode=0o755, exist_ok=True)

with open(arguments.input, "r") as f:
     mapped = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
     gzfile = gzip.GzipFile(mode="r", fileobj=mapped)
     done = False
     while True:
        segments = []
        line = b""
        while line.strip() != b"$$$$":
            line = gzfile.readline()
            if line == b"":
                done = True
                break
            segments.append(line)
        segment = b''.join(segments).decode()
        rebuilt = "\n> <Molfile>\n" + segment
        subsegments = [subseg for subseg in rebuilt.split("\n> <")]
        info = [subseg.split(">\n") for subseg in subsegments][1:-1]
        chem = {i[0]:([x for x in i[1].split('\n') if x] if i[0] != "Molfile" else i[1]) for i in info}
        entry = typeChemical(chem)
        if entry:
            entries.append(entry)
        if done:
            break

split_count = int(arguments.split_count or 5000)
split_index = 0
for entry in sorted(entries):
    chebi_id, json_text = entry[0], json.dumps(entry[1])
    if chebi_id > split_index:
        f = open(f"{arguments.output_dir}/chebi-{split_index}+{split_count}.json", "w")
        split_index += split_count
    f.write(json_text.strip() + "\n")
