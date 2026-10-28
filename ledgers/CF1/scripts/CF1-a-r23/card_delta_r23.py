"""Compare cards.json of the CF1 hub deck at the previous pin (7143726) and at 503d139; list in-slice (L01, L02) changes."""
import json
import subprocess
import sys

root = sys.argv[1]
def at(rev):
    text = subprocess.run(["git", "-C", root, "show", f"{rev}:course/modules/CF/CF1/cards.json"], capture_output=True, text=True, check=True).stdout
    return {c["id"]: c for c in json.loads(text)}
old = at("7143726")
new = {c["id"]: c for c in json.load(open(f"{root}/course/modules/CF/CF1/cards.json", encoding="utf-8"))}
print("cards old/new:", len(old), len(new))
print("added:", sorted(set(new) - set(old)), "removed:", sorted(set(old) - set(new)))
for k in sorted(set(old) & set(new)):
    if old[k] != new[k] and "L01" in (old[k]["lesson"], new[k]["lesson"]) or old.get(k, {}).get("lesson") == "L02" and old[k] != new[k]:
        print("in-slice changed:", k, old[k]["lesson"], "grade", old[k]["grade"], "->", new[k]["grade"])
