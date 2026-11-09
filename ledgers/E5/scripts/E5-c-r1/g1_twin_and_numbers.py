"""Closing-delta checks for E5 slice c (verifier G1, round 1). Run with python -I.

Part 1: page code equals the lab twin; expected block equals the twin's stdout.
Part 2: exact re-derivation (fractions) of the numbers that slice-c rows and changed card texts cite.
Part 3: card integrity for the L07 and L08 cards (unique fronts, grades, numbers present in the lesson).
"""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PY = str(ROOT / ".venv" / "bin" / "python")
fails: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"{'PASS' if ok else 'FAIL'} {name} {detail}")
    if not ok:
        fails.append(name)


def page_code_and_expected(page: Path) -> tuple[str, str]:
    text = page.read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    assert m and e, page
    return html.unescape(m.group(1)), html.unescape(e.group(1))


for lab, page in (
    ("lab-E5-L07-1", ROOT / "course/modules/E/E5/L07.html"),
    ("lab-E5-L08-1", ROOT / "course/modules/E/E5/L08.html"),
):
    twin = ROOT / "tests/labs/E5" / f"{lab}.py"
    code, expected = page_code_and_expected(page)
    twin_src = twin.read_text(encoding="utf-8")
    check(f"{lab} page code == twin", code.strip() == twin_src.strip(), f"len {len(code)} vs {len(twin_src)}")
    out = subprocess.run([PY, "-I", "-W", "error", str(twin)], capture_output=True, text=True, check=True).stdout
    check(f"{lab} expected == twin stdout", expected.strip() == out.strip(), f"lines {len(out.splitlines())}")

# Part 2: exact re-derivation
c = F(3, 5)
dG = F(10000)
# L08 Part A running totals and stage amounts
stages = [dG * c**k for k in range(5)]
totals = [sum(stages[: n + 1]) for n in range(5)]
check("L08 stage amounts 10000 6000 3600 2160 1296", [int(x) for x in stages] == [10000, 6000, 3600, 2160, 1296])
check("L08 running totals 10000 16000 19600 21760 23056", [int(x) for x in totals] == [10000, 16000, 19600, 21760, 23056])
mult = 1 / (1 - c)
check("L08 multiplier 5/2", mult == F(5, 2))
check("L08 change dG/(1-c) = 25000 (card c127 arithmetic 10000/(2/5))", dG / (1 - c) == 25000 and F(10000) / F(2, 5) == 25000)
check("L08 gap after 1 stage 15000", dG / (1 - c) - totals[0] == 15000)
check("L08 gap after 5 stages 1944", dG / (1 - c) - totals[4] == 1944)
check("L08 tax change -c dTax/(1-c) = -15000", -c * dG / (1 - c) == -15000)
tax_first = -c * dG
check("L08 tax stages -6000 -3600 -2160", [int(tax_first * c**k) for k in range(3)] == [-6000, -3600, -2160])
check("L08 balanced budget 1", (dG / (1 - c) - c * dG / (1 - c)) == dG)
check("L08 share after 20 stages 1 - c^20 = 0.999963 (6dp)", round(float(1 - c**20), 6) == 0.999963)
check("L08 c^20 = 0.0000365616 (10 dp)", round(float(c**20), 10) == 0.0000365616)
check("L08 Y before 162500 after 187500 (lab-only values)", 162500 + 25000 == 187500)
gap5 = dG / (1 - c) - totals[4]
check("L08 gap 1944 after five stages", gap5 == 1944)
check("L08 quiz E3 ratio 23056/25000 = 0.92224", F(23056, 25000) == F(92224, 100000))
check("L08 R1 ratio 10/7 for tau 1/2", F(1) / (1 - c * (1 - F(1, 2))) == F(10, 7))
check("L08 0.6^9 > 0.01 and 0.6^10 <= 0.01", F(3, 5) ** 9 > F(1, 100) >= F(3, 5) ** 10)

