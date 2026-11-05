"""Independent re-derivation of the numbers printed or stated in E4 L04-L06 (verifier round 8).

Written from the page text, not from the lab twins. Exact Fractions throughout. Run with: python -I this_file.
Methods differ from the twins: L04 rank by maximal nonzero minor (not elimination); L05 by the closed-form
recursion check and direct substitution; L06 by Gaussian conditioning through the joint covariance matrix of
(v, s, p) (not by the twin's residual function), and the alternative-slope residual by hand-written formulas.
"""

from fractions import Fraction as F
from itertools import combinations


def det(m):
    n = len(m)
    if n == 1:
        return m[0][0]
    if n == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    return sum((-1) ** j * m[0][j] * det([r[:j] + r[j + 1 :] for r in m[1:]]) for j in range(n))


def rank_minor(m):
    """Rank = largest k such that some k x k minor is nonzero (exact)."""
    rows, cols = len(m), len(m[0])
    for k in range(min(rows, cols), 0, -1):
        for rs in combinations(range(rows), k):
            for cs in combinations(range(cols), k):
                if det([[m[r][c] for c in cs] for r in rs]) != 0:
                    return k
    return 0


print("== L04 (minor-based ranks)")
inc = [[1, 1, 1], [0, 1, 2]]
comp = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 2, 3]]
print("rank incomplete", rank_minor(inc), "rank complete", rank_minor(comp))
for name, xi in [("(1,2,3)", [1, 2, 3]), ("(0,0,1)", [0, 0, 1]), ("(5,0,0)", [5, 0, 0])]:
    print("incomplete", name, "augmented", rank_minor(inc + [xi]), "attainable", rank_minor(inc + [xi]) == rank_minor(inc))
for name, xi in [("(1,2,3)", [1, 2, 3]), ("(0,0,1)", [0, 0, 1]), ("(5,0,0)", [5, 0, 0])]:
    print("complete", name, "augmented", rank_minor(comp + [xi]), "attainable", rank_minor(comp + [xi]) == rank_minor(comp))
print("M1 rank (1,2,0),(2,4,0):", rank_minor([[1, 2, 0], [2, 4, 0]]))
print("M3 rank:", rank_minor([[1, 2, 0], [0, 1, 1], [1, 3, 1], [2, 5, 1]]))
print("E3 rank:", rank_minor([[1, 1, 0], [0, 1, 1], [1, 2, 1]]))
print("Ex 2.2 (1,2,3)=r1+r2 check:", [a + b for a, b in zip([1, 1, 1], [0, 1, 2])])
print("Misc2 rank (1,1,1),(1,1,1),(0,1,2):", rank_minor([[1, 1, 1], [1, 1, 1], [0, 1, 2]]))
print("P2 family check t=1/3:", end=" ")
t = F(1, 3)
z = [1 - t, 2 - 2 * t, 3 - 3 * t, t]
A4 = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 2, 3]]
print([sum(z[j] * A4[j][k] for j in range(4)) for k in range(3)])
print("Remark 3.2 kernel dim J - rank (Ex 2.3):", 4 - rank_minor(comp))

print("== L05 (closed form vs recursion)")


def psi(c, a, b, s, d):
    return ((a - s * c[0]) / b, -(s * c[1] + d) / b)


for label, (a, b, s, d) in [("base", (F(10), F(2), F(1, 2), F(3, 4))), ("equal", (F(10), F(2), F(2), F(3, 4))), ("large", (F(10), F(2), F(3), F(3, 4)))]:
    cstar = (a / (b + s), -d / (b + s))
    c = (F(0), F(0))
    path = [c]
    for _ in range(6):
        c = psi(c, a, b, s, d)
        path.append(c)
    e0 = [p[0] - cstar[0] for p in path]
    ratios = [e0[k + 1] / e0[k] for k in range(len(e0) - 1) if e0[k] != 0]
    print(label, "c*", cstar, "c0 path", [str(p[0]) for p in path][:7], "ratios c0", [str(r) for r in ratios][:4])
    print(label, "psi(c*)==c*", psi(cstar, a, b, s, d) == cstar)
