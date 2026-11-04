"""Write every PC3 card as text (id, lesson, grade, basis, front, back), in file order. usage: python -I dump_cards_r4.py <checkout-root> <out-file>"""
import json
import sys
from pathlib import Path

cards = json.loads((Path(sys.argv[1]) / "course/modules/PC/PC3/cards.json").read_text(encoding="utf-8"))
with open(sys.argv[2], "w", encoding="utf-8") as fh:
    for c in cards:
        fh.write(f"{c['id']} [{c['lesson']}] grade={c.get('grade')} basis={c.get('basis')!r} cite={c.get('cite')}\n")
        fh.write(f"  F: {c['front']}\n  B: {c['back']}\n")
print(len(cards))
