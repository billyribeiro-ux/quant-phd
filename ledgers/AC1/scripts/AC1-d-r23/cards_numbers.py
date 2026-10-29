# Checks every number in every card back and front appears in the card's own lesson (tag-stripped text).
# Usage: python -I cards_numbers.py <checkout>
import html, json, re, sys
from pathlib import Path
root = Path(sys.argv[1]) / "course/modules/AC/AC1"
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)), "duplicate fronts", len(cards) - len({c["front"] for c in cards}))
texts: dict[str, str] = {}
bad = 0
for c in cards:
    lesson = c["lesson"]
    if lesson not in texts:
        raw = (root / f"{lesson}.html").read_text(encoding="utf-8")
        texts[lesson] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    for field in ("front", "back"):
        for num in re.findall(r"\d{1,3}(?:,\d{3})+|\d+\.\d+", c[field]):
            if num not in texts[lesson]:
                bad += 1
                print("MISSING", c["id"], field, num)
print("number misses", bad)
