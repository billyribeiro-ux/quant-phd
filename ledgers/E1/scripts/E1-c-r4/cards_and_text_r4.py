"""Card and text checks for E1 slice c (L07-L09), verifier round 4.

Run from the repository root: python -I ledgers/E1/scripts/E1-c-r4/cards_and_text_r4.py
Checks: card ids and lessons, duplicate fronts and backs over the whole deck, every number in a slice card back
appears in its lesson page, the banned-string list of BUILDER_RULES 1.3-1.4, forbidden attributions and names, and
registered notation symbols (notation/notation.json) against symbols used in the slice pages.
"""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
E1 = ROOT / "course/modules/E/E1"
SLICE = ("L07", "L08", "L09")


def text_of(path: Path) -> str:
    return re.sub(r"<[^>]+>", " ", path.read_text(encoding="utf-8"))


def main() -> int:
    cards = json.loads((E1 / "cards.json").read_text(encoding="utf-8"))
    print(f"cards in deck: {len(cards)}")
    ids = [c["id"] for c in cards]
    print("duplicate ids:", sorted({i for i in ids if ids.count(i) > 1}))
    fronts = collections.Counter(c["front"].strip().lower() for c in cards)
    backs = collections.Counter(c["back"].strip().lower() for c in cards)
    print("duplicate fronts:", [f for f, n in fronts.items() if n > 1])
    print("duplicate backs:", [b[:50] for b, n in backs.items() if n > 1])
    bad_id = [c["id"] for c in cards if not re.fullmatch(r"E1-c\d{3}", c["id"])]
    print("malformed ids:", bad_id)

    slice_cards = [c for c in cards if c["lesson"] in SLICE]
    print(f"slice cards (L07-L09): {len(slice_cards)} ids {slice_cards[0]['id']}..{slice_cards[-1]['id']}")
    missing_numbers = []
    for c in slice_cards:
        page = text_of(E1 / f"{c['lesson']}.html").replace(",", "")
        for n in set(re.findall(r"\d+(?:\.\d+)?", c["back"])):
            if n not in page:
                missing_numbers.append((c["id"], n))
    print("card back numbers absent from the lesson text:", missing_numbers)

    body = "\n".join((E1 / f"{p}.html").read_text(encoding="utf-8") for p in SLICE)
    body_no_code = re.sub(r"<pre.*?</pre>", "", body, flags=re.S)
    banned = [
        "TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
        "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
        "obviously", "clearly", "...",
    ]
    print("banned strings in slice pages (outside code):", [b for b in banned if b.lower() in body_no_code.lower()])
    process = ["builder", "verifier", "round ", "REQUESTS", "planner", "ledger"]
    print("process words in slice pages:", [w for w in process if w.lower() in body_no_code.lower()])
    names = ["Nash", "Lagrang", "KKT", "convex", "expected utility", "first welfare", "Edgeworth", "Lindahl",
             "Coase", "Samuelson", "Pigou ", "Pigou)", "Varian", "Arrow", "Debreu"]
    print("forbidden names or attributions in slice pages and cards:",
          [n for n in names if n.lower() in (body + json.dumps(slice_cards)).lower()])
    registered = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))["symbols"]
    print("registered notation symbols:", [s["symbol"] for s in registered])
    used_registered = [s for s in ["\\mathbb{Q}", "\\Phi", "\\gamma_3", "\\gamma_4", "R^\\ast", "R_f", "\\mathbb{R}",
                                   "\\R", "T ="] if s in body]
    print("registered symbols or macros used in slice pages:", used_registered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
