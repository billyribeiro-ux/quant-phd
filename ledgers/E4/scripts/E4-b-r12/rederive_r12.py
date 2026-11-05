"""Round-12 E4 slice b: exact re-derivation of the identities in the changed hunks (L04 row 7, L05 A2/Lemma 2.1/Prop 2.2/E2,
L06 Lemma 6.3/6.4 proofs, Prop 6.7, Cor 6.8, Example 6.9, M1-M3, R1, E1-E2, key-results rows). Exact Fractions, random inputs."""
import random
from fractions import Fraction as F

rng = random.Random(12)


def rnd() -> F:
    return F(rng.randint(1, 40), rng.randint(1, 20))


fails = []
n_checks = 0


def check(name, cond):
    global n_checks
    n_checks += 1
    if not cond:
        fails.append(name)


# L06 Lemma 6.3 (V_I, omega) and Lemma 6.4 (b, Var(v|p), V_U closed form), random exact parameters
for trial in range(300):
    sv2, se2, su2 = rnd(), rnd(), rnd()
    ts, tu = rnd() * rng.choice([1, -1]), rnd() * rng.choice([1, -1])
    if (ts, tu) == (0, 0):
        continue
    var_s = sv2 + se2
    omega = sv2 / var_s
    VI = sv2 * se2 / var_s
    check("omega*Var(s)=sv2", omega * var_s == sv2)
    check("VI=sv2(1-omega)", VI == sv2 * (1 - omega))
    check("omega/VI = 1/se2", omega / VI == 1 / se2)
    check("1/VI = tau_v+tau_e", 1 / VI == 1 / sv2 + 1 / se2)
    var_p = ts * ts * var_s + tu * tu * su2
    cov_vp = ts * sv2
    check("var_p>0", var_p > 0)
    b = cov_vp / var_p
    VU_def = sv2 - b * cov_vp
    VU_closed = sv2 * (ts * ts * se2 + tu * tu * su2) / var_p
    check("VU closed form (Lemma 6.4 proof)", VU_def == VU_closed)
    check("VU > 0", VU_closed > 0)
    check("var(e)=VU via expansion", sv2 - 2 * b * cov_vp + b * b * var_p == VU_def)

