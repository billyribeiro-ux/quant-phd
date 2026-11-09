"""Round-5 slice-a delta checks (run as: python3 -I checks_r5.py <checkout-root>).

Covers: hub structure counts, hours arithmetic, why-it-matters word counts, placement numbers,
skill-check arithmetic, changed-line ranges vs carried rows, References section locations,
L04 misconception numbering, and card-id/front uniqueness across the unit.
"""
import html
import json
import re
import subprocess
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

root = Path(sys.argv[1])
M2 = root / "course/modules/M/M2"
index = (M2 / "index.html").read_text(encoding="utf-8")
lines = index.splitlines()


def lr(a, b):
    return "\n".join(f"{i + 1}: {lines[i][:150]}" for i in range(a - 1, b))


print("== H01 structure")
print("objective items in section 'objectives' lines 40-60:",
      len(re.findall(r"<li>", "\n".join(lines[39:60]))))
print("lesson cards (class=lesson-card or data-lesson):",
      len(re.findall(r'data-lesson=|class="lesson-card"', index)))
print("ladder rungs:", len(re.findall(r'class="rung-title"', index)))
print("placement items:", len(re.findall(r'<li class="item"', index)),
      "data-skill items:", len(re.findall(r"data-skill", index)),
      "data-mastery:", re.findall(r'data-mastery="([^"]+)"', index))
print("explain blocks in placement:", len(re.findall(r'<div class="explain" hidden>', index)))
print("== H02 hours")
print(re.findall(r'data-hours-[a-z]+="[^"]+"', index))
proj = (M2 / "project.html").read_text(encoding="utf-8")
print("project:", re.findall(r'data-hours-project="[^"]+"', proj))
hours = {}
for f in sorted(M2.glob("L*.html")):
    hours[f.name] = re.findall(r'data-hours="([^"]+)"', f.read_text(encoding="utf-8"))
print("lesson data-hours values (distinct):", sorted({tuple(v) for v in hours.values()}), "files:", len(hours))
print("240 + 60 =", 240 + 60, "; 60/300 =", Fraction(60, 300), "=", float(Fraction(60, 300)) * 100, "%")
print("== H03 placement numbers")
print("0.8*8 =", 0.8 * 8, "; 6/8 =", 6 / 8, "; 7/8 =", 7 / 8)
print("== H08 skill-check arithmetic (exact, Fractions)")
h = Fraction(1, 10)


def f4(x):
    return x ** 4


d2 = (f4(1 + h) - 2 * f4(1) + f4(1 - h)) / h ** 2
print("second difference of x^4 at 1, h=0.1 (exact):", d2, "=", float(d2), "; 12 + 2h^2 =", 12 + 2 * h ** 2)
print("(1.1)^4 + (0.9)^4 - 2 =", Fraction(11, 10) ** 4 + Fraction(9, 10) ** 4 - 2)
c3 = ((1 + h) ** 3 - (1 - h) ** 3) / (2 * h)
print("central difference of x^3 at 1, h=0.1 (exact):", c3, "; 3 + h^2 =", 3 + h ** 2)
print("== X-HRS why-it-matters word counts")
for f in sorted(M2.glob("L0*.html")):
    t = f.read_text(encoding="utf-8")
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', t, re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))
    print(f.name, "why-it-matters words:", len(txt.split()))
print("== REF sections")
for f in sorted(M2.glob("L*.html")) + [M2 / "index.html"]:
    t = f.read_text(encoding="utf-8").splitlines()
    refs = [i + 1 for i, s in enumerate(t) if re.search(r'id="s9"|id="references"|>References<|h2 id="h-references"', s)]
    print(f.name, "references heading lines:", refs, "total lines:", len(t))
print("== L04 misconception numbering")
l04 = (M2 / "L04.html").read_text(encoding="utf-8").splitlines()
for i, s in enumerate(l04):
    if 'class="misconception"' in s:
        print("misconception block at line", i + 1, "->", re.sub(r"<[^>]+>", "", l04[i + 1])[:90])
print("== cards")
cards = json.loads((M2 / "cards.json").read_text(encoding="utf-8"))
print("cards:", len(cards), "dup ids:", [k for k, v in Counter(c["id"] for c in cards).items() if v > 1],
      "dup fronts:", [k for k, v in Counter(c["front"].strip().lower() for c in cards).items() if v > 1])
print("cards with no grade key:", [c["id"] for c in cards if "grade" not in c])
print("slice cards (L01-L06):", sum(1 for c in cards if c["lesson"] in {"L01", "L02", "L03", "L04", "L05", "L06"}))
print("== changed hunks vs slice (git diff -U0 edbb7aa8..HEAD)")
out = subprocess.run(["git", "-C", str(root), "diff", "-U0", "edbb7aa8..HEAD", "--",
                      "course/modules/M/M2/index.html", "course/modules/M/M2/L01.html",
                      "course/modules/M/M2/L02.html", "course/modules/M/M2/L03.html",
                      "course/modules/M/M2/L04.html", "course/modules/M/M2/L05.html",
                      "course/modules/M/M2/L06.html", "tests/labs/M2/"],
                     capture_output=True, text=True).stdout
print("\n".join(l for l in out.splitlines() if l.startswith(("+++", "@@"))))
