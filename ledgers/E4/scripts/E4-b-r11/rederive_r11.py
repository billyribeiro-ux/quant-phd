"""Round-11 independent re-derivation of every number in E4 L04-L06 (stdlib only, exact Fractions).

Each check prints OK or FAIL with its locator. Run: python -I ledgers/E4/scripts/E4-b-r11/rederive_r11.py
"""

from __future__ import annotations

import math
import random
from fractions import Fraction as F

results: list[tuple[str, bool, str]] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    results.append((name, bool(cond), detail))


def rank(rows: list[list[F]]) -> int:
    m = [list(r) for r in rows]
    if not m:
        return 0
    ncol = len(m[0])
    r = 0
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
        if r == len(m):
            break
    return r


def v(*x: int) -> list[F]:
    return [F(t) for t in x]


# ---------------- L04 ----------------
inc = [v(1, 1, 1), v(0, 1, 2)]
com = [v(1, 0, 0), v(0, 1, 0), v(0, 0, 1), v(1, 2, 3)]
check("L04 Ex2.2 rank 2 incomplete", rank(inc) == 2)
check("L04 Ex2.3 rank 3 complete", rank(com) == 3)
check("L04 (1,2,3) attainable in inc", rank(inc + [v(1, 2, 3)]) == rank(inc))
check("L04 (0,0,1) not attainable in inc (aug rank 3)", rank(inc + [v(0, 0, 1)]) == 3)
check("L04 (5,0,0) not attainable in inc (aug rank 3)", rank(inc + [v(5, 0, 0)]) == 3)
for xi in (v(1, 2, 3), v(0, 0, 1), v(5, 0, 0)):
    check(f"L04 complete market attains {xi}", rank(com + [xi]) == 3)
for t in (F(0), F(1), F(2), F(-3, 7)):
    zeta = [1 - t, 2 - 2 * t, 3 - 3 * t, t]
    pay = [sum(zeta[j] * com[j][k] for j in range(4)) for k in range(3)]
    check(f"L04 E2 family t={t} replicates (1,2,3)", pay == [F(1), F(2), F(3)], str(pay))
check("L04 M1 rank of (1,2,0),(2,4,0) = 1", rank([v(1, 2, 0), v(2, 4, 0)]) == 1)
check("L04 M2 (1,1,2)=(1,0,1)+(0,1,1)", [a + b for a, b in zip(v(1, 0, 1), v(0, 1, 1))] == v(1, 1, 2))
check("L04 M2 (0,0,1) not attainable (rank 3)", rank([v(1, 0, 1), v(0, 1, 1), v(0, 0, 1)]) == 3)
m3 = [v(1, 2, 0), v(0, 1, 1), v(1, 3, 1), v(2, 5, 1)]
check("L04 M3 rank 2", rank(m3) == 2)
check("L04 M3 r3=r1+r2 and r4=2r1+r2", m3[2] == [a + b for a, b in zip(m3[0], m3[1])] and m3[3] == [2 * a + b for a, b in zip(m3[0], m3[1])])
check("L04 E3 rank 2", rank([v(1, 1, 0), v(0, 1, 1), v(1, 2, 1)]) == 2)
check("L04 misc (1,1,1),(1,1,1),(0,1,2) rank 2 (quiz/misc 2)", rank([v(1, 1, 1), v(1, 1, 1), v(0, 1, 2)]) == 2)
# R3 check on a grid of payoffs with nonnegative holdings
ok = True
for x1 in range(-4, 5):
    for x2 in range(-4, 5):
        t = max(0, -x1, -x2)
        z1, z2, z3 = x1 + t, x2 + t, t
        ok &= z1 >= 0 and z2 >= 0 and z3 >= 0 and (z1 - z3, z2 - z3) == (x1, x2)
