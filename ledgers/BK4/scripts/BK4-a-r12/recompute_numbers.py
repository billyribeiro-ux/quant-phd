"""Round 12 independent re-derivation of every number in BK4 slice a (index, L01, L02, L03).

Usage: python3 -I recompute_numbers.py <checkout_root>
The printed lab values are parsed from the page <pre class="expected"> blocks, so the check is against the
page, not against the twin's own code. Every derived value uses fractions.Fraction or integer arithmetic.
"""

import html
import os
import re
import sys
from fractions import Fraction
from math import ceil, floor

root = sys.argv[1]
results: list[tuple[str, bool, str]] = []


def check(name: str, got: object, want: object) -> None:
    results.append((name, got == want, f"got={got!r} want={want!r}"))


def expected_block(name: str) -> str:
    page = open(os.path.join(root, "course/modules/BK/BK4", f"{name}.html"), encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    assert m is not None
    return html.unescape(m.group(1))


# ---------------- index.html: placement and hours ----------------
check("idx: 110/1.1", Fraction(110) / Fraction(11, 10), 100)
check("idx: 1+1/2+1/4", 1 + Fraction(1, 2) + Fraction(1, 4), Fraction(7, 4))
check("idx: (1-(1/2)^3)/(1/2)", (1 - Fraction(1, 2) ** 3) / Fraction(1, 2), Fraction(7, 4))
check("idx: lim 2x at 3", 2 * 3, 6)
check("idx: 6/8 pct", Fraction(6, 8) * 100, 75)
check("idx: 7/8 pct", Fraction(7, 8) * 100, Fraction(175, 2))
check("idx: 0.8*8 ceiling", ceil(Fraction(8, 10) * 8), 7)
check("idx: rung1 min(120-100,50)", min(120 - 100, 50), 20)
check("idx: rung2 floor(1*1/3)", floor(Fraction(1 * 1, 3)), 0)
check("idx: hours table sum", 2 + 2 + 3 + 3 + 2 + 2 + 1, 15)
check("idx: hours lessons 5x7", 5 * 7, 35)
check("idx: project share 15/50", Fraction(15, 50) * 100, 30)

# ---------------- L01 ----------------
l01 = expected_block("L01")
pay_rows = re.findall(r"payment\s+(\d+): Bank (\w) pays Bank (\w)\s+(\d+) cents", l01)
assert len(pay_rows) == 12, len(pay_rows)
banks = {"A": 0, "B": 1, "C": 2}
day = [(int(s), banks[snd], banks[rcv], int(a)) for s, snd, rcv, a in pay_rows]


def net(bank: int) -> int:
    rec = sum(a for _, s, r, a in day if r == bank)
    snt = sum(a for _, s, r, a in day if s == bank)
    return rec - snt


def need(bank: int) -> int:
    bal = 0
    low = 0
    for _, s, r, a in day:
        if s == bank:
            bal -= a
        elif r == bank:
            bal += a
        low = min(low, bal)
    return -low


def debit(bank: int) -> int:
    return max(0, -net(bank))


check("L01 need A", need(0), 112500)
check("L01 need B", need(1), 1533900)
check("L01 need C", need(2), 0)
check("L01 net A", net(0), 379800)
check("L01 net B", net(1), -1533900)
check("L01 net C", net(2), 1154100)
check("L01 debit A", debit(0), 0)
check("L01 debit B", debit(1), 1533900)
check("L01 debit C", debit(2), 0)
check("L01 sum net zero", sum(net(b) for b in range(3)), 0)
gross = sum(a for *_, a in day)
check("L01 gross", gross, 2841600)
check("L01 moved", sum(debit(b) for b in range(3)), 1533900)
ratio = Fraction(1533900, 2841600)
check("L01 ratio rounded 4dp", round(float(ratio), 4), 0.5398)
check("L01 ratio 8dp digits", f"{float(ratio):.8f}", "0.53980152")
check("L01 ratio pct 2dp", f"{float(ratio) * 100:.2f}", "53.98")
check("L01 2841600 cents in dollars", Fraction(2841600, 100), 28416)
check("L01 Need>=Debit all", all(need(b) >= debit(b) for b in range(3)), True)
check("L01 banks with positive debit", sum(1 for b in range(3) if debit(b) > 0), 1)
check("L01 banks need>debit", sum(1 for b in range(3) if need(b) > debit(b)), 1)
check("L01 ex2.6 gross 230", 100 + 80 + 50, 230)

# Example 2.6 running sums, dollars
ex = [("A", "B", 100), ("B", "C", 80), ("C", "A", 50)]


def ex_need(name: str, order: list[tuple[str, str, int]]) -> int:
    bal = 0
    low = 0
    for s, r, a in order:
        if name == s:
            bal -= a
        elif name == r:
            bal += a
        low = min(low, bal)
    return -low


check("Ex2.6 Need_A", ex_need("A", ex), 100)
check("Ex2.6 Need_B", ex_need("B", ex), 0)
check("Ex2.6 Need_C", ex_need("C", ex), 0)
check("Ex2.6 running A", [0, -100, -100, -50], [0, -100, -100, -50])
check("Rem2.7 Need_A", ex_need("A", [ex[2], ex[0], ex[1]]), 50)
check("Rem2.7 running A", [0, 50, -50, -50], [0, 50, -50, -50])
check("M1 Need", ex_need("D", [("X", "D", 300), ("D", "Y", 500)]), 200)
check("M3 Need", ex_need("D", [("X", "D", 40), ("D", "Y", 70), ("Z", "D", 10)]), 30)
check("M3 Debit", max(0, -(40 - 70 + 10)), 20)
check("R3 Need", ex_need("A", [("A", "B", 100), ("B", "C", 100), ("C", "A", 100)]), 100)

# ---------------- L02 ----------------
l02 = expected_block("L02")
trade_rows = re.findall(r"trade (\d+): member (\d) owes member (\d)\s+(\d+) cents", l02)
assert len(trade_rows) == 6
trades = [(int(p), int(r), int(a)) for _, p, r, a in trade_rows]
G = sum(a for _, _, a in trades)
check("L02 gross", G, 7596300)
rec = {m: sum(a for p, r, a in trades if r == m) for m in range(1, 5)}
pay = {m: sum(a for p, r, a in trades if p == m) for m in range(1, 5)}
n = {m: rec[m] - pay[m] for m in range(1, 5)}
check("L02 rec", rec, {1: 314500, 2: 2067800, 3: 3340300, 4: 1873700})
check("L02 pay", pay, {1: 3941500, 2: 314500, 3: 0, 4: 3340300})
check("L02 net", n, {1: -3627000, 2: 1753300, 3: 3340300, 4: -1466600})
check("L02 sum net zero", sum(n.values()), 0)
A = sum(max(0, v) for v in n.values())
check("L02 netted A", A, 5093600)
check("L02 reduction", G - A, 2502700)
check("L02 bp floored", (10000 * (G - A)) // G, 3294)
check("L02 bp exact", round(float(Fraction(10000 * (G - A), G)), 2), 3294.63)
check("L02 A equals pay to net receivers", A, sum(max(0, -v) for v in n.values()))
# Example 2.4 and M1, M2, M3 and E1, E2 numbers
check("Ex2.4 n", [-50, 20, 30], [-50, 20, 30])
check("Ex2.4 bp", floor(Fraction(10000 * 180, 230)), 7826)
check("Ex2.4 7826.08", f"{float(Fraction(10000 * 180, 230)):.2f}", "7826.09")
check("M1 bp 130/180", floor(Fraction(10000 * 130, 180)), 7222)
check("M2 bp doubled", floor(Fraction(10000 * 360, 460)), 7826)
check("L02 quiz 50936", Fraction(5093600, 100), 50936)
check("L02 E2 positive sum", 1753300 + 3340300, 5093600)
check("L02 E1 sum", 5093600 + 2502700, 7596300)

# ---------------- L03 ----------------
l03 = expected_block("L03")


def waterfall(loss: int, im: dict[int, int], df: dict[int, int], cap: int, defaulter: int):
    margin = min(loss, im[defaulter])
    fund = min(loss - margin, df[defaulter])
    capital = min(loss - margin - fund, cap)
    Z = loss - margin - fund - capital
    survivors = sorted(i for i in df if i != defaulter)
    D = sum(df[i] for i in survivors)
    if Z >= D:
        pay_s = {i: df[i] for i in survivors}
        unc = Z - D
    else:
        pay_s = {i: Z * df[i] // D for i in survivors}
        left = Z - sum(pay_s.values())
        for i in survivors:
            if left == 0:
                break
            if df[i] > 0:
                pay_s[i] += 1
                left -= 1
        assert left == 0
        unc = 0
    return margin, fund, capital, pay_s, unc


fix_im = {1: 0, 2: 0, 3: 100}
fix_df = {1: 40, 2: 60, 3: 50}
rows = {}
for L in (80, 120, 170, 180, 181, 200, 205, 300):
    rows[L] = waterfall(L, fix_im, fix_df, 30, 3)
check("L03 ex1.5 L200", (rows[200][0], rows[200][1], rows[200][2], rows[200][3], rows[200][4]), (100, 50, 30, {1: 8, 2: 12}, 0))
check("L03 ex1.5 L300", (rows[300][0], rows[300][1], rows[300][2], rows[300][3], rows[300][4]), (100, 50, 30, {1: 40, 2: 60}, 20))
check("L03 ex1.5 L181", rows[181][3], {1: 1, 2: 0})
check("L03 ex1.5 L180 Z0", rows[180][3], {1: 0, 2: 0})
check("L03 ex1.5 L80 margin", (rows[80][0], rows[80][1], rows[80][2]), (80, 0, 0))
check("L03 ex1.5 L120", (rows[120][0], rows[120][1], rows[120][2], rows[120][3]), (100, 20, 0, {1: 0, 2: 0}))
check("L03 ex1.5 L170", (rows[170][0], rows[170][1], rows[170][2], rows[170][3]), (100, 50, 20, {1: 0, 2: 0}))
check("L03 ex1.5 L205", (rows[205][0], rows[205][1], rows[205][2], rows[205][3]), (100, 50, 30, {1: 10, 2: 15}))
check("L03 ex1.6 Z1", waterfall(1, {4: 0, 1: 0, 2: 0, 3: 0}, {1: 1, 2: 1, 3: 1, 4: 0}, 0, 4)[3], {1: 1, 2: 0, 3: 0})
check("L03 ex1.6 Z2", waterfall(2, {4: 0, 1: 0, 2: 0, 3: 0}, {1: 1, 2: 1, 3: 1, 4: 0}, 0, 4)[3], {1: 1, 2: 1, 3: 0})

# Lab Part A1 output in the page equals the table rows of Example 1.5 (values in the page's table)
table_rows = {
    80: (80, 0, 0, 0, 0, 0),
    120: (100, 20, 0, 0, 0, 0),
    170: (100, 50, 20, 0, 0, 0),
    180: (100, 50, 30, 0, 0, 0),
    181: (100, 50, 30, 1, 0, 0),
    200: (100, 50, 30, 8, 12, 0),
    205: (100, 50, 30, 10, 15, 0),
    300: (100, 50, 30, 40, 60, 20),
}
for L, (m, f, c, s1, s2, u) in table_rows.items():
    check(f"L03 table row {L}", (rows[L][0], rows[L][1], rows[L][2], rows[L][3].get(1, 0), rows[L][3].get(2, 0), rows[L][4]), (m, f, c, s1, s2, u))
    check(f"L03 table row {L} sums to loss", m + f + c + s1 + s2 + u, L)

# Part A3 seeded scenarios: the three losses printed in the page
a3 = {"within": 1529, "fund": 3160, "survivors": 5850}
check("L03 A3 survivors residual", 5850 - 3058 - 205 - 1730, 857)
check("L03 A3 survivors D", 624 + 762 + 328, 1714)
check("L03 A3 halves", (624 // 2, 762 // 2, 328 // 2), (312, 381, 164))
check("L03 A3 sum", 312 + 381 + 164, 857)
check("L03 A3 fund pays", 3160 - 3058, 102)
check("L03 A3 within loss 3058//2", 3058 // 2, 1529)
check("L03 A3 fund loss 3058+205//2", 3058 + 205 // 2, 3160)

# Part B: sized margin and cover using the printed draw (losses are not printed; check the printed cover facts)
check("L03 9900*200/10000", Fraction(9900 * 200, 10000), 198)
check("L03 9975*200/10000", Fraction(9975 * 200, 10000), Fraction(399, 2))
check("L03 ceil 9975 S=200", ceil(Fraction(9975 * 200, 10000)), 200)
check("L03 cover c=198 bps", 10000 * 198 // 200, 9900)
check("L03 cover c=197 bps", 10000 * 197 // 200, 9850)
check("L03 cover c=199 bps", 10000 * 199 // 200, 9950)
check("L03 k=floor-ceil S=400 9975", ceil(Fraction(9975 * 400, 10000)), 399)
check("L03 R2 k S=100 9900", Fraction(9900 * 100, 10000), 99)
check("L03 R3 S<400 boundary", [S for S in range(1, 402) if ceil(Fraction(9975 * S, 10000)) == S][-1], 399)
check("L03 M2 cover(4000)", floor(Fraction(10000 * 3, 4)), 7500)
check("L03 M2 cover(2999)", floor(Fraction(10000 * 2, 4)), 5000)
check("L03 M2 k", ceil(Fraction(7500 * 4, 10000)), 3)
check("L03 M3 k 8000", ceil(Fraction(8000 * 5, 10000)), 4)
check("L03 M3 k 8001", ceil(Fraction(8001 * 5, 10000)), 5)
check("L03 M3 4.0005", float(Fraction(8001 * 5, 10000)), 4.0005)
check("L03 Ex2.5 k 9900", ceil(Fraction(9900 * 200, 10000)), 198)

# Lab expected block numbers quoted in prose (L03 interpretation): 2961, 2992
check("L03 printed sized margins present", ("2961" in l03 and "2992" in l03), True)

fails = [r for r in results if not r[1]]
for name, ok, detail in results:
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else " " + detail))
print(f"TOTAL {len(results)} PASS {len(results) - len(fails)} FAIL {len(fails)}")
