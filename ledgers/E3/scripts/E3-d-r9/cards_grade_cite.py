"""Round-3 check of BUILDER_RULES section 7 on cards.json: a card with a non-T grade must cite registry keys or name a
basis; every cite key must be in references/references.json; a grade must be one of T, A, B, C, D, X.

Usage (from the checkout): .venv/bin/python ledgers/E3/scripts/E3-d-r3/cards_grade_cite.py
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
cards = json.loads((ROOT / "course/modules/E/E3/cards.json").read_text(encoding="utf-8"))
refs = json.loads((ROOT / "references/references.json").read_text(encoding="utf-8"))
keys = {r.get("key") for r in refs["entries"]}
grades = Counter(c.get("grade", "<none>") for c in cards)
print("grades:", dict(grades))
bad_grade = [c["id"] for c in cards if c.get("grade") not in (None, "T", "A", "B", "C", "D", "X")]
print("bad grade values:", bad_grade)
missing_basis = [c["id"] for c in cards if c.get("grade") not in (None, "T") and not (c.get("cite") or c.get("basis"))]
print("graded non-theorem cards with neither cite nor basis:", missing_basis)
unknown = sorted({(c["id"], k) for c in cards for k in c.get("cite", []) if k not in keys})
print("cite keys not in registry:", unknown)
print("cite usage:", dict(Counter(k for c in cards for k in c.get("cite", []))))
print("basis values:", sorted({c["basis"] for c in cards if "basis" in c}))
for c in cards:
    if c.get("grade") == "T" and (c.get("cite") or c.get("basis")):
        print("T card with cite/basis:", c["id"])
