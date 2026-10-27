"""Banned-string scan (BUILDER_RULES 1.3-1.4) over the visible text of S7 L01 and L02, and the card inventory."""
import json
import re
import sys
from pathlib import Path

TXT = Path(sys.argv[1])
CHK = Path(sys.argv[2])
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "roughly", "about ", "historically", "...", "…", "?"]
total = {}
for name in ("L01", "L02"):
    text = (TXT / f"{name}.txt").read_text(encoding="utf-8")
    for b in BANNED:
        n = text.count(b)
        if n:
            total[(name, b)] = n
    print(name, "chars", len(text), "lines", text.count("\n"))
for k, v in sorted(total.items()):
    print("HIT", k[0], repr(k[1]), v)
cards = json.loads((CHK / "course/modules/S/S7/cards.json").read_text(encoding="utf-8"))
cards = cards["cards"] if isinstance(cards, dict) and "cards" in cards else cards
l12 = [c for c in cards if c.get("lesson") in ("L01", "L02")]
ids = [c["id"] for c in cards]
print("cards total", len(cards), "unique ids", len(set(ids)), "L01+L02 cards", len(l12))
print("duplicate ids:", sorted({i for i in ids if ids.count(i) > 1}))
