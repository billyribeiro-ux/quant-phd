"""Exact-precision (60-digit Decimal) observed information and standard errors for a fixed set of responses."""
import sys, json
from decimal import Decimal as D, getcontext
from fractions import Fraction
sys.path.insert(0, "/tmp/E3d_r10_ws/ref")
import elicit as sol
from instance import make_instance
getcontext().prec = 60

def dec(q):  # Fraction -> Decimal
    return D(q.numerator) / D(q.denominator)

def parse(r):
    pa = [int(x) for x in r["prizes_a"]]; qa = [Fraction(str(s)) for s in r["probs_a"]]
    pb = [int(x) for x in r["prizes_b"]]; qb = [Fraction(str(s)) for s in r["probs_b"]]
    return pa, qa, pb, qb, r["choice"]

def ce(prizes, probs, gamma, lam):
    e = 1 - gamma
    total = sum((dec(p) * (D(x) ** e if x >= 0 else -lam * (D(-x) ** e)) for x, p in zip(prizes, probs)), D(0))
    if total >= 0:
        return total ** (1 / e)
    return -((-total / lam) ** (1 / e))

def loglik(parsed, zeta, la, lk):
    gamma = 1 / (1 + (-zeta).exp())
    lam, kappa = la.exp(), lk.exp()
    tot = D(0)
    for pa, qa, pb, qb, ch in parsed:
        z = kappa * (ce(pa, qa, gamma, lam) - ce(pb, qb, gamma, lam)) / D(10000)
        tot += -((1 + (-z).exp()).ln()) if ch == "A" else -((1 + z.exp()).ln())
    return tot

def inv3(m):
    n = 3
    aug = [row[:] + [D(1) if i == j else D(0) for j in range(n)] for i, row in enumerate(m)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(aug[r][c]))
        aug[c], aug[p] = aug[p], aug[c]
        d = aug[c][c]
        aug[c] = [x / d for x in aug[c]]
        for r in range(n):
            if r != c:
                f = aug[r][c]
                aug[r] = [x - f * y for x, y in zip(aug[r], aug[c])]
    return [row[n:] for row in aug]

def exact_se(responses, est, h=D("1e-15")):
    parsed = [parse(r) for r in responses]
    g, l, k = D(repr(est["gamma_hat"])), D(repr(est["lambda_hat"])), D(repr(est["kappa_hat"]))
    th = [(g / (1 - g)).ln(), l.ln(), k.ln()]
    def at(*mv):
        y = list(th)
        for i, a in mv:
            y[i] += a
        return loglik(parsed, y[0], y[1], y[2])
    f0 = at()
    info = [[D(0)] * 3 for _ in range(3)]
    for i in range(3):
        info[i][i] = -(at((i, h)) - 2 * f0 + at((i, -h))) / (h * h)
        for j in range(i + 1, 3):
            v = -(at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h))) / (4 * h * h)
            info[i][j] = info[j][i] = v
    cov = inv3(info)
    gam = g
    out = {
        "diag_cov": [float(cov[i][i]) for i in range(3)],
        "se_gamma": float(gam * (1 - gam) * cov[0][0].sqrt()),
        "se_lambda": float(l * cov[1][1].sqrt()),
        "se_kappa": float(k * cov[2][2].sqrt()),
        "eig_info_min": None,
    }
    # gradient size at the float estimate (should be ~0)
    return out, info

if __name__ == "__main__":
    for seed in (49, 0):
        inst = make_instance(seed)
        resp = json.loads(inst["responses_json"])
        est = sol.estimate(resp)
        print("seed", seed, "ref est", {k: round(v, 6) for k, v in est.items() if k != "log_likelihood"}, flush=True)
        out, info = exact_se(resp, est)
        print("seed", seed, "EXACT (60-digit) SE:", {k: v for k, v in out.items() if k.startswith("se_")}, flush=True)
        print("seed", seed, "EXACT diag cov", out["diag_cov"], flush=True)
        print("seed", seed, "info diag", [float(info[i][i]) for i in range(3)], flush=True)
