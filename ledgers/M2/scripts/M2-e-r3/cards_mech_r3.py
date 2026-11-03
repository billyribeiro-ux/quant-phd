"""Round-3 mechanical card checks: unique ids and fronts, grade and basis fields, numbers and locators against the lesson text.

Lesson text comes from tools-free cleaning of course/modules/M/M2/L##.html (HTML tags removed, <pre> kept).
"""

import json
import pathlib
import re
import sys
from collections import Counter
from html.parser import HTMLParser

ROOT = pathlib.Path(sys.argv[1])
CARDS = ROOT / "course/modules/M/M2/cards.json"


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


def lesson_text(n: str) -> str:
    p = Text()
    p.feed((ROOT / f"course/modules/M/M2/{n}.html").read_text(encoding="utf-8"))
    return re.sub(r"\s+", " ", " ".join(p.parts))


cards = json.loads(CARDS.read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)), "id format ok", all(re.fullmatch(r"M2-c\d{3}", i) for i in ids))
fronts = Counter(re.sub(r"[^a-z0-9 ]", "", c["front"].lower()) for c in cards)
print("duplicate fronts (normalised)", [f for f, k in fronts.items() if k > 1])
print("grades", dict(Counter(c.get("grade") for c in cards)))
bad_basis = [c["id"] for c in cards if c.get("grade") in ("C", "T") and not c.get("basis") and c.get("grade") == "C"]
print("grade C without basis", bad_basis)
print("grade T with basis", [c["id"] for c in cards if c.get("grade") == "T" and c.get("basis")])
print("per lesson", dict(sorted(Counter(c["lesson"] for c in cards).items())))

texts = {}
LOC = re.compile(r"\b(Theorem|Proposition|Lemma|Corollary|Example|Remark|Assumption|Definition|Problem|Section|Misconception|Lab)\s+(\d+(?:\.\d+)?)")
fails = []
for c in cards:
    n = c["lesson"]
    if n not in texts:
        texts[n] = lesson_text(n)
    t = texts[n]
    body = c["front"] + " " + c["back"]
    for num in set(re.findall(r"\d+(?:\.\d+)?", body)):
        if num not in t and not re.search(r"(?<![\d.])" + re.escape(num) + r"(?![\d])", t):
            fails.append((c["id"], "number", num))
    for kind, num in set(LOC.findall(body)):
        if kind == "Section":
            continue
        if f"{kind} {num}" not in t:
            fails.append((c["id"], "locator", f"{kind} {num}"))
print("cards with a number absent from own lesson or a locator not found in it:", len(fails))
for f in fails[:80]:
    print("  ", f)
