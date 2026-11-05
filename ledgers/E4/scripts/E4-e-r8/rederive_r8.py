"""Round 8, slice e: independent exact and float re-derivation of every number that a card of E4 states.

Each check prints CHECK <name> <computed> <card or lesson value> <OK|MISMATCH>. Exact values use fractions.Fraction;
float checks use math. Nothing is imported from the course or the labs.
"""
import itertools
import math
from fractions import Fraction as F

rows = []


def check(name, got, want, tol=None):
    if tol is None:
        ok = got == want
    else:
        ok = abs(got - want) <= tol
    rows.append(ok)
    print(f"CHECK {name} computed={got} stated={want} {'OK' if ok else 'MISMATCH'}")


# ---------- L01 ----------
pi1 = [F(1, 8), F(3, 8), F(3, 8), F(1, 8)]
q1 = [F(1, 2), F(1, 3), F(1, 4), F(1, 5)]
x1 = [F(100), F(40), F(0), F(250)]
y1 = [F(0), F(60), F(120), F(30)]
val = lambda p, x: sum(a * b for a, b in zip(p, x))
check("L01 V(x) at prices", val(q1, x1), F(340, 3))
check("L01 V(y)", val(q1, y1), F(56))
comb = [2 * a - F(1, 2) * b for a, b in zip(x1, y1)]
check("L01 V(2x-y/2)", val(q1, comb), F(596, 3))
check("L01 2V(x)-V(y)/2", 2 * val(q1, x1) - F(1, 2) * val(q1, y1), F(596, 3))
check("L01 E x", val(pi1, x1), F(235, 4))
check("L01 340/3 float", round(float(F(340, 3)), 2), 113.33)
check("L01 235/4 float", float(F(235, 4)), 58.75)
check("L01 M1 V", F(10) * F(1, 3) + F(30) * F(1, 2), F(55, 3))
check("L01 M1 E", F(10) * F(1, 2) + F(30) * F(1, 4), F(25, 2))
check("L01 E2 security 3 pays 1 ... (value of e1 under q)", q1[0], F(1, 2))
check("L01 sum of prices (scale of q)", sum(q1), F(77, 60))
# P1 riskless claim value 0.2+0.3+0.1 is card arithmetic
check("L01 card 0.6", F(2, 10) + F(3, 10) + F(1, 10), F(6, 10))
check("L01 M2 V = q2*x2 (q2=1/2, x2=50)", F(1, 2) * 50, F(25))

# ---------- L02 ----------
pi = [F(1, 2), F(1, 4), F(1, 4)]
e1 = [F(3), F(4), F(1)]
e2 = [F(1), F(4), F(3)]
ebar = [a + b for a, b in zip(e1, e2)]
check("L02 ebar", ebar, [F(4), F(8), F(4)])
theta1 = sum(p * a / b for p, a, b in zip(pi, e1, ebar))
theta2 = sum(p * a / b for p, a, b in zip(pi, e2, ebar))
check("L02 theta1", theta1, F(9, 16))
check("L02 theta2", theta2, F(7, 16))
qs = [p / b for p, b in zip(pi, ebar)]
check("L02 q*", qs, [F(1, 8), F(1, 32), F(1, 16)])
check("L02 q*.ebar", sum(a * b for a, b in zip(qs, ebar)), F(1))
x1s = [theta1 * b for b in ebar]
x2s = [theta2 * b for b in ebar]
check("L02 x1*", x1s, [F(9, 4), F(9, 2), F(9, 4)])
check("L02 x2*", x2s, [F(7, 4), F(7, 2), F(7, 4)])
check("L02 w1 = q*.e1", sum(a * b for a, b in zip(qs, e1)), F(9, 16))
check("L02 budget1", sum(a * b for a, b in zip(qs, x1s)), F(9, 16))
check("L02 ratio agent1 pi/(x q)", [p / (x * q) for p, x, q in zip(pi, x1s, qs)], [F(16, 9)] * 3)
check("L02 ratio agent2 pi/(x q)", [p / (x * q) for p, x, q in zip(pi, x2s, qs)], [F(16, 7)] * 3)
check("L02 1/w2", 1 / theta2, F(16, 7))
# Remark 2.6 example at q=(2,1,1)
qq = [F(2), F(1), F(1)]
w1 = sum(a * b for a, b in zip(qq, e1))
w2 = sum(a * b for a, b in zip(qq, e2))
check("L02 Remark 2.6 wealths", (w1, w2), (F(11), F(9)))
d1 = [p * w1 / q for p, q in zip(pi, qq)]
d2 = [p * w2 / q for p, q in zip(pi, qq)]
z = [a + b - c for a, b, c in zip(d1, d2, ebar)]
check("L02 Remark 2.6 excess demand", z, [F(1), F(-3), F(1)])
check("L02 Remark 2.6 unweighted sum", sum(z), F(-1))
check("L02 Remark 2.6 q.z", sum(a * b for a, b in zip(qq, z)), F(0))
check("L02 M1 demand", [F(1, 2) * F(1, 2) / F(1, 4), F(1, 2) * F(1, 2) / F(1, 8)], [F(1), F(2)])
check("L02 misconception v", F(1, 8) - F(1, 32), F(3, 32))
check("L02 endowment cost", sum(a * b for a, b in zip(qs, e1)), F(9, 16))

