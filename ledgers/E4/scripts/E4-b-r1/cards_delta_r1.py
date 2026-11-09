import json
import re
import sys
from collections import Counter

ROOT = sys.argv[1]
old = json.load(open(sys.argv[2], encoding="utf-8"))
new = json.load(open(sys.argv[3], encoding="utf-8"))
ids = [c["id"] for c in new]
print("total cards", len(new), "unique ids", len(set(ids)), "ok" if len(set(ids)) == len(ids) else "DUP-IDS")
om = {c["id"]: c for c in old}
nm = {c["id"]: c for c in new}
slice_les = {"L04", "L05", "L06"}
print("slice-b cards (L04-L06):", sum(1 for c in new if c["lesson"] in slice_les))
changed_b = [i for i in om if i in nm and om[i] != nm[i] and nm[i]["lesson"] in slice_les]
print("changed slice-b cards:", changed_b)
print("removed:", sorted(set(om) - set(nm)), "added:", sorted(set(nm) - set(om)))
# duplicates of front text within the whole file and of back text
fronts = Counter(c["front"].strip().lower() for c in new)
print("duplicate fronts:", [f for f, n in fronts.items() if n > 1])
backs = Counter(c["back"].strip().lower() for c in new)
print("duplicate backs:", [f[:60] for f, n in backs.items() if n > 1])
process = re.compile(r"\b(round|fixer|verifier|builder|ruling|pending|TODO|FIXME|draft|revised|the fix|we changed|patched)\b", re.I)
scope = re.compile(r"\b(only|all|always|every|any|same|drives|exactly)\b", re.I)
for i in changed_b + sorted(set(nm) - set(om)):
    c = nm[i]
    txt = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    pw = process.findall(txt)
    sw = scope.findall(txt)
    print(i, "process:", pw, "scope:", sw)
