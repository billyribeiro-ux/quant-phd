"""Near-duplicate scan over the L01-L04 cards: pairs whose fronts or backs are similar."""
import difflib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course/modules/M/M4"
cards = [c for c in json.loads((root / "cards.json").read_text(encoding="utf-8")) if c["lesson"] in ("L01", "L02", "L03", "L04")]
pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1:]:
        fr = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
        bk = difflib.SequenceMatcher(None, a["back"].lower(), b["back"].lower()).ratio()
        if fr > 0.45 or bk > 0.45:
            pairs.append((round(max(fr, bk), 2), a["id"], b["id"], round(fr, 2), round(bk, 2)))
for p in sorted(pairs, reverse=True):
    print(p)
    a = next(c for c in cards if c["id"] == p[1])
    b = next(c for c in cards if c["id"] == p[2])
    print("   A:", a["front"], "=>", a["back"][:150])
    print("   B:", b["front"], "=>", b["back"][:150])