# ---------- L03 ----------
mrs = lambda p, x, s, t: (p[s] / x[s]) / (p[t] / x[t])
xa = x1s
for s, t, want in [(0, 1, F(4)), (0, 2, F(2)), (1, 2, F(1, 2))]:
    check(f"L03 MRS1 {s}{t}", mrs(pi, xa, s, t), want)
    check(f"L03 MRS2 {s}{t}", mrs(pi, x2s, s, t), want)
    check(f"L03 price ratio {s}{t}", qs[s] / qs[t], want)
check("L03 endowment MRS12 agent1", mrs(pi, e1, 0, 1), F(8, 3))
check("L03 endowment MRS12 agent2", mrs(pi, e2, 0, 1), F(8))
d1ep = F(1, 2) * F(-1, 3) + F(1, 4) * 1
d2ep = F(1, 2) * 1 + F(1, 4) * (-1)
check("L03 R2 derivative agent1", d1ep, F(1, 12))
check("L03 R2 derivative agent2", d2ep, F(1, 4))
# grid counts
GRID = [F(k, 4) for k in range(5)]
ebar_l = ebar


def U(bundle):
    if any(b <= 0 for b in bundle):
        return -math.inf
    return sum(float(p) * math.log(float(b)) for p, b in zip(pi, bundle))


x1_eq = x1s
x2_eq = x2s
ue1, ue2 = U(x1_eq), U(x2_eq)
ref1, ref2 = U(e1), U(e2)
TOL = 1e-12
cnt_eq = 0
cnt_end = 0
for f in itertools.product(GRID, repeat=3):
    a1 = [fi * b for fi, b in zip(f, ebar_l)]
    a2 = [b - a for a, b in zip(a1, ebar_l)]
    for ref, (u1, u2) in [(0, (ue1, ue2)), (1, (ref1, ref2))]:
        v1, v2 = U(a1), U(a2)
        better = (v1 > u1 + TOL) or (v2 > u2 + TOL)
        worse = (v1 < u1 - TOL) or (v2 < u2 - TOL)
        if better and not worse:
            if ref == 0:
                cnt_eq += 1
            else:
                cnt_end += 1
check("L03 grid allocations", len(list(itertools.product(GRID, repeat=3))), 125)
check("L03 Pareto improvements of equilibrium on grid", cnt_eq, 0)
check("L03 Pareto improvements of endowment on grid", cnt_end, 2)

