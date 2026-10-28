"""Recheck the CF8 project page's lab outputs and the numbers its prose states (CF8-c r1, independent of the builder).

Usage: .venv/bin/python -I -W error ledgers/CF8/scripts/CF8-c-r1/recheck_project_labs.py
Reads course/modules/CF/CF8/project.html; prints one line per check with the observed value, and exits 1 on a mismatch.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGE = (ROOT / "course/modules/CF/CF8/project.html").read_text(encoding="utf-8")
PY = sys.executable
bad: list[str] = []


def check(label: str, ok: bool, observed: object) -> None:
    print(("PASS " if ok else "FAIL ") + label + f" -> {observed}")
    if not ok:
        bad.append(label)


def pre_expected(lab: str) -> str:
    section = PAGE.split(f'id="{lab}"', 1)[1]
    block = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section, re.S)
    assert block is not None
    return html.unescape(block.group(1)).strip()


def run(path: Path) -> str:
    out = subprocess.run([PY, "-I", "-W", "error", str(path)], capture_output=True, text=True, check=True)
    return out.stdout.strip()


# Lab 1 and Lab 3 twins: output equals the page's embedded expected block
lab1 = run(ROOT / "tests/labs/CF8/lab-CF8-project-1.py")
check("lab1 twin output equals page expected block", lab1 == pre_expected("lab-CF8-project-1"), "identical" if lab1 == pre_expected("lab-CF8-project-1") else "differs")
lab3 = run(ROOT / "tests/labs/CF8/lab-CF8-project-3.py")
check("lab3 twin output equals page expected block", lab3 == pre_expected("lab-CF8-project-3"), "identical" if lab3 == pre_expected("lab-CF8-project-3") else "differs")

# Lab 2: fill the blank with the rule of the page (shortfall, capped at availability) and with the uncapped version
lab2_src = (ROOT / "tests/labs/CF8/lab-CF8-project-2.py").read_text(encoding="utf-8")
ok_expr = "min(max(MINIMUM_CASH - before, 0), COMMITMENT - drawn)"
filled = Path("/tmp/cf8-v/c/lab2_filled.py")
filled.write_text(lab2_src, encoding="utf-8")
check("lab2 twin contains the capped draw expression", ok_expr in lab2_src, ok_expr)
no_cap = Path("/tmp/cf8-v/c/lab2_nocap.py")
no_cap.write_text(lab2_src.replace(ok_expr, "max(MINIMUM_CASH - before, 0)"), encoding="utf-8")
blank_src = PAGE.split('id="lab-CF8-project-2"', 1)[1].split("</pre>", 1)[0]
blanked = Path("/tmp/cf8-v/c/lab2_blank_page.txt")
check("page lab 2 has the blank ___ in place of the draw", "draw = ___" in blank_src, "draw = ___")
exp2 = pre_expected("lab-CF8-project-2")
check("lab2 capped version matches the page expected block", run(filled) == exp2, "match")
check("lab2 uncapped version also matches (commitment never binds in lab 2)", run(no_cap) == exp2, "match")

# Lab 1 interpretation: week 11 to 13 numbers and the required-commitment claim
C = dict(
    sales=[1_000_000] * 3 + [800_000] * 10,
    purch=[700_000] * 13,
    opex=[250_000] * 13,
)


def half_up(v: Fraction) -> int:
    import math

    return math.floor(v + Fraction(1, 2))


def wk(weekly: list[int], lag: int, w: int) -> Fraction:
    def day(d: int) -> Fraction:
        wk_ = 1 if d < 1 else (d - 1) // 7 + 1
        return Fraction(weekly[wk_ - 1], 7)

    return sum((day(d - lag) for d in range(7 * w - 6, 7 * w + 1)), Fraction(0))


def path(commit: int, capped: bool, lag_c: int = 45, lag_p: int = 30) -> list[tuple[int, int, int, int, int, int]]:
    cash, drawn = 150_000, 0
    out = []
    for w in range(1, 14):
        r = half_up(wk(C["sales"], lag_c, w))
        d = half_up(wk(C["purch"], lag_p, w) + C["opex"][w - 1])
        before = cash + r - d
        need = max(400_000 - before, 0)
        avail = commit - drawn
        draw = min(need, avail) if capped else need
        repay = 0 if need > 0 else min(before - 400_000, drawn)
        cash = before + draw - repay
        drawn += draw - repay
        head = cash + commit - drawn - 1_200_000
        out.append((r, d, draw, repay, cash, drawn, head))
    return out


cap = path(1_000_000, True)
free = path(1_000_000, False)
check("lab1 capped path equals free path (commitment never binds)", cap == free, "equal")
peak = max(x[5] for x in cap)
check("lab1 peak drawn is 314286 cents", peak == 314_286, peak)
check("lab1 week 13 headroom is -114286 cents", cap[-1][6] == -114_286, cap[-1][6])
check("lab1 week 11 draw is 14286 cents (142.86 dollars)", cap[10][2] == 14_286, cap[10][2])
same_at_peak = path(314_286, True)
flows = lambda p_: [x[:6] for x in p_]  # receipts, disbursements, draw, repay, cash, drawn: liquidity depends on the commitment
check("lab1 commitment at the peak 314286 gives the same draws, repayments and cash (required commitment claim)", flows(same_at_peak) == flows(cap), "same")
check("lab1 min liquidity is 1085714 cents (exemplar B threshold claim)", min(x[4] + 1_000_000 - x[5] for x in cap) == 1_085_714, min(x[4] + 1_000_000 - x[5] for x in cap))

# Lab 3 interpretation: binding week and shortfall
c3 = dict(sales=[1_000_000] * 5 + [700_000] * 8, purch=[700_000] * 13, opex=[250_000] * 13)
cash, drawn = 100_000, 200_000
binds = []
rows3 = []
for w in range(1, 14):
    r = half_up(wk(c3["sales"], 30, w))
    d = half_up(wk(c3["purch"], 20, w) + c3["opex"][w - 1])
    before = cash + r - d
    need = max(300_000 - before, 0)
    avail = 800_000 - drawn
    if need > avail:
        binds.append(w)
    draw = min(need, avail)
    repay = 0 if need > 0 else min(before - 300_000, drawn)
    cash = before + draw - repay
    drawn += draw - repay
    rows3.append((w, cash, drawn))
check("lab3 commitment binds only in week 13", binds == [13], binds)
short = max(max(300_000 - c, 0) for _, c, _ in rows3)
check("lab3 largest shortfall is 64286 cents", short == 64_286, short)
# five-day impacts by the day oracle: DSO window and DPO window
def cum(weekly: list[int], lag: int) -> Fraction:
    def day(d: int) -> Fraction:
        wk_ = 1 if d < 1 else (d - 1) // 7 + 1
        return Fraction(weekly[wk_ - 1], 7)

    return sum((day(k) for k in range(-300, 92 - lag)), Fraction(0))

dso = half_up(cum(c3["sales"], 25) - cum(c3["sales"], 30))
dpo = half_up(cum(c3["purch"], 20) - cum(c3["purch"], 25))
check("lab3 DSO five-day impact is 500000 cents (5000.00)", dso == 500_000, dso)
check("lab3 DPO five-day impact is 500000 cents (5000.00)", dpo == 500_000, dpo)

# Lab 1 exemplar A and B DSO five-day impact: days 47 to 51 at 800000 cents a week
imp = half_up(Fraction(5 * 800_000, 7))
check("lab1 five-day DSO impact 571429 cents (exemplar B 5714.29)", imp == 571_429, imp)

# rounding claim: truncation wrong exactly for 4, 5, 6 sevenths
wrong = [r for r in range(7) if int(Fraction(r, 7)) != half_up(Fraction(r, 7))]
check("truncation is wrong for 4, 5 and 6 sevenths of a cent only", wrong == [4, 5, 6], wrong)

print("RESULT", "PASS" if not bad else f"FAIL {bad}")
sys.exit(1 if bad else 0)
