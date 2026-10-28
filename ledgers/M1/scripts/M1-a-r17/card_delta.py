"""Round-17 card delta for M1 L01-L03: changed/new cards since de53f7e, and near-duplicate scan.

Usage: python -I card_delta.py <checkout> <old_cards.json>
"""
import difflib
import itertools
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
old = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
new = json.loads((root / "course/modules/M/M1/cards.json").read_text(encoding="utf-8"))
old_by = {c["id"]: c for c in old}
lessons = {"L01", "L02", "L03"}
changed = [c["id"] for c in new if c["id"] in old_by and old_by[c["id"]] != c and c["lesson"] in lessons]
added = [c["id"] for c in new if c["id"] not in old_by and c["lesson"] in lessons]
print("changed L01-L03:", changed)
print("added L01-L03:", added)
for a, b in itertools.combinations(new, 2):
    if a["lesson"] not in lessons or b["lesson"] not in lessons:
        continue
    fr = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
    br = difflib.SequenceMatcher(None, a["back"].lower(), b["back"].lower()).ratio()
    if fr > 0.6 or br > 0.7:
        print("near-dup", a["id"], b["id"], round(fr, 2), round(br, 2))
for c in new:
    if c["id"] in ("M1-c060", "M1-c063", "M1-c175", "M1-c056"):
        print(c["id"], "|", c["front"], "||", c["back"])
