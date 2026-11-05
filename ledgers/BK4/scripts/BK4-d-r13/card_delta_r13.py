# Compare cards.json at the previous pin (5db69a9) with the working tree; list added, removed and changed card ids.
import json
import subprocess
import sys

PREV = "5db69a9bee460736c318ebfacc7200ee5a6eb0f0"
old = json.loads(subprocess.check_output(["git", "show", f"{PREV}:course/modules/BK/BK4/cards.json"]).decode("utf-8"))
new = json.load(open(sys.argv[1], encoding="utf-8"))
o = {c["id"]: c for c in old}
n = {c["id"]: c for c in new}
print("old", len(o), "new", len(n))
print("added:", sorted(set(n) - set(o)))
print("removed:", sorted(set(o) - set(n)))
print("changed:", sorted(k for k in set(o) & set(n) if o[k] != n[k]))
print("unchanged count:", sum(1 for k in set(o) & set(n) if o[k] == n[k]))
