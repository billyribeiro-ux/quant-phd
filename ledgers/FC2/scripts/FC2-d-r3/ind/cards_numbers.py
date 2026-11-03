"""For every card: each multi-digit number (2+ digits, or a fraction a/b) on the card must appear in its lesson text
(stripped HTML, all lesson pages), and every named label (Lab 1, Part B; Problem X; Theorem n.m; Example n.m;
Proposition n.m; Remark n.m; Assumption An) in the card's back must occur in the lesson text."""
import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/FC/FC2/cards.json").read_text(encoding="utf-8"))
texts = {}
for n in range(1, 9):
    s = (root / f"course/modules/FC/FC2/L0{n}.html").read_text(encoding="utf-8")
    s = re.sub(r"<[^>]+>", " ", s)
    texts[f"L0{n}"] = html.unescape(s)
miss = []
labels = []
for c in cards:
    t = texts[c["lesson"]]
    for field in ("front", "back"):
        for num in re.findall(r"(?<![\w.])\d{2,}(?:[.,]\d+)?|\d+/\d+", c[field]):
            if num not in t:
                miss.append((c["id"], field, num))
    for lab in re.findall(r"(?:Theorem|Example|Proposition|Remark|Definition|Lemma|Corollary|Problem|Lab \d, Part|Section|Assumption) [A-Z]?\d(?:\.\d+)?", c["back"]):
        labels.append((c["id"], lab, lab in t))
print("cards:", len(cards), "number misses:", len(miss))
for m in miss[:40]:
    print("  NUM-MISS", m)
bad = [x for x in labels if not x[2]]
print("label references:", len(labels), "not literally in lesson:", len(bad))
for b in bad[:40]:
    print("  LABEL?", b)
