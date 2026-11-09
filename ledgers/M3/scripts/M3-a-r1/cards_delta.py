"""Compare M3 cards.json at the base pin and at HEAD; list changed cards by lesson."""
import json
import subprocess
import sys

REPO = "/Users/billyribeiro/.fanout/wt/verifyF21-M3-a"
PATH = "course/modules/M/M3/cards.json"


def load(rev):
    raw = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{PATH}"], capture_output=True, text=True, check=True).stdout
    return json.loads(raw)


old = load("9294b914")
new = load("HEAD")
print("old cards", len(old), "new cards", len(new))
oid = {c["id"]: c for c in old}
nid = {c["id"]: c for c in new}
print("removed:", sorted(set(oid) - set(nid)))
print("added:", sorted(set(nid) - set(oid)))
changed = [i for i in oid if i in nid and oid[i] != nid[i]]
print("changed:", changed)
for i in sorted(set(nid) - set(oid)):
    print("ADDED", i, nid[i]["lesson"], nid[i].get("grade"))
for i in sorted(set(oid) - set(nid)):
    print("REMOVED", i, oid[i]["lesson"], oid[i].get("grade"))
for i in changed:
    print("CHANGED", i, "lesson", nid[i]["lesson"], "grade", oid[i].get("grade"), "->", nid[i].get("grade"))
print("L01-L03 cards at HEAD:", sum(1 for c in new if c["lesson"] in ("L01", "L02", "L03")))
print("L01-L03 cards at base:", sum(1 for c in old if c["lesson"] in ("L01", "L02", "L03")))
print("order preserved (ids at HEAD in old order minus new):", [c["id"] for c in new if c["id"] in oid] == [c["id"] for c in old if c["id"] in nid])
