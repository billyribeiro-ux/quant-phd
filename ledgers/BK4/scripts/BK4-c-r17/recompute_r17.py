"""Round 17 (BK4 slice c): independent recomputation of the numbers printed or quoted on project.html.
Usage: python -I recompute_r17.py <checkout-root>. Writes nothing; prints every check with its value."""
import html
import math
import random
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(sys.argv[1])
PAGE = (ROOT / "course/modules/BK/BK4/project.html").read_text(encoding="utf-8")
PY = str(ROOT / ".venv/bin/python")
ok = True


def check(name, got, want):
    global ok
    flag = "PASS" if got == want else "FAIL"
    ok = ok and got == want
    print(f"{flag} {name}: recomputed={got!r} page={want!r}")


# Reference instance of Labs 1-3: 40 losses from random.Random(1), randint(0, 120000)
rng = random.Random(1)
losses = [rng.randint(0, 120_000) for _ in range(40)]
check("largest loss of the 40 seeded scenarios (Lab 3 Part B prints 118151)", max(losses), 118151)
S = len(losses)
srt = sorted(losses)


def k_of(t):
    return -((-t * S) // 10_000)


def cover(M):
    return 10_000 * sum(1 for x in losses if x <= M) // S


for t, margin_want, k_want, below_want in ((9000, 105154, 36, 8750), (9500, 111074, 38, 9250), (9750, 117088, 39, 9500)):
    k = k_of(t)
    m = srt[k - 1]
    check(f"target {t}: k", k, k_want)
    check(f"target {t}: margin", m, margin_want)
    check(f"target {t}: cover at margin", cover(m), t)
    check(f"target {t}: cover one cent below", cover(m - 1), below_want)
    # brute force least integer margin reaching the target
    brute = next(M for M in range(0, max(losses) + 1) if cover(M) >= t)
    check(f"target {t}: brute-force least margin agrees", brute, margin_want)
check("exact position for 9550 bps times 40 scenarios (page: 191/5, i.e. 38.2)", Fraction(9550 * 40, 10_000), Fraction(191, 5))
check("exact position for 9500 bps times 40 scenarios (Exemplar B: 38.0)", Fraction(9500 * 40, 10_000), Fraction(38, 1))
check("k for 9550 bps (Lab 1: 39)", k_of(9550), 39)
check("Lab 1 margin for 9550 bps", srt[39 - 1], 117088)
check("cover at 117088 at 9550 target floor", cover(117088), 9750)
check("38 of 40 scenarios is 95.00 % (page: 95.00 %)", Fraction(38, 40) * 100, Fraction(9500, 100))
# Lab 1 layers and shares
margin_d, fund_d, cap = 50_000, 6_000, 20_000
loss = 80_000
a1 = min(loss, margin_d)
a2 = min(loss - a1, fund_d)
a3 = min(loss - a1 - a2, cap)
R = loss - a1 - a2 - a3
check("Lab 1 residual R", R, 4000)
funds = {1: 4000, 3: 5000, 4: 3000}
pool = sum(funds.values())
check("pool of survivors 1,3,4", pool, 12000)
shares = {m: R * f // pool for m, f in funds.items()}
check("Lab 1 floored shares", shares, {1: 1333, 3: 1666, 4: 1000})
left = R - sum(shares.values())
check("Lab 1 leftover cent", left, 1)
shares[1] += 1
check("Lab 1 survivor payments", shares, {1: 1334, 3: 1666, 4: 1000})
check("Exemplar B: 1333+1666+1000 is one cent short of 4000", 1333 + 1666 + 1000, 3999)
check("Exemplar B: 111074 less 105154 (page 5920)", 111074 - 105154, 5920)
check("Exemplar B: 9500 less 9000 bps (page 500)", 9500 - 9000, 500)
# Lab 3 part A rows
for L_, want_row in ((20_000, (20000, 0, 0, 0)), (55_000, (50000, 5000, 0, 0)), (70_000, (50000, 6000, 14000, 0)),
                     (80_000, (50000, 6000, 20000, 4000)), (100_000, (50000, 6000, 20000, 24000))):
    x1 = min(L_, margin_d)
    x2 = min(L_ - x1, fund_d)
    x3 = min(L_ - x1 - x2, cap)
    rr = L_ - x1 - x2 - x3
    check(f"Lab 3 part A layers at loss {L_}", (x1, x2, x3, rr), want_row)
check("Lab 3 part A uncovered at 100000", max(0, 24000 - pool), 12000)
# Lab 3 part C
for t, past_m, past_f in ((9500, 2, 2), (9000, 4, 2)):
    M = srt[k_of(t) - 1]
    check(f"Lab 3 part C target {t}: past margin", sum(1 for x in losses if x > M), past_m)
    check(f"Lab 3 part C target {t}: past default fund", sum(1 for x in losses if x > M + fund_d), past_f)
    check(f"Lab 3 part C target {t}: past CCP capital", sum(1 for x in losses if x > M + fund_d + cap), 0)
print("ALL PASS" if ok else "SOME FAIL")

# Lab numbers: run each project twin and compare stdout to the page's expected block
for n in (1, 2, 3):
    m = re.search(r'id="lab-BK4-project-%d".*?<pre class="expected"[^>]*>(.*?)</pre>' % n, PAGE, re.S)
    want = html.unescape(m.group(1)).rstrip("\n")
    twin = ROOT / f"tests/labs/BK4/lab-BK4-project-{n}.py"
    if n == 2:
        # the page runs the completed twin for the instant check (Rung 2 convention, FINAL-ARCHITECT-RULINGS 11)
        pass
    r = subprocess.run([PY, "-I", "-W", "error", str(twin)], capture_output=True, text=True)
    got = r.stdout.rstrip("\n")
    print(f"lab project-{n} twin exit={r.returncode} stdout == page expected block: {got == want}")
