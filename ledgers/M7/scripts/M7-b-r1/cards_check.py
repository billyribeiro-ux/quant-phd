"""Verifier script (M7-b round 1): card cross-checks for L04-L06.

(a) every numeric token in a card's back that is a fraction or decimal appears in its lesson page text or in the lab output;
(b) every 'Proposition/Theorem/Lemma/Definition/Remark/Example/Problem/Lemma' label cited in a card exists on its lesson page;
(c) duplicate fronts / near-duplicate backs across the whole unit.
"""
import html
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(sys.argv[1])
cards = json.loads((ROOT / "course/modules/M/M7/cards.json").read_text(encoding="utf-8"))
pages = {}
for lab in ["L04", "L05", "L06"]:
    raw = (ROOT / f"course/modules/M/M7/{lab}.html").read_text(encoding="utf-8")
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    text = re.sub(r"\s+", " ", text)
    pages[lab] = text
# lab outputs (expected blocks) as text
outs = {}
for lab in ["L04", "L05", "L06"]:
    raw = (ROOT / f"course/modules/M/M7/{lab}.html").read_text(encoding="utf-8")
    outs[lab] = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', raw, re.S).group(1))
problems = []
for c in cards:
    lesson = c["lesson"]
    if lesson not in pages:
        continue
    back = c["back"] + " " + c["front"]
    for tok in re.findall(r"-?\d+/\d+|-?\d+\.\d+", back):
        t = tok.replace("−", "-")
        forms = {t, t.lstrip("-"), "−" + t.lstrip("-")}
        present = any(f in pages[lesson] or f in outs[lesson] for f in forms)
        if not present:
            problems.append((c["id"], "number not on page or output", tok))
    for kind, num in re.findall(r"(Proposition|Theorem|Lemma|Definition|Remark|Example|Problem) (\d\.\d|[A-Z]\d)", back):
        label = f"{kind} {num}"
        if label not in pages[lesson] and not any(label in pages[x] for x in pages):
            problems.append((c["id"], "label not on any slice page", label))
        elif label not in pages[lesson]:
            problems.append((c["id"], "label is on another lesson page (check it is cited as such)", label))
print("card checks: cards in slice", sum(1 for c in cards if c["lesson"] in pages))
for p in problems:
    print(p)
print("problem count", len(problems))
# duplicate scan across whole unit
allc = cards
dups = []
for i in range(len(allc)):
    for j in range(i + 1, len(allc)):
        a, b = allc[i], allc[j]
        r = SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
        if r > 0.85:
            dups.append((a["id"], b["id"], round(r, 2), a["front"][:80], b["front"][:80]))
print("near-duplicate fronts (ratio>0.85), unit-wide:", len(dups))
for d in dups:
    print(d)