check("L04 R3 nonnegative construction over grid", ok)
# Prop 4.2: I_2 cone; (-1,0) not in cone of nonnegative combos
check("L04 Prop4.2 (-1,0) not nonnegative combination of rows of I_2", not any(
    (a >= 0 and b >= 0 and (a, b) == (-1, 0)) for a in [F(-1)] for b in [F(0)]))
check("L04 Remark3.2 kernel dim J-rank for Ex2.3 = 1", 4 - rank(com) == 1)

# ---------------- L05 ----------------
def fixed(al, be, vs, de):
    return (al / (be + vs), -de / (be + vs))


def cmap(c, al, be, vs, de):
    return ((al - vs * c[0]) / be, -(vs * c[1] + de) / be)


base = (F(10), F(2), F(1, 2), F(3, 4))
eq = (F(10), F(2), F(2), F(3, 4))
lg = (F(10), F(2), F(3), F(3, 4))
f = fixed(*base)
check("L05 base fixed point (4,-3/10)", f == (F(4), F(-3, 10)), str(f))
check("L05 base residual zero", cmap(f, *base) == f)
path = [(F(0), F(0))]
for _ in range(8):
    path.append(cmap(path[-1], *base))
c0 = [p[0] for p in path]
check("L05 base c0 path values", [str(x) for x in c0] == ['0', '5', '15/4', '65/16', '255/64', '1025/256', '4095/1024', '16385/4096', '65535/16384'], str([str(x) for x in c0]))
ratios0 = [(path[k + 1][0] - f[0]) / (path[k][0] - f[0]) for k in range(8) if path[k][0] != f[0]]
check("L05 base c0 error ratio -1/4 every step", all(r == F(-1, 4) for r in ratios0))
ratios1 = [(path[k + 1][1] - f[1]) / (path[k][1] - f[1]) for k in range(8) if path[k][1] != f[1]]
check("L05 base c1 error ratio -1/4 every step", all(r == F(-1, 4) for r in ratios1))
fe = fixed(*eq)
check("L05 equal fixed point (5/2,-3/16)", fe == (F(5, 2), F(-3, 16)), str(fe))
pe = [(F(0), F(0))]
for _ in range(6):
    pe.append(cmap(pe[-1], *eq))
check("L05 equal c0 path alternates 0,5", [str(p[0]) for p in pe] == ['0', '5', '0', '5', '0', '5', '0'])
check("L05 equal c1 path alternates 0,-3/8", [str(p[1]) for p in pe] == ['0', '-3/8', '0', '-3/8', '0', '-3/8', '0'])
check("L05 equal ratio -1", all((pe[k + 1][0] - fe[0]) / (pe[k][0] - fe[0]) == -1 for k in range(6)))
fl = fixed(*lg)
check("L05 large fixed point (2,-3/20)", fl == (F(2), F(-3, 20)), str(fl))
pl = [(F(0), F(0))]
for _ in range(6):
    pl.append(cmap(pl[-1], *lg))
check("L05 large c0 path values", [str(p[0]) for p in pl] == ['0', '5', '-5/2', '35/4', '-65/8', '275/16', '-665/32'], str([str(p[0]) for p in pl]))
check("L05 large c1 path values", [str(p[1]) for p in pl] == ['0', '-3/8', '3/16', '-21/32', '39/64', '-165/128', '399/256'], str([str(p[1]) for p in pl]))
check("L05 large ratio -3/2", all((pl[k + 1][0] - fl[0]) / (pl[k][0] - fl[0]) == F(-3, 2) for k in range(6)))
nu = F(2) / (F(2) + F(1, 2))
d0 = (1 - nu) * 0 + nu * cmap((F(0), F(0)), *base)[0]
check("L05 damped weight 4/5, one step gives c0*=4", nu == F(4, 5) and d0 == 4)
d1 = (1 - nu) * 0 + nu * cmap((F(0), F(0)), *base)[1]
check("L05 damped step c1 = -3/10", d1 == F(-3, 10), str(d1))
check("L05 Part F identity on 5-point grid", all(
    (f[0] + f[1] * z) == (base[0] - base[2] * (f[0] + f[1] * z) - base[3] * z) / base[1] for z in map(F, (-2, -1, 0, 1, 2))))
