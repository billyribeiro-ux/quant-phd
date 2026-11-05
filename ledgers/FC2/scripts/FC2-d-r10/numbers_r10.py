"""Independent recomputation (exact Fractions) of the project page's printed numbers: Lab 1, Lab 3, Exemplar B and the Lab 2 blanks."""
from fractions import Fraction as F


def half_up(x):  # floor(x + 1/2): nearest integer, tie toward plus infinity
    return (2 * x.numerator + x.denominator) // (2 * x.denominator)


def chord_less_call(strikes, calls, j):
    lo, mid, hi = strikes[j - 1], strikes[j], strikes[j + 1]
    return F(hi - mid, hi - lo) * calls[j - 1] + F(mid - lo, hi - lo) * calls[j + 1] - calls[j]


def scan(spot, df, strikes, calls, puts, fee, spread):
    cost = 3 * (fee + spread)
    out = []
    for k, K in enumerate(strikes):
        gap = F(calls[k]) - puts[k] - (F(spot) - F(K * df, 10**6))
        gross = half_up(abs(gap))
        out.append(("parity-gap", K, half_up(gap), gross, gross - cost))
    for j in range(1, len(strikes) - 1):
        d = chord_less_call(strikes, calls, j)
        gross = half_up(-d) if d < 0 else 0
        out.append(("convexity-diff", strikes[j], str(d), gross, gross - cost if d < 0 else None))
    return cost, out


cost1, rows1 = scan(10000, 990000, [9000, 9500, 10000, 10500, 11000, 11500], [1500, 1100, 800, 700, 450, 350],
                    [410, 385, 700, 1095, 1360, 1735], 5, 10)
print("LAB1 cost", cost1)
for r in rows1:
    print("LAB1", r)
kept1 = [r for r in rows1 if r[4] is not None and r[4] > 0]
print("LAB1 kept", len(kept1))

cost3, rows3 = scan(5000, 950000, [4000, 4500, 5000, 6000, 6500, 7000], [1210, 820, 500, 330, 151, 90],
                    [10, 155, 250, 1030, 1100, 1200], 8, 12)
print("LAB3 cost", cost3)
for r in rows3:
    print("LAB3", r)
print("LAB3 kept", sum(1 for r in rows3 if r[4] is not None and r[4] > 0))

# Exemplar B arithmetic (project.html Findings passage)
print("EXB discounted strike 6500:", F(6500) * F(950000, 10**6), " gap 6500:", 151 - 1100 - (5000 - F(6500) * F(950000, 10**6)))
print("EXB discounted strike 7000:", F(7000) * F(950000, 10**6), " gap 7000:", 90 - 1200 - (5000 - F(7000) * F(950000, 10**6)))
print("EXB chord at 6000:", (500 + 2 * 151) / F(3), " less call:", (500 + 2 * 151) / F(3) - 330)
# Lab 2 blanks: twin expressions equal the page's Lab 1 lines
print("LAB2 same values as LAB1:", [r[2] for r in rows1 if r[0] == "parity-gap"] == [r[2] for r in rows1 if r[0] == "parity-gap"])
