"""Verifier round 6: slice-card delta between the round-5 pin (dde0486b) and the round-6 pin (e896b7a4).
Usage: python3 -I cards_delta_r6.py <cards_at_dde.json> <cards_at_e89.json>
Prints removed/added/changed ids, the slice (L05-L08) subset of each, and citation resolution in the slice lesson pages."""
import json
import re
import sys

old = {c["id"]: c for c in json.load(open(sys.argv[1], encoding="utf-8"))}
new = {c["id"]: c for c in json.load(open(sys.argv[2], encoding="utf-8"))}
SLICE = ("L05", "L06", "L07", "L08")
print("removed", sorted(set(old) - set(new)), "added", sorted(set(new) - set(old)))
changed = [i for i in old if i in new and old[i] != new[i]]
print("changed", changed)
print("slice ids", sum(1 for c in new.values() if c["lesson"] in SLICE))
print("slice changed", [i for i in changed if new[i]["lesson"] in SLICE])
print("slice removed", [i for i in set(old) - set(new) if old[i]["lesson"] in SLICE])
root = "course/modules/CS/CS2"
pages = {n: open(f"{root}/{n}.html", encoding="utf-8").read() for n in ("L05", "L06", "L07", "L08")}
pat = re.compile(r"\b(Definition|Proposition|Lemma|Theorem|Corollary|Remark|Example|Problem|Assumption)\s+([0-9]+\.[0-9]+|[A-Z][0-9]+)")
dangling = []
for c in new.values():
    if c["lesson"] not in SLICE:
        continue
    for kind, num in pat.findall(c["back"] + " " + c["front"]):
        if re.search(kind + r"\s+" + re.escape(num) + r"\b", pages[c["lesson"]]) is None:
            dangling.append((c["id"], kind, num))
print("dangling citations in slice cards", dangling)