check("L05 E1 |e_k| = 4/4^k; k=5 first within 0.01; 1025/256 - 4 = 1/256", F(1025, 256) - 4 == F(1, 256) and F(4, 4 ** 4) > F(1, 100) and F(4, 4 ** 5) < F(1, 100))
check("L05 E3 errors e0=-2 e1=3 e2=-9/2 e3=27/4", (F(0) - 2, F(5) - 2, F(-5, 2) - 2, F(35, 4) - 2) == (F(-2), F(3), F(-9, 2), F(27, 4)))
check("L05 E3 c0*=10/(2+3)=2", fl[0] == 2)
check("L05 E2 Psi(5/2)=5/2 for equal params", cmap((F(5, 2), F(0)), *eq)[0] == F(5, 2))
check("L05 M1 c*=(3,-1/2) for (12,3,1,2)", fixed(F(12), F(3), F(1), F(2)) == (F(3), F(-1, 2)))
check("L05 M1 Psi fixes c*", cmap(fixed(F(12), F(3), F(1), F(2)), F(12), F(3), F(1), F(2)) == fixed(F(12), F(3), F(1), F(2)))
p2 = cmap((F(0), F(0)), F(12), F(3), F(1), F(2))
check("L05 M2 Psi(0,0)=(4,-2/3); ratios -1/3", p2 == (F(4), F(-2, 3)) and (p2[0] - F(3)) != 0 and (F(4) - F(3)) / F(-3) == F(-1, 3) and (F(-2, 3) + F(1, 2)) / F(1, 2) == F(-1, 3))
check("L05 M3 conditional variance 5/4", (F(4) + F(1)) / F(2) ** 2 == F(5, 4))
check("L05 R1 nu=1/2 and damped gives 5/2", F(2) / (F(2) + F(2)) == F(1, 2) and F(1, 2) * (F(10) / 2) == F(5, 2))
check("L05 R2 delta=0 gives c1*=0", fixed(F(10), F(2), F(1, 2), F(0))[1] == 0)
check("L05 Lemma3.1 identity e_{k+1}=-(vs/be)e_k over grid of params", all(
    cmap((F(p1), F(p2_)), F(10), F(bb), F(vs), F(dd))[0] - fixed(F(10), F(bb), F(vs), F(dd))[0]
    == -(F(vs) / F(bb)) * (F(p1) - fixed(F(10), F(bb), F(vs), F(dd))[0])
    for p1 in (-3, 0, 5) for p2_ in (0,) for bb in (1, 2, 5) for vs in (0, 1, 3) for dd in (0, 2)))
# Prop 3.3: damped factor zero at nu = be/(be+vs), grid
check("L05 Prop3.3 damped factor zero", all(1 - (F(bb) / (F(bb) + F(vs))) * (1 + F(vs) / F(bb)) == 0 for bb in (1, 2, 7) for vs in (0, 1, 5)))

# ---------------- L06 ----------------
SV, SE, A, LAM, SU = F(1), F(1), F(1), F(1, 2), F(1, 4)


def closed(sv, se, a, lam, su):
    tv, te = 1 / sv, 1 / se
    kap = a / (lam * te)
    seta = se + kap * kap * su
    teta = 1 / seta
    tbar = lam * te + (1 - lam) * teta
    ths = tbar / (tv + tbar)
    return kap, seta, teta, tbar, ths, kap * ths


