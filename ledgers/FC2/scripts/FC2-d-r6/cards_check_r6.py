"""Round 6 FC2-d: card checks against the CURRENT lesson text of this checkout.

Lesson text is extracted losslessly (tags stripped, entities unescaped, MathJax delimiters kept). For every card:
 1. each cited label (Definition/Proposition/Theorem/Lemma/Remark/Example/Assumption/Problem/Section/Lab/Solution N)
    exists in the card's own lesson text;
 2. each decimal number on the card appears in that lesson text;
 3. each integer of two or more digits on the card appears in the lesson text or in its page's expected/output text.
Then: ids unique, front texts unique, and near-duplicate pairs (difflib ratio >= 0.80) are listed for review.
Run as: <checkout>/.venv/bin/python -I <this file> <checkout>
"""

import difflib
import html
import json
import pathlib
import re
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(sys.argv[1])
MOD = ROOT / "course/modules/FC/FC2"


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1
        if tag in ("p", "li", "tr", "div", "h1", "h2", "h3", "h4", "pre", "br", "dd", "dt", "td", "th"):
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


def lesson_text(path: pathlib.Path) -> str:
    p = Text()
    p.feed(path.read_text(encoding="utf-8"))
    return html.unescape("".join(p.parts))


txt = {}
for lesson in ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08"]:
    raw = lesson_text(MOD / f"{lesson}.html")
    txt[lesson] = raw.replace("\\(", "").replace("\\)", "")
pages_all = "\n".join(lesson_text(MOD / f"{n}.html") for n in ["project"]) + "\n".join(txt.values())
txt_project = lesson_text(MOD / "project.html")

cards = json.loads((MOD / "cards.json").read_text(encoding="utf-8"))
label_re = re.compile(
    r"\b(Definition|Proposition|Theorem|Lemma|Corollary|Remark|Example|Assumption|Problem|Section|Lab|Solution)"
    r"\s+([A-Z]?\d+(?:\.\d+)?(?:\([a-z]\))?)"
)
findings: list[tuple[str, str, str, str]] = []
for c in cards:
    lesson = c["lesson"]
    body = txt[lesson]
    srcs = " ".join(str(c.get(k, "")) for k in ("front", "back", "basis"))
    for kind, num in label_re.findall(srcs):
        base = num.split("(")[0]
        pat = re.compile(re.escape(kind) + r"\s+" + re.escape(base) + r"(?![\d.])")
        if not pat.search(body):
            findings.append((c["id"], lesson, f"{kind} {num}", "label not in lesson text"))
    for num in sorted(set(re.findall(r"(?<![\w/])\d+\.\d+", srcs))):
        if num not in body:
            findings.append((c["id"], lesson, num, "decimal not in lesson text"))
    for num in sorted(set(re.findall(r"(?<![\w/.])\d{2,}(?![\d.])", srcs))):
        if num not in body and num not in txt_project:
            findings.append((c["id"], lesson, num, "integer not in lesson or project text"))

ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)) == len(ids))
print("unique fronts:", len({c["front"] for c in cards}) == len(cards))
for f in findings:
    print("FINDING", f)
print("finding count:", len(findings))

pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a = cards[i]["front"] + " " + cards[i]["back"]
        b = cards[j]["front"] + " " + cards[j]["back"]
        r = difflib.SequenceMatcher(None, a, b).ratio()
        if r >= 0.80:
            pairs.append((round(r, 3), cards[i]["id"], cards[j]["id"]))
print("near-duplicate pairs (ratio >= 0.80):", len(pairs))
for p in sorted(pairs, reverse=True):
    print("PAIR", p)
for cid in ["FC2-c030", "FC2-c049", "FC2-c145"]:
    c = next(x for x in cards if x["id"] == cid)
    print("CHANGED", cid, json.dumps(c, ensure_ascii=False))
