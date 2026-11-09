"""FC1-a round 2: scan the L01-L03 cards for near-duplicate fronts and backs (difflib ratio) and for id/lesson sanity."""

import difflib
import json
import re
from pathlib import Path

cards = json.loads(Path("course/modules/FC/FC1/cards.json").read_text(encoding="utf-8"))
sel = [c for c in cards if c["lesson"] in ("L01", "L02", "L03")]
print("slice cards:", len(sel), "ids:", sel[0]["id"], "...", sel[-1]["id"])
bad_ids = [c["id"] for c in sel if not re.fullmatch(r"FC1-c\d{3}", c["id"])]
print("bad ids:", bad_ids)
print("grades used:", sorted({c.get("grade", "-") for c in sel}))
print("C without basis:", [c["id"] for c in sel if c.get("grade") == "C" and not c.get("basis")])
pairs = []
for i, a in enumerate(sel):
    for b in sel[i + 1:]:
        rf = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
        rb = difflib.SequenceMatcher(None, a["back"].lower(), b["back"].lower()).ratio()
        if rf > 0.45 or rb > 0.45 or (rf + rb) / 2 > 0.4:
            pairs.append((round((rf + rb) / 2, 3), a["id"], b["id"], round(rf, 2), round(rb, 2)))
for p in sorted(pairs, reverse=True):
    print("near-dup:", p)
