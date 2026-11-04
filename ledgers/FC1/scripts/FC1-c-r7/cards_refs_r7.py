"""Round-7 check: every numbered reference in a card (Proposition, Remark, Example, Assumption, Definition, Corollary,
Problem, Section) appears in that card's own lesson text (lessons stripped by strip_html_r7.py). Stdlib only.
Usage: python3 -I cards_refs_r7.py <cards.json> <dir with L01.txt..L05.txt>"""
import json
import pathlib
import re
import sys

cards = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
lessons = {p.stem: p.read_text(encoding="utf-8") for p in pathlib.Path(sys.argv[2]).glob("L0*.txt")}
pattern = re.compile(r"\b(Proposition|Remark|Example|Assumption|Definition|Corollary|Problem|Section|Lemma)\s+([A-Z]?\d+(?:\.\d+)?)")
refs = 0
missing = []
for card in cards:
    text = card["front"] + " " + card["back"]
    body = lessons[card["lesson"]]
    for kind, num in pattern.findall(text):
        refs += 1
        head = f"{kind} {num}"
        if head not in body:
            missing.append((card["id"], card["lesson"], head))
print("cards", len(cards), "numbered references", refs, "absent from the card's own lesson", len(missing))
for item in missing:
    print("ABSENT", item)