# ---------- L04 ----------
def rank(rows_):
    m = [[F(v) for v in r] for r in rows_]
    r = 0
    ncol = len(m[0])
    for c in range(ncol):
        piv = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c] / m[r][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return r


A2 = [[1, 1, 1], [0, 1, 2]]
A3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 2, 3]]
check("L04 rank incomplete", rank(A2), 2)
check("L04 rank complete", rank(A3), 3)
check("L04 augmented (1,2,3)", rank(A2 + [[1, 2, 3]]), 2)
check("L04 augmented (0,0,1)", rank(A2 + [[0, 0, 1]]), 3)
check("L04 augmented (5,0,0)", rank(A2 + [[5, 0, 0]]), 3)
check("L04 complete attains (5,0,0)", rank(A3 + [[5, 0, 0]]), 3)
check("L04 kernel dim J-rank", 4 - rank(A3), 1)
check("L04 kernel dim incomplete", 2 - rank(A2), 0)
check("L04 misc rows rank", rank([[1, 1, 1], [1, 1, 1], [0, 1, 2]]), 2)
check("L04 M1 rank", rank([[1, 2, 0], [2, 4, 0]]), 1)
check("L04 M3 rank", rank([[1, 2, 0], [0, 1, 1], [1, 3, 1], [2, 5, 1]]), 2)
check("L04 E3 rank", rank([[1, 1, 0], [0, 1, 1], [1, 2, 1]]), 2)
check("L04 (1,2,3) = 1e1+2e2+3e3", [1 * 1, 2, 3], [1, 2, 3])

# ---------- L05 ----------
al, be, vs, de = F(10), F(2), F(1, 2), F(3, 4)
c0s = al / (be + vs)
c1s = -de / (be + vs)
check("L05 base fixed point", (c0s, c1s), (F(4), F(-3, 10)))
Psi = lambda c: ((al - vs * c[0]) / be, -(vs * c[1] + de) / be)
c = (F(0), F(0))
path = [c[0]]
for _ in range(8):
    c = Psi(c)
    path.append(c[0])
check("L05 base c0 path", [str(x) for x in path[:6]], ["0", "5", "15/4", "65/16", "255/64", "1025/256"])
check("L05 ratio base", (path[2] - c0s) / (path[1] - c0s), F(-1, 4))
check("L05 E1 error k=5", abs(path[5] - c0s), F(1, 256))
check("L05 E1 error k=4", abs(path[4] - c0s), F(1, 64))
# varsigma=beta=2
al2, be2, vs2, de2 = F(10), F(2), F(2), F(3, 4)
c0e = al2 / (be2 + vs2)
check("L05 C fixed point c0", c0e, F(5, 2))
check("L05 C fixed point c1", -de2 / (be2 + vs2), F(-3, 16))
p2 = [F(0)]
cc = F(0)
for _ in range(6):
    cc = (al2 - vs2 * cc) / be2
    p2.append(cc)
check("L05 C path", [str(x) for x in p2], ["0", "5", "0", "5", "0", "5", "0"])
# varsigma=3 beta=2
vs3 = F(3)
c0l = al2 / (be2 + vs3)
check("L05 D fixed point", c0l, F(2))
check("L05 D fixed point c1", -de2 / (be2 + vs3), F(-3, 20))
p3 = [F(0)]
cc = F(0)
for _ in range(6):
    cc = (al2 - vs3 * cc) / be2
    p3.append(cc)
check("L05 D path", [str(x) for x in p3[:4]], ["0", "5", "-5/2", "35/4"])
check("L05 D error e3", p3[3] - c0l, F(27, 4))
check("L05 D ratio", (p3[2] - c0l) / (p3[1] - c0l), F(-3, 2))
c0M = F(12) / (F(3) + F(1)); c1M = -F(2) / (F(3) + F(1))
PsiM = lambda c: ((F(12) - F(1) * c[0]) / F(3), -(F(1) * c[1] + F(2)) / F(3))
n1 = PsiM((F(0), F(0)))
check("L05 M2 c0 fixed point", c0M, F(3))
check("L05 M2 c1 fixed point", c1M, F(-1, 2))
check("L05 M2 ratio c0", (n1[0] - c0M) / (F(0) - c0M), F(-1, 3))
check("L05 M2 ratio c1", (n1[1] - c1M) / (F(0) - c1M), F(-1, 3))
check("L05 E1 fraction ratio", F(-1, 4) * -4, F(1))

