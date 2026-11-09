"""Round-12 verifier (M3 slice d): ruling 13 check. For each lesson, lists the key-results rows graded C and the cards
graded C (grade and basis), and flags any T card that cites lab output or SIMULATED values. Run from the checkout root
with python -I. The lesson text is extracted in memory with the parser below."""

import json
import re
from html.parser import HTMLParser


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.out = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self.skip += 1
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "tr", "div", "section", "pre", "dt", "dd", "table", "ol", "ul"):
            self.out.append("\n")
        if tag in ("td", "th"):
            self.out.append(" | ")
        if tag == "section" and "id" in a:
            self.out.append(f"\n[section {a['id']}]")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, d):
        if not self.skip:
            self.out.append(d)


cards = json.load(open("course/modules/M/M3/cards.json", encoding="utf-8"))
for i in range(1, 10):
    lesson = f"L0{i}"
    parser = Text()
    parser.feed(open(f"course/modules/M/M3/{lesson}.html", encoding="utf-8").read())
    body = re.sub(r"[ \t]+", " ", "".join(parser.out))
    body = re.sub(r"\n\s*\n+", "\n", body)
    kr = body[body.find("[section key-results]"): body.find("[section quiz]")]
    rows = [r for r in kr.split("\n") if r.startswith(" | ") and r.count(" | ") >= 3]
    print(f"== {lesson} key-results rows: {len(rows)}")
    for r in rows:
        parts = [p.strip() for p in r.split(" | ")[1:]]
        if len(parts) >= 3 and parts[1] == "C":
            print("  KR C:", parts[2][:150])
    for c in [c for c in cards if c["lesson"] == lesson and c.get("grade") == "C"]:
        print("  CARD C", c["id"], "| basis:", c["basis"][:150])
bad = [c["id"] for c in cards if c.get("grade") == "T" and re.search(r"\bLab\b|SIMULATED|seed", c["front"] + " " + c["back"])]
print("T cards citing lab output or SIMULATED values:", bad)
