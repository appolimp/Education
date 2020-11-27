import os
import tempfile
import json
import argparse


def key_val(key, val):
    if val:
        dat[key] = dat.setdefault(key, []) + [val]
        with open(storage_path, 'w') as file:
            json.dump(dat, file, skipkeys=True, indent=4, sort_keys=True)
    else:
        ans = dat.get(key)
        print(', '.join(ans) if ans else None)


storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
try:
    with open(storage_path) as f:
        dat = json.load(f)
except FileNotFoundError:
    dat = {}


parser = argparse.ArgumentParser()
parser.add_argument("--key", help="give me a name")
parser.add_argument("--val", help="give me a val")
args = parser.parse_args()

key_val(args.key, args.val)
# print(dat)
