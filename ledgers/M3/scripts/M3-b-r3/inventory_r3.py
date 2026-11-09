"""Round-3 slice b: inventory of anchors, hours, quiz items, macros, figures, citations, forward references.

Run from the checkout root. Output saved as inventory_r3.out.
"""
import glob
import json
import re
from collections import Counter

P = "course/modules/M/M3/"
notation = json.load(open("notation/notation.json", encoding="utf-8"))
macros = set(notation["macros"].keys())
print("== hours (L01..L09 data-hours) and hub split")
hours = {}
for f in sorted(glob.glob(P + "L0*.html")):
    m = re.search(r'data-hours="(\d+)"', open(f, encoding="utf-8").read())
    hours[f.split("/")[-1]] = int(m.group(1))
print(hours, "sum =", sum(hours.values()))
hub = open(P + "index.html", encoding="utf-8").read()
print(re.findall(r'data-hours-(?:lessons|project)="\d+"', hub))
print("== per-page anchors and counts")
for page in ("L04", "L05", "L06"):
    t = open(P + page + ".html", encoding="utf-8").read()
    print(page, "quiz items:", t.count('<li class="item"'), "problems:", len(re.findall(r'class="problem" id=', t)),
          "solutions:", t.count('<details class="solution"'), "misconceptions:", t.count('class="misconception"'),
          "dfn:", re.findall(r'<dfn id="([^"]+)"', t), "svg:", t.count("<svg"), "chart:", t.count('class="chart"'),
          "data-cite:", t.count("data-cite"), "mathrm{diag}:", t.count("mathrm{diag}"),
          "ellipsis-chars:", t.count("…"), "dots:", len(re.findall(r"\.\.\.", t)))
    cmds = Counter(re.findall(r"\\[A-Za-z]+", t))
    print("  registered macros used:", {c: n for c, n in cmds.items() if c in macros})
    print("  forward 'below' / 'stated below' in why-it-matters:",
          bool(re.search(r'why-it-matters">[^<]*(below|stated below)', t)))
print("== lab sections")
for page in ("L04", "L05", "L06"):
    t = open(P + page + ".html", encoding="utf-8").read()
    print(page, re.findall(r'<section class="lab" id="([^"]+)"', t), "main() bare calls in twins:")
for i in (4, 5, 6):
    tw = open(f"tests/labs/M3/lab-M3-L0{i}-1.py", encoding="utf-8").read()
    print(f"  twin L0{i}: last line {tw.strip().splitlines()[-1]!r}; seeded: {bool(re.search(r'default_rng\(', tw))}; "
          f"network imports: {bool(re.search(r'urllib|requests|socket|http', tw))}")
print("== cards by lesson and slice ids")
cards = json.load(open(P + "cards.json", encoding="utf-8"))
print("total", len(cards), dict(sorted(Counter(c["lesson"] for c in cards).items())))
print("slice ids L04-L06:", sum(1 for c in cards if c["lesson"] in ("L04", "L05", "L06")))
print("ids present c101,c102,c176:", [c["id"] for c in cards if c["id"] in ("M3-c101", "M3-c102", "M3-c176")])
print("grades on slice cards:", Counter(c.get("grade") for c in cards if c["lesson"] in ("L04", "L05", "L06")))
print("cite fields on slice cards:", sum(1 for c in cards if c["lesson"] in ("L04", "L05", "L06") and "cite" in c))
