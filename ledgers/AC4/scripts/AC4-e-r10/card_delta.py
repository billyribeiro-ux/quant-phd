"""Compare AC4 cards.json at the previous pin (argv[1]) with the current one (argv[2])."""
import json
import sys

old = {c["id"]: c for c in json.load(open(sys.argv[1], encoding="utf-8"))}
new_list = json.load(open(sys.argv[2], encoding="utf-8"))
new = {c["id"]: c for c in new_list}
print("old", len(old), "new", len(new_list), "unique new", len(new))
print("removed", sorted(set(old) - set(new)))
print("added", sorted(set(new) - set(old)))
for cid in sorted(set(old) & set(new)):
    if old[cid] != new[cid]:
        print("CHANGED", cid, new[cid]["lesson"])
        print("  front:", new[cid]["front"])
        print("  back :", new[cid]["back"])
        print("  grade:", new[cid].get("grade"), "basis:", new[cid].get("basis"))
for cid in sorted(set(new) - set(old)):
    c = new[cid]
    print("ADDED", cid, c["lesson"], c.get("grade"), "|", c["front"], "|", c["back"], "|", c.get("basis"))