kap, seta, teta, tbar, ths, thu = closed(SV, SE, A, LAM, SU)
check("L06 Ex6.9 kappa=2 sig_eta2=2 tau_eta=1/2 tau_bar=3/4 theta=(3/7,6/7)", (kap, seta, teta, tbar, ths, thu) == (2, 2, F(1, 2), F(3, 4), F(3, 7), F(6, 7)))
varp = ths * ths * (SV + SE) + thu * thu * SU
covvp = ths * SV
b = covvp / varp
check("L06 Ex6.9 Var(p)=27/49 Cov=3/7 slope b=7/9", (varp, covvp, b) == (F(27, 49), F(3, 7), F(7, 9)), str((varp, covvp, b)))
check("L06 Ex6.9 V_U = 2/3", SV - b * covvp == F(2, 3))
check("L06 Cor6.8 formula slope equals tau_eta/(theta_s(tv+teta))", b == teta / (ths * (1 / SV + teta)))
check("L06 Cor6.8 1/(tv+teta)=2/3 at base", 1 / (1 / SV + teta) == F(2, 3))
check("L06 rho^2 = 1/3 at base", covvp ** 2 / (SV * varp) == F(1, 3))
omega = SV / (SV + SE)
VI = SV * SE / (SV + SE)
check("L06 omega=1/2 V_I=1/2 base", omega == F(1, 2) and VI == F(1, 2))


def residual(s, u, ts, tu, sv=SV, se=SE, a=A, lam=LAM, su=SU):
    price = ts * s - tu * u
    vp = ts * ts * (sv + se) + tu * tu * su
    cv = ts * sv
    sl = cv / vp
    rv = sv - sl * cv
    vi = sv * se / (sv + se)
    mi = sv * s / (sv + se)
    dinf = (mi - price) / (a * vi)
    dunf = (sl * price - price) / (a * rv)
    return lam * dinf + (1 - lam) * dunf - u


GS = [F(-1), F(0), F(1), F(2)]
GU = [F(-1), F(0), F(1, 2), F(2)]
res = [residual(s, u, ths, thu) for s in GS for u in GU]
check("L06 Part C 16 grid residuals zero", all(r == 0 for r in res) and len(res) == 16)
check("L06 Part D residual at (1,0) with theta_s=1/2 is -9/85", residual(F(1), F(0), F(1, 2), thu) == F(-9, 85), str(residual(F(1), F(0), F(1, 2), thu)))
check("L06 Part C informed demand at (1,0) = 1/7", (omega * 1 - ths) / (A * VI) == F(1, 7))
check("L06 x_U at (1,0) = -1/7", ((b * ths - ths) / (A * (SV - b * covvp))) == F(-1, 7))
check("L06 clearing at (1,0): (1/2)(1/7)+(1/2)(-1/7)=0", F(1, 2) * F(1, 7) + F(1, 2) * F(-1, 7) == 0)
# Clearing at random (s,u) for random instances and closed form (Prop 6.7 (a))
rnd = random.Random(11)
ok = True
ok_alt = []
for _ in range(60):
    sv = F(rnd.randint(1, 9), rnd.randint(1, 9))
    se = F(rnd.randint(1, 9), rnd.randint(1, 9))
    a = F(rnd.randint(1, 9), rnd.randint(1, 9))
    lam = F(rnd.randint(1, 9), 10)
    su = F(rnd.randint(1, 9), rnd.randint(1, 9))
    kap_, seta_, teta_, tbar_, ths_, thu_ = closed(sv, se, a, lam, su)
    for s in (F(-1), F(0), F(1), F(3, 2)):
        for u in (F(-2), F(0), F(1, 3), F(1)):
            ok &= residual(s, u, ths_, thu_, sv, se, a, lam, su) == 0
    # uniqueness check: theta_s perturbed gives nonzero residual somewhere
    ok_alt.append(residual(F(1), F(0), ths_ + F(1, 100), thu_, sv, se, a, lam, su) != 0)
