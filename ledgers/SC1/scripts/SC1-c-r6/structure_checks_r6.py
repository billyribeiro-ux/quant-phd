"""Round-6 structural and card checks for SC1 slice c (L07, L08, their twins, and the L07/L08 cards).

Standard library only. Reads files from the checkout; writes nothing except the printed report.
"""

from __future__ import annotations

import collections
import html
import json
import re
import sys
from itertools import product  # noqa: F401
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
MOD = ROOT / "course/modules/SC/SC1"
TW = ROOT / "tests/labs/SC1"

for lesson in ("L07", "L08"):
    page = (MOD / f"{lesson}.html").read_text(encoding="utf-8")
    print(f"== {lesson}")
    print("  problems (class=problem):", page.count('class="problem" id='))
    print("  solutions (details.solution):", page.count('<details class="solution">'))
    print("  misconceptions:", page.count('class="misconception"'))
    print("  quiz items:", page.count('class="item"'))
    print("  labs:", re.findall(r'<section class="lab[^"]*" id="([^"]+)"', page))
    print("  hypothesis/interpretation:", page.count('class="hypothesis"'), page.count('class="interpretation"'))
    print("  data-files present:", "data-files" in page)
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', page, re.S)
    words = len(re.sub(r"<[^>]+>", "", m.group(1)).split())
    print("  why-it-matters tokens (markup stripped, approx):", words)
    print("  external src/href:", re.findall(r'(?:src|href)="(?:https?:|//)[^"]*"', page))
    print("  data-cite markup:", page.count("data-cite"))
    print("  banned phrases:", [p for p in ("TODO", "TBD", "lorem", "for brevity", "details omitted",
                                          "beyond the scope", "left as an exercise", "you can add more",
                                          "it is important to note", "studies show", "experts agree",
                                          "it is well known", "obviously", "clearly", "it can be shown")
                               if p.lower() in re.sub(r"<[^>]+>", " ", page).lower()])
    print("  process words (builder/verifier/fixer/round N/REQUEST/ledger):",
          re.findall(r"\b(builder|verifier|fixer|ledger|REQUEST\w*|round \d+)\b", page, re.I))

# notation: macros used on the two pages that are not KaTeX built-ins or registered macros
notation = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))
registered = set(notation["macros"].keys())
for lesson in ("L07", "L08"):
    page = (MOD / f"{lesson}.html").read_text(encoding="utf-8")
    cmds = sorted(set(re.findall(r"\\[A-Za-z]+", page)))
    custom = [c for c in cmds if c[1:][:1].isupper() and c not in registered]
    print(f"== {lesson} capitalised macros not registered:", custom)

# cards
cards = json.loads((MOD / "cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("== cards: total", len(cards), "dup ids", [k for k, v in collections.Counter(ids).items() if v > 1])
print("   dup fronts", [k[:60] for k, v in collections.Counter(c["front"] for c in cards).items() if v > 1])
sel = [c for c in cards if c["lesson"] in ("L07", "L08")]
print("   L07/L08 cards:", len(sel), "first", sel[0]["id"], "last", sel[-1]["id"])
allpages = (MOD / "L07.html").read_text(encoding="utf-8") + (MOD / "L08.html").read_text(encoding="utf-8")
allpages_plain = html.unescape(re.sub(r"<[^>]+>", " ", allpages))
for c in sel:
    nums = set(re.findall(r"\d+\.\d+|\d{2,}", c["back"]))
    missing = [n for n in nums if n not in allpages_plain and n not in allpages]
    if missing:
        print("   card", c["id"], "numbers not found in its lesson pages:", missing)
    if c.get("grade") in ("C", "D", "X", "B") and not c.get("basis"):
        print("   card", c["id"], "graded", c["grade"], "without basis")
print("   done")

print("== end")
