"""Round 7: independent exact re-derivation of the numbers quoted on E4 card faces and backs (Fractions and floats, stdlib only)."""
import math
from fractions import Fraction as F

fails = []
n = 0


def check(label, got, want, tol=None):
    global n
    n += 1
    ok = (abs(float(got) - float(want)) <= tol) if tol is not None else (got == want)
    print(f"{'OK  ' if ok else 'FAIL'} {label}: got {got} want {want}")
    if not ok:
        fails.append(label)


# L01 (c011-c016, c221)
claim, other = (100, 40, 0, 250), (0, 60, 120, 30)
q = (F(1, 2), F(1, 3), F(1, 4), F(1, 5))
pi = (F(1, 8), F(3, 8), F(3, 8), F(1, 8))
val = lambda x, p: sum(a * b for a, b in zip(x, p))
check("c011 V(claim)", val(claim, q), F(340, 3))
check("c011 340/3 to 2dp", round(float(F(340, 3)), 2), 113.33, 1e-9)
check("c015 V(other)", val(other, q), 56)
comb = [2 * a - F(1, 2) * b for a, b in zip(claim, other)]
check("c012 V(2x-y/2)", val(comb, q), F(596, 3))
check("c012 2V(x)-V(y)/2", 2 * val(claim, q) - F(1, 2) * val(other, q), F(596, 3))
check("c013 E[claim]", val(claim, pi), F(235, 4))
check("c013 235/4 = 58.75", float(F(235, 4)), 58.75, 1e-12)
# L01 M1 (E3 solution) value 55/3 and 12.5
check("L01 M1 V", val((10, 0, 30), (F(1, 3), F(1, 5), F(1, 2))), F(55, 3))

# L02 Example 2.11 and Prop 2.9 (c029-c038)
P = (F(1, 2), F(1, 4), F(1, 4))
e1, e2 = (F(3), F(4), F(1)), (F(1), F(4), F(3))
E = tuple(a + b for a, b in zip(e1, e2))
check("c031 aggregate", E, (4, 8, 4))
qs = tuple(p / t for p, t in zip(P, E))
check("c031 q*", qs, (F(1, 8), F(1, 32), F(1, 16)))
th1 = sum(p * a / t for p, a, t in zip(P, e1, E))
check("c030 theta_1", th1, F(9, 16))
check("c030 theta_2", 1 - th1, F(7, 16))
x1 = tuple(th1 * t for t in E)
x2 = tuple((1 - th1) * t for t in E)
check("c032 x1", x1, (F(9, 4), F(9, 2), F(9, 4)))
check("c032 x2", x2, (F(7, 4), F(7, 2), F(7, 4)))
w1 = val(qs, e1)
check("c034 ratio agent1 = 1/w1", [P[s] / (x1[s] * qs[s]) for s in range(3)], [1 / w1] * 3)
check("c034 1/w1 = 16/9", 1 / w1, F(16, 9))
check("c034 1/w2 = 16/7", 1 / val(qs, e2), F(16, 7))
check("c038 cost of e1 at q*", w1, F(9, 16))
check("c037 v=(1,-1,0) value", val((1, -1, 0), qs), F(3, 32))
# Remark 2.6 at q=(2,1,1)
qq = (2, 1, 1)
w_a, w_b = val(qq, e1), val(qq, e2)
d1 = tuple(P[s] * w_a / qq[s] for s in range(3))
d2 = tuple(P[s] * w_b / qq[s] for s in range(3))
z = tuple(d1[s] + d2[s] - E[s] for s in range(3))
check("Remark 2.6 wealths", (w_a, w_b), (11, 9))
check("Remark 2.6 excess demand", z, (1, -3, 1))
check("Remark 2.6 q.z", val(qq, z), 0)
# M-series L02 quick check: M2 demand (3/4, 3/8, 3/2)
check("L02 M2 demand", tuple(F(1, 4) * 3 / 1 if s == 0 else (F(1, 4) * 3 / 2 if s == 1 else F(1, 2) * 3 / 1) for s in range(3)), (F(3, 4), F(3, 8), F(3, 2)))

# L03 Example 3.6 MRS (c046)
def mrs(x, s, t):
    return (P[s] / x[s]) / (P[t] / x[t])
check("c046 MRS1_12", mrs(x1, 0, 1), 4)
check("c046 MRS1_13", mrs(x1, 0, 2), 2)
check("c046 MRS1_23", mrs(x1, 1, 2), F(1, 2))
check("c046 MRS2_12", mrs(x2, 0, 1), 4)
check("c046 MRS2_13", mrs(x2, 0, 2), 2)
check("c046 MRS2_23", mrs(x2, 1, 2), F(1, 2))
check("c046 price ratios", (qs[0] / qs[1], qs[0] / qs[2], qs[1] / qs[2]), (4, 2, F(1, 2)))
# c049 R2 derivatives at eps=0
d_u1 = F(1, 2) * F(-1, 3) + F(1, 4) * 1
d_u2 = F(1, 2) * 1 + F(1, 4) * (-1)
check("c049 dU1", d_u1, F(1, 12))
check("c049 dU2", d_u2, F(1, 4))
check("c049 MRS endowment 8/3", (P[0] / e1[0]) / (P[1] / e1[1]), F(8, 3))

