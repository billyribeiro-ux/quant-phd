"""Round 28: cards.json scan (duplicates, per-lesson counts, cite keys in the registry, grades). Usage: python -I cards_scan_r28B.py <checkout>"""
import json
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
c = json.loads((root / "course/modules/S/S7/cards.json").read_text(encoding="utf-8"))
cards = c["cards"] if isinstance(c, dict) and "cards" in c else c
reg = json.loads((root / "references/references.json").read_text(encoding="utf-8"))
keys = {e["key"] for e in (reg["entries"] if isinstance(reg, dict) and "entries" in reg else reg)}
ids = [x["id"] for x in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)))
print("duplicate fronts:", sum(v - 1 for v in Counter(x["front"] for x in cards).values() if v > 1),
      "duplicate backs:", sum(v - 1 for v in Counter(x.get("back", "") for x in cards).values() if v > 1))
per = Counter(x["lesson"] for x in cards)
print("per lesson:", dict(sorted(per.items())), "sum", sum(per.values()))
missing = sorted({k for x in cards for k in x.get("cite", []) if k not in keys})
print("cite keys missing from the registry:", missing)
print("grades:", dict(Counter(x.get("grade", "-") for x in cards)))
print("cards without grade:", sum(1 for x in cards if "grade" not in x))
