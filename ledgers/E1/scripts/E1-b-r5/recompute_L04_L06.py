"""Round-5 independent recomputation for E1 slice b (L04-L06). Run with python -I."""
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

getcontext().prec = 60

def pc(a):  # L04 Example 2.4 closed form p*(a) = sqrt(1+a) - 1
    return (1 + a).sqrt() - 1

dp = 1 / (2 * D(121).sqrt())
print("dp/da at 120 =", dp, "1/22 =", D(1) / 22)
fe, ce = {}, {}
for h in (D(1), D("0.1"), D("0.01"), D("0.001")):
    fwd = (pc(D(120) + h) - pc(D(120))) / h
    cen = (pc(D(120) + h) - pc(D(120) - h)) / (2 * h)
    fe[h], ce[h] = abs(fwd - dp), abs(cen - dp)
    print("h", h, "forward_error", f"{float(fe[h]):.6e}", "central_error", f"{float(ce[h]):.6e}")
ks = [D(1), D("0.1"), D("0.01"), D("0.001")]
for i in range(3):
    print("forward ratio", ks[i], "/", ks[i + 1], f"{float(fe[ks[i]] / fe[ks[i+1]]):.5f}")
    print("central ratio", ks[i], "/", ks[i + 1], f"{float(ce[ks[i]] / ce[ks[i+1]]):.7f}")
print("Remark 3.3 fwd/central at h=0.01:", f"{float(fe[D('0.01')] / ce[D('0.01')]):.5f}")
lead_f = D("0.001") / 10648
lead_c = D("1e-6") / 2576816
print("Example 3.2 forward/leading at h=0.001:", f"{float(fe[D('0.001')] / lead_f):.8f}")
print("Example 3.2 central/leading at h=0.001 minus 1:", f"{float(ce[D('0.001')] / lead_c - 1):.3e}")
print("Example 3.2 at h=1: central/leading", f"{float(ce[D(1)] / (D(1) / 2576816)):.7f}", "forward/leading", f"{float(fe[D(1)] / (D(1) / 10648)):.5f}")
rise = (pc(D("121.2")) - pc(D(120))) / pc(D(120)) * 100
print("E2 exact percent change for a 1% rise in a:", f"{float(rise):.7f}", "p at 121.2:", f"{float(pc(D('121.2'))):.7f}")
print("L04 Example 2.4 elasticity (a/p)(dp/da) = 6/11 =", D(6) / D(11))

# L04 Problem R1 and M1 quick exact checks
print("R1 dp/da =", F(-1, 2), "check D_a/(S'-D_p) =", F(1) / (F(-3) - F(-1)))
print("M1 eps(10) =", F(-40, 60), " a/(2b) =", F(100, 8))

# L05 closed forms and Lerner index over the three cases
for a, b, c in ((120, 1, 20), (90, 3, 10), (200, 4, 5)):
    pm = F(a + b * c, 2 * b)
    q = a - b * pm
    lerner = (pm - c) / pm
    eps = -b * pm / q
    prof = (pm - c) * q
    print("L05 case", (a, b, c), "p_m", pm, "Q", q, "profit", prof,
          "Lerner", lerner, "1/|eps|", 1 / abs(eps), "gap to a/2b", pm - F(a, 2 * b),
          "profit closed form", prof == F((a - b * c) ** 2, 4 * b))

# L06 closed forms in the reference case and the iteration
a, b, c = 120, 1, 20
d = F(a - b * c)
print("L06 d", d, "Cournot each", d / 3, "total", 2 * d / 3, "fee", F(a + 2 * b * c, 3 * b),
      "profit each", d * d / (9 * b), "rounded half up to cents", int(F(d * d / (9 * b) + F(1, 2))))
print("L06 monopoly", d / 2, F(a + b * c, 2 * b), d * d / (4 * b))
print("L06 Bertrand h at 45 sharing", (45 - c) * (a - 45) / 2, "undercut limit", (45 - c) * (a - 45))
x, xs = F(0), []
for t in range(31):
    xs.append(x)
    x = max(F(0), (d - x) / 2)
print("L06 x_1, x_2 =", xs[1], xs[2], "first t with |x_t-d/3|<1e-6:",
      next(t for t in range(31) if abs(xs[t] - d / 3) < F(1, 10**6)),
      "gap at t=30:", xs[30] - d / 3)
print("L06 E1 check 2^24 vs 2^25 vs 100/3*1e6:", 2**24, 2**25, F(100, 3) * 10**6)
print("L06 Prop 4.1 diffs:", 2 * d / 3 - d / 2, d - 2 * d / 3, F(a + b * c, 2 * b) - F(a + 2 * b * c, 3 * b), F(a + 2 * b * c, 3 * b) - c,
      d * d / (4 * b) - 2 * d * d / (9 * b))
