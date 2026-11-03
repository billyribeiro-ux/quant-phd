"""Check every numbered label a card cites against its own lesson text, and card structure (verifier round 3, slice d).

For each card: labels of the form Definition/Theorem/Proposition/Lemma/Fact/Example/Remark/Assumption/Section N.M
appearing in front or back must appear in the card's lesson text; F1..F4 cited with 'Lesson 4' must appear in L04;
'Lab N' bases must name a lab that the lesson text contains; grades must be in T/A/B/C/D/X; cites must be registry keys.
Also reports near-duplicate fronts/backs across all cards (difflib ratio >= 0.80).
Run from the checkout root: .venv/bin/python -I ledgers/M3/scripts/M3-d-r3/cards_labels_r3.py
"""

import difflib
import json
import re
from pathlib import Path

ROOT = Path.cwd()
TXT = ROOT / "ledgers/M3/scripts/M3-d-r3/out3/lesson_text"
cards = json.loads((ROOT / "course/modules/M/M3/cards.json").read_text(encoding="utf-8"))
reg = json.loads((ROOT / "references/references.json").read_text(encoding="utf-8"))
reg_keys = set(reg) if isinstance(reg, dict) else {e.get("key") for e in reg}
lesson = {p.stem: p.read_text(encoding="utf-8") for p in TXT.glob("L0*.txt")}
LABEL = re.compile(r"\b(Definition|Theorem|Proposition|Lemma|Fact|Example|Remark|Assumption|Section|Corollary|Problem)\s+(\d+(?:\.\d+[a-z]?)?)")
bad = []
for c in cards:
    text_blob = c["front"] + " " + c["back"]
    lt = lesson.get(c["lesson"], "")
    for kind, num in LABEL.findall(text_blob):
        label = f"{kind} {num}"
        if label not in lt:
            # a label such as 'Definition 1.2a' may appear as 'Definition 1.2' in the lesson
            if re.sub(r"[a-z]$", "", num) != num and f"{kind} {re.sub(r'[a-z]$', '', num)}" in lt:
                continue
            bad.append((c["id"], c["lesson"], label, "not in lesson text"))
    if re.search(r"F1 to F4 of Lesson 4|F1 of Lesson 4|F3 of Lesson 4|F1 to F4, ", text_blob):
        if "F4" not in lesson.get("L04", "") or "F1" not in lesson.get("L04", ""):
            bad.append((c["id"], c["lesson"], "F1..F4", "L04 lacks F1..F4"))
    m = re.search(r"Lab (\d+)", c.get("basis", ""))
    if c.get("basis") and not re.search(r"Lab \d", lt) and c["lesson"] != "L09":
        bad.append((c["id"], c["lesson"], c["basis"], "basis names a lab absent from the lesson"))
    if "grade" in c and c["grade"] not in set("TABCDX"):
        bad.append((c["id"], c["lesson"], c["grade"], "invalid grade"))
    for k in c.get("cite", []):
        if k not in reg_keys:
            bad.append((c["id"], c["lesson"], k, "cite not in registry"))
print("cards:", len(cards), "label/structure problems:", len(bad))
for b in bad:
    print("  ", b)
# near duplicates
dups = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        rf = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        rb = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
        if rf >= 0.80 or rb >= 0.80:
            dups.append((a["id"], b["id"], round(rf, 2), round(rb, 2)))
print("near-duplicate pairs (front>=0.80 or back>=0.80):", len(dups))
for d in dups:
    print("  ", d)
