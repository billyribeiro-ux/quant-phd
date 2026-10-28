"""Round 8 AC1-a mechanical checks: twin-to-page equality, banned phrases, citation markup, notation macros,
card id/front duplicates, and the Proposition 3.2 write-off scope witness (hand arithmetic recomputed in code)."""

from __future__ import annotations

import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path("/tmp/verify8-AC1-a")
PAGES = {"L01": "lab-AC1-L01-1.py", "L02": "lab-AC1-L02-1.py", "L03": "lab-AC1-L03-1.py"}
PAGE_FILES = ["index.html", "L01.html", "L02.html", "L03.html"]
BANNED = ["roughly half", "about 6", "historically", "as much as", "TODO", "TBD", "lorem", "…", "..."]
NOTATION_BAD = ["gamma3", "gamma4", "\\Phi", "\\mathbb", "\\Rstar", "\\R_f", "\\mathbf"]


def main() -> int:
    bad = 0
    base = ROOT / "course/modules/AC/AC1"
    for lesson, twin in PAGES.items():
        page = (base / f"{lesson}.html").read_text(encoding="utf-8")
        twin_src = (ROOT / "tests/labs/AC1" / twin).read_text(encoding="utf-8")
        blocks = re.findall(r'<code class="language-python" data-run>(.*?)</code>', page, flags=re.S)
        same = [html.unescape(b).rstrip("\n") == twin_src.rstrip("\n") for b in blocks]
        print(f"{lesson} data-run blocks {len(blocks)} equal to twin: {same}")
        bad += 0 if (len(blocks) == 1 and all(same)) else 1
    for name in PAGE_FILES:
        text = (base / name).read_text(encoding="utf-8")
        for phrase in BANNED:
            n = text.count(phrase)
            if n:
                print(f"{name}: banned/ellipsis '{phrase}' x{n}")
                bad += 1
        for macro in NOTATION_BAD:
            if macro in text:
                print(f"{name}: notation macro {macro} present")
                bad += 1
        for marker in ("data-cite", 'class="cite"', "data-key"):
            if marker in text:
                print(f"{name}: citation markup {marker}")
                bad += 1
    print("banned, notation and citation scan finished; problems:", bad)

    cards = json.loads((base / "cards.json").read_text(encoding="utf-8"))
    ids = [c["id"] for c in cards]
    fronts = [c["front"].strip().lower() for c in cards]
    print("cards total", len(cards), "unique ids", len(set(ids)), "unique fronts", len(set(fronts)))
    dup_fronts = sorted({f for f in fronts if fronts.count(f) > 1})
    print("duplicate fronts:", dup_fronts)

    # Proposition 3.2 scope witness: a write-off breaks R - K = dA when R, K are the only inputs.
    sales, collections, writeoff = 100, 0, 30
    d_ar = sales - collections - writeoff
    print(f"write-off witness: R={sales} K={collections} dA={d_ar} R-K={sales - collections} identity holds: {sales - collections == d_ar}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
