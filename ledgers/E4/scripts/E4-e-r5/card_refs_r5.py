"""Every labelled item a card cites (Definition/Proposition/Lemma/Corollary/Remark/Example/Assumption/Fact/Problem/Lab part)
must appear in the text of the card's own lesson (rendered text in scratch/txt). Also: duplicate fronts/backs, empty fields."""
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

cards = json.load(open(sys.argv[1], encoding="utf-8"))
txt_dir = Path(sys.argv[2])
norm = lambda s: re.sub(r"\s+", " ", unicodedata.normalize("NFKC", s)).strip().lower()
lessons = {p.stem.upper(): norm(p.read_text(encoding="utf-8")) for p in txt_dir.glob("L0*.txt")}
label = re.compile(r"\b(Definition|Proposition|Lemma|Corollary|Remark|Example|Assumption|Fact|Problem|Problem Res|Problem M|Mech|Proof|Res|Emp|Lab|Part)\s+(?:[A-Z]{1,3}\s?)?(\d+(?:\.\d+)?)")
problems = []
seen_fronts, seen_backs = Counter(), Counter()
for c in cards:
    t = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    seen_fronts[norm(c["front"])] += 1; seen_backs[norm(c["back"])] += 1
    for k in ("front", "back"):
        if not c[k].strip():
            problems.append((c["id"], "empty " + k))
    if c.get("grade") in ("T", "C") and not c.get("basis"):
        problems.append((c["id"], "graded without basis"))
    for m in label.finditer(c["front"] + " " + c["back"]):
        word, num = m.group(1), m.group(2)
        if word in ("Lab", "Part"):
            continue
        needle = f"{word.lower()} {num.lower()}"
        if word in ("Assumption",):
            needle = f"assumption {m.group(0).split()[-1].lower()}" if False else None
        if needle and needle not in lessons[c["lesson"]]:
            problems.append((c["id"], f"{m.group(0)} not found in {c['lesson']} text"))
dups_f = [k for k, v in seen_fronts.items() if v > 1]
dups_b = [k for k, v in seen_backs.items() if v > 1]
print("cards", len(cards), "labelled-reference problems:", len(problems))
for p in problems:
    print("  ", p)
print("duplicate normalised fronts:", len(dups_f), "duplicate backs:", len(dups_b))
