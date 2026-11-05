"""E3 slice f round 11: which labelled blocks of L01-L04 have a card. Run from the checkout root with python3 -I."""
import json
import re
from pathlib import Path

UNIT = Path("course/modules/E/E3")
cards = json.loads((UNIT / "cards.json").read_text(encoding="utf-8"))
for i in range(1, 5):
    lesson = f"L0{i}"
    text = (UNIT / f"{lesson}.html").read_text(encoding="utf-8")
    labels = set(re.findall(r'class="block-title[^"]*">((?:Definition|Proposition|Theorem|Lemma|Remark|Example|Assumptions?)\s+[A-Z]?\d+(?:\.\d+)?|Assumptions? [A-Z]\d)', text))
    cards_here = [c for c in cards if c["lesson"] == lesson]
    blob = " ".join(c["front"] + " " + c["back"] for c in cards_here)
    uncarded = []
    for lab in sorted(labels):
        kind_num = re.sub(r"^Assumptions?\s+", "Assumption ", lab)
        m = re.search(r"([A-Z]?\d+(?:\.\d+)?)$", kind_num)
        num = m.group(1) if m else ""
        kind = kind_num.split()[0].rstrip("s")
        hit = bool(re.search(r"(?<![\d.])" + re.escape(num) + r"(?![\d])", blob)) and (kind.lower() in blob.lower() or kind.startswith("Assumption") and "assumption" in blob.lower())
        if not hit:
            uncarded.append(lab)
    print(lesson, "labelled blocks", len(labels), "slice cards", len(cards_here), "blocks with no card mention:", uncarded)