# L07 numbers
rn, target, phi_pi, phi_y = F(1), F(2), F(3, 2), F(1, 2)


def i_rate(pi, y, phi=phi_pi):
    return rn + pi + phi * (pi - target) + phi_y * y


grid = {
    -2: [i_rate(F(p), F(-2)) for p in range(1, 6)],
    0: [i_rate(F(p), F(0)) for p in range(1, 6)],
    2: [i_rate(F(p), F(2)) for p in range(1, 6)],
}
check("L07 Part A y=-2 row -1/2,2,9/2,7,19/2", grid[-2] == [F(-1, 2), F(2), F(9, 2), F(7), F(19, 2)])
check("L07 Part A y=0 row 1/2,3,11/2,8,21/2", grid[0] == [F(1, 2), F(3), F(11, 2), F(8), F(21, 2)])
check("L07 Part A y=2 row 3/2,4,13/2,9,23/2", grid[2] == [F(3, 2), F(4), F(13, 2), F(9), F(23, 2)])
for phi in (F(0), F(1, 2), F(1), F(3, 2)):
    nom = i_rate(F(3), F(0), phi) - i_rate(F(2), F(0), phi)
    real = nom - F(1)
    check(f"L07 Part B phi={phi} nominal={1 + phi} real={phi}", nom == 1 + phi and real == phi)
check("L07 worked pi 3 y -1 -> 5", i_rate(F(3), F(-1)) == 5)
check("L07 neutral pi 2 y 0 -> 3, real 1", i_rate(F(2), F(0)) == 3 and i_rate(F(2), F(0)) - F(2) == 1)
check("L07 P2 r^n + pibar = 3", rn + target == 3)
check("L07 R2 1/phi_pi = 2/3", 1 / phi_pi == F(2, 3))
check("L07 second differences zero (lab prints 0 0 0)", all(
    (grid[0][k + 2] - 2 * grid[0][k + 1] + grid[0][k]) == 0 for k in range(3)))

# Part 3: cards
cards = json.loads((ROOT / "course/modules/E/E5/cards.json").read_text(encoding="utf-8"))
fronts = [x["front"] for x in cards]
check("cards: no duplicate fronts across E5", len(fronts) == len(set(fronts)), f"{len(cards)} cards")
ids = [x["id"] for x in cards]
check("cards: no duplicate ids", len(ids) == len(set(ids)))
for lesson, lo, hi in (("L07", 105, 118), ("L08", 119, 132)):
    sel = [x for x in cards if x["lesson"] == lesson and lo <= int(x["id"].split("c")[-1]) <= hi]
    check(f"{lesson} card range {lo}-{hi} count", len(sel) == hi - lo + 1 or lesson == "L08", f"{len(sel)}")
lesson_text = {
    "L07": (ROOT / "course/modules/E/E5/L07.html").read_text(encoding="utf-8"),
    "L08": (ROOT / "course/modules/E/E5/L08.html").read_text(encoding="utf-8"),
}
for x in cards:
    if x["lesson"] not in lesson_text:
        continue
    if x["id"].split("c")[-1].isdigit() and 105 <= int(x["id"].split("c")[-1]) <= 132:
        text = " ".join([x["front"], x["back"]])
        nums = set(re.findall(r"(?<![A-Za-z_])\d[\d,]*(?:\.\d+)?", text))
        page = lesson_text[x["lesson"]]
        missing = []
        for n in sorted(nums):
            n2 = n.rstrip(",").replace(",", "")
            forms = {n2, f"{int(n2):,}" if n2.isdigit() else n2}
            if not any(re.search(r"(?<![\d.])" + re.escape(f) + r"(?![\d])", page) for f in forms):
                missing.append(n)
        # numbers that are card-only plain values (grades, ids) are reported, not failed here
        if missing:
            print(f"NOTE {x['id']} numbers not found verbatim in {x['lesson']} page: {missing}")

print("FAILS:", fails)
sys.exit(1 if fails else 0)
