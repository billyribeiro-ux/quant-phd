"""Round-1 card-object delta: compare every card object by id between dde0486b and HEAD (read-only)."""
import json
import subprocess
import sys

root = sys.argv[1]

def load(rev):
    raw = subprocess.run(["git", "-C", root, "show", f"{rev}:course/modules/FC/FC1/cards.json"],
                         capture_output=True, text=True, check=True).stdout
    return {c["id"]: c for c in json.loads(raw)}

a, b = load("dde0486b"), load("HEAD")
changed = sorted(i for i in set(a) & set(b) if a[i] != b[i])
removed = sorted(set(a) - set(b))
added = sorted(set(b) - set(a))
print("changed:", [(i, a[i]["lesson"]) for i in changed])
print("removed:", [(i, a[i]["lesson"]) for i in removed])
print("added:", [(i, b[i]["lesson"]) for i in added])
print("slice (L01-L03) changed:", [i for i in changed if a[i]["lesson"] in ("L01", "L02", "L03")])
print("slice (L01-L03) removed:", [i for i in removed if a[i]["lesson"] in ("L01", "L02", "L03")])
print("slice (L01-L03) added:", [i for i in added if b[i]["lesson"] in ("L01", "L02", "L03")])
print("L01-L03 count dde0486b:", sum(1 for c in a.values() if c["lesson"] in ("L01", "L02", "L03")),
      "HEAD:", sum(1 for c in b.values() if c["lesson"] in ("L01", "L02", "L03")))
