"""Verifier check (FC2 slice c, round 3): L07/L08 cards.

1. ids unique across cards.json; the 37 L07/L08 cards are present with lesson fields matching.
2. every numeric token in each L07/L08 card front/back appears in its lesson's visible text (tags, scripts and
   attributes removed; entities and minus and superscript glyphs normalised).
3. near-duplicate fronts across the whole file (difflib ratio >= 0.75) are listed for review.
4. grade and basis fields for L07/L08 cards are listed for review.
Run: .venv/bin/python -I ledgers/FC2/scripts/FC2-c-r3/cards_check.py
"""

from __future__ import annotations

import difflib
import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
cards = json.loads((ROOT / "course/modules/FC/FC2/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
dup = [k for k, v in Counter(ids).items() if v > 1]
print("cards:", len(cards), "unique ids:", len(set(ids)), "duplicate ids:", dup)

SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")


def visible(path: Path) -> str:
    t = path.read_text(encoding="utf-8")
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<pre.*?</pre>", lambda m: m.group(0), t, flags=re.S)  # code stays visible text
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t).replace("−", "-")
    return t.translate(SUP)


texts = {
    "L07": visible(ROOT / "course/modules/FC/FC2/L07.html"),
    "L08": visible(ROOT / "course/modules/FC/FC2/L08.html"),
}
l78 = [c for c in cards if c.get("lesson") in ("L07", "L08")]
print("L07/L08 cards:", len(l78), Counter(c["lesson"] for c in l78))
missing: list[str] = []
for c in l78:
    body = f"{c['front']} {c['back']}".replace("−", "-").translate(SUP)
    for tok in set(re.findall(r"\d+(?:\.\d+)?", body)):
        if tok not in texts[c["lesson"]]:
            missing.append(f"{c['id']}:{tok}")
print("numeric tokens not found in own lesson text:", missing if missing else "none")

near = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i]["front"], cards[j]["front"]
        r = difflib.SequenceMatcher(None, a, b).ratio()
        if r >= 0.75:
            near.append((round(r, 2), cards[i]["id"], cards[j]["id"]))
print("near-duplicate front pairs (ratio>=0.75):", near if near else "none")

for c in l78:
    print(c["id"], c["lesson"], "grade=", c.get("grade", "-"), "basis=", c.get("basis", "-"), "keys=", sorted(c.keys()))