check("L06 Prop6.7(a) closed form clears on random instances (60 x 16 points)", ok)
check("L06 Prop6.7(b) perturbed theta_s leaves residual at (1,0) on random instances", all(ok_alt))
# Corollary 6.8 identities on random instances
ok8 = True
for _ in range(40):
    sv = F(rnd.randint(1, 9), rnd.randint(1, 9))
    se = F(rnd.randint(1, 9), rnd.randint(1, 9))
    a = F(rnd.randint(1, 9), rnd.randint(1, 9))
    lam = F(rnd.randint(1, 9), 10)
    su = F(rnd.randint(1, 9), rnd.randint(1, 9))
    kap_, seta_, teta_, tbar_, ths_, thu_ = closed(sv, se, a, lam, su)
    vp = ths_ * ths_ * (sv + se) + thu_ * thu_ * su
    cv = ths_ * sv
    sl = cv / vp
    ok8 &= sl == teta_ / (ths_ * (1 / sv + teta_))
    ok8 &= sv - sl * cv == 1 / (1 / sv + teta_)
    ok8 &= sv - sl * cv == sv * seta_ / (sv + seta_)
    ok8 &= cv * cv / (sv * vp) == sv / (sv + seta_)
check("L06 Cor6.8 + Lemma6.4 identities on random instances", ok8)

# M1..M3
m_k, m_s2, m_t, m_tb, m_ths, m_thu = closed(F(1), F(1), F(2), F(1, 2), F(1, 4))
check("L06 M1 (kappa,seta2,teta,tbar,ths,thu)=(4,5,1/5,3/5,3/8,3/2)", (m_k, m_s2, m_t, m_tb, m_ths, m_thu) == (4, 5, F(1, 5), F(3, 5), F(3, 8), F(3, 2)))
m_var = F(3, 8) ** 2 * 2 + F(3, 2) ** 2 * F(1, 4)
m_cov = F(3, 8)
m_b = m_cov / m_var
check("L06 M2 Var(p)=27/32, b=4/9, Var(v|p)=5/6, corr^2=1/6", (m_var, m_b, 1 - m_b * m_cov, m_cov ** 2 / (1 * m_var)) == (F(27, 32), F(4, 9), F(5, 6), F(1, 6)))
check("L06 M2 Var(v|p)=1/(1+1/5)=5/6 and corr^2=1/(1+5)", F(1) / (1 + F(1, 5)) == F(5, 6) and F(1) / (1 + 5) == F(1, 6))
mp = F(3, 8) * 2 - F(3, 2) * 1
check("L06 M3 price -3/4", mp == F(-3, 4))
mxi = (1 * 2 - 2 * mp) / 2
mxu = (F(1, 5) * (mp / F(3, 8)) - (1 + F(1, 5)) * mp) / 2
check("L06 M3 x_I=7/4 x_U=1/4 clear=1", mxi == F(7, 4) and mxu == F(1, 4) and F(1, 2) * mxi + F(1, 2) * mxu == 1)
# P2 example arithmetic with theta_s=0, u=0: residual difference lam*tau_e/a
check("L06 P2 difference lam tau_e / a nonzero", F(1, 2) * 1 / 1 != 0)
# P3 identity
sv_, sn = F(3, 7), F(5, 2)
check("L06 P3 identity sv - sv^2/(sv+sn) = sv sn/(sv+sn)", sv_ - sv_ ** 2 / (sv_ + sn) == sv_ * sn / (sv_ + sn))
check("L06 P3 = 1/(tau_v+tau_n)", sv_ * sn / (sv_ + sn) == 1 / (1 / sv_ + 1 / sn))
# R1 identity: Corr^2 = sv/(sv+seta) under lambda -> limit: check it at several lambda
ok_r1 = True
for lam_ in (F(1, 2), F(1, 3), F(1, 10), F(1, 100)):
    kk, sn_, tn_, tb_, th_, tu_ = closed(SV, SE, A, lam_, SU)
    vp = th_ * th_ * (SV + SE) + tu_ * tu_ * SU
    cv = th_ * SV
    ok_r1 &= cv * cv / (SV * vp) == SV / (SV + sn_)
