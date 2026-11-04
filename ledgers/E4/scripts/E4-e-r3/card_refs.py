"""Slice e check: every labelled item a card names must be printed in the card's lesson (or another E4 lesson).

Usage: python -I card_refs.py <cards.json> <lesson-text-dir>
The lesson-text dir holds L01.txt to L09.txt, the output of html_to_text.py.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

KINDS = r"(Definition|Proposition|Lemma|Corollary|Theorem|Remark|Example|Assumption|Fact|Problem|Lab|Section)"
REF = re.compile(r"\b" + KINDS + r" ([A-Z]?\d+(?:\.\d+)?|[A-Z]\d+)")


def main() -> None:
    cards = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    texts = {p.stem: p.read_text(encoding="utf-8") for p in Path(sys.argv[2]).glob("*.txt")}
    missing = 0
    total = 0
    for card in cards:
        body = card["front"] + " " + card["back"]
        for match in REF.finditer(body):
            kind, num = match.group(1), match.group(2)
            if kind in ("Section", "Lab"):
                continue
            total += 1
            pattern = f"{kind} {num}"
            if pattern in texts.get(card["lesson"], ""):
                continue
            where = [name for name, text in texts.items() if pattern in text]
            if where:
                print(f"CROSS {card['id']} ({card['lesson']}): '{pattern}' printed only in {sorted(where)}")
            else:
                missing += 1
                print(f"MISSING {card['id']} ({card['lesson']}): '{pattern}' printed in no E4 lesson")
    print(f"references checked={total} missing={missing}")


if __name__ == "__main__":
    main()
