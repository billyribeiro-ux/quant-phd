"""SC1-c round 7: card checks for L07 and L08 (run from the checkout root; stdlib only).

Prints: duplicate fronts and ids over all of cards.json; every L07/L08 card; the closed-form cards with
their assumption wording; numbers in each L07/L08 card back that do not occur in the lesson page;
and the cards that differ from the round-6 pin (4bd8cb94).
"""

from __future__ import annotations

import collections
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[4]
cards = json.loads((ROOT / "course/modules/SC/SC1/cards.json").read_text(encoding="utf-8"))
print(f"cards: {len(cards)}")
fr = collections.Counter(c["front"] for c in cards)
ids = collections.Counter(c["id"] for c in cards)
print("duplicate fronts:", [k for k, v in fr.items() if v > 1])
print("duplicate ids:", [k for k, v in ids.items() if v > 1])
mine = [c for c in cards if c["lesson"] in ("L07", "L08")]
print(f"L07/L08 cards: {len(mine)}")
for c in mine:
    print(f"{c['id']} [{c['lesson']}] grade={c.get('grade')} cite={c.get('cite')} basis={c.get('basis')}")
    print("  F:", c["front"])
    print("  B:", c["back"])
print("== closed-form cards: wording of assumptions")
pat = re.compile(r"closed form|√\(2/π\)|0\.3173|erfc|Φ|E\[M|E\[τ|f_a|density")
for c in mine:
    txt = c["front"] + " || " + c["back"]
    if pat.search(txt):
        has = bool(re.search(r"[Aa]ssum|under H|H2|hypothes|Under", txt))
        print(f"{c['id']} assumption_wording={has}")
print("== numbers in L07/L08 card backs that do not occur in the lesson page (len>=3)")
for c in mine:
    page = (ROOT / f"course/modules/SC/SC1/{c['lesson']}.html").read_text(encoding="utf-8")
    nums = set(re.findall(r"\d+(?:\.\d+)?", c["back"]))
    missing = sorted(n for n in nums if len(n) >= 3 and n not in page)
    if missing:
        print(c["id"], missing)
print("== cards changed since round-6 pin 4bd8cb94")
old = json.loads(subprocess.run(["git", "show", "4bd8cb94:course/modules/SC/SC1/cards.json"], capture_output=True, text=True, cwd=ROOT, check=True).stdout)
oldid = {c["id"]: c for c in old}
for c in cards:
    if oldid.get(c["id"]) != c:
        print("changed:", c["id"], c["lesson"])