# ---------- L06 ----------
sv2 = F(1); se2 = F(1); a = F(1); lam = F(1, 2); su2 = F(1, 4)
tv = 1 / sv2; te = 1 / se2
kappa = a / (lam * te)
seta2 = se2 + kappa ** 2 * su2
taueta = 1 / seta2
taubar = lam * te + (1 - lam) * taueta
ths = taubar / (tv + taubar)
thu = kappa * ths
check("L06 Ex6.9 kappa", kappa, F(2))
check("L06 Ex6.9 seta2", seta2, F(2))
check("L06 Ex6.9 taubar", taubar, F(3, 4))
check("L06 Ex6.9 theta_s", ths, F(3, 7))
check("L06 Ex6.9 theta_u", thu, F(6, 7))
varp = ths ** 2 * (sv2 + se2) + thu ** 2 * su2
bslope = taueta / (ths * (tv + taueta))
VU = 1 / (tv + taueta)
check("L06 Ex6.9 slope b", bslope, F(7, 9))
check("L06 Ex6.9 VU", VU, F(2, 3))
check("L06 Ex6.9 Var p", varp, F(27, 49))
omega = sv2 / (sv2 + se2)
VI = sv2 * se2 / (sv2 + se2)
pp = F(1) * ths - F(1) * thu * 0
pval = ths * 1 - thu * 0
xI = (omega * 1 - pval) / (a * VI)
xU = (bslope * pval - pval) / (a * VU)
check("L06 xI at (1,0)", xI, F(1, 7))
check("L06 xU at (1,0)", xU, F(-1, 7))
# Alternative slope residual at (s,u)=(1,0): theta_s=1/2 theta_u=6/7
ta, tb = F(1, 2), F(6, 7)
pa = ta * 1 - tb * 0
Pa = pa
Cov = ta * sv2
Varp = ta ** 2 * (sv2 + se2) + tb ** 2 * su2
ba = Cov / Varp
VUa = sv2 - ba * Cov
xIa = (omega * 1 - pa) / (a * VI)
xUa = (ba * pa - pa) / (a * VUa)
check("L06 D residual at (1,0) alt slope", lam * xIa + (1 - lam) * xUa - 0, F(-9, 85))
# grid of 16 points, equilibrium residual zero
cnt0 = 0
for s_ in (-1, 0, 1, 2):
    for u_ in (-1, 0, F(1, 2), 2):
        s_ = F(s_); u_ = F(u_)
        p_ = ths * s_ - thu * u_
        xi = (omega * s_ - p_) / (a * VI)
        xu = (bslope * p_ - p_) / (a * VU)
        if lam * xi + (1 - lam) * xu - u_ == 0:
            cnt0 += 1
check("L06 Part C zero residuals on 16-point grid", cnt0, 16)
# M1-M3
k1 = a * se2 / lam
check("L06 M1 kappa (a=2)", F(2) * 1 / F(1, 2), F(4))
th_m = (F(3, 5)) / (1 + F(3, 5))
check("L06 M1 theta_s", th_m, F(3, 8))
check("L06 M1 theta_u", 4 * th_m, F(3, 2))
pm = F(3, 8) * 2 - F(3, 2) * 1
check("L06 M3 price", pm, F(-3, 4))
xim = (F(2) + F(3, 2)) / 2
check("L06 M3 xI", xim, F(7, 4))
Ym = pm / F(3, 8)
xum = (F(1, 5) * Ym - F(6, 5) * pm) / 2
check("L06 M3 xU", xum, F(1, 4))
check("L06 M3 clears", F(1, 2) * xim + F(1, 2) * xum, F(1))
check("L06 M2 Var p", (F(3, 8)) ** 2 * 2 + (F(3, 2)) ** 2 * F(1, 4), F(27, 32))
check("L06 M2 b", (F(3, 8)) / F(27, 32), F(4, 9))
check("L06 M2 Var(v|p)", 1 - F(4, 9) * F(3, 8), F(5, 6))
check("L06 M2 corr2", (F(3, 8)) ** 2 / F(27, 32), F(1, 6))
# E2 numbers
check("L06 E2 diff", 0.426617 - 3 / 7, -0.001954, tol=1e-6)
check("L06 E2 SE units", (0.426617 - 3 / 7) / (0.006497 / 3), -0.90, tol=0.01)
check("L06 E1 0.80 vs 7/9", (0.80 - 7 / 9) / 0.05, 0.44, tol=0.01)

