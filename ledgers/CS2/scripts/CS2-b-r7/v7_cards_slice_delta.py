"""Round 7 (CS2 slice b): slice cards (lessons L05-L08) compared between the round-6 pin and this pin; duplicate scan."""
import json
import re
import subprocess
import sys

root = sys.argv[1]
old = json.loads(subprocess.run(["git", "-C", root, "show", "e896b7a4:course/modules/CS/CS2/cards.json"],
                                capture_output=True, text=True, check=True).stdout)
new = json.load(open(f"{root}/course/modules/CS/CS2/cards.json", encoding="utf-8"))
SLICE = {"L05", "L06", "L07", "L08"}
old_s = [c for c in old if c["lesson"] in SLICE]
new_s = [c for c in new if c["lesson"] in SLICE]
print(f"slice cards old {len(old_s)} new {len(new_s)}; byte-identical objects: {old_s == new_s}")
print(f"all cards old {len(old)} new {len(new)}; ids unique new: {len({c['id'] for c in new}) == len(new)}")
print("ids removed:", sorted({c['id'] for c in old} - {c['id'] for c in new}))
print("ids added:", sorted({c['id'] for c in new} - {c['id'] for c in old}))
changed = [c['id'] for c in old if c['id'] in {x['id'] for x in new} and c not in new]
print("changed ids:", changed)
# duplicate scan across all cards on normalised fronts and backs
def norm(s): return re.sub(r"\W+", " ", s.lower()).strip()
fronts = {}
for c in new:
    fronts.setdefault(norm(c["front"]), []).append(c["id"])
print("duplicate normalised fronts:", [v for v in fronts.values() if len(v) > 1])
backs = {}
for c in new:
    backs.setdefault(norm(c["back"]), []).append(c["id"])
print("duplicate normalised backs:", [v for v in backs.values() if len(v) > 1])