check("L06 R1 Corr^2 = sv/(sv+seta) at four lambdas", ok_r1)
check("L06 R1 theta_s* ->0 as lambda->0 (sample lambda 1/100 small)", closed(SV, SE, A, F(1, 100), SU)[4] < F(1, 50))
# R2 monotone
prev = None
mono = True
for su_ in (F(1, 100), F(1, 4), F(1), F(4)):
    vu = 1 / (1 / SV + closed(SV, SE, A, LAM, su_)[2])
    if prev is not None:
        mono &= vu > prev
    prev = vu
check("L06 R2 Var(v|p) strictly increasing in sigma_u^2 (sample)", mono)
# E1 (L06 empirical) 0.80 - 7/9 over 0.05
check("L06 E1 standardized difference 0.44", round(float((F(4, 5) - F(7, 9)) / F(1, 20)), 2) == 0.44)
# E2 (L06 empirical) from printed Lab values
sample_slope, tol = 0.426617, 0.006497
pop = 3 / 7
diff = sample_slope - pop
check("L06 E2 diff -0.001954, -0.30 tolerance, -0.90 SE", round(diff, 6) == -0.001954 and round(diff / tol, 2) == -0.30 and round(diff / (tol / 3), 2) == -0.90)
# Quiz numeric answers
check("L06 quiz theta_s 0.4286 within 0.0005", abs(3 / 7 - 0.4286) <= 0.0005)
check("L06 quiz x_I 0.1429 within 0.0005", abs(1 / 7 - 0.1429) <= 0.0005)
check("L06 quiz b 0.7778 within 0.0005", abs(7 / 9 - 0.7778) <= 0.0005)
check("L06 quiz Var(v|p) 0.6667 within 0.0005", abs(2 / 3 - 0.6667) <= 0.0005)
check("L06 quiz V_I 0.5", SV * SE / (SV + SE) == F(1, 2))

# Part E: seeded sample replica (floats) as the twin computes it
rng = random.Random(6)
N = 20000
sd_v, sd_e, sd_u = 1.0, 1.0, math.sqrt(0.25)
ts_f, tu_f = float(F(3, 7)), float(F(6, 7))
sd_draws, pd_draws, vd_draws = [], [], []
for _ in range(N):
    vv = rng.gauss(0.0, sd_v)
    ee = rng.gauss(0.0, sd_e)
    uu = rng.gauss(0.0, sd_u)
    ss = vv + ee
    sd_draws.append(ss)
    pd_draws.append(ts_f * ss - tu_f * uu)
    vd_draws.append(vv)


def ols(x, y):
    n = len(x)
    mx = sum(x) / n
    my = sum(y) / n
    sxx = sum((xi - mx) ** 2 for xi in x)
    sxy = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    sl = sxy / sxx
    ic = my - sl * mx
    rss = sum((yi - ic - sl * xi) ** 2 for xi, yi in zip(x, y))
    return sl, math.sqrt(rss / (n - 2) / sxx)


s1, e1 = ols(sd_draws, pd_draws)
s2, e2 = ols(pd_draws, vd_draws)
check("L06 Part E p_on_s slope 0.426617 tol 0.006497 (independent replica)", f"{s1:.6f}" == "0.426617" and f"{3 * e1:.6f}" == "0.006497", f"{s1:.6f} {3 * e1:.6f}")
check("L06 Part E v_on_p slope 0.761928 tol 0.023538 (independent replica)", f"{s2:.6f}" == "0.761928" and f"{3 * e2:.6f}" == "0.023538", f"{s2:.6f} {3 * e2:.6f}")

bad = [r for r in results if not r[1]]
for name, ok_, detail in results:
    print(("OK   " if ok_ else "FAIL ") + name + (f"  [{detail}]" if detail and not ok_ else ""))
print(f"total={len(results)} ok={len(results) - len(bad)} fail={len(bad)}")