# L06 Example 6.9 base instance and M1-M3
sv2, se2, a, lam, su2 = F(1), F(1), F(1), F(1, 2), F(1, 4)
tv, te = 1 / sv2, 1 / se2
kappa = a * se2 / lam
seta2 = se2 + kappa * kappa * su2
taueta = 1 / seta2
taubar = lam * te + (1 - lam) * taueta
ths = taubar / (tv + taubar)
thu = kappa * ths
b = taueta / (ths * (tv + taueta))
VU = 1 / (tv + taueta)
check("ex6.9 kappa", kappa == 2)
check("ex6.9 seta2", seta2 == 2)
check("ex6.9 taueta", taueta == F(1, 2))
check("ex6.9 taubar", taubar == F(3, 4))
check("ex6.9 theta_s", ths == F(3, 7))
check("ex6.9 theta_u", thu == F(6, 7))
check("ex6.9 b", b == F(7, 9))
check("ex6.9 VU", VU == F(2, 3))
p = ths * 1 - thu * 0
VI = sv2 * se2 / (sv2 + se2)
xI = ((sv2 / (sv2 + se2)) * 1 - p) / (a * VI)
xU = (b * p - p) / (a * VU)
check("ex6.9 xI=1/7", xI == F(1, 7))
check("ex6.9 xU=-1/7", xU == F(-1, 7))
check("ex6.9 clears at (1,0)", lam * xI + (1 - lam) * xU == 0)
# M1
a, lam, su2 = F(2), F(1, 2), F(1, 4)
kappa = a * F(1) / lam
seta2 = 1 + kappa * kappa * su2
taueta = 1 / seta2
taubar = lam * 1 + (1 - lam) * taueta
ths = taubar / (1 + taubar)
thu = kappa * ths
check("M1 kappa 4", kappa == 4)
check("M1 seta2 5", seta2 == 5)
check("M1 taueta 1/5", taueta == F(1, 5))
check("M1 taubar 3/5", taubar == F(3, 5))
check("M1 theta_s 3/8", ths == F(3, 8))
check("M1 theta_u 3/2", thu == F(3, 2))
# M2
var_p = ths * ths * 2 + thu * thu * su2
cov = ths
bM2 = cov / var_p
VUM2 = 1 - bM2 * cov
corr2 = cov * cov / (1 * var_p)
check("M2 var_p 27/32", var_p == F(27, 32))
check("M2 b 4/9", bM2 == F(4, 9))
check("M2 VU 5/6", VUM2 == F(5, 6))
check("M2 VU = 1/(tv+taueta)", VUM2 == 1 / (1 + taueta))
check("M2 corr2 1/6", corr2 == F(1, 6))
# M3
s, u = F(2), F(1)
pM3 = ths * s - thu * u
xI = (1 * s - (1 + 1) * pM3) / a
Y = pM3 / ths
xU = (taueta * Y - (1 + taueta) * pM3) / a
check("M3 price -3/4", pM3 == F(-3, 4))
check("M3 xI 7/4", xI == F(7, 4))
check("M3 Y -2", Y == -2)
check("M3 xU 1/4", xU == F(1, 4))
check("M3 clears", lam * xI + (1 - lam) * xU == u)
# R1 limit identities at lam small: Corr^2 = sv2/(sv2+seta2) for random params
for trial in range(100):
    sv2, se2, a, su2 = rnd(), rnd(), rnd(), rnd()
    lam = rnd() / 50 + F(1, 10000)
    if lam >= 1:
        continue
    kappa = a * se2 / lam
    seta2 = se2 + kappa * kappa * su2
    taueta = 1 / seta2
    taubar = lam / se2 + (1 - lam) * taueta
    ths = taubar / (1 / sv2 + taubar)
    thu = kappa * ths
    var_p = ths * ths * (sv2 + se2) + thu * thu * su2
    corr2 = (ths * sv2) ** 2 / (var_p * sv2)
    check("R1 corr2 formula", corr2 == sv2 / (sv2 + seta2))
    check("R1 var_p = ths^2(sv2+seta2)", var_p == ths * ths * (sv2 + seta2))
# Prop 6.7 uniqueness and existence: clearing identity at random (s,u) for closed-form theta
for trial in range(100):
    sv2, se2, a, su2, lam = rnd(), rnd(), rnd(), rnd(), F(rng.randint(1, 9), 10)
    te, tv = 1 / se2, 1 / sv2
    kappa = a * se2 / lam
    seta2 = se2 + kappa * kappa * su2
    taueta = 1 / seta2
    taubar = lam * te + (1 - lam) * taueta
    ths = taubar / (tv + taubar)
    thu = kappa * ths
    for s_, u_ in [(F(0), F(0)), (F(1), F(0)), (F(0), F(1)), (F(3), F(-2))]:
        p_ = ths * s_ - thu * u_
        xI = (te * s_ - (tv + te) * p_) / a
        Y = p_ / ths
        xU = (taueta * Y - (tv + taueta) * p_) / a
        check("Prop6.7 clearing identity", lam * xI + (1 - lam) * xU == u_)

# L05: Lemma 2.1, Prop 2.2 fixed point, Lemma 3.1, Prop 3.3 damped factor, at random exact parameters
for trial in range(200):
    al, be, de = rnd(), rnd(), rnd()
    vs = rnd() * rng.choice([1, 0])
    c0s = al / (be + vs)
    c1s = -de / (be + vs)
    check("P2.2 c0 fixed", (al - vs * c0s) / be == c0s)
    check("P2.2 c1 fixed", -(vs * c1s + de) / be == c1s)
    nu = be / (be + vs)
    check("P3.3 factor zero", 1 - nu * (1 + vs / be) == 0)
    c0 = F(rng.randint(-9, 9), 3)
    e0 = c0 - c0s
    e1 = (al - vs * c0) / be - c0s
    check("L3.1 ratio", e1 == -(vs / be) * e0)
