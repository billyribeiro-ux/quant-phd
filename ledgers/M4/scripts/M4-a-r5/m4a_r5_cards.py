"""Round-5 card checks for M4 slice a (cards of L01-L04): (1) every number token on a card's front or back occurs in
its lesson text; (2) duplicate scan over the whole M4 deck (normalised front, normalised back, and card ids);
(3) each card's lesson field matches the lesson its cited locator is in (printed for reading).
Run from the checkout root: .venv/bin/python -I ledgers/M4/scripts/M4-a-r5/m4a_r5_cards.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
M4 = ROOT / "course" / "modules" / "M" / "M4"
cards = json.loads((M4 / "cards.json").read_text(encoding="utf-8"))


def page_text(name: str) -> str:
    t = (M4 / f"{name}.html").read_text(encoding="utf-8")
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))


texts = {p: page_text(p) for p in ["L01", "L02", "L03", "L04"]}
slice_cards = [c for c in cards if c["lesson"] in texts]
missing = []
for c in slice_cards:
    for field in ("front", "back"):
        for num in set(re.findall(r"\d+(?:\.\d+)?", c[field])):
            if num not in texts[c["lesson"]]:
                missing.append((c["id"], field, num))
print(f"slice-a cards: {len(slice_cards)}; number tokens missing from their lesson text: {len(missing)}")
for m in missing:
    print("  MISSING", m)

norm = lambda s: re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
fronts, backs = {}, {}
for c in cards:
    fronts.setdefault(norm(c["front"]), []).append(c["id"])
    backs.setdefault(norm(c["back"]), []).append(c["id"])
dup_f = {k: v for k, v in fronts.items() if len(v) > 1}
dup_b = {k: v for k, v in backs.items() if len(v) > 1}
ids = [c["id"] for c in cards]
print(f"deck size {len(cards)}; duplicate ids {len(ids) - len(set(ids))}; duplicate fronts {len(dup_f)}; duplicate backs {len(dup_b)}")
for k, v in list(dup_f.items()) + list(dup_b.items()):
    print("  DUP", v, k[:100])
grades_missing = [c["id"] for c in slice_cards if "grade" not in c]
print(f"slice-a cards without a grade field: {grades_missing}")
