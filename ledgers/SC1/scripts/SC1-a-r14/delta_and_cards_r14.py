"""Round-14 SC1-a: (1) delta of slice-a files between the round-13 pin and this pin, (2) L01-L03 card changes,
(3) byte-identity of the lab sections and twins that rows carry from round 13."""
import json
import re
import subprocess
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE14-SC1-a"
PREV = "e919577b45b431ce68e1e6533b00b8a301277937"
CUR = "8e5751c903f0246115eba746afdf5d71f612bb37"
files = [
    "course/modules/SC/SC1/index.html",
    "course/modules/SC/SC1/L01.html",
    "course/modules/SC/SC1/L02.html",
    "course/modules/SC/SC1/L03.html",
    "course/modules/SC/SC1/cards.json",
    "tests/labs/SC1/lab-SC1-L01-1.py",
    "tests/labs/SC1/lab-SC1-L02-1.py",
    "tests/labs/SC1/lab-SC1-L03-1.py",
    "course/modules/SC/SC1/project.html",
    "course/modules/SC/SC1/L06.html",
]
stat = subprocess.run(["git", "-C", ROOT, "diff", "--stat", PREV, CUR, "--"] + files, capture_output=True, text=True).stdout
print("== diffstat (slice-a files and cross-slice files cited by hub rows)")
print(stat)
diff = subprocess.run(["git", "-C", ROOT, "diff", PREV, CUR, "--"] + files, capture_output=True, text=True).stdout
open(ROOT + "/ledgers/SC1/scripts/SC1-a-r14/delta_slice_a_r14.diff", "w", encoding="utf-8").write(diff)
print("== hunks in slice-a pages (line numbers in new file)")
cur_file = None
for line in diff.splitlines():
    if line.startswith("+++ "):
        cur_file = line[6:]
    if line.startswith("@@"):
        print(cur_file, line[:60])

print("== lab sections and twins byte-identical between pins?")
def show(path, rev):
    return subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{path}"], capture_output=True, text=True).stdout
for page, (a, b) in {"L01": (134, 209), "L02": (168, 279)}.items():
    p = f"course/modules/SC/SC1/{page}.html"
    old = show(p, PREV).splitlines()[a - 1 : b]
    new = open(ROOT + "/" + p, encoding="utf-8").read().splitlines()[a - 1 : b]
    print(page, "lab section lines", a, b, "identical:", old == new)
for lab in ["L01", "L02", "L03"]:
    p = f"tests/labs/SC1/lab-SC1-{lab}-1.py"
    print(lab, "twin identical:", show(p, PREV) == open(ROOT + "/" + p, encoding="utf-8").read())
p = "course/modules/SC/SC1/L03.html"
print("L03.html identical:", show(p, PREV) == open(ROOT + "/" + p, encoding="utf-8").read())

print("== cards")
prev = json.loads(show("course/modules/SC/SC1/cards.json", PREV))
cur = json.load(open(ROOT + "/course/modules/SC/SC1/cards.json", encoding="utf-8"))
pb = {c["id"]: c for c in prev}
cb = {c["id"]: c for c in cur}
print("total prev", len(prev), "cur", len(cur))
print("L01-L03 prev", sum(c["lesson"] in ("L01", "L02", "L03") for c in prev), "cur", sum(c["lesson"] in ("L01", "L02", "L03") for c in cur))
print("added", sorted(set(cb) - set(pb)), "removed", sorted(set(pb) - set(cb)))
changed = sorted(i for i in set(pb) & set(cb) if pb[i] != cb[i])
print("changed", len(changed), changed)
print("changed L01-L03:", [i for i in changed if cb[i]["lesson"] in ("L01", "L02", "L03")])
fronts = {}
for c in cur:
    fronts.setdefault(re.sub(r"\W+", " ", c["front"].lower()).strip(), []).append(c["id"])
print("duplicate fronts:", [v for v in fronts.values() if len(v) > 1])
print("duplicate ids:", len(cur) - len(cb))
