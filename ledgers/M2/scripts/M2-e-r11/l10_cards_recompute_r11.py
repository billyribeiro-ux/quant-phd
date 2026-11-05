"""Recompute the numbers on the changed-lesson L10 cards (c139, c140, c141, c136, c138) with exact fractions."""
from fractions import Fraction as Fr
def lower_upper(f, a, b, n):
    d = (b - a) / n
    xs = [a + i * d for i in range(n + 1)]
    # f is monotone on [a, b] in both cases, so the inf/sup on each subinterval is at an endpoint
    lo = sum(min(f(xs[i]), f(xs[i + 1])) * d for i in range(n))
    up = sum(max(f(xs[i]), f(xs[i + 1])) * d for i in range(n))
    return lo, up
F = lambda x: x**3 - 2 * x
f = lambda x: 3 * x**2 - 2
for n in (1, 2, 4, 256):
    lo, up = lower_upper(f, Fr(0), Fr(1), n)
    print("c139 n", n, "U-L", up - lo, "=3/n?", up - lo == Fr(3, n))
lo, up = lower_upper(f, Fr(0), Fr(1), 256)
print("c139 n=256 L =", float(lo), "U =", float(up), "-1 between:", float(lo) < -1 < float(up))
g = lambda x: 1 / (1 + x) ** 2
for n in (1, 2, 4, 128):
    lo, up = lower_upper(g, Fr(0), Fr(1), n)
    print("c140 n", n, "U-L", up - lo, "=3/(4n)?", up - lo == Fr(3, 4 * n), "brackets 1/2:", lo <= Fr(1, 2) <= up)
h = 1e-6
x0 = 0.3
cd = ((x0 + h) / (1 + x0 + h) - (x0 - h) / (1 + x0 - h)) / (2 * h)
print("c141 central diff", f"{cd:.8f}", "f(0.3)", f"{1 / 1.3 ** 2:.10f}", "abs diff", abs(cd - 1 / 1.3 ** 2))
print("c136 integral 1/(1+x)^2 on [0,1] =", Fr(1,2), "F(1)-F(0) with F=x/(1+x):", Fr(1,2) - 0)
