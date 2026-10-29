"""Independent recomputation for E1 slice c round 9 (stdlib only, exact Fractions)."""
from fractions import Fraction as F

# Round-9 delta numbers: L09 E2 share and 4-unit surplus (Lab 1 Part B market)
def public_surplus(g):
    def agg(x):
        return (1000 - 100 * x) + max(F(0), 600 - 200 * x)
    kink = F(3)
    pieces = [(F(0), min(g, kink))]
    if g > kink:
        pieces.append((kink, g))
    area = F(0)
    for a, b in pieces:
        area += (agg(a) + agg(b)) / 2 * (b - a)
    return area - 400 * g

vals = {n: public_surplus(F(n)) for n in range(0, 11)}
print("Part B surplus by integer q:", {k: str(v) for k, v in vals.items()})
print("argmax over 0..10:", max(vals, key=vals.get))
print("surplus at 4 units:", vals[4], "share of 2700 =", float(vals[4] / 2700), "percent", float(100 * vals[4] / 2700))
print("surplus at 7 units share:", float(vals[7] / 2700), "percent", float(100 * vals[7] / 2700))

# L09 E1: loss of 100-cent tax, b=10, a=1000, c=200
b = F(10)
q_t = F(1000 - 200 - 100, 10)
print("E1 q(100) =", q_t, " loss =", b / 2 * (q_t - 68) ** 2)

# L09 Part A: DWL = e^2/(2b)
print("Part A DWL e^2/(2b) =", F(120) ** 2 / (2 * b))

# L07 reference case a=120 b=1 c=20, d=100
d, bb = F(100), F(1)
W = lambda Q: (2 * d * Q - Q * Q) / (2 * bb)
Qm, Qc = d / 2, 2 * d / 3
print("Monopoly DWL", W(d) - W(Qm), " Cournot DWL", W(d) - W(Qc), " Cournot DWL as float", float(W(d) - W(Qc)))
print("Monopoly profit", (F(70) - 20) * Qm, " Card E1-c102 check")
print("Cournot DWL / W(d) =", (W(d) - W(Qc)) / W(d), " monopoly DWL / W(d) =", (W(d) - W(Qm)) / W(d))
print("CS shift (C - M) in d^2/b units:", F(2, 9) - F(1, 8), " PS shift:", F(1, 4) - F(2, 9), " W shift:", F(4, 9) - F(3, 8))

# L08 grid counts (lab output used; recomputed here)
X, Y = 8, 4
grid = [(x, y) for x in range(X + 1) for y in range(Y + 1)]
interior_diag = [(x, y) for (x, y) in grid if 0 < x < X and 0 < y < Y and y * X == x * Y]
print("grid size", len(grid), "interior diagonal", interior_diag)

# Card E1-c136 (L05): pi(p) = (a-bc)^2/(4b) - b(p-p_m)^2
a, c = F(120), F(20)
for bcoef in (F(1), F(2)):
    pm = (a + bcoef * c) / (2 * bcoef)
    for p in (F(30), F(55), F(70), F(90)):
        pi = (p - c) * (a - bcoef * p)
        form = (a - bcoef * c) ** 2 / (4 * bcoef) - bcoef * (p - pm) ** 2
        assert pi == form, (bcoef, p)
print("completing-the-square identity holds for sampled p and b in {1,2}")
