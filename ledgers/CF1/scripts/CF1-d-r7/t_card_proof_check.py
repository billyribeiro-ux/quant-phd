"""Structural check for T cards: each Theorem/Proposition/Corollary label in a T card's back is a claim block with a proof.

Run: /path/to/checkout/.venv/bin/python -I t_card_proof_check.py <checkout>
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) / "course/modules/CF/CF1"


def blocks(lesson: str) -> dict[str, tuple[bool, bool, bool]]:
    t = (ROOT / f"{lesson}.html").read_text(encoding="utf-8")
    bl = [(m.start(), m.group(0)) for m in re.finditer(r'<span class="block-title[^"]*"[^>]*>(.*?)</span>', t)]
    out: dict[str, tuple[bool, bool, bool]] = {}
    for i, (pos, bt) in enumerate(bl):
        label = html.unescape(re.sub(r"<[^>]+>", "", bt)).strip()
        m = re.match(r"((?:Theorem|Proposition|Corollary|Lemma|Definition|Remark|Example|Problem)\s+[A-Z]?\d+(?:\.\d+)?)", label)
        if not m:
            continue
        nxt = bl[i + 1][0] if i + 1 < len(bl) else len(t)
        seg = t[pos:nxt]
        out[m.group(1)] = ("claim" in bt, "Proof" in seg or 'class="block proof"' in seg, "data-grade" in bt)
    return out


cards = json.loads((ROOT / "cards.json").read_text(encoding="utf-8"))
rows = []
for c in cards:
    if c["grade"] != "T":
        continue
    labs = re.findall(r"\b(Theorem|Proposition|Corollary)\s+(\d+\.\d+)", c["back"])
    if not labs:
        continue
    key = f"{labs[0][0]} {labs[0][1]}"
    info = blocks(c["lesson"]).get(key)
    rows.append((c["id"], key, info))
print("T cards with a theorem-type label:", len(rows))
print("label not found:", [r[:2] for r in rows if r[2] is None])
print("block not a claim:", [r[:2] for r in rows if r[2] and not r[2][0]])
print("block without proof:", [r[:2] for r in rows if r[2] and not r[2][1]])
