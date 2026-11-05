"""Verifier r10: independent re-derivation of Lab 3 numbers with scipy L-BFGS-B on the raw parameters (no shared code)."""
from fractions import Fraction as F
import numpy as np
from scipy.optimize import minimize
import re, html

page = open("/Users/billyribeiro/.fanout/wt/verifyD10-E3-e/course/modules/E/E3/project.html", encoding="utf-8").read()
sec = re.search(r'<section class="lab[^"]*" id="lab-E3-project-3".*?</section>', page, re.S).group(0)
code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
start = code.index("ANSWERS: list")
end = code.index("\n]\n", start) + 3
ns = {}
exec("from fractions import Fraction\n" + code[start:end], ns)  # data only, copied from the page's ANSWERS literal
ANS = ns["ANSWERS"]
print("answers", len(ANS))

def ce(prizes, probs, g, lam):
    # independent: value of lottery then invert piecewise
    W = sum(float(F(p)) * (x**(1-g) if x >= 0 else -lam*((-x)**(1-g))) for x, p in zip(prizes, probs))
    if W >= 0:
        return W**(1/(1-g))
    return -((-W/lam)**(1/(1-g)))

def nll(theta):
    g, lam, kap = theta
    s = 0.0
    for _, c, pa, qa, pb, qb in ANS:
        z = kap*(ce(pa, qa, g, lam) - ce(pb, qb, g, lam))/10000.0
        p_a = 1/(1+np.exp(-z))
        p = p_a if c == "A" else 1-p_a
        s += -np.log(p)
    return s

best = None
for g0 in (0.2, 0.5, 0.8):
    for l0 in (1.0, 3.0, 8.0):
        for k0 in (0.5, 2.0):
            r = minimize(nll, [g0, l0, k0], method="L-BFGS-B", bounds=[(1e-6, 1-1e-6), (1e-6, 200), (1e-6, 200)],
                         options={"ftol": 1e-15, "gtol": 1e-10, "maxiter": 5000})
            if best is None or r.fun < best.fun:
                best = r
th = best.x
print("best nll", best.fun, "LL", -best.fun, "theta", th)
# observed information in raw params by central differences with step 1e-4 (different from page)
def hess(f, x, h=1e-4):
    n = len(x); H = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            ei = np.zeros(n); ej = np.zeros(n); ei[i] = h; ej[j] = h
            H[i, j] = (f(x+ei+ej) - f(x+ei-ej) - f(x-ei+ej) + f(x-ei-ej))/(4*h*h)
    return H
# coordinates zeta, log lam, log kap
def nll_c(t):
    g = 1/(1+np.exp(-t[0])); return nll([g, np.exp(t[1]), np.exp(t[2])])
tc = np.array([np.log(th[0]/(1-th[0])), np.log(th[1]), np.log(th[2])])
H = hess(nll_c, tc, h=1e-4)
cov = np.linalg.inv(H)
g, l, k = th
se_g = g*(1-g)*np.sqrt(cov[0, 0]); se_l = l*np.sqrt(cov[1, 1]); se_k = k*np.sqrt(cov[2, 2])
print(f"gamma_hat {g:.4f} se {se_g:.2f} | lambda_hat {l:.4f} se {se_l:.2f} | kappa_hat {k:.4f} se {se_k:.2f}")
grad = [(nll_c(tc+np.eye(3)[i]*1e-6)-nll_c(tc-np.eye(3)[i]*1e-6))/2e-6 for i in range(3)]
print("max |score| at optimum (scipy opt, coords):", max(abs(x) for x in grad))
print("gradient-based LL at estimate:", f"{-nll(th):.4f}")
