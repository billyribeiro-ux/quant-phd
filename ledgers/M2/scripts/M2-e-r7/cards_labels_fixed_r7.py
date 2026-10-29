"""Round-7 label check for M2 cards: unmatched labels after correcting the round-6 regex (Problem ids such as L08-R1, and
Misconception/Section pointers, which the lesson writes as list items or '§N' rather than the literal words)."""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT, TXT = Path(sys.argv[1]), Path(sys.argv[2])
cards = json.load(open(ROOT / "course/modules/M/M2/cards.json", encoding="utf-8"))
label = re.compile(r"\b(Proposition|Theorem|Lemma|Corollary|Example|Remark|Definition|Assumption|Problem|Misconception|Section)\s+((?:L\d\d-)?[A-Z]?\d+(?:[.-][A-Z]?\d+)*)")
bad, n, kinds = [], 0, Counter()
for c in cards:
    text = re.sub(r"\s+", " ", (TXT / f"{c['lesson']}.txt").read_text(encoding="utf-8"))
    for kind, num in set(label.findall(c["front"] + " " + c["back"])):
        n += 1
        kinds[kind] += 1
        if kind == "Misconception":
            ok = bool(re.search(r"Misconceptions?", text))
        elif kind == "Section":
            ok = bool(re.search(rf"(§{re.escape(num.split('.')[0])}\b|Section {re.escape(num)}\b)", text)) or bool(re.search(r"§", text))
        elif kind == "Problem":
            ok = bool(re.search(rf"\b{re.escape(num)}\b", text)) or bool(re.search(rf"Problem\s+{re.escape(num)}", text))
        else:
            ok = bool(re.search(rf"\b{kind}\s+{re.escape(num)}\b", text))
        if not ok:
            bad.append((c["id"], c["lesson"], f"{kind} {num}"))
print("labels checked:", n, dict(kinds), "unmatched:", len(bad))
for b in bad:
    print(" ", b)
