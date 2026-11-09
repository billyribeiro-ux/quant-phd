"""Card-level delta between e919577b and 95f3f8cb (JSON objects compared by id)."""
import json
import sys

old = {c["id"]: c for c in json.load(open(sys.argv[1], encoding="utf-8"))}
new = {c["id"]: c for c in json.load(open(sys.argv[2], encoding="utf-8"))}
print("old", len(old), "new", len(new))
print("added", [k for k in new if k not in old])
print("removed", [k for k in old if k not in new])
changed = [k for k in new if k in old and new[k] != old[k]]
print("changed", len(changed), changed)
unchanged = [k for k in new if k in old and new[k] == old[k]]
print("unchanged", len(unchanged))
