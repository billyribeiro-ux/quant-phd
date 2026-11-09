"""Static checks on the hub and L01-L03 pages (round 5): figure/data/image markers, h1 titles, hub lesson cards, hours."""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course/modules/E/E1"
for name in ("index.html", "L01.html", "L02.html", "L03.html"):
    text = (root / name).read_text(encoding="utf-8")
    print(name, "data-files|<svg|<img count:", len(re.findall(r"data-files|<svg|<img", text)))
for lid in ("L01", "L02", "L03"):
    text = (root / f"{lid}.html").read_text(encoding="utf-8")
    print(lid, "h1:", re.findall(r"<h1>(.*?)</h1>", text), "| eyebrow:", re.findall(r'class="eyebrow">(.*?)</p>', text)[:1])
index = (root / "index.html").read_text(encoding="utf-8")
print("hub eyebrow:", re.findall(r'class="eyebrow">(90 h.*?)</p>', index))
print("hub lesson card titles:", re.findall(r'card-title">(.*?)</span>', index))
print("hub data-hours:", re.findall(r'data-hours-[a-z]+="\d+"', index))
print("hub lesson kickers:", re.findall(r'card-kicker">(L0\d · \d+ h)</span>', index))
print("arithmetic: lessons 9 x 10 =", 9 * 10, "; total 90 + 30 =", 90 + 30, "; project share 30/120 =", round(100 * 30 / 120), "%")
