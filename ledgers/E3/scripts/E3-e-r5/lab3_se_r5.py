"""Independent check of Lab 3 standard errors and score (rung 3 reference case), round 5.

Uses the answers as printed in project.html Lab 3 (copied by hand from the page, not from the twin). Newton's method on
the log-likelihood in (zeta, log lambda, log kappa) with a central-difference Hessian at step 1e-4, then the
observed information at the estimate by central differences at steps 1e-4 and 1e-5 (both reported). Standard library only.
"""

import math
from fractions import Fraction as F

ANS = [
    (0, "B", [6200, -15100], ["9/10", "1/10"], [3300, -3000, -700], ["1/20", "7/20", "3/5"]),
    (1, "B", [-9400, -10100, 19000], ["2/5", "3/10", "3/10"], [-12200, 17000, -1100], ["1/2", "1/4", "1/4"]),
    (2, "A", [10700, -3400, -13400], ["7/10", "1/10", "1/5"], [-14900, -13600, 15200], ["9/20", "2/5", "3/20"]),
    (3, "A", [18800, -12500], ["3/4", "1/4"], [16500, -17700], ["2/5", "3/5"]),
    (4, "B", [-10700, -5600, -7300], ["1/2", "2/5", "1/10"], [-13800, -9700], ["1/4", "3/4"]),
    (5, "B", [-11600, 7900, -12200], ["3/4", "1/10", "3/20"], [-12000, 11300], ["17/20", "3/20"]),
    (6, "A", [-9900, 5400, -4200], ["1/2", "1/4", "1/4"], [-15300, 16100, 6800], ["1/4", "1/2", "1/4"]),
    (7, "A", [600, -17500], ["3/5", "2/5"], [15800, -2600, -17600], ["2/5", "2/5", "1/5"]),
    (8, "B", [-10400, 13800], ["9/10", "1/10"], [10400, 1800], ["1/20", "19/20"]),
    (9, "B", [-17900, -12000, -3600], ["1/4", "1/4", "1/2"], [15600, 11600, -12200], ["3/10", "13/20", "1/20"]),
    (10, "B", [17000, 1600], ["1/10", "9/10"], [-18700, 3800], ["7/20", "13/20"]),
    (11, "B", [10400, -11300], ["2/5", "3/5"], [9300, 7200, -13200], ["1/2", "1/4", "1/4"]),
]


def pv(x, g, lam):
    return x ** (1 - g) if x >= 0 else -lam * (-x) ** (1 - g)


def pce(prizes, probs, g, lam):
    v = sum(float(F(p)) * pv(x, g, lam) for x, p in zip(prizes, probs))
    return v ** (1 / (1 - g)) if v >= 0 else -((-v / lam) ** (1 / (1 - g)))


def ll(t):
    g = 1 / (1 + math.exp(-t[0]))
    lam, k = math.exp(t[1]), math.exp(t[2])
    s = 0.0
    for _, c, pa, qa, pb, qb in ANS:
        z = k * (pce(pa, qa, g, lam) - pce(pb, qb, g, lam)) / 10000.0
        s += -math.log1p(math.exp(-z)) if c == "A" else -math.log1p(math.exp(z))
    return s


def grad(t, h):
    out = []
    for i in range(3):
        u, d = list(t), list(t)
        u[i] += h
        d[i] -= h
        out.append((ll(u) - ll(d)) / (2 * h))
    return out


def hess_neg(t, h):
    H = [[0.0] * 3 for _ in range(3)]
    f0 = ll(t)
    for i in range(3):
        u, d = list(t), list(t)
        u[i] += h
        d[i] -= h
        H[i][i] = -(ll(u) - 2 * f0 + ll(d)) / (h * h)
    for i in range(3):
        for j in range(i + 1, 3):
            def sh(a, b):
                x = list(t)
                x[i] += a
                x[j] += b
                return ll(x)
            H[i][j] = H[j][i] = -(sh(h, h) - sh(h, -h) - sh(-h, h) + sh(-h, -h)) / (4 * h * h)
    return H


def solve3(A, b):
    M = [row[:] + [bb] for row, bb in zip(A, b)]
    for c in range(3):
        p = max(range(c, 3), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(3):
            if r != c:
                f = M[r][c] / M[c][c]
                M[r] = [a - f * bb for a, bb in zip(M[r], M[c])]
    return [M[i][3] / M[i][i] for i in range(3)]


def inv3(A):
    cols = [solve3(A, [1.0 if k == i else 0.0 for k in range(3)]) for i in range(3)]
    return [[cols[j][i] for j in range(3)] for i in range(3)]


# start from the estimate of the independent coordinate search (round-5 labs_recompute_r5.py)
t = [math.log(0.6352 / (1 - 0.6352)), math.log(6.1503), math.log(2.0201)]
for _ in range(50):
    g = grad(t, 1e-5)
    H = hess_neg(t, 1e-4)
    step = solve3(H, g)
    t = [x + s for x, s in zip(t, step)]
    if max(abs(s) for s in step) < 1e-10:
        break
gamma = 1 / (1 + math.exp(-t[0]))
lam, k = math.exp(t[1]), math.exp(t[2])
print(f"estimate: gamma {gamma:.6f} lambda {lam:.6f} kappa {k:.6f} loglik {ll(t):.6f}")
for h in (1e-4, 1e-5):
    cov = inv3(hess_neg(t, h))
    se_g = gamma * (1 - gamma) * math.sqrt(cov[0][0])
    se_l = lam * math.sqrt(cov[1][1])
    se_k = k * math.sqrt(cov[2][2])
    print(f"step {h:g}: se_gamma {se_g:.4f} se_lambda {se_l:.4f} se_kappa {se_k:.4f}")
print(f"largest score component (central difference 1e-5, coordinates): {max(abs(x) for x in grad(t, 1e-5)):.3e}")
print(f"largest score component (central difference 1e-6, coordinates): {max(abs(x) for x in grad(t, 1e-6)):.3e}")
