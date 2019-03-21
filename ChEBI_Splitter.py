import sys
import mmap
import json
if __name__ == "__main__":
    with open(sys.argv[1], 'r+') as f:
        data = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
        i = 0
        f = None
        split_count = 5000
        split_index = 0
        break_count = 0
        while True:
            line = data.readline()
            if line.strip():
                chebi_id, json_text = line.decode('utf-8').strip().split(' ', maxsplit=1)
                if int(chebi_id) > split_index:
                    f = open('chebi_split/chebi-%d+%d.json' % (split_index, split_count), 'w')
                    split_index += split_count
                #chebi_id = int(chebi_id)
                #res = json.loads(line.split(' ', maxsplit=1)[-1].decode('utf-8'))
                #chebi_id = int(res['ChEBI ID'].split(':')[-1])
                #f.write(str(chebi_id) + ' ' + line+'\n')
                f.write(json_text.strip()+'\n')
            else:
                break_count += 1
            if break_count > 20:
                break
