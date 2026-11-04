"""Round-4 re-derivation of the numbers on PC3 cards (slice d), with exact fractions and displayed-digit checks.

usage: python -I rederive_r4.py   (prints one line per check; ends with the count of mismatches)
"""
import math
from fractions import Fraction as F
from itertools import product

checks: list[tuple[str, object, object]] = []


def add(name: str, got: object, want: object) -> None:
    checks.append((name, got, want))


def disp(x: float, places: int) -> str:
    return f"{x:.{places}f}"


ln = math.log

# L01: Example 1.4, c007, c128, c129, c156, c009, c016, c013, c014, c130-c133
lo, hi = F(20) * 2 * 300, F(60) * 10 * 390
add("c007 lower bound", int(lo), 12000)
add("c007 upper bound", int(hi), 234000)
add("c128 ratio 19.5", hi / lo, F(39, 2))
add("c129 factor product 3*5*1.3", F(3) * 5 * F(13, 10), F(39, 2))
base = ln(19.5)
add("c156 ln 19.5 ten places", f"{base:.10f}", "2.9704144656")
t_sym = ln(F(40) * 10 * 390 / (F(20) * 2 * 300))
t_quote = ln(F(60) * 8 * 390 / (F(20) * 4 * 300))
t_min = ln(F(60) * 10 * 360 / (F(20) * 2 * 330))
add("c009 symbols reduction 0.4055", disp(base - t_sym, 4), "0.4055")
add("c009 quote reduction 0.9163", disp(base - t_quote, 4), "0.9163")
add("c009 minutes reduction 0.1754", disp(base - t_min, 4), "0.1754")
add("c009 quote share 30.8 percent", disp(100 * (base - t_quote) / base, 1), "30.8")
add("c009 minutes share 5.9 percent", disp(100 * (base - t_min) / base, 1), "5.9")
add("c016 ln 1.5", disp(ln(1.5), 4), "0.4055")
add("c016 ln(2.5/1.01)", disp(ln(2.5 / 1.01), 4), "0.9063")
add("c016 ln 2.5 < ln 3", ln(2.5) < ln(3), True)
for n, x, tag in ((10, F(1, 100), "x=1/100"), (10, F(1, 20), "x=1/20")):
    ex = (1 + x) ** n
    rem = ex - 1 - n * x
    bnd = F(n * (n - 1), 2) * (1 + x) ** (n - 2) * x * x
    if tag == "x=1/100":
        add("c130 remainder n=10 x=1/100", f"{float(rem):.10f}", "0.0046221254")
        add("c131 bound n=10 x=1/100", f"{float(bnd):.10f}", "0.0048728552")
        add("c013 (1+x)^10 exact", f"{float(ex):.10f}", "1.1046221254")
        add("c011 Example 1.7 ratio", disp(float(rem / bnd), 4), "0.9485")
    else:
        add("c014 exact (1.05)^10 to 4 places", disp(float(ex), 4), "1.6289")
        add("c014 miss 0.1289", disp(float(rem), 4), "0.1289")
        add("c133 bound n=10 x=1/20", f"{float(bnd):.10f}", "0.1662137374")
add("c132 remainder below bound", F(46221254, 10**10) < F(48728552, 10**10), True)

# L02 cards c021-c035
add("c023 P(both|at least one)=1/3", F(1, 4) / F(3, 4), F(1, 3))
add("c023 P(both|first heads)=1/2", F(1, 4) / F(1, 2), F(1, 2))
add("c026 P(first red)=12/20", F(12, 20), F(3, 5))
add("c027 P(second red)=12/20", F(12, 20), F(3, 5))
add("c028 P(both red)=6/20", F(6, 20), F(3, 10))
add("c029 P(second red|first blue)=3/4", F(3, 4), F(3, 4))
add("c031 goat-reveal prob and conditional", (F(1, 3) + F(1, 3)) == F(2, 3) and F(1, 3) / F(2, 3) == F(1, 2), True)
add("c033 P(bag1|red)=3/4", F(1, 2) * F(3, 4) / F(1, 2), F(3, 4))
add("c035 P(B)=29/100", F(3, 10) * F(1, 2) + F(7, 10) * F(1, 5), F(29, 100))
add("c035 P(A|B)=15/29", F(3, 10) * F(1, 2) / F(29, 100), F(15, 29))