# L05 base instance and E2, E3, M1, M2, M3, E1, R1 numbers
al, be, vs, de = F(10), F(2), F(1, 2), F(3, 4)
c0s, c1s = al / (be + vs), -de / (be + vs)
check("L05 base c0*=4", c0s == 4)
check("L05 base c1*=-3/10", c1s == F(-3, 10))
path = [F(0)]
for _ in range(8):
    path.append((al - vs * path[-1]) / be)
check("L05 base c0 path 15/4 at k2", path[2] == F(15, 4))
check("L05 base c0 path 1025/256 at k5", path[5] == F(1025, 256))
check("E1 e5 = 4/1024", (path[5] - c0s) == F(1, 256))
# E2: varsigma = beta = 2
vs2, be2 = F(2), F(2)
p2 = [F(0)]
for _ in range(6):
    p2.append((al - vs2 * p2[-1]) / be2)
check("E2 path alternates 0,5", p2[:4] == [0, 5, 0, 5])
check("E2 fixed point 5/2", al / (be2 + vs2) == F(5, 2))
check("E2 Psi(5/2)=5/2", (al - vs2 * F(5, 2)) / be2 == F(5, 2))
# E3: varsigma = 3, beta = 2
vs3, be3 = F(3), F(2)
c0s3 = al / (be3 + vs3)
check("E3 c0*=2", c0s3 == 2)
p3 = [F(0)]
for _ in range(3):
    p3.append((al - vs3 * p3[-1]) / be3)
check("E3 path 0,5,-5/2,35/4", p3 == [0, 5, F(-5, 2), F(35, 4)])
check("E3 e3=27/4", p3[3] - c0s3 == F(27, 4))
# M1 and M2
al1, be1, vs1, de1 = F(12), F(3), F(1), F(2)
c0m1, c1m1 = al1 / (be1 + vs1), -de1 / (be1 + vs1)
check("M1 c0*=3", c0m1 == 3)
check("M1 c1*=-1/2", c1m1 == F(-1, 2))
check("M1 Psi(0,0)=(4,-2/3)", (al1 / be1, -(vs1 * 0 + de1) / be1) == (4, F(-2, 3)))
check("M2 e1/e0 = -1/3 (c0)", (F(4) - 3) / (0 - 3) == F(-1, 3))
check("M2 e1/e0 = -1/3 (c1)", (F(-2, 3) + F(1, 2)) / (F(0) + F(1, 2)) == F(-1, 3))
# M3
check("M3 L05 var 5/4", (F(4) + F(1)) / F(2) ** 2 == F(5, 4))
# R1: damped step at vs = be = 2, alpha 10
check("R1 nu=1/2", F(2) / (F(2) + F(2)) == F(1, 2))
check("R1 damped = 5/2", F(1, 2) * 0 + F(1, 2) * (F(10) / F(2)) == F(5, 2))
# R2
check("R2 c1*=0 when delta=0", -F(0) / (F(2) + F(1, 2)) == 0)
# Example in E2 solution (L05): Psi formula
check("L05 E2 Psi(5/2) uses (10-2*5/2)/2", (F(10) - 2 * F(5, 2)) / 2 == F(5, 2))

# L06 E1 and E2 (numbers quoted on the page)
check("L06 E1 diff 0.80-7/9 = 0.0222 (4 dp)", round(0.80 - 7 / 9, 4) == 0.0222)
check("L06 E1 0.0222/0.05 = 0.44", round((0.80 - 7 / 9) / 0.05, 2) == 0.44)
diff = 0.426617 - 3 / 7
check("L06 E2 diff -0.001954", round(diff, 6) == -0.001954)
check("L06 E2 diff/tol = -0.30", round(diff / 0.006497, 2) == -0.30)
check("L06 E2 se = 0.002166", round(0.006497 / 3, 6) == 0.002166)
check("L06 E2 diff/se = -0.90", round(diff / (0.006497 / 3), 2) == -0.90)

print("checks", n_checks, "failures", len(fails))
for f_ in fails[:20]:
    print("FAIL", f_)
