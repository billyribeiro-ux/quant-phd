"""Round 10 independent recomputation of every number in the BK4 slice pages (hub, L01-L03).

Reads the printed expected blocks from the pages (parsed as text, not by importing the labs) and recomputes the
derived quantities with separate code. Also re-simulates the L03 seeded inputs with its own RNG sequence.
Usage: recompute_numbers.py <checkout-root>
"""

import html
import math
import random
import re
import sys
from fractions import Fraction
from pathlib import Path

root = Path(sys.argv[1]).resolve()
base = root / "course/modules/BK/BK4"


def expected_block(page: str, lab: str) -> str:
    text = (base / f"{page}.html").read_text(encoding="utf-8")
    section = re.search(rf'<section class="lab" id="{lab}".*?</section>', text, re.S).group(0)
    return html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section, re.S).group(1))


def check(label: str, got: object, want: object) -> None:
    print(f"{'PASS' if got == want else 'FAIL'} {label}: recomputed {got!r}, page {want!r}")


# ---- L01: payments parsed from Part A of the printed block
b1 = expected_block("L01", "lab-BK4-L01-1")
names = {"Bank A": 0, "Bank B": 1, "Bank C": 2}
pays = []
for m in re.finditer(r"payment\s+(\d+): (Bank \w) pays (Bank \w)\s+(\d+) cents", b1):
    pays.append((int(m.group(1)), names[m.group(2)], names[m.group(3)], int(m.group(4))))
check("L01 payment count", len(pays), 12)
bal = {0: 0, 1: 0, 2: 0}
net = {0: 0, 1: 0, 2: 0}
need = {0: 0, 1: 0, 2: 0}
for _, s, r, a in sorted(pays):
    bal[s] -= a
    bal[r] += a
    net[s] -= a
    net[r] += a
    for b in bal:
        need[b] = max(need[b], -bal[b])
debit = {b: max(0, -net[b]) for b in net}
check("L01 net positions", [net[0], net[1], net[2]], [379800, -1533900, 1154100])
check("L01 RTGS peak need", [need[0], need[1], need[2]], [112500, 1533900, 0])
check("L01 DNS net debit", [debit[0], debit[1], debit[2]], [0, 1533900, 0])
check("L01 sum of net positions", sum(net.values()), 0)
gross = sum(a for *_, a in pays)
check("L01 gross value cents", gross, 2841600)
moved = sum(debit.values())
check("L01 amount moved cents", moved, 1533900)
check("L01 ratio to four places", f"{moved / gross:.4f}", "0.5398")
check("L01 ratio digits", f"{moved / gross:.8f}", "0.53980152")
check("L01 share percent two places", f"{100 * moved / gross:.2f}", "53.98")
check("L01 Example 2.6 need A (dollars)", max(0, -min(0, -100, -100, -50)), 100)
# Example 2.6 and Remark 2.7 and misconception numbers
ex = {"A": [0, -100, -100, -50], "B": [0, 100, 20, 20], "C": [0, 0, 80, 30]}
check("L01 Example 2.6 needs", [max(0, -min(v)) for v in ex.values()], [100, 0, 0])
check("L01 Example 2.6 debits", [max(0, -v[-1]) for v in ex.values()], [50, 0, 0])
check("L01 Example 2.6 gross dollars", 100 + 80 + 50, 230)
rem = [0, 50, -50, -50]
check("L01 Remark 2.7 need A", max(0, -min(rem)), 50)
check("L01 M1 need", max(0, -min([0, 300, -200])), 200)
check("L01 M3 need and debit", (max(0, -min([0, 40, -30, -20])), max(0, 20)), (30, 20))
check("L01 R3 need", max(0, -min([0, -100, -100, 0])), 100)
check("L01 Q9 dollars", 2841600 // 100, 28416)

# ---- L02: trades parsed from the printed block
b2 = expected_block("L02", "lab-BK4-L02-1")
trades = [
    (int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))
    for m in re.finditer(r"trade (\d+): member (\d) owes member (\d)\s+(\d+) cents", b2)
]
check("L02 trade count", len(trades), 6)
rec = {i: 0 for i in range(1, 5)}
pay = {i: 0 for i in range(1, 5)}
for _, p, r, a in trades:
    pay[p] += a
    rec[r] += a