a, b, s, d = F(10), F(2), F(1, 2), F(3, 4)
w = b / (b + s)
c0 = (F(0), F(0))
img = psi(c0, a, b, s, d)
damped = ((1 - w) * c0[0] + w * img[0], (1 - w) * c0[1] + w * img[1])
print("damped weight", w, "damped", damped, "== c*", damped == (a / (b + s), -d / (b + s)))

print("== L06 (Gaussian conditioning via covariance matrix)")
sv, se, su, lam, A = F(1), F(1), F(1, 4), F(1, 2), F(1)
kappa = A * se / lam
sig_eta2 = se + kappa**2 * su
tau_v, tau_e, tau_eta = 1 / sv, 1 / se, 1 / sig_eta2
taubar = lam * tau_e + (1 - lam) * tau_eta
thS = taubar / (tau_v + taubar)
thU = kappa * thS
print("kappa", kappa, "sig_eta2", sig_eta2, "tau_eta", tau_eta, "taubar", taubar, "thS", thS, "thU", thU)


def cov_price_and_v(thS_, thU_):
    # covariance of (v, s, u) is diag-ish: Var v = sv, Var s = sv+se, Var u = su, Cov(v,s)=sv, others 0
    cov_vs = sv
    var_s = sv + se
    var_p = thS_**2 * var_s + thU_**2 * su
    cov_vp = thS_ * cov_vs
    return var_p, cov_vp


def resid(s_, u_, thS_, thU_):
    """Total demand minus supply at (s,u), demands from the Gaussian posterior formulas, by direct conditioning."""
    p_ = thS_ * s_ - thU_ * u_
    var_p, cov_vp = cov_price_and_v(thS_, thU_)
    beta_u = cov_vp / var_p  # projection slope of v on p
    post_u = sv - beta_u * cov_vp
    # informed: condition v on (s,p): posterior mean of v given s and p, computed via the 2x2 system
    # cov(v,(s,p)) and cov((s,p)) with p = thS s - thU u; u independent of (v,s) so cov(p,v)=thS*sv, cov(p,s)=thS*var_s
    cov_s_p = thS_ * (sv + se)  # Cov(s, p) includes thU*Cov(s,u)=0
    cov_p_p = var_p
    cov_s_s = sv + se
    # solve [[var_s, cov_s_p],[cov_s_p, var_p]] x = [cov(v,s), cov(v,p)]
    det2 = cov_s_s * cov_p_p - cov_s_p * cov_s_p
    cvs, cvp = sv, cov_vp
    x_s = (cvs * cov_p_p - cvp * cov_s_p) / det2
    x_p = (cov_s_s * cvp - cov_s_p * cvs) / det2
    mean_inf = x_s * s_ + x_p * p_
    var_inf = sv - (x_s * cvs + x_p * cvp)
    dI = (mean_inf - p_) / (A * var_inf)
    dU = (beta_u * p_ - p_) / (A * post_u)
    return lam * dI + (1 - lam) * dU - u_


grid_s = [F(-1), F(0), F(1), F(2)]
grid_u = [F(-1), F(0), F(1, 2), F(2)]
vals = [resid(x, y, thS, thU) for x in grid_s for y in grid_u]
print("grid residuals zero:", sum(1 for v_ in vals if v_ == 0), "of", len(vals))
print("residual at (1,0) with thS=1/2:", resid(F(1), F(0), F(1, 2), thU))
print("informed demand at (1,0) with a=1:", (F(1) * sv / (sv + se) - thS * F(1)) / (sv * se / (sv + se)))
var_p0, cov0 = cov_price_and_v(thS, thU)
print("Var p", var_p0, "Cov", cov0, "slope", cov0 / var_p0, "post", sv - (cov0 / var_p0) * cov0, "rho2", cov0**2 / (sv * var_p0))
print("M1 instance (a=2):")
a2 = F(2)
k2 = a2 * se / lam
se2 = se + k2**2 * su
te2 = 1 / se2
tb2 = lam * (1 / se) + (1 - lam) * te2
th2 = tb2 / (1 + tb2)
print("  kappa", k2, "sig_eta2", se2, "tau_eta", te2, "taubar", tb2, "thS", th2, "thU", k2 * th2)
