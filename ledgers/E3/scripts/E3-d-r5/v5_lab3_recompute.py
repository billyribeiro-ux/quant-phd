"""Independent recomputation of the Lab 3 reference case (round 5 verifier, stdlib only).

Reads the ANSWERS list from project.html (html-unescaped, so no retyping), then:
(1) maximises the log-likelihood with its own method (random-restart compass search in the three coordinates
    followed by a Newton polish with a 1e-4 central-difference Hessian), independent of the page's second_order_search;
(2) prints gamma, lambda, kappa, the log-likelihood and the largest score component at that point;
(3) computes the observed-information standard errors at steps 1e-4 and 1e-5 and reports them with the delta method;
(4) counts mixed-sign answers and the number of distinct prizes per lottery and the prize range.
Run: python3 -I ledgers/E3/scripts/E3-d-r5/v5_lab3_recompute.py
"""
import html
import math
import random
import re
from fractions import Fraction

PAGE = "course/modules/E/E3/project.html"
text = open(PAGE, encoding="utf-8").read()
m = re.search(r"ANSWERS: list\[.*?\] = \[(.*?)\n\]\n", text, flags=re.S)
assert m, "ANSWERS block not found"
ANSWERS = eval("[" + html.unescape(m.group(1)) + "]", {"Fraction": Fraction})
assert len(ANSWERS) == 12


def value(x, gamma, lam):
    if x >= 0:
        return math.pow(x, 1.0 - gamma)
    return -lam * math.pow(-x, 1.0 - gamma)


def ce(prizes, probs, gamma, lam):
    total = sum(float(Fraction(p)) * value(x, gamma, lam) for x, p in zip(prizes, probs))
    if total >= 0:
        return math.pow(total, 1.0 / (1.0 - gamma))
    return -math.pow(-total / lam, 1.0 / (1.0 - gamma))


def ll(xi):
    gamma = 1 / (1 + math.exp(-xi[0]))
    lam, kappa = math.exp(xi[1]), math.exp(xi[2])
    tot = 0.0
    for _, choice, pa, qa, pb, qb in ANSWERS:
        z = kappa * (ce(pa, qa, gamma, lam) - ce(pb, qb, gamma, lam)) / 10000.0
        tot += -math.log1p(math.exp(-z)) if choice == "A" else -math.log1p(math.exp(z))
    return tot


def ll_safe(xi):
    try:
        v = ll(xi)
        return v if math.isfinite(v) else -math.inf
    except (OverflowError, ValueError, ZeroDivisionError):
        return -math.inf


random.seed(12345)
best, best_v = None, -math.inf
for _ in range(60):
    x = [random.uniform(-3, 3), random.uniform(-2, 2.5), random.uniform(-2, 2)]
    v = ll_safe(x)
    step = 0.5
    while step > 1e-9:
        improved = False
        for d in range(3):
            for s in (step, -step):
                y = list(x)
                y[d] += s
                w = ll_safe(y)
                if w > v:
                    x, v, improved = y, w, True
        if not improved:
            step /= 2
    if v > best_v:
        best, best_v = x, v


def grad_hess(xi, h):
    g = [0.0] * 3
    H = [[0.0] * 3 for _ in range(3)]
    f0 = ll(xi)
    for i in range(3):
        up = list(xi); dn = list(xi)
        up[i] += h; dn[i] -= h
        g[i] = (ll(up) - ll(dn)) / (2 * h)
        H[i][i] = (ll(up) - 2 * f0 + ll(dn)) / (h * h)
    for i in range(3):
        for j in range(i + 1, 3):
            def sh(a, b):
                y = list(xi); y[i] += a; y[j] += b; return ll(y)
            H[i][j] = H[j][i] = (sh(h, h) - sh(h, -h) - sh(-h, h) + sh(-h, -h)) / (4 * h * h)
    return g, H


def solve3(A, b):
    M = [list(A[i]) + [b[i]] for i in range(3)]
    for c in range(3):
        p = max(range(c, 3), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(3):
            if r != c:
                f = M[r][c] / M[c][c]
                M[r] = [a - f * bb for a, bb in zip(M[r], M[c])]
    return [M[i][3] / M[i][i] for i in range(3)]


xi = list(best)
for _ in range(30):
    g, H = grad_hess(xi, 1e-4)
    step = solve3([[-H[i][j] for j in range(3)] for i in range(3)], g)  # Newton on -ll: x - H^-1 g
    # newton step for maximisation: xi += inv(H) g ; H here is the Hessian of ll, so solve H d = -g
    d = solve3(H, [-x for x in g])
    t = 1.0
    while t > 1e-12 and ll_safe([a + t * b for a, b in zip(xi, d)]) < ll_safe(xi):
        t /= 2
    xi = [a + t * b for a, b in zip(xi, d)]

gamma = 1 / (1 + math.exp(-xi[0])); lam = math.exp(xi[1]); kappa = math.exp(xi[2])
print("gamma_hat", f"{gamma:.6f}", "lambda_hat", f"{lam:.6f}", "kappa_hat", f"{kappa:.6f}")
print("log-likelihood", f"{ll(xi):.6f}", "multistart best", f"{best_v:.6f}")
g, _ = grad_hess(xi, 1e-5)
print("largest score component (step 1e-5, coords)", f"{max(abs(v) for v in g):.2e}")


def inverse3(A):
    cols = [solve3(A, [1.0 if k == i else 0.0 for k in range(3)]) for i in range(3)]
    return [[cols[j][i] for j in range(3)] for i in range(3)]


for h in (1e-4, 1e-5):
    _, H = grad_hess(xi, h)
    neg = [[-H[i][j] for j in range(3)] for i in range(3)]
    cov = inverse3(neg)
    se = [gamma * (1 - gamma) * math.sqrt(cov[0][0]), lam * math.sqrt(cov[1][1]), kappa * math.sqrt(cov[2][2])]
    print("step", h, "se_gamma", f"{se[0]:.4f}", "se_lambda", f"{se[1]:.4f}", "se_kappa", f"{se[2]:.4f}")

def mixed(prizes, probs):
    g_ = any(x > 0 and Fraction(p) > 0 for x, p in zip(prizes, probs))
    l_ = any(x < 0 and Fraction(p) > 0 for x, p in zip(prizes, probs))
    return g_ and l_

print("mixed pairs (either lottery):", sum(1 for a in ANSWERS if mixed(a[2], a[3]) or mixed(a[4], a[5])), "of", len(ANSWERS))
allp = [x for a in ANSWERS for x in a[2] + a[4]]
print("prize range", min(allp), max(allp))
print("prize counts per lottery", sorted({len(a[2]) for a in ANSWERS} | {len(a[4]) for a in ANSWERS}))
for a in ANSWERS:
    for prizes, probs in ((a[2], a[3]), (a[4], a[5])):
        assert sum(Fraction(p) for p in probs) == 1 and all(Fraction(p) >= 0 for p in probs), a
print("all lotteries: probabilities nonnegative and sum to exactly 1")
