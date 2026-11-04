"""E4-c round 3: exact re-checks of the sentences changed in this round (L07 Remark 7.9, L08 Cor 3.2, L08 misconception, L09 misconception 2).

Standard library only. Usage: python -I recheck_c_r3.py
"""
from fractions import Fraction as F
import itertools

# L08 Corollary 3.2: Corr(v, p*)^2 for p* = (1-b) vbar + b s - kappa b u, with exact moments.
# Var(v)=sv, Var(eps)=se, Var(u)=su; s = v + eps; cov(v,s)=sv; var(s)=sv+se; u independent of (v,eps).
bad = 0
n = 0
vals = [F(1, 4), F(1, 2), F(1), F(2), F(3)]
for sv, se, su, a, lam in itertools.product(vals, vals, [F(0), F(1, 3), F(1), F(5)], [F(1, 2), F(2)], [F(1, 4), F(1, 2), F(1)]):
    kappa = a * se / lam
    tau_v, tau_e = 1 / sv, 1 / se
    A = lam * tau_e + (1 - lam) * (1 / (se + kappa * kappa * su))
    beta = A / (tau_v + A)
    cov_vp = beta * sv
    var_p = beta * beta * (sv + se) + kappa * kappa * beta * beta * su
    corr2 = cov_vp * cov_vp / (sv * var_p)
    sigma_eta2 = se + kappa * kappa * su
    closed1 = sv / (sv + sigma_eta2)
    closed2 = sv / (sv + se + kappa * kappa * su)
    tau_eta = 1 / sigma_eta2
    closed3 = tau_eta / (tau_v + tau_eta)
    n += 1
    if not (corr2 == closed1 == closed2 == closed3):
        bad += 1
print("Cor 3.2 exact identity over", n, "parameter tuples; failures:", bad)

# L07 Remark 7.9: on the Part B sweep, Var(p) rises while rho^2 falls (recomputed).
sweep = []
for sd in [F(1, 4), F(1, 2), F(1), F(2), F(4)]:
    su2 = sd * sd
    sv2 = se2 = F(1)
    a, lam = F(1), F(1, 2)
    kappa = a * se2 / lam
    sig_eta2 = se2 + kappa * kappa * su2
    tau_bar = lam / se2 + (1 - lam) * (1 / sig_eta2)
    ts = tau_bar / (1 / sv2 + tau_bar)
    tu = kappa * ts
    varp = ts * ts * (sv2 + se2) + tu * tu * su2
    rho2 = (ts * sv2) ** 2 / (sv2 * varp)
    sweep.append((sd, varp, rho2))
    print("L07 sweep sd", sd, "var_p", varp, "rho2", rho2)
print("Var(p) strictly increasing:", all(b[1] > a[1] for a, b in zip(sweep, sweep[1:])),
      "| rho2 strictly decreasing:", all(b[2] < a[2] for a, b in zip(sweep, sweep[1:])))

# L08 misconception: bisection roots fall as cost rises (printed roots from the lab output)
roots = [(0.13, 0.965625410), (0.14, 0.815032329), (0.15, 0.657828572), (0.16, 0.480567912), (0.17, 0.231615819)]
print("root falls as cost rises:", all(b[1] < a[1] for a, b in zip(roots, roots[1:])))

# L09 misconception 2 (omega labels): exhaustive check of the example
P1 = [{"w1", "w2"}, {"w3"}]
P2 = [{"w1"}, {"w2", "w3"}]
E = {"w1", "w2"}
def cell(P, w):
    return next(c for c in P if w in c)
def meet(w):
    seen = {w}
    frontier = [w]
    while frontier:
        u = frontier.pop()
        for P in (P1, P2):
            for v in cell(P, u):
                if v not in seen:
                    seen.add(v)
                    frontier.append(v)
    return seen
print("w1 knows E in trader 1 cell:", cell(P1, "w1") <= E, "| trader 2 cell:", cell(P2, "w1") <= E)
print("meet(w1) =", sorted(meet("w1")), "| meet subset of E:", meet("w1") <= E)
print("w2 and w3 share a P2 cell:", cell(P2, "w2") == cell(P2, "w3"))