# L04 (c060-c073, c214-c228): ranks and attainability
def rank(M):
    rows = [list(map(F, r)) for r in M]
    r = 0
    ncol = len(rows[0])
    for col in range(ncol):
        piv = next((i for i in range(r, len(rows)) if rows[i][col] != 0), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][col] != 0:
                f = rows[i][col] / rows[r][col]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
    return r
A2 = [(1, 1, 1), (0, 1, 2)]
A4 = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 2, 3)]
check("c062 rank A2", rank(A2), 2)
check("c064 rank A4", rank(A4), 3)
check("c065 aug rank (1,2,3)", rank(A2 + [(1, 2, 3)]), 2)
check("c065 aug rank (0,0,1)", rank(A2 + [(0, 0, 1)]), 3)
check("c065 aug rank (5,0,0)", rank(A2 + [(5, 0, 0)]), 3)
check("c071 rank rows (1,1,1),(1,1,1),(0,1,2)", rank([(1, 1, 1), (1, 1, 1), (0, 1, 2)]), 2)
check("c072 (1,2,3) by (1,2,3,0)", tuple(sum(z[j] * A4[j][k] for j in range(4)) for z in [(1, 2, 3, 0)] for k in range(3)), (1, 2, 3))
t = F(7, 5)
check("c072 family (1-t,2-2t,3-3t,t) replicates", tuple(sum(z[j] * A4[j][k] for j in range(4)) for z in [(1 - t, 2 - 2 * t, 3 - 3 * t, t)] for k in range(3)), (1, 2, 3))
check("c218 kernel dim J-rank", 4 - rank(A4), 1)

# L05 (c090-c094, c219): fixed points and error ratios
def fp(al, be, vs, de):
    return (F(al) / (be + vs), F(-de) / (be + vs))
check("c090 fixed point base", fp(10, 2, F(1, 2), F(3, 4)), (4, F(-3, 10)))
check("c219 fixed point varsigma=2", fp(10, 2, 2, F(3, 4)), (F(5, 2), F(-3, 16)))
def psi(c, al, be, vs, de):
    return ((al - vs * c[0]) / be, -(vs * c[1] + de) / be)
path = [(F(0), F(0))]
for _ in range(8):
    path.append(psi(path[-1], 10, 2, F(1, 2), F(3, 4)))
check("c091 c0 path start", [str(p[0]) for p in path[:4]], ['0', '5', '15/4', '65/16'])
ts = fp(10, 2, F(1, 2), F(3, 4))
e0 = path[0][0] - ts[0]; e1_ = path[1][0] - ts[0]
check("c091 ratio -1/4", e1_ / e0, F(-1, 4))
p3 = [(F(0), F(0))]
for _ in range(3):
    p3.append(psi(p3[-1], 10, 2, 3, F(3, 4)))
check("c093 path varsigma=3", [str(p[0]) for p in p3], ['0', '5', '-5/2', '35/4'])
check("c093 ratio -3/2", (p3[2][0] - 2) / (p3[1][0] - 2), F(-3, 2))
check("c094 damped step", tuple((1 - F(4, 5)) * 0 + F(4, 5) * c for c in psi((F(0), F(0)), 10, 2, F(1, 2), F(3, 4))), (4, F(-3, 10)))
check("c094 weight 4/5", F(2) / (2 + F(1, 2)), F(4, 5))

# L06 (c118-c124, c220): base instance
sv2, se2, a, lam, su2 = F(1), F(1), F(1), F(1, 2), F(1, 4)
kappa = a * se2 / lam
seta2 = se2 + kappa ** 2 * su2
taueta = 1 / seta2
taubar = lam / se2 + (1 - lam) * taueta
ths = taubar / (1 / sv2 + taubar)
thu = kappa * ths
check("c118 kappa", kappa, 2)
check("c118 sig_eta2", seta2, 2)
check("c118 tau_bar", taubar, F(3, 4))
check("c118 theta_s", ths, F(3, 7))
check("c118 theta_u", thu, F(6, 7))
varp = ths ** 2 * (sv2 + se2) + thu ** 2 * su2
covvp = ths * sv2
check("L06 Part B var_p", varp, F(27, 49))
check("c119 slope b", covvp / varp, F(7, 9))
check("c119 Var(v|p)", sv2 - (covvp / varp) * covvp, F(2, 3))
vi = sv2 * se2 / (sv2 + se2)
xI = (F(1, 2) * 1 - ths * 1) / (a * vi)
check("c120 x_I at (1,0)", xI, F(1, 7))
bb = covvp / varp
xU = (bb * ths - ths) / (a * (sv2 - bb * covvp))
check("c220 x_U at (1,0)", xU, F(-1, 7))
check("c220 clearing", F(1, 2) * xI + F(1, 2) * xU, 0)
# alternative slope residual -9/85 (c123)
alt = F(1, 2)
varp2 = alt ** 2 * (sv2 + se2) + thu ** 2 * su2
cov2 = alt * sv2
bslope = cov2 / varp2
rv2 = sv2 - bslope * cov2
xU2 = (bslope * alt - alt) / (a * rv2)
check("c123 residual at (1,0), theta_s=1/2", F(1, 2) * 0 + F(1, 2) * xU2 - 0, F(-9, 85))
# c122 grid of 16
gS = [F(x) for x in (-1, 0, 1, 2)]
gU = [F(-1), F(0), F(1, 2), F(2)]
def resid(s, u):
    price = ths * s - thu * u
    vp = ths ** 2 * (sv2 + se2) + thu ** 2 * su2
    cv = ths * sv2
    b = cv / vp
    rv = sv2 - b * cv
    vI = sv2 * se2 / (sv2 + se2)
    mI = sv2 * s / (sv2 + se2)
    dI = (mI - price) / (a * vI)
    dU = (b * price - price) / (a * rv)
    return lam * dI + (1 - lam) * dU - u
