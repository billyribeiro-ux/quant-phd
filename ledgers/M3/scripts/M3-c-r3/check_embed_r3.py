"""Compare each slice lab section with its twin: page code == twin text, expected block == twin stdout, no markers.

Usage: python -I check_embed_r3.py <repo-root> <stdout-dir>
"""
import sys
from html.parser import HTMLParser

ROOT, OUTDIR = sys.argv[1], sys.argv[2]


class Pres(HTMLParser):
    def __init__(self, section_id):
        super().__init__(convert_charrefs=True)
        self.section_id = section_id
        self.depth = 0
        self.in_section = False
        self.in_pre = False
        self.pres = []  # (class, text)
        self.cur = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "section" and a.get("id") == self.section_id:
            self.in_section = True
            self.depth = 0
        if self.in_section:
            if tag == "section":
                self.depth += 1
            if tag == "pre":
                self.in_pre = True
                self.cur = [a.get("class", ""), []]

    def handle_endtag(self, tag):
        if self.in_section:
            if tag == "pre" and self.in_pre:
                self.in_pre = False
                self.pres.append((self.cur[0], "".join(self.cur[1])))
            if tag == "section":
                if self.depth == 0:
                    self.in_section = False
                else:
                    self.depth -= 1

    def handle_data(self, data):
        if self.in_section and self.in_pre:
            self.cur[1].append(data)


ok_all = True
for n in ("07", "08", "09"):
    page = f"{ROOT}/course/modules/M/M3/L{n}.html"
    p = Pres(f"lab-M3-L{n}-1")
    p.feed(open(page, encoding="utf-8").read())
    code = [t for c, t in p.pres if "expected" not in c.split()]
    expected = [t for c, t in p.pres if "expected" in c.split()]
    twin = open(f"{ROOT}/tests/labs/M3/lab-M3-L{n}-1.py", encoding="utf-8").read()
    stdout = open(f"{OUTDIR}/twin_L{n}.stdout", encoding="utf-8").read()
    code_eq = len(code) == 1 and code[0].rstrip("\n") == twin.rstrip("\n")
    exp_eq = len(expected) == 1 and expected[0].rstrip("\n") == stdout.rstrip("\n")
    markers = "@@" in "".join(code + expected)
    print(f"L{n}: code_blocks={len(code)} expected_blocks={len(expected)} code==twin:{code_eq} expected==stdout:{exp_eq} markers:{markers}")
    ok_all = ok_all and code_eq and exp_eq and not markers
print("EMBED", "PASS" if ok_all else "FAIL")
