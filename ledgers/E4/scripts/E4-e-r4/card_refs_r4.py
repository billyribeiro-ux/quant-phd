"""Round-4 check: every labelled item a card names is printed in its own lesson, or in another E4 lesson.

Usage: python -I card_refs_r4.py <cards.json> <txt-dir>
txt-dir holds L01.txt to L09.txt (output of html_to_text.py). Also checks that quoted assumption and
definition numbers exist, and reports each cross-lesson reference with its lesson of origin.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

KINDS = r"(Definition|Proposition|Lemma|Corollary|Remark|Example|Assumption|Fact|Problem|Misconception)"
REF = re.compile(r"\b" + KINDS + r" (\(?[A-Z]?\d+(?:\.\d+)?\)?|[A-Z]\d+|[A-Z])")


def main() -> None:
    cards = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    texts = {p.stem: p.read_text(encoding="utf-8") for p in Path(sys.argv[2]).glob("L*.txt")}
    total = missing = cross = 0
    for card in cards:
        body = card["front"] + " " + card["back"]
        for m in REF.finditer(body):
            kind, num = m.group(1), m.group(2).strip("()")
            if kind == "Misconception":
                continue
            total += 1
            pattern = f"{kind} {num}"
            if pattern in texts.get(card["lesson"], "") or pattern.replace("Problem ", "") in texts.get(
                card["lesson"], ""
            ):
                continue
            where = [name for name, t in texts.items() if pattern in t]
            if where:
                cross += 1
                print(f"CROSS {card['id']} ({card['lesson']}): '{pattern}' printed only in {sorted(where)}")
            else:
                missing += 1
                print(f"MISSING {card['id']} ({card['lesson']}): '{pattern}' printed in no E4 lesson")
    print(f"references checked={total} cross_lesson={cross} missing={missing}")


if __name__ == "__main__":
    main()
