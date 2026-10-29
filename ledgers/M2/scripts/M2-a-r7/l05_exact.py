"""Exact rational central differences for the three L05 functions at x = 3/2, h = 1/10000."""
from fractions import Fraction as F

X = F(3, 2)
H = F(1, 10000)
p = lambda x: (x**2 + 1) * x**3
q = lambda x: (x**2 + 1) / (x + 2)
c = lambda x: (x**2 + 1) ** 3
dp = lambda x: 2 * x * x**3 + (x**2 + 1) * 3 * x**2
dq = lambda x: (2 * x * (x + 2) - (x**2 + 1)) / (x + 2) ** 2
dc = lambda x: 6 * x * (x**2 + 1) ** 2
for name, f, df in [("product p", p, dp), ("quotient q", q, dq), ("composite c", c, dc)]:
    cd = (f(X + H) - f(X - H)) / (2 * H)
    err = abs(df(X) - cd)
    print(name, "analytic", float(df(X)), "central", float(cd), "exact abs err", float(err), f"{float(err):.4e}")
    print("   exact err rational (float repr):", float(err))
# leading term h^2 f'''/6 for p at 1.5
print("p''' at 1.5 =", 60 * float(X) ** 2 + 6, " h^2 p'''/6 =", float(H**2) * (60 * float(X) ** 2 + 6) / 6)