# ---------- L07 ----------
def seta(sd):
    kap = F(1) / F(1, 2)  # a*se2/lam with a=1, lam=1/2 -> 2
    return F(1) + kap ** 2 * sd ** 2


def rho2(sd, lam_=F(1, 2), a_=F(1)):
    k = a_ * F(1) / lam_
    return F(1) / (F(1) + F(1) + k ** 2 * sd ** 2)


def varp(sd):
    k = F(2)
    tau_eta = 1 / (1 + k ** 2 * sd ** 2)
    tbar = F(1, 2) * 1 + F(1, 2) * tau_eta
    th = tbar / (1 + tbar)
    return th ** 2 * 2 + (k * th) ** 2 * sd ** 2


for sd, want_r, want_v in [(F(1, 4), F(4, 9), F(729, 1444)), (F(1, 2), F(1, 3), F(27, 49)), (F(1), F(1, 6), F(27, 32)),
                            (F(2), F(1, 18), F(729, 338)), (F(4), F(1, 66), F(35937, 4802))]:
    check(f"L07 rho2 sd={sd}", rho2(sd), want_r)
    check(f"L07 Var p sd={sd}", varp(sd), want_v)
check("L07 sd=1/100 rho2", rho2(F(1, 100)), F(2500, 5001))
check("L07 lam=1/4 rho2", rho2(F(1, 2), lam_=F(1, 4)), F(1, 6))
check("L07 lam=3/4 rho2", rho2(F(1, 2), lam_=F(3, 4)), F(9, 22))
check("L07 a=1/2 rho2", rho2(F(1, 2), a_=F(1, 2)), F(4, 9))
check("L07 a=2 rho2", rho2(F(1, 2), a_=F(2)), F(1, 6))
check("L07 M1 rho2 sd=1", rho2(F(1)), F(1, 6))
check("L07 M3 rho2", F(2) / (F(2) + 5), F(2, 7))
check("L07 E1 diff", F(1, 3) - 0.330625, 0.002708, tol=1e-6)
check("L07 E1 tolerance units", (1 / 3 - 0.330625) / 0.02, 0.135, tol=1e-3)
check("L07 E2 sigma_u^2", (F(1, 4) ** 0 * 0) + (F(1) / F(1, 4) * 0) + (F(3) - 1) / 4, F(1, 2))
check("L07 E2 sigma_u = 1/sqrt2", round(math.sqrt(0.5), 4), 0.7071)
check("L07 R2 chi", F(1) ** 2 * F(1) ** 4 / F(1, 2) ** 2, F(4))
check("L07 R2 sigma_u", math.sqrt(2 / 4), 1 / math.sqrt(2), tol=1e-12)
check("L07 benchmark", F(1) / (F(1) + F(1)), F(1, 2))
check("L07 sd=4 seta2", 1 + 4 * 16 * F(1), F(65))
check("L07 base rho2 = 1/3", rho2(F(1, 2)), F(1, 3))

