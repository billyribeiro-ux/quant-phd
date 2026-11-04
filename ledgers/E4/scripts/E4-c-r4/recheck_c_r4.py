"""E4-c round 4: independent re-derivation of the numbers printed or quoted in L07, L08 and L09.

Standard library only. Usage: python -I recheck_c_r4.py. Written from the page formulas, not from the lab twins.
"""
import math
from fractions import Fraction as F
from itertools import product

print("== L07 (exact Fractions, sig_v2 = sig_e2 = 1)")
def rho2(a, lam, sd, sv=F(1), se=F(1)):
    tau_v, tau_e = 1 / sv, 1 / se
    kappa = a / (lam * tau_e)
    seta2 = se + kappa * kappa * sd * sd
    tau_eta = 1 / seta2
    A = lam * tau_e + (1 - lam) * tau_eta
    beta = A / (tau_v + A)
    p_s = beta
    p_u = kappa * beta
    var_p = p_s * p_s * (sv + se) + p_u * p_u * sd * sd
    r2 = sv * sv * p_s * p_s / (sv * var_p)
    return r2, seta2, var_p, r2 == sv / (sv + seta2)

for sd in [F(1, 4), F(1, 2), F(1), F(2), F(4)]:
    r2, s2, vp, eq = rho2(F(1), F(1, 2), sd)
    print(f"sd {sd} sig_eta2 {s2} var_p {vp} ({float(vp):.6f}) rho2 {r2} closed_form_eq {eq}")
for lam in [F(1, 4), F(1, 2), F(3, 4)]:
    print("lam", lam, "rho2", rho2(F(1), lam, F(1, 2))[0])
for a in [F(1, 2), F(1), F(2)]:
    print("a", a, "rho2", rho2(a, F(1, 2), F(1, 2))[0])
print("tiny sd 1/100 rho2", rho2(F(1), F(1, 2), F(1, 100))[0], "benchmark", F(1, 2))
print("M1 sd=1 rho2", rho2(F(1), F(1, 2), F(1))[0], "M2 lam=3/4 sd=1/2 rho2", rho2(F(1), F(3, 4), F(1, 2))[0])
print("M3 sv2=2 sd=1 rho2", rho2(F(1), F(1, 2), F(1), sv=F(2))[0])
print("E2 check: sigma_u^2=1/2 gives rho2", rho2(F(1), F(1, 2), F(1, math.isqrt(2)) if False else F(0)) if False else "skipped")
print("R2 check: sigma_u^2 = 1/2, rho2/rho0^2 =", rho2(F(1), F(1, 2), F(2) ** F(-1, 2))[0] / F(1, 2))
print("Misc: rho2 at sd=1/2 is 1/3:", rho2(F(1), F(1, 2), F(1, 2))[0] == F(1, 3))
print("Base instance Var(p)", rho2(F(1), F(1, 2), F(1, 2))[2], "sd=4 var_p", rho2(F(1), F(1, 2), F(4))[2])
print("Canon witness Var(p) for p=v^2 with v~N(0,1): E[v^4]-1 =", 3 - 1, "; Cov =", 0)
print("E1: |1/3 - 0.330625| / 0.02 =", (1 / 3 - 0.330625) / 0.02)
print("E2 numeric: 1 + 4 u^2 = 3 -> u^2 =", (3 - 1) / 4, "; sigma_u =", math.sqrt(0.5))
print("R2 closed form at a=1,lam=1/2,sv=se=1: chi =", 1 / (F(1, 2)) ** 2, "sigma_u =", math.sqrt(2 / 4))

print("\n== L08 (floats; a = 2, sig_v2 = sig_e2 = sig_u2 = 1, v-bar = 0)")
a, sv, se, su = 2.0, 1.0, 1.0, 1.0
tv, te = 1 / sv, 1 / se

def parts(lam, sd2=su):
    kappa = a * se / lam
    teta = 1 / (se + kappa * kappa * sd2)
    seta2 = 1 / teta
    A = lam * te + (1 - lam) * teta
    beta = A / (tv + A)
    bs = sv / (sv + se)
    by = teta / (tv + teta)
    VI = 1 / (tv + te)
    VU = 1 / (tv + teta)
    DI = (bs - beta) ** 2 * (sv + se) + kappa * kappa * beta * beta * sd2
    DU = (by - beta) ** 2 * (sv + seta2)
    return kappa, teta, beta, bs, by, VI, VU, DI, DU

def G(lam, sd2=su):
    kappa, teta, beta, bs, by, VI, VU, DI, DU = parts(lam, sd2)
    return math.log((1 + DI / VI) / (1 + DU / VU)) / (2 * a)

def corr2(lam):
    kappa, teta, beta, *_ = parts(lam)
    return teta / (tv + teta)

