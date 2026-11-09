"""For each L01-L04 card, list numbers in its back and whether the number string occurs in the lesson HTML.

Fractions are checked as n/d and as LaTeX \\tfrac{n}{d} or \\tfrac nd forms. A miss is printed for manual reading.
"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course/modules/M/M4"
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))
texts = {n: (root / f"{n}.html").read_text(encoding="utf-8") for n in ("L01", "L02", "L03", "L04")}
misses = []
checked = 0
for c in cards:
    if c["lesson"] not in texts:
        continue
    lesson = texts[c["lesson"]]
    nums = set(re.findall(r"\d+(?:\.\d+)?(?:/\d+)?", c["back"]))
    for num in sorted(nums):
        if num in ("1", "0", "2", "3", "4", "5"):
            continue
        checked += 1
        ok = num in lesson
        if not ok and "/" in num:
            n, d = num.split("/")
            ok = bool(re.search(r"\\tfrac\{?%s\}?\{?%s\}?" % (n, d), lesson)) or (n + "/" + d) in lesson
        if not ok:
            misses.append((c["id"], c["lesson"], num))
print("numbers checked (excluding 0-5):", checked)
for m in misses:
    print("NOT FOUND VERBATIM:", m)