# ---------- L08 ----------
a8 = 2.0
G = lambda lam: None  # placeholder
def gain(lam, var_u=1.0):
    if lam == 0.0:
        return math.log(1 + 1.0 / 1.0) / (2 * a8)
    tau_v, tau_e = 1.0, 1.0
    kap = a8 * 1.0 / lam
    tau_eta = 1.0 / (1.0 + kap * kap * var_u)
    A = lam * tau_e + (1 - lam) * tau_eta
    beta = A / (tau_v + A)
    bs = tau_e / (tau_v + tau_e)
    by = tau_eta / (tau_v + tau_eta)
    VI = 1 / (tau_v + tau_e)
    VU = 1 / (tau_v + tau_eta)
    varDI = (bs - beta) ** 2 * 2.0 + (kap * beta) ** 2 * var_u
    varDU = (by - beta) ** 2 * (1.0 + 1.0 / tau_eta)
    return math.log((1 + varDI / VI) / (1 + varDU / VU)) / (2 * a8)


def corr2(lam, var_u=1.0):
    kap = a8 / lam
    tau_eta = 1.0 / (1.0 + kap * kap * var_u)
    return tau_eta / (1.0 + tau_eta)


check("L08 G(0)", gain(0.0), math.log(2) / 4, tol=1e-12)
check("L08 G(1)", gain(1.0), math.log(5 / 3) / 4, tol=1e-12)
check("L08 G(0) printed", round(gain(0.0), 6), 0.173287)
check("L08 G(1) printed", round(gain(1.0), 6), 0.127706)
check("L08 G(0.5) printed", round(gain(0.5), 6), 0.158997, tol=1e-6)
check("L08 Corr2 at lam=1/2 unit variances", corr2(0.5), 1 / 18, tol=1e-12)
check("L08 G(1e-6)-G(0)", gain(1e-6) - gain(0.0), -6.25e-14, tol=1e-12)
check("L08 corr2 lam=1 printed", round(corr2(1.0), 6), 0.166667)


def bisect(cost):
    if cost >= gain(0.0):
        return 0.0, gain(0.0) - cost
    if cost <= gain(1.0):
        return 1.0, gain(1.0) - cost
    lo, hi = 0.0, 1.0
    while hi - lo > 1e-12:
        mid = (lo + hi) / 2
        if gain(mid) - cost > 0:
            lo = mid
        else:
            hi = mid
    lam_ = (lo + hi) / 2
    return lam_, gain(lam_) - cost


for cost, want in [(0.12, 1.0), (0.13, 0.965625410), (0.14, 0.815032329), (0.15, 0.657828572),
                   (0.16, 0.480567912), (0.17, 0.231615819), (0.18, 0.0)]:
    lam_, gap = bisect(cost)
    check(f"L08 lam* cost {cost}", round(lam_, 9), want, tol=1e-8)
    if 0.12 < cost < 0.18:
        check(f"L08 gap cost {cost} is ~0", abs(gap) < 1e-12, True)
check("L08 boundary gap 0.12", abs(bisect(0.12)[1]), 7.71e-3, tol=1e-5)
check("L08 boundary gap 0.18", abs(bisect(0.18)[1]), 6.71e-3, tol=1e-5)
check("L08 Corr2 at lam*(0.15)", round(corr2(bisect(0.15)[0]), 6), 0.088941, tol=1e-6)
check("L08 Corr2 at lam*(0.17)", round(corr2(bisect(0.17)[0]), 6), 0.013061, tol=1e-6)
check("L08 Emp3 G(1) closed form", gain(1.0), math.log(5 / 3) / 4, tol=1e-12)
# A part slope: b_y/beta with lam=0.5
lam5 = 0.5
kap5 = a8 / lam5
te5 = 1 / (1 + kap5 ** 2)
A5 = lam5 * 1 + (1 - lam5) * te5
beta5 = A5 / (1 + A5)
by5 = te5 / (1 + te5)
check("L08 b_y/beta at lam=0.5", round(by5 / beta5, 4), 0.1605, tol=1e-9)
# Emp 3 check of values
check("L08 Emp3 varDI", (0.5 - 0.5) ** 2 * 2 + 4 * 0.25, 1.0)
check("L08 Emp3 varDU", (1 / 6 - 0.5) ** 2 * 6, 2 / 3, tol=1e-12)

