"""Maps each card's 'Misconception n' locator to the n-th <li class="misconception"> of its lesson (ordered list) and prints both texts."""
import html.parser, json, pathlib, re, sys

root = pathlib.Path(sys.argv[1])
cards = json.loads((root / "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))

class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.items, self.depth, self.cur, self.in_wrong = [], 0, None, False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "li" and a.get("class") == "misconception":
            self.cur = []
        if tag == "p" and a.get("class") == "wrong" and self.cur is not None:
            self.in_wrong = True
    def handle_endtag(self, tag):
        if tag == "p" and self.in_wrong:
            self.in_wrong = False
        if tag == "li" and self.cur is not None:
            self.items.append("".join(self.cur)); self.cur = None
    def handle_data(self, d):
        if self.in_wrong and self.cur is not None:
            self.cur.append(d)

pat = re.compile(r"Misconception (\d)")
for c in cards:
    m = pat.search(c["back"]) or pat.search(c["front"])
    if not m:
        continue
    n = int(m.group(1))
    p = P(); p.feed((root / f"course/modules/M/M2/{c['lesson']}.html").read_text(encoding="utf-8"))
    item = p.items[n - 1] if n <= len(p.items) else "<missing>"
    print(c["id"], c["lesson"], f"M{n}", "| card:", c["front"][:70], "| item:", " ".join(item.split())[:90])