G = sum(a for *_, a in trades)
n = {i: rec[i] - pay[i] for i in range(1, 5)}
A = sum(max(0, v) for v in n.values())
check("L02 gross notional", G, 7596300)
check("L02 receivables sum", sum(rec.values()), G)
check("L02 net obligations", [n[1], n[2], n[3], n[4]], [-3627000, 1753300, 3340300, -1466600])
check("L02 sum net zero", sum(n.values()), 0)
check("L02 netted amount", A, 5093600)
check("L02 netted equals payers", A, sum(max(0, -v) for v in n.values()))
check("L02 reduction", G - A, 2502700)
check("L02 reduction bps floored", (10000 * (G - A)) // G, 3294)
check("L02 bps exact ratio", f"{10000 * (G - A) / G:.2f}", "3294.63")
check("L02 Ex2.4 bps", math.floor(10000 * Fraction(180, 230)), 7826)
check("L02 Ex2.4 bps decimal", f"{10000 * 180 / 230:.2f}", "7826.09")
check("L02 Ex2.4 netted", 20 + 30, 50)
check("L02 M1 n", [40 - 50, 50 - 70, 70 - 20, 20 - 40], [-10, -20, 50, -20])
check("L02 M1 bps", math.floor(10000 * Fraction(130, 180)), 7222)
check("L02 M2 bps", math.floor(10000 * Fraction(360, 460)), 7826)
check("L02 E3 members both", [i for i in range(1, 5) if rec[i] > 0 and pay[i] > 0], [1, 2, 4])
check("L02 E2 positive sum", 1753300 + 3340300, 5093600)
check("L02 Q9 dollars", 5093600 // 100, 50936)

# ---- L03: re-simulate the seeded inputs with an independent generator call order
rng = random.Random(2026)
im = {i: rng.randint(1000, 5000) for i in (1, 2, 3, 4)}
df = {i: rng.randint(100, 900) for i in (1, 2, 3, 4)}
capital = rng.randint(500, 2000)
check("L03 margins", [im[1], im[2], im[3], im[4]], [1487, 2308, 3058, 4896])
check("L03 default funds", [df[1], df[2], df[3], df[4]], [624, 762, 205, 328])
check("L03 capital", capital, 1730)
losses = [rng.randint(0, 3000) for _ in range(200)]
srt = sorted(losses)
for target, want_margin in ((9900, 2961), (9975, 2992)):
    k = math.ceil(Fraction(target * 200, 10000))
    check(f"L03 k for {target}", k, 198 if target == 9900 else 200)
    check(f"L03 sized margin {target}", srt[k - 1], want_margin)
    cov = lambda M: 10000 * sum(1 for x in losses if x <= M) // 200
    check(f"L03 cover at sized margin {target}", cov(srt[k - 1]), 9900 if target == 9900 else 10000)
    check(f"L03 cover one below {target}", cov(srt[k - 1] - 1), 9850 if target == 9900 else 9950)
    brute = min(M for M in range(max(losses) + 1) if cov(M) >= target)
    check(f"L03 brute force {target}", brute, want_margin)
check("L03 9975 sized margin is the largest loss", srt[-1], 2992)
above = sum(1 for x in losses if x > 2961)
check("L03 scenarios above 9900 margin", above, 2)
check("L03 losses above 9900 margin when 2961 is L(198)", srt[197], 2961)
# Part A3 scenario arithmetic from the printed inputs
dfsur = df[1] + df[2] + df[4]
check("L03 survivor DF total", dfsur, 1714)
check("L03 A3 surviving scenario loss", im[3] + df[3] + capital + dfsur // 2, 5850)
check("L03 A3 residual", 5850 - im[3] - df[3] - capital, 857)
check("L03 A3 half shares", [df[1] // 2, df[2] // 2, df[4] // 2], [312, 381, 164])
check("L03 A3 default fund scenario", (3160 - 3058, 3058), (102, 3058))
check("L03 A3 within margin loss", im[3] // 2, 1529)
check("L03 reach default fund loss", im[3] + df[3] // 2, 3160)
check("L03 E3 cover count", 9900 // 50, 198)

# Example 1.5 and Table rows
def wf(L, IM, DF, K, surv):
    a1 = min(L, IM)
    a2 = min(L - a1, DF)
    a3 = min(L - a1 - a2, K)
    Z = L - a1 - a2 - a3
    D = sum(surv.values())
    if Z >= D:
        return a1, a2, a3, dict(surv), Z - D
    x = {i: Z * v // D for i, v in surv.items()}
    left = Z - sum(x.values())
    for i in sorted(surv):
        if left and surv[i] > 0:
            x[i] += 1
            left -= 1
    return a1, a2, a3, x, 0

rows = {}
for L in (80, 120, 170, 180, 181, 200, 205, 300):
    rows[L] = wf(L, 100, 50, 30, {1: 40, 2: 60})
check("Ex1.5 rows margin/DF/CCP", [(rows[L][0], rows[L][1], rows[L][2]) for L in rows],
      [(80, 0, 0), (100, 20, 0), (100, 50, 20), (100, 50, 30), (100, 50, 30), (100, 50, 30), (100, 50, 30), (100, 50, 30)])
check("Ex1.5 survivors", [tuple(rows[L][3][i] for i in (1, 2)) for L in rows],
      [(0, 0), (0, 0), (0, 0), (0, 0), (1, 0), (8, 12), (10, 15), (40, 60)])
check("Ex1.5 uncovered", [rows[L][4] for L in rows], [0, 0, 0, 0, 0, 0, 0, 20])
check("Ex1.5 conservation", [sum(rows[L][:3]) + sum(rows[L][3].values()) + rows[L][4] for L in rows], list(rows))
r6 = wf(2, 0, 0, 0, {1: 1, 2: 1, 3: 1})
check("Ex1.6 residual 2", r6[3], {1: 1, 2: 1, 3: 0})
r5 = wf(1, 0, 0, 0, {1: 1, 2: 1, 3: 1})
check("Ex1.6 residual 1", r5[3], {1: 1, 2: 0, 3: 0})

# ---- Hub and L01-L03 small arithmetic
check("hub 110/1.1", round(110 / 1.1), 100)
check("hub 1+1/2+1/4", 1 + Fraction(1, 2) + Fraction(1, 4), Fraction(7, 4))
check("hub rung 1 min(120-100,50)", min(120 - 100, 50), 20)
check("hub hours table sum", 2 + 2 + 3 + 3 + 2 + 2 + 1, 15)
check("hub 15/50 percent", 100 * 15 / 50, 30.0)
check("hub 0.8 x 8", 0.8 * 8, 6.4)
check("hub 6/8 and 7/8 percent", (6 / 8 * 100, 7 / 8 * 100), (75.0, 87.5))
check("L03 M2 cover(4000)", math.floor(Fraction(10000 * 3, 4)), 7500)
check("L03 M2 k", math.ceil(Fraction(7500 * 4, 10000)), 3)
check("L03 M3 k 8001", math.ceil(Fraction(8001 * 5, 10000)), 5)
check("L03 R3 boundary", math.ceil(Fraction(9975 * 400, 10000)), 399)
check("L03 Q10 k", math.ceil(Fraction(9975 * 400, 10000)), 399)
check("L03 R2 k 9900 S100", math.ceil(Fraction(9900 * 100, 10000)), 99)