# ---------- L09 ----------
STATES = range(1, 7)
P1 = [{1, 2}, {3}, {4, 5, 6}]
P2 = [{1, 2, 3}, {4, 5}, {6}]
VALUES = (-2, -1, 0, 1, 2)
PRI = F(1, 6)


def cell(part, w):
    return next(c for c in part if w in c)


def post(part, w, rec):
    c = cell(part, w)
    return sum(F(rec[k]) for k in c) / len(c)


def meet_(w):
    reached = {w}
    fr = [w]
    while fr:
        cur = fr.pop()
        for part in (P1, P2):
            for o in cell(part, cur):
                if o not in reached:
                    reached.add(o)
                    fr.append(o)
    return reached


check("L09 meet(1)", sorted(meet_(1)), [1, 2, 3])
check("L09 meet(4)", sorted(meet_(4)), [4, 5, 6])
cnt_pos1 = cnt_pos1_nn = cnt_nn1 = cnt_nn_nonzero1 = 0
cnt_pos4 = cnt_pos4_nn = cnt_nn4 = cnt_nn_nonzero4 = 0
total = 0
for vals in itertools.product(VALUES, repeat=6):
    total += 1
    rec = dict(zip(STATES, vals))
    neg = {k: -v for k, v in rec.items()}
    for st, m, pos_c, pos_nn, nn_c, nn_nz in [
        (1, meet_(1), 0, 0, 0, 0), (4, meet_(4), 0, 0, 0, 0)]:
        g1 = post(P1, st, rec)
        g2 = post(P2, st, neg)
        if g1 > 0 and g2 > 0:
            if st == 1:
                cnt_pos1 += 1
            else:
                cnt_pos4 += 1
            nn = all(post(P1, w, rec) >= 0 and post(P2, w, neg) >= 0 for w in m)
            if nn:
                if st == 1:
                    cnt_pos1_nn += 1
                else:
                    cnt_pos4_nn += 1
        nn_all = all(post(P1, w, rec) >= 0 and post(P2, w, neg) >= 0 for w in m)
        if nn_all:
            nz = any(post(P1, w, rec) != 0 or post(P2, w, neg) != 0 for w in m)
            if st == 1:
                cnt_nn1 += 1
                cnt_nn_nonzero1 += nz
            else:
                cnt_nn4 += 1
                cnt_nn_nonzero4 += nz
check("L09 bets enumerated", total, 15625)
check("L09 strict both at state1", cnt_pos1, 500)
check("L09 strict both and nonneg on meet state1", cnt_pos1_nn, 0)
check("L09 nonneg on meet state1", cnt_nn1, 625)
check("L09 nonneg with nonzero posterior state1", cnt_nn_nonzero1, 0)
check("L09 strict both at state4", cnt_pos4, 500)
check("L09 strict both and nonneg on meet state4", cnt_pos4_nn, 0)
check("L09 nonneg on meet state4", cnt_nn4, 625)
check("L09 nonneg with nonzero posterior state4", cnt_nn_nonzero4, 0)
check("L09 Example 2.4 g1(1)", post(P1, 1, {1: -1, 2: 2, 3: -2, 4: -2, 5: -2, 6: -2}), F(1, 2))
check("L09 Example 2.4 g2(1)", post(P2, 1, {1: 1, 2: -2, 3: 2, 4: 2, 5: 2, 6: 2}), F(1, 3))
check("L09 Example 2.4 g1(3)", post(P1, 3, {1: -1, 2: 2, 3: -2, 4: -2, 5: -2, 6: -2}), F(-2))
check("L09 two-prior receipts", (F(7, 10) - F(3, 10), -(F(4, 10) - F(6, 10))), (F(4, 10), F(2, 10)))

print("SUMMARY checks", len(rows), "failures", rows.count(False))