# L03 cards c040-c061, c134-c136
add("c040 100*7/2", 100 * F(7, 2), 350)
add("c045 E[100g]-100", 100 * F(7, 2) - 100, 250)
add("c046 average 2300/6", F(250 + 250 + 300 + 400 + 500 + 600, 6), F(1150, 3))
add("c058 gain 100/3", F(1150, 3) - 350, F(100, 3))
add("c051 per-turn 25 and six turns 150", (F(1, 2) * 150 + F(1, 2) * -100, 6 * 25), (25, 150))
add("c054 2^6 sequences", 2**6, 64)
add("c055 four path totals mean 50", sum(max(a, a + b) for a, b in product((100, -100), repeat=2)) / F(4), 50)
add("c056 faces with 100f<250", [f for f in range(1, 7) if 100 * f < 250], [1, 2])
add("c059 stop payoff mean 350", 100 * F(7, 2), 350)
add("c061 fair turn mean 0", F(1, 2) * 100 + F(1, 2) * -100, 0)
add("c134 100 times E[face]", 100 * F(7, 2), 350)
add("L03 E2 625/8 - 150 = -575/8", F(625, 8) - 150, F(-575, 8))
add("c057/c058 1150/3 - 350 = 100/3", F(1150, 3) - 350, F(100, 3))

HORIZON = 6


def rule_value(outcomes, rule):
    def value(h):
        if len(h) == HORIZON or rule(h):
            return F(sum(h))
        return sum((p * value((*h, x)) for x, p in outcomes), F(0))
    return value(())


RULES = [
    ("play all", lambda h: False),
    ("first win", lambda h: bool(h) and h[-1] > 0),
    ("first loss", lambda h: bool(h) and h[-1] < 0),
    ("total>=100", lambda h: sum(h) >= 100),
    ("|total|>=200", lambda h: sum(h) >= 200 or sum(h) <= -200),
]
BIASED = ((150, F(1, 2)), (-100, F(1, 2)))
FAIR = ((100, F(1, 2)), (-100, F(1, 2)))
biased = {n: rule_value(BIASED, r) for n, r in RULES}
fair = {n: rule_value(FAIR, r) for n, r in RULES}
add("c051 biased play-all 150", biased["play all"], 150)
add("c052 biased first loss 1575/32", biased["first loss"], F(1575, 32))
add("c135 biased total>=100 575/8", biased["total>=100"], F(575, 8))
add("c136 biased |total|>=200 625/8", biased["|total|>=200"], F(625, 8))
add("c053 fair five rules all zero", all(v == 0 for v in fair.values()), True)
cont = F(sum(100 * g for g in range(1, 7)), 6) - 100
best = max(sum((F(100 * f) if bits[f - 1] else cont) for f in range(1, 7)) / 6 for bits in product((0, 1), repeat=6))
add("c047 best of 64 policies 1150/3", best, F(1150, 3))

# L04 cards c066-c083, c137-c141, c153-c154, c168
add("c070 E at v=10000", 5 - F(1, 2) * (max(10000 - 10010, 0) + max(9990 - 10000, 0)), 5)
add("c070 E at v=10020", 5 - F(1, 2) * (max(10020 - 10010, 0) + max(9990 - 10020, 0)), 0)
add("c070 E at v=9985", 5 - F(1, 2) * (max(9985 - 10010, 0) + max(9990 - 9985, 0)), F(5, 2))
add("c072 uninformed (1-p)h = h/2 = quarter of 2h", F(1, 2) * 10, F(2 * 10, 4))
add("c074 std 5|I| at 3 and 10 units", (5 * 3, 5 * 10), (15, 50))
add("c078 E at v=a+h is zero, terms h/2", (F(1, 2) * 10 - F(1, 2) * 10, F(1, 2) * 10), (0, 5))
add("c079 P&L 10010-10000", 10010 - 10000, 10)
add("c080 variance 25*10^2", 25 * 10**2, 2500)
add("c082 d=(1-p)h/p at p=3/5 h=10", (1 - F(3, 5)) * 10 / F(3, 5), F(20, 3))
add("c083 variance 25 at |I|=1 and 100 at |I|=2", (25 * 1, 25 * 4), (25, 100))
add("c067 mid 9990 gives 40, settlement 30", (-9950 + 9990, -9950 + 9980), (40, 30))
add("c067 turn-20 mid (9980+10000)/2", (9980 + 10000) / 2, 9990)
add("c075 nine grid values 9980..10020", len(range(9980, 10025, 5)), 9)
add("c137-c140 seed-0 cash flow, inventory, settlement, P&L", (-9950, 1, 9980, -9950 + 1 * 9980), (-9950, 1, 9980, 30))
add("c153 p=1/2 uninformed buy 1/4", F(1, 2) * F(1, 2), F(1, 4))

