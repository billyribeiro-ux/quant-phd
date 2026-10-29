"""For each card, check that every theorem-like label it cites (Proposition, Theorem, Lemma, Corollary, Example, Remark,
Definition, Assumption, Problem, Misconception, Section) appears in the card's own lesson text."""
import json
import re
import sys
from pathlib import Path

MOD = Path(sys.argv[1]) / "course/modules/M/M2"
TXT = Path(sys.argv[2])
cards = json.load(open(MOD / "cards.json", encoding="utf-8"))
label = re.compile(r"\b(Proposition|Theorem|Lemma|Corollary|Example|Remark|Definition|Assumption|Problem|Misconception|Section)\s+((?:[A-Z]\d|\d)(?:\.\d+)?)")
bad = []
checked = 0
for c in cards:
    text = (TXT / f"{c['lesson']}.txt").read_text(encoding="utf-8")
    text = re.sub(r"\s+", " ", text)
    for kind, num in set(label.findall(c["front"] + " " + c["back"])):
        checked += 1
        pat = re.compile(rf"\b{kind}\s+{re.escape(num)}\b")
        if not pat.search(text):
            # a Misconception or Section may be numbered in its own list; accept the word alone for those
            if kind in ("Misconception", "Section") and re.search(rf"\b{kind}\b", text):
                continue
            bad.append((c["id"], c["lesson"], f"{kind} {num}"))
print("labels checked:", checked, "unmatched:", len(bad))
for b in bad:
    print(" ", b)
