"""Round 4 checks for SC1 L07 and L08: card coverage of misconceptions, card basis for A3/A4 results,
and the sequence count that the L08 Part A sentence reports.

Run: python -I -W error ledgers/SC1/scripts/SC1-c-r4/cards_and_counts_r4.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE4-SC1-c")


def main() -> None:
    cards = json.loads((ROOT / "course/modules/SC/SC1/cards.json").read_text(encoding="utf-8"))
    by_id = {c["id"]: c for c in cards}
    print("cards total", len(cards), "unique ids", len(by_id))

    # Misconception headings on each page, and whether a card with the same subject exists.
    subjects = {
        "L07": [
            ("same law as B_H", "SC1-c191"),
            ("grid maximum can overstate", "SC1-c153"),
            ("normal one-time marginals", "SC1-c154"),
        ],
        "L08": [
            ("finite on every path", "SC1-c176"),
            ("same probability as the terminal value", None),
            ("mean of tau_a is finite", "SC1-c178"),
        ],
    }
    for lesson, items in subjects.items():
        for label, cid in items:
            if cid is None:
                found = [c["id"] for c in cards if c.get("lesson") == lesson and "B_" in c["front"] and "τ" in c["front"]
                         and ("P(τ" in c["front"] or "terminal" in c["front"] or "B_H" in c["front"])]
                print(f"{lesson} misconception [{label}] -> card candidates {found}")
            else:
                print(f"{lesson} misconception [{label}] -> {cid} present: {cid in by_id}")
    print("SC1-c190 present:", "SC1-c190" in by_id, "; SC1-c163 present:", "SC1-c163" in by_id)
    print("SC1-c192 basis:", by_id["SC1-c192"].get("basis"))
    a34 = re.compile(r"A3|A4")
    print("SC1-c192 basis names A3/A4:", bool(a34.search(by_id["SC1-c192"].get("basis", ""))))
    for cid in ("SC1-c139", "SC1-c140"):
        print(cid, "basis names A3/A4:", bool(a34.search(by_id[cid].get("basis", ""))))

    # Sequence counts: distinct step sequences versus (sequence, level) pairs.
    distinct = sum(2**n for n in range(1, 13))
    pairs = sum(n * 2**n for n in range(1, 13))
    print("distinct step sequences for n = 1..12:", distinct)
    print("(sequence, level a <= n) pairs for n = 1..12:", pairs)

    twin = (ROOT / "tests/labs/SC1/lab-SC1-L08-1.py").read_text(encoding="utf-8")
    m = re.search(r'print\(f"Part A: sequences checked: [^"]*"\)', twin)
    print("twin Part A label line:", m.group(0) if m else "not found")
    page = (ROOT / "course/modules/SC/SC1/L08.html").read_text(encoding="utf-8")
    print("L08 page says 'all 90114 step sequences':", "90114 step sequences" in page)
    print("L08 page key-results says 'all 90114 sequences':", "all 90114 sequences" in page)


if __name__ == "__main__":
    main()
