"""Card-by-card diff of course/modules/CF/CF1/cards.json between two git revisions (stdlib + git)."""
import json
import subprocess
import sys

ROOT, OLD, NEW = sys.argv[1], sys.argv[2], sys.argv[3]


def load(rev):
    return {c["id"]: c for c in json.loads(subprocess.check_output(["git", "show", f"{rev}:course/modules/CF/CF1/cards.json"], cwd=ROOT))}


a, b = load(OLD), load(NEW)
print("ids equal:", set(a) == set(b), "count", len(b))
for cid in sorted(b):
    keys = sorted(k for k in set(a[cid]) | set(b[cid]) if a[cid].get(k) != b[cid].get(k))
    if keys:
        print(cid, b[cid]["lesson"], keys)