G0 = math.log(1 + sv / se) / (2 * a)
print("G(0) closed", G0, "printed 0.173287 diff", abs(G0 - 0.173287))
print("G(1) recomputed", G(1.0), "closed ln(5/3)/4", math.log(5 / 3) / 4)
print("G(1e-6)-G(0) =", G(1e-6) - G0)
grid = [k / 1000 for k in range(1, 1000)]
vals = [G(l) for l in grid]
print("G strictly decreasing on 999 grid points:", all(vals[i] > vals[i + 1] for i in range(len(vals) - 1)))
cvals = [corr2(l) for l in grid]
print("Corr^2 strictly increasing on grid:", all(cvals[i] < cvals[i + 1] for i in range(len(cvals) - 1)))
print("Example 1.1 at lam=1/2: tau_eta =", parts(0.5)[1], "corr2 =", corr2(0.5))

def solve(c):
    if c >= G0:
        return 0.0, G0 - c
    if c <= G(1.0):
        return 1.0, G(1.0) - c
    lo, hi = 0.0, 1.0
    # N(lo) = G0 - c > 0 >= N(hi) = G(1) - c
    while hi - lo > 1e-12:
        mid = (lo + hi) / 2
        if G(mid) - c > 0:
            lo = mid
        else:
            hi = mid
    lam = (lo + hi) / 2
    return lam, G(lam) - c

for c in [0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18]:
    lam, gap = solve(c)
    print(f"cost {c} lam* {lam:.9f} gap {gap:.3e} corr2 {corr2(lam) if 0 < lam <= 1 else 0.0:.6f}")
print("Mis 2: G(0) =", G0, "ln2/4 =", math.log(2) / 4)
print("Emp 1 gap at cost 0.15 printed 1.83e-15; recomputed N(lam*) =", G(solve(0.15)[0]) - 0.15)
print("Emp 3 G(1) =", G(1.0), "vs ln(5/3)/4", math.log(5 / 3) / 4)
print("Quiz Corr at lam=1/2 (tau_eta = 1/17):", (1 / 17) / (1 + 1 / 17), "vs 1/18 =", 1 / 18)
print("Mech1 kappa=4, tau_eta(sigma_u^2=1)=1/17:", 2 * 1 / 0.5, 1 / (1 + 16))
print("Mech3 E[exp(-Z^2/2)], Z~N(0,4): (1+4)^-0.5 =", 5 ** -0.5, "; Jensen lower bound exp(-2) =", math.exp(-2))
print("Mech2: x* = (1-0.5)/(3*2) =", (1 - 0.5) / 6, "; exponent -(1/2)^2/(2*2) =", -(0.25) / 4)
print("L08 Part C boundary net benefit at cost 0.12:", G(1.0) - 0.12, "; at cost 0.18:", G0 - 0.18)
print("Part A sample: none rerun here (see twin output)")

print("\n== L09 (exact enumeration, independent of the twin)")
STATES = range(1, 7)
P1 = [{1, 2}, {3}, {4, 5, 6}]
P2 = [{1, 2, 3}, {4, 5}, {6}]
def cell(part, w):
    return next(c for c in part if w in c)
def meet(w):
    reach = {w}
    changed = True
    while changed:
        changed = False
        for part in (P1, P2):
            for r in list(reach):
                for x in cell(part, r):
                    if x not in reach:
                        reach.add(x); changed = True
    return reach
def post(part, x, w):
    c = cell(part, w)
    return F(sum(x[k - 1] for k in c), len(c))
bets = list(product([-2, -1, 0, 1, 2], repeat=6))
print("bets:", len(bets))
for w in (1, 4):
    M = meet(w)
    strict = [b for b in bets if post(P1, b, w) > 0 and post(P2, tuple(-v for v in b), w) > 0]
    both_nonneg = [b for b in bets if all(post(P1, b, s) >= 0 and post(P2, tuple(-v for v in b), s) >= 0 for s in M)]
    strict_common = [b for b in strict if b in both_nonneg]
    nonzero = [b for b in both_nonneg if any(post(P1, b, s) != 0 or post(P2, tuple(-v for v in b), s) != 0 for s in M)]
    print(f"state {w}: meet {sorted(M)} strict {len(strict)} nonneg-on-meet {len(both_nonneg)} strict&nonneg {len(strict_common)} nonzero-on-meet among nonneg {len(nonzero)}")
    if strict:
        print("  first strict bet", strict[0], "agent1 meet posts", [str(post(P1, strict[0], s)) for s in sorted(M)], "agent2", [str(post(P2, tuple(-v for v in strict[0]), s)) for s in sorted(M)])
zero_on_123 = [b for b in bets if b[2] == 0 and b[1] == -b[0]]
print("Emp3 count of bets with x3=0 and x2=-x1 (free x4..x6):", len(zero_on_123))
print("Res1 check: no bet has S1>=0 and -S1-k*pi(M)>=0 for k>0 by construction (algebra)")
print("Mech1 g1: ", [post(P1, (2, 0, -1, 4), w) for w in (1, 2, 3, 4)] if False else "skipped")
