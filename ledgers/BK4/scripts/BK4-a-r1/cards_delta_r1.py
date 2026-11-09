"""Card delta check for BK4 slice a, round 1 (run with python -I).

Compares cards.json at the base pin e919577b with the working copy (pin 95f3f8cb),
lists added, removed and changed cards by id, checks duplicates, and checks that every
label and every number a changed or added card states appears in its lesson text.
"""
import html
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(sys.argv[1])
BASE = "e919577b45b431ce68e1e6533b00b8a301277937"
BK4 = ROOT / "course/modules/BK/BK4"

old = json.loads(subprocess.run(["git", "-C", str(ROOT), "show", f"{BASE}:course/modules/BK/BK4/cards.json"],
                                capture_output=True, text=True, check=True).stdout)
new = json.loads((BK4 / "cards.json").read_text(encoding="utf-8"))
oi = {c["id"]: c for c in old}
ni = {c["id"]: c for c in new}
print("cards old", len(old), "new", len(new))
print("removed", sorted(set(oi) - set(ni)))
print("added", sorted(set(ni) - set(oi)))
changed = sorted(k for k in oi if k in ni and oi[k] != ni[k])
print("changed", changed)
print("dup id new", [k for k, v in Counter(c["id"] for c in new).items() if v > 1])
print("dup front new", [k for k, v in Counter(c["front"] for c in new).items() if v > 1])
print("dup back new", [k for k, v in Counter(c["back"] for c in new).items() if v > 1])
print("per lesson new", dict(Counter(c["lesson"] for c in new)))

lesson_text = {}
for lesson in ["L01", "L02", "L03", "L04", "L05"]:
    raw = (BK4 / f"{lesson}.html").read_text(encoding="utf-8")
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    lesson_text[lesson] = re.sub(r"\s+", " ", txt)

label_re = re.compile(r"\b(Proposition|Definition|Example|Remark|Problem|Corollary|Assumption|Section|Lab 1|Part [A-D]|Lemma)\s?([0-9A-Z][0-9.A-Za-z]*)")
num_re = re.compile(r"\b\d+(?:/\d+)?\b")
for cid in changed + sorted(set(ni) - set(oi)):
    c = ni[cid]
    text = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    body = lesson_text[c["lesson"]]
    print(f"\n== {cid} lesson {c['lesson']} grade {c.get('grade')}")
    for m in sorted(set(label_re.findall(text))):
        lab = " ".join(x for x in m if x).strip()
        lab_clean = lab.rstrip(".")
        found = lab_clean in body
        print(f"  label {lab_clean!r}: {'found' if found else 'NOT FOUND'} in {c['lesson']}")
    for n in sorted(set(num_re.findall(c["back"]))):
        print(f"  back number {n}: {'found' if n in body else 'not in lesson text (check manually)'}")
