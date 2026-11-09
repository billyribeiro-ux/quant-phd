"""Card checks for L08-L10 (verifier round 1): counts, ids, grade/basis rule, and card-number presence in lesson text.

Usage: python -I card_check.py <checkout-root>
"""
import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course/modules/M/M4"
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("total cards", len(cards), "unique ids", len(set(ids)), "unique fronts", len({c["front"].strip().lower() for c in cards}))
sl = [c for c in cards if c["lesson"] in ("L08", "L09", "L10")]
print("L08-L10 cards", len(sl), {l: sum(1 for c in sl if c["lesson"] == l) for l in ("L08", "L09", "L10")})
bad_basis = [c["id"] for c in sl if c["grade"] != "T" and not (c.get("basis") or c.get("cite"))]
print("non-T cards without basis or cite:", bad_basis)
pages = {l: html.unescape(re.sub(r"<[^>]+>", " ", (root / f"{l}.html").read_text(encoding="utf-8"))) for l in ("L08", "L09", "L10")}
numbers = {
    "M4-c141": ["7/60", "0.1167"], "M4-c142": ["40.4006", "40"], "M4-c143": ["0.8552", "0.0056"],
    "M4-c157": ["0.063451", "1.5240"], "M4-c161": ["0.634510", "0.002"], "M4-c168": ["0.002128"],
    "M4-c172": ["2.205308"], "M4-c185": ["-0.0080", "+0.0066", "+0.0022", "-0.0056", "-0.0074"],
    "M4-c188": ["0.9770", "-2.0055", "0.0230", "0.0055"], "M4-c189": ["+0.0031", "0.0031"],
    "M4-c190": ["-0.0235"], "M4-c237": ["1.8838"], "M4-c238": ["0.8518"], "M4-c239": ["0.9396"],
    "M4-c240": ["1.1987"], "M4-c233": ["0.847994"], "M4-c234": ["0.843496"], "M4-c235": ["0.835793"],
    "M4-c236": ["0.833926"], "M4-c165": ["0.833333"], "M4-c166": ["3.4689", "0.0311"],
    "M4-c169": ["+0.9919", "0.9919"], "M4-c170": ["1.0211"], "M4-c171": ["0.8807"], "M4-c162": ["1.8220"],
    "M4-c126": ["0.0187"], "M4-c167": ["0.8548"],
}
by_id = {c["id"]: c for c in cards}
for cid, needles in numbers.items():
    lesson = by_id[cid]["lesson"]
    missing = [n for n in needles if n not in pages[lesson]]
    if missing:
        print("NOT IN LESSON", cid, lesson, missing)
print("number-presence check done for", len(numbers), "cards")
