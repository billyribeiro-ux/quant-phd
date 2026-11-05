"""Structural facts for the E4 slice pages: why-it-matters word counts, section and item counts, data-hours."""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course/modules/E/E4"
for name in ("L01", "L02", "L03"):
    html = (root / f"{name}.html").read_text(encoding="utf-8")
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', html, re.S)
    text = re.sub(r"<[^>]+>", " ", m.group(1))
    text = re.sub(r"\\\((.*?)\\\)", r" \1 ", text)
    words = len(text.split())
    problems = re.findall(r'class="problem" id="([A-Z]\d)"', html)
    quiz_items = len(re.findall(r'<li class="item"', html))
    miscs = len(re.findall(r'<li class="misconception"', html))
    tiers = re.findall(r'data-tier="(\w+)"', html)
    dfns = re.findall(r'<dfn id="([^"]+)" data-concept="([^"]+)"', html)
    print(f"{name}: why_it_matters_words={words} problems={problems} quiz_items={quiz_items} misconceptions={miscs} tiers={tiers} dfn_with_concept={dfns}")
    print(f"   details_solution={len(re.findall(r'<details class=\"solution\"', html))} data-hours={re.search(r'data-hours=\"(\d+)\"', html).group(1)} lab_sections={len(re.findall(r'<section class=\"lab\"', html))}")
hub = (root / "index.html").read_text(encoding="utf-8")
print("hub objectives:", len(re.findall(r'<ol class="objectives">', hub)), "items:", len(re.findall(r'<li><strong>(Decompose|Solve|Prove|Decide|Derive|Compute|Write|Check|Measure)', hub)))
print("hub hours attrs:", re.findall(r'data-hours-(lessons|project)="(\d+)"', hub))
print("hub placement items:", len(re.findall(r'<li class="item"', hub)))
print("hub cards:", len(re.findall(r'class="card" href', hub)))