zeros = sum(1 for s in gS for u in gU if resid(s, u) == 0)
check("c122 zero residuals of 16", zeros, 16)

# L07 (c141-c146): sweeps
def rho2(sd, lm=F(1, 2), a_=F(1)):
    kap = a_ * se2 / lm
    sig_eta2 = se2 + kap ** 2 * sd ** 2
    return sv2 / (sv2 + sig_eta2), sig_eta2
check("c142 rho2 sweep", [rho2(s)[0] for s in (F(1, 4), F(1, 2), F(1), F(2), F(4))], [F(4, 9), F(1, 3), F(1, 6), F(1, 18), F(1, 66)])
check("c144 rho2 lam sweep", [rho2(F(1, 2), l)[0] for l in (F(1, 4), F(1, 2), F(3, 4))], [F(1, 6), F(1, 3), F(9, 22)])
check("c145 rho2 a sweep", [rho2(F(1, 2), F(1, 2), x)[0] for x in (F(1, 2), F(1), F(2))], [F(4, 9), F(1, 3), F(1, 6)])
check("c140 rho2 tiny sd", rho2(F(1, 100))[0], F(2500, 5001))
check("c141 rho2 base", rho2(F(1, 2))[0], F(1, 3))
check("c143 var_p sd=1/4 model", (F(9, 19)) ** 2 * 2 + (F(18, 19)) ** 2 * F(1, 16), F(729, 1444))
check("c146 1/3 - 0.330625 in tol units", round((1 / 3 - 0.330625) / 0.02, 3), 0.135, 1e-9)
check("L07 E2 sigma_u", math.sqrt(F(1, 2)), math.sqrt(0.5), 1e-12)

# L08 (c151-c188, c222-c224)
def gain0(a_=2.0, vv=1.0, ee=1.0):
    return math.log(1 + vv / ee) / (2 * a_)
def gain1():
    return math.log(5 / 3) / 4
check("c180 G(0)=ln2/4", gain0(), math.log(2) / 4, 1e-15)
check("c180 G(0) to 6dp", round(gain0(), 6), 0.173287, 1e-12)
check("c222 G(1)=ln(5/3)/4 to 6dp", round(gain1(), 6), 0.127706, 1e-12)
check("c216 Emp3 tau_eta lam=1", F(1) / (1 + F(2) ** 2 * 1), F(1, 5))
check("Mech1 tau_eta", F(1) / (1 + F(4) * 1), F(1, 5))
check("c242 corr at lam=1/2 sigma_u=1", (F(1, 17)) / (1 + F(1, 17)), F(1, 18))
check("L08 Mech2 x*", (1 - F(1, 2)) / (3 * 2), F(1, 12))
check("L08 Mech2 exponent", -(F(1, 2)) ** 2 / (2 * 2), F(-1, 16))
check("L08 Mech3 1/sqrt5", round(1 / math.sqrt(5), 7), 0.4472136, 1e-12)
check("L08 Emp1 gap printed 1.83e-15 small", abs(1.83e-15) < 1e-13, True)
check("c183 gap at 0.12 >0 and 0.18 <0 sign", (0.12 <= gain1(), 0.18 >= gain0()), (True, True))
check("c223 slope diff", round(abs(0.1595 - 0.1605), 4), 0.001, 1e-9)

# L09 (c200-c211)
bets = 5 ** 6
check("c204 bets", bets, 15625)
check("c203 625", 5 * 5 ** 3, 625)
check("c200 g1(1)", F(-1 + 2, 2), F(1, 2))
check("c200 g2(1) mean of -x on {1,2,3}", F(1 + -2 + 2, 3), F(1, 3))
check("c205 trader1 0.4", 0.7 * 1 + 0.3 * -1, 0.4, 1e-12)
check("c205 trader2 0.2", -(0.4 * 1 + 0.6 * -1), 0.2, 1e-12)
nu1, nu2 = 0.7, 0.4
th = (nu1 + nu2) / 2
tt = th / (1 - th)
check("c211 trader1 receipt >0", nu1 - (1 - nu1) * tt > 0, True)
check("c211 trader2 receipt >0", (1 - nu2) * tt - nu2 > 0, True)

print(f"\nchecks {n}, failures {len(fails)}: {fails}")
