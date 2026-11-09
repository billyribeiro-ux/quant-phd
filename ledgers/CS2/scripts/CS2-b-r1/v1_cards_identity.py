"""Round-1 delta check for CS2 slice b: which cards.json objects differ between the base pin and HEAD.

Run with: python -I this_file.py <checkout_dir>
Reads cards.json at both pins via git show (no working-tree reads for the base).
"""
import json
import subprocess
import sys

CHECKOUT = sys.argv[1]
BASE = "aa659725"
HEAD = "95f3f8cb"
PATH = "course/modules/CS/CS2/cards.json"


def git_show(rev: str) -> str:
    return subprocess.run(
        ["git", "-C", CHECKOUT, "show", f"{rev}:{PATH}"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


base_raw = git_show(BASE)
head_raw = git_show(HEAD)
base = json.loads(base_raw)
head = json.loads(head_raw)
print("base objects", len(base), "head objects", len(head))
bmap = {c["id"]: c for c in base}
hmap = {c["id"]: c for c in head}
print("ids only in base", sorted(set(bmap) - set(hmap)))
print("ids only in head", sorted(set(hmap) - set(bmap)))
changed = sorted(k for k in bmap if k in hmap and bmap[k] != hmap[k])
print("changed ids", changed)
print("changed lessons", sorted({bmap[k]["lesson"] for k in changed}))
slice_ids = sorted(k for k, c in bmap.items() if c.get("lesson") in {"L05", "L06", "L07", "L08"})
print("slice (L05-L08) card objects at base:", len(slice_ids))
print("slice card objects changed at HEAD:", [k for k in slice_ids if k in changed])
# byte identity of each slice object: compare the canonical serialization of each object
same = all(json.dumps(bmap[k], sort_keys=True) == json.dumps(hmap[k], sort_keys=True) for k in slice_ids)
print("slice card objects canonical-identical:", same)
print("slice cards by lesson at HEAD:", {l: sum(1 for k in slice_ids if hmap[k]["lesson"] == l) for l in ["L05", "L06", "L07", "L08"]})
# duplicate fronts across the whole deck at HEAD
fronts: dict[str, list[str]] = {}
for c in head:
    fronts.setdefault(c["front"].strip().lower(), []).append(c["id"])
dups = {f: ids for f, ids in fronts.items() if len(ids) > 1}
print("duplicate fronts across deck at HEAD:", len(dups), dups if dups else "")
ids_head = [c["id"] for c in head]
print("duplicate ids at HEAD:", len(ids_head) - len(set(ids_head)))
print("total objects at HEAD:", len(head), "slice objects:", len(slice_ids))
