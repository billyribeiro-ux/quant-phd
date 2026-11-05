"""Verifier r10: re-derive the numbers quoted in grader docstrings and comments with the reference solution and my own oracle."""
import json, math, sys
from fractions import Fraction as F
GRADER = "/Users/billyribeiro/.fanout/wt/verifyD10-E3-e/course/modules/E/E3/grader"
sys.path.insert(0, GRADER)
import reference as ref
from instance import make_instance

def parse(r):
    return ([int(x) for x in r["prizes_a"]], [F(s) for s in r["probs_a"]], [int(x) for x in r["prizes_b"]], [F(s) for s in r["probs_b"]], r["choice"])

def v(x, g, lam):
    return x**(1-g) if x >= 0 else -lam*((-x)**(1-g))

def ce(pr, pb, g, lam):
    t = sum(float(p)*v(x, g, lam) for x, p in zip(pr, pb))
    return t**(1/(1-g)) if t >= 0 else -((-t/lam)**(1/(1-g)))

def ll(parsed, g, lam, kap, order=None):
    seq = parsed if order is None else parsed[::-1]
    s = 0.0
    for pa, qa, pb, qb, c in seq:
        z = kap*(ce(pa, qa, g, lam) - ce(pb, qb, g, lam))/10000.0
        s += -math.log1p(math.exp(-z)) if c == "A" else -math.log1p(math.exp(z))
    return s

def obs_info(parsed, theta, h, rev=False):
    def at(*mv):
        y = list(theta)
        for i, a in mv: y[i] += a
        g = 1/(1+math.exp(-y[0]))
        return ll(parsed, g, math.exp(y[1]), math.exp(y[2]), order=(1 if rev else None))
    f0 = at(); I = [[0.0]*3 for _ in range(3)]
    for i in range(3):
        I[i][i] = -(at((i, h)) - 2*f0 + at((i, -h)))/(h*h)
        for j in range(i+1, 3):
            I[i][j] = I[j][i] = -(at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h)))/(4*h*h)
    return I

def inv3(m):
    import numpy as np
    return np.linalg.inv(np.array(m)).tolist()

def ses(parsed, est, h, rev=False):
    g, l, k = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
    th = [math.log(g/(1-g)), math.log(l), math.log(k)]
    C = inv3(obs_info(parsed, th, h, rev))
    return g*(1-g)*math.sqrt(C[0][0]), l*math.sqrt(C[1][1]), k*math.sqrt(C[2][2])

# seed 49 (LARGE_LAMBDA) and seed 30 (LOW_KAPPA)
for seed in (30, 49):
    inst = make_instance(seed)
    resp = json.loads(inst["responses_json"])
    est = ref.estimate(resp)
    print("seed", seed, {k: round(v_, 6) for k, v_ in est.items()}, "true", inst["gamma"], inst["lambda"], inst["kappa"])
    parsed = [parse(r) for r in resp]
    if seed == 49:
        for h in (1e-5, 1e-6):
            print("  h", h, "SE gamma, lambda, kappa (forward):", [round(x, 5) for x in ses(parsed, est, h)])
            print("  h", h, "SE (reverse order):", [round(x, 5) for x in ses(parsed, est, h, rev=True)])
