import sys, json, math, os
G = "/Users/billyribeiro/.fanout/wt/verifyD7-E3-d/course/modules/E/E3/grader"
sys.path.insert(0, "/Users/billyribeiro/.fanout/scratch-E3-d-r7/work")
import shutil
shutil.copy(G + "/reference.py", "/Users/billyribeiro/.fanout/scratch-E3-d-r7/work/elicit.py")
shutil.copy(G + "/instance.py", "/Users/billyribeiro/.fanout/scratch-E3-d-r7/work/instance.py")
import elicit as sol
from instance import make_instance
from fractions import Fraction
from collections.abc import Callable

def parse(r):
    return ([int(x) for x in r["prizes_a"]], [Fraction(s) for s in r["probs_a"]],
            [int(x) for x in r["prizes_b"]], [Fraction(s) for s in r["probs_b"]], r["choice"])

def ll_xi(xi, parsed, order="fwd"):
    gamma = 1.0 / (1.0 + math.exp(-xi[0])); lam = math.exp(xi[1]); kappa = math.exp(xi[2])
    total = 0.0
    seq = parsed if order == "fwd" else list(reversed(parsed))
    for pa, qa, pb, qb, ch in seq:
        ca = sol._prospect_ce(pa, qa, gamma, lam); cb = sol._prospect_ce(pb, qb, gamma, lam)
        z = kappa * (ca - cb) / 10000.0
        total += -math.log1p(math.exp(-z)) if ch == "A" else -math.log1p(math.exp(z))
    return total

def oinfo(xi, parsed, h, order):
    f = lambda t: ll_xi(t, parsed, order)
    info = [[0.0]*3 for _ in range(3)]
    def at(*moves):
        y = list(xi)
        for idx, a in moves: y[idx] += a
        return f(y)
    f0 = at()
    for i in range(3):
        info[i][i] = -(at((i,h)) - 2*f0 + at((i,-h)))/(h*h)
        for j in range(i+1,3):
            v = -(at((i,h),(j,h)) - at((i,h),(j,-h)) - at((i,-h),(j,h)) + at((i,-h),(j,-h)))/(4*h*h)
            info[i][j] = info[j][i] = v
    return info

def inv3(m):
    aug = [list(r) + [1.0 if i==j else 0.0 for j in range(3)] for i, r in enumerate(m)]
    for c in range(3):
        p = max(range(c,3), key=lambda r: abs(aug[r][c])); aug[c], aug[p] = aug[p], aug[c]
        d = aug[c][c]; aug[c] = [x/d for x in aug[c]]
        for r in range(3):
            if r != c:
                fct = aug[r][c]; aug[r] = [x - fct*y for x, y in zip(aug[r], aug[c])]
    return [row[3:] for row in aug]

inst = make_instance(49)
resp = json.loads(inst["responses_json"])
parsed = [parse(r) for r in resp]
fit = sol.estimate(resp)
g, l, k = fit["gamma_hat"], fit["lambda_hat"], fit["kappa_hat"]
print("seed49 truth", inst["gamma"], inst["lambda"], inst["kappa"], "wealth", inst["wealth_cents"])
print("seed49 estimate", g, l, k, {x: fit[x] for x in ("se_gamma","se_lambda","se_kappa")})
xi = [math.log(g/(1-g)), math.log(l), math.log(k)]
for h in (1e-5, 1e-6):
    for order in ("fwd", "rev"):
        cov = inv3(oinfo(xi, parsed, h, order))
        se_g = g*(1-g)*math.sqrt(cov[0][0]); se_l = l*math.sqrt(cov[1][1]); se_k = k*math.sqrt(cov[2][2])
        print("h", h, order, "se_gamma %.5f se_lambda %.2f se_kappa %.2f" % (se_g, se_l, se_k))
# also the instance's own true-parameter check on seed 30 and kappa
i30 = make_instance(30)
print("seed30 kappa", i30["kappa"], "gamma", i30["gamma"], "lambda", i30["lambda"])
