import json, math, sys
sys.path.insert(0, sys.argv[1])
from instance import make_instance
import elicit as sol
from fractions import Fraction

inst = make_instance(49)
RESP = json.loads(inst["responses_json"])

def parse(r):
    return ([int(x) for x in r["prizes_a"]], [Fraction(s) for s in r["probs_a"]],
            [int(x) for x in r["prizes_b"]], [Fraction(s) for s in r["probs_b"]], r["choice"])

def ce(prizes, probs, gamma, lam):
    total = sum(float(p) * (math.pow(float(x), 1 - gamma) if x >= 0 else -lam * math.pow(float(-x), 1 - gamma)) for x, p in zip(prizes, probs))
    return math.pow(total, 1 / (1 - gamma)) if total >= 0 else -math.pow(-total / lam, 1 / (1 - gamma))

def loglik(parsed, gamma, lam, kappa):
    t = 0.0
    for pa, qa, pb, qb, c in parsed:
        z = kappa * (ce(pa, qa, gamma, lam) - ce(pb, qb, gamma, lam)) / 10000.0
        t += -math.log1p(math.exp(-z)) if c == "A" else -math.log1p(math.exp(z))
    return t

def info(parsed_list, theta, h):
    def at(*moves):
        y = list(theta)
        for idx, amt in moves: y[idx] += amt
        return loglik(parsed_list, 1 / (1 + math.exp(-y[0])), math.exp(y[1]), math.exp(y[2]))
    f0 = at(); I = [[0.0]*3 for _ in range(3)]
    for i in range(3):
        I[i][i] = -(at((i, h)) - 2*f0 + at((i, -h))) / (h*h)
        for j in range(i+1, 3):
            I[i][j] = I[j][i] = -(at((i,h),(j,h)) - at((i,h),(j,-h)) - at((i,-h),(j,h)) + at((i,-h),(j,-h))) / (4*h*h)
    return I

def inv3(m):
    aug = [list(r) + [1.0 if i == j else 0.0 for j in range(3)] for i, r in enumerate(m)]
    for col in range(3):
        piv = max(range(col, 3), key=lambda r: abs(aug[r][col])); aug[col], aug[piv] = aug[piv], aug[col]
        d = aug[col][col]; aug[col] = [x/d for x in aug[col]]
        for r in range(3):
            if r != col:
                f = aug[r][col]; aug[r] = [x - f*y for x, y in zip(aug[r], aug[col])]
    return [r[3:] for r in aug]

est = sol.estimate(RESP)
g, l, k = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
print("reference estimate seed 49:", g, l, k, "se_lambda", est["se_lambda"])
theta = [math.log(g/(1-g)), math.log(l), math.log(k)]
parsed = [parse(r) for r in RESP]
rev = list(reversed(parsed))
for h in (1e-5, 1e-6):
    cov_f = inv3(info(parsed, theta, h)); cov_r = inv3(info(rev, theta, h))
    se_f = l * math.sqrt(cov_f[1][1]); se_r = l * math.sqrt(cov_r[1][1])
    gs_f = g*(1-g)*math.sqrt(cov_f[0][0]); gs_r = g*(1-g)*math.sqrt(cov_r[0][0])
    print(f"h={h:g} se_lambda forward {se_f:.4f} reversed {se_r:.4f} change {100*(se_r-se_f)/se_f:+.2f}% | se_gamma forward {gs_f:.5f}")
