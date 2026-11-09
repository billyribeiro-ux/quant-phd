"""Closing-delta card checks (CF8-c round 1). Run as: python3 -I d1_cards_checks.py <cards.json>.

Reads the lesson HTML of the checkout (ROOT) and prints, for every card: duplicate pairs,
process words, numbers absent from the card's own lesson, and registry-symbol tokens.
"""

import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser

ROOT = "/Users/billyribeiro/.fanout/wt/verifyG1-CF8-c/course/modules/CF/CF8/"


class _Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


def lesson_text(lid: str) -> str:
    parser = _Text()
    with open(ROOT + lid + ".html", encoding="utf-8") as fh:
        parser.feed(fh.read())
    text = " ".join(parser.parts).replace("{,}", ",")
    return re.sub(r"\s+", " ", text)


def main() -> None:
    with open(sys.argv[1], encoding="utf-8") as fh:
        cards = json.load(fh)
    print("cards", len(cards), "unique ids", len({c["id"] for c in cards}))
    pairs = [(c["front"], c["back"]) for c in cards]
    print("duplicate (front,back) pairs", len(pairs) - len(set(pairs)))
    print("duplicate fronts", len(cards) - len({c["front"] for c in cards}))
    print("lesson counts", dict(Counter(c["lesson"] for c in cards)))
    process = re.compile(r"\b(round|builder|verifier|revision|this slice|fanout|ruling|blind|rulings)\b", re.I)
    registry = [r"\bT\b", r"\bQ\b", r"\\Phi|Φ", r"R_f", r"R\^", r"gamma|γ"]
    texts: dict[str, str] = {}
    for c in cards:
        if c["lesson"] not in texts:
            texts[c["lesson"]] = lesson_text(c["lesson"])
        both = c["front"] + " " + c["back"]
        if process.search(both):
            print("PROCESS WORD", c["id"])
        for pattern in registry:
            if re.search(pattern, both):
                print("REGISTRY SYMBOL TOKEN", c["id"], pattern)
        for num in sorted(set(re.findall(r"\d[\d,\.]*\d|\d", both))):
            token = num.rstrip(".,")
            if token and token not in texts[c["lesson"]]:
                found = [lid for lid in texts if token in texts[lid]]
                print("NUM NOT IN OWN LESSON", c["id"], c["lesson"], repr(token), "found in", found)
    print("checked", len(cards), "cards")


if __name__ == "__main__":
    main()
