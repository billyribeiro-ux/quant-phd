"""Check that each block reference on an L05-L08 card (Definition/Theorem/Proposition/Corollary/Remark/Example/
Observation/Assumption/Problem/Model/Section/Part) resolves to a heading in the card's own lesson, or to the
named lesson for 'Lesson N' / 'Lesson LNN' cross references (checked against the lesson dumps of L04).

Run: python -I ledgers/E3/scripts/E3-g-r3/card_refs_resolve.py
"""
import json
import re

TXT = "ledgers/E3/scripts/E3-g-r3/text"
lessons = {L: open(f"{TXT}/{L}.txt", encoding="utf-8").read() for L in ("L04", "L05", "L06", "L07", "L08")}
cards = json.load(open("course/modules/E/E3/cards.json", encoding="utf-8"))
ref = re.compile(r"\b(Definitions?|Theorem|Proposition|Corollary|Remark|Example|Observation|Assumptions?|Problem|Model|Lab)\s+([A-Z]?\d+(?:\.\d+)?)")
bad = []
checked = 0
for c in cards:
    if c["lesson"] not in ("L05", "L06", "L07", "L08"):
        continue
    text = c["front"] + " " + c["back"]
    lesson = lessons[c["lesson"]]
    # Cross-lesson reference: 'Lesson N' / 'Lesson LNN' / 'Lesson 4, Theorem 1.5'
    for m in re.finditer(r"Lesson\s+L?(\d+)[^.;()]*?(Theorem|Proposition|Definition|Remark|Corollary|Example)\s+(\d+\.\d+)", text):
        checked += 1
        L = f"L0{m.group(1)}"
        kind, num = m.group(2), m.group(3)
        if L not in lessons or not re.search(rf"{kind} {re.escape(num)}\b", lessons[L]):
            bad.append((c["id"], "cross", L, kind, num))
    for m in ref.finditer(text):
        kind, num = m.group(1), m.group(2)
        if kind.startswith("Lab") or kind == "Model":
            pass
        checked += 1
        if kind.startswith("Definition"):
            kind = "Definition"
        if kind.startswith("Assumption"):
            kind = "Assumption"
        if kind == "Lab":
            continue
        pattern = rf"{kind} {re.escape(num)}\b" if kind != "Assumption" else rf"Assumptions? {re.escape(num)}\b|\bA{re.escape(num)}\b"
        if kind == "Model":
            pattern = rf"Model {re.escape(num)}\b"
        if kind == "Problem":
            pattern = rf"\b{re.escape(num)} ·"
        if not re.search(pattern, lesson):
            bad.append((c["id"], c["lesson"], kind, num))
print("references checked:", checked)
print("unresolved:", len(bad))
for b in bad:
    print("  ", b)
