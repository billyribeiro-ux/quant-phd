"""Alternative correct implementation of lab 1 in integer cents with exact rational rounding."""
from fractions import Fraction
N = 10_000_000
def half_up(fr):
    m = (abs(fr) + Fraction(1, 2)).__floor__()
    return m if fr >= 0 else -m
def fx(c):
    return f"{'-' if c < 0 else ''}{abs(c)//100}.{abs(c)%100:02d}"
print("SIMULATED price paths, P_0 = 1.00; nominal debt 100000.00 dollars, fixed (A1)")
paths = {"falling": (100, 97, 94, 91, 88, 85), "rising": (100, 103, 106, 109, 112, 115)}
for name, ps in paths.items():
    print(f"Part A, path {name}, real debt in dollars by period:")
    for t, p in enumerate(ps):
        print(f"  t={t} price={fx(p)} real debt={fx(half_up(Fraction(N * 100, p)))}")
print("Part B, burden change from t=0 to t=5, percent of the period-0 real debt:")
for name, ps in paths.items():
    print(f"  path {name}: {fx(half_up(Fraction(100 * (ps[0] - ps[-1]), ps[-1]) * 100))}")
end_f = Fraction(N * 100, 85); end_r = Fraction(N * 100, 115)
print("Part C, period 5, falling path minus rising path, real debt in dollars:")
print(f"  difference: {fx(half_up(end_f - end_r))}")
