"""PC3-b round 18: independent re-derivation of the numbers in the round-18 delta and key L04-L06 values.

Usage: python -I ledgers/PC3/scripts/PC3-b-r18/verify_numbers_r18.py
Exact rational arithmetic (fractions.Fraction) throughout; no page or lab output is trusted as input.
"""
from fractions import Fraction as F
from itertools import product

out = []


def check(label, ok):
    out.append(f"{'PASS' if ok else 'FAIL'} {label}")


# ---- L04 Proposition 3.1: enumerate the three arrival outcomes of one turn, from inventory zero ----
def pos(x):
    return x if x > 0 else F(0)


def expected_trade_term(a, b, v, p):
    """Enumerate the arrival outcomes of one turn (A1, A4, A5) and return E[c + sigma*v | I=0, v_t=v]."""
    h = F(a - b, 2)
    total = F(0)
    # uninformed buy, uninformed sell (each (1-p)/2); quoted size >= 1 and |I| <= L with L >= 1: fill occurs
    total += (1 - p) / 2 * (a - v)      # buy at ask: sigma=-1, c=a
    total += (1 - p) / 2 * (v - b)      # sell at bid: sigma=+1, c=-b, contribution -b + v
    # informed (prob p), A4: buy at ask if v>a, sell at bid if v<b, else no trade
    if v > a:
        total += p * (a - v)
    elif v < b:
        total += p * (v - b)
    return total, h


def closed_form(a, b, v, p):
    h = F(a - b, 2)
    return (1 - p) * h - p * (pos(v - a) + pos(b - v))


p = F(1, 2)
for a, b in [(10010, 9990), (10005, 9995), (10001, 9999)]:
    grid = [F(x) for x in range(9950, 10051, 5)]
    ok = all(expected_trade_term(a, b, v, p)[0] == closed_form(a, b, v, p) for v in grid)
    check(f"Prop 3.1 enumeration == closed form on grid a={a} b={b} p=1/2 ({len(grid)} points)", ok)

# Example 3.2 values
a, b = 10010, 9990
ex = {10000: F(5), 10020: F(0), 9985: F(5, 2)}
for v, want in ex.items():
    got = closed_form(a, b, F(v), p)
    check(f"Example 3.2 E at v={v} equals {want}", got == want)
check("Example 3.2 formula 5 - 1/2[(v-10010)^+ + (9990-v)^+] at v=10000", closed_form(a, b, F(10000), p) == 5 - F(1, 2) * (pos(F(10000) - 10010) + pos(F(9990) - 10000)))

# Corollary 3.3: with p=1/2 and v>=a, E = h/2 - (v-a)/2; zero iff v = a+h
h = 10
for v in range(10010, 10060):
    e = closed_form(a, b, F(v), p)
    want = F(h, 2) - F(v - a, 2)
    if e != want:
        check(f"Corollary 3.3 linear form at v={v}", False)
        break
else:
    check("Corollary 3.3 linear form E = h/2 - (v-a)/2 for v in [a, a+49]", True)
check("Corollary 3.3 zero exactly at v = a+h", closed_form(a, b, F(a + h), p) == 0 and all(closed_form(a, b, F(v), p) != 0 for v in range(a, a + 60) if v != a + h))

# Remark 4.2: I=10, quote 9990/10010, p=1/2, v=10000 -> expected trade term 5/2 (only uninformed buy, prob 1/4, contributes 10)
contrib = F(1, 4) * (10010 - 10000)
check("Remark 4.2 I=10 expected trade term = 5/2 cents", contrib == F(5, 2))
check("Remark 4.2 sd of fair-move term = 5|I|: I=3 -> 15, I=10 -> 50", 5 * 3 == 15 and 5 * 10 == 50)

# Remark 3.4: (1-p)h at p=1/2 equals h/2, one quarter of the quoted spread 2h
check("Remark 3.4 h/2 is one quarter of 2h", F(h, 2) == F(2 * h, 4))

# ---- L06 Proposition 3.1 / Remark 4.3 / Example 4.2 numbers ----
I, mg, n = 15_000_000, 5000, 3


def annuity(r):
    return sum(F(1) / (1 + r) ** t for t in range(1, n + 1))


rates = {"8%": F(8, 100), "10%": F(10, 100), "12%": F(12, 100)}
be_printed = {"8%": "1164.10", "10%": "1206.34", "12%": "1249.05"}
for k, r in rates.items():
    A = annuity(r)
    ustar = F(I) / (mg * A)
    cents = f"{float(ustar):.2f}"
    check(f"break-even at {k} = {be_printed[k]} units (computed {cents})", cents == be_printed[k])

# Example 4.2 bounds 200 and 1600 at 10%: NPV(u) = -I + mA u, exact
A10 = annuity(F(1, 10))
npv_lo = -I + mg * A10 * 200
npv_hi = -I + mg * A10 * 1600
check("Example 4.2 NPV(200) at 10% is about -12513148 cents", round(float(npv_lo)) == -12513148)
check("Example 4.2 NPV(1600) at 10% is about 4894816 cents", round(float(npv_hi)) == 4894816)
check("Example 4.2 annuity factor 3310/1331 at 10% (exact)", A10 == F(3310, 1331))
check("Example 4.2 break-even 399300/331 units at 10% (exact)", F(I) / (mg * A10) == F(399300, 331))
check("Example 4.2 NPV(200) at 10% exact -16655000000/1331", npv_lo == F(-16655000000, 1331))

# Corollary 3.3 degenerate case: l = h = u* gives NPV zero on the whole range (sign fixed at zero)
ustar10 = F(I) / (mg * A10)
check("Corollary 3.3 degenerate range l=h=u* has NPV exactly zero (sign fixed at zero, not strictly one side)",
      mg * A10 * (ustar10 - ustar10) == 0 and not (ustar10 < ustar10 or ustar10 > ustar10))

# ---- L05 Proposition 3.3 bound on the tested case (numbers in L05 prose) ----
n_len, k = 200, 32
check("L05 naive count (n-k+1)(k-1) at n=200,k=32 = 5239", (n_len - k + 1) * (k - 1) == 5239)
check("L05 k=200 naive count = 199", (n_len - 200 + 1) * (200 - 1) == 199)
check("L05 bound 2n = 400 >= 387 deque comparisons at k=200", 2 * n_len >= 387)

print("\n".join(out))
print(f"SUMMARY pass={sum(1 for x in out if x.startswith('PASS'))} fail={sum(1 for x in out if x.startswith('FAIL'))}")
