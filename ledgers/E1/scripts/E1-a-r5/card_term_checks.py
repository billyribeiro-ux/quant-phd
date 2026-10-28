"""Card and term checks for E1 slice a (hub index.html, L01-L03): duplicates, grades, and term scans."""
import collections
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
unit = root / "course/modules/E/E1"
cards = json.loads((unit / "cards.json").read_text(encoding="utf-8"))
print("cards total", len(cards), "dup ids", len(cards) - len({c["id"] for c in cards}))
print("dup fronts", [k for k, v in collections.Counter(c["front"].lower() for c in cards).items() if v > 1])
print("dup backs", [k for k, v in collections.Counter(c["back"].lower() for c in cards).items() if v > 1])
slice_cards = [c for c in cards if c["lesson"] in ("L01", "L02", "L03")]
print("slice cards", len(slice_cards), "grades", dict(collections.Counter(c.get("grade") for c in slice_cards)))
for c in slice_cards:
    if "level curve" in c["back"] or "indifference" in c["back"]:
        print("term in card", c["id"], "->", c["back"][:120])
terms = ["level curve", "indifference", "Lagrang", "Nash", "convex", "KKT", "expected utility", "first welfare", "Pareto", "Cournot", "Bertrand"]
for name in ("index.html", "L01.html", "L02.html", "L03.html"):
    text = (unit / name).read_text(encoding="utf-8")
    counts = {t: len(re.findall(re.escape(t), text, flags=re.I)) for t in terms}
    print(name, {k: v for k, v in counts.items() if v})