# L05 cards c084-c101, c142-c146
add("c087 (n-k+1)(k-1), n=200 k=8", (200 - 8 + 1) * (8 - 1), 1351)
add("c097 (200-32+1)(32-1)", (200 - 32 + 1) * (32 - 1), 5239)
add("c088 n^2/4 at k=101, n=200", (200 - 101 + 1) * (101 - 1), 10000)
add("c091 bound 2n at n=200", 2 * 200, 400)
add("c144 387 <= 400", 387 <= 400, True)
add("c093 (4,4,5)", (max(3, 1, 4), max(1, 4, 1), max(4, 1, 5)), (4, 4, 5))
add("c094 (5,5,1,3)", (max(2, 5), max(5, 1), max(1, 0), max(0, 3)), (5, 5, 1, 3))
add("c095 n-1 at n=5", 5 - 1, 4)

# L06 cards c102-c127, c147-c152
A = sum(F(1) / F(11, 10) ** t for t in range(1, 4))
add("c115 annuity A", A, F(3310, 1331))
add("c117 NPV at 200 units exact", -15000000 + 200 * 5000 * A, F(-16655000000, 1331))
add("c117 NPV at 200 units displayed", str(round(float(-15000000 + 200 * 5000 * A))), "-12513148")
add("c150 NPV at 1600 units displayed", str(round(float(-15000000 + 1600 * 5000 * A))), "4894816")
add("c123 NPV at 1200 units, two places", round(float(-15000000 + 1200 * 5000 * A), 2), -78888.05)
add("c147 break-even 399300/331", F(3000) / A, F(399300, 331))
add("c126 M3 break-even 33275/331", F(100000 * 1331, 400 * 3310), F(33275, 331))
add("c125 M2 NPV 500/121", -100 + F(60) / F(11, 10) + F(60) / F(121, 100), F(500, 121))
m_star = F(15000000 * 1331, 1600 * 3310)
add("c152 margin 3769.8 cents", disp(float(m_star), 1), "3769.8")
add("c127 margin factor 0.7540", disp(float(m_star) / 5000, 4), "0.7540")
add("c127 fall 24.6 percent", disp(100 * (1 - float(m_star) / 5000), 1), "24.6")
add("c151 average slope 21.2366", disp((1249.0469 - 1164.1005) / 4, 4), "21.2366")
be8 = 3000 / sum(1 / 1.08**t for t in range(1, 4))
be12 = 3000 / sum(1 / 1.12**t for t in range(1, 4))
add("c116 break-even 8 percent 1164.10", disp(be8, 2), "1164.10")
add("c148 break-even 12 percent 1249.05", disp(be12, 2), "1249.05")
add("c124 NPV at 1200 units positive at 8 percent", -15000000 + 1200 * 5000 * sum(1 / 1.08**t for t in range(1, 4)) > 0, True)
signs = [(-15000000 + 200 * 5000 * sum(1 / (1 + r) ** t for t in range(1, 4)) < 0,
          -15000000 + 1600 * 5000 * sum(1 / (1 + r) ** t for t in range(1, 4)) > 0) for r in (0.08, 0.10, 0.12)]
add("c149 negative at 200 and positive at 1600 at 8, 10, 12 percent", all(a and b for a, b in signs), True)
add("c114 Fermi range [200, 1600]", (2000 * 1 * F(1, 10), 4000 * 2 * F(1, 5)), (200, 1600))
add("c109 S/D = 4900/0.98 = 5000", F(4900) / F(98, 100), 5000)
add("c107 M1 payoff 5050-5000", 5050 - 5000, 50)
add("c119 payoffs 0 at 10000 and 100 at 10100", (10000 - 10000, 10100 - 10000), (0, 100))

bad = []
for name, got, want in checks:
    ok = got == want
    if not ok:
        bad.append(name)
    print(("OK  " if ok else "BAD ") + name + " | got " + repr(got) + " | want " + repr(want))
print("checks", len(checks), "mismatches", len(bad))
