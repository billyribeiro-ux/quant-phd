# Independent re-derivation of the numbers quoted in project.html and test_project.py docstrings.
import sys, json, math
from fractions import Fraction
G = "/Users/billyribeiro/.fanout/wt/verifyD8-E3-d/course/modules/E/E3/grader"
sys.path.insert(0, G)
import instance, reference
from instance import make_instance

def value(x, g, l):
    return math.pow(x, 1 - g) if x >= 0 else -l * math.pow(-x, 1 - g)

def ce(prizes, probs, g, l):
    t = sum(float(p) * value(x, g, l) for x, p in zip(prizes, probs))
    return math.pow(t, 1 / (1 - g)) if t >= 0 else -math.pow(-t / l, 1 / (1 - g))

def ll(parsed, g, l, k):
    tot = 0.0
    for pa, qa, pb, qb, c in parsed:
        z = k * (ce(pa, qa, g, l) - ce(pb, qb, g, l)) / 10000.0
        tot += -math.log1p(math.exp(-z)) if c == "A" else -math.log1p(math.exp(z))
    return tot

def parse(r):
    return ([int(x) for x in r["prizes_a"]], [Fraction(s) for s in r["probs_a"]],
            [int(x) for x in r["prizes_b"]], [Fraction(s) for s in r["probs_b"]], r["choice"])

# (1) LOW_KAPPA and the seed windows
i30 = make_instance(30)
print("seed30 kappa:", i30["kappa"], "kappa<1:", i30["kappa"] < 1, "gamma", i30["gamma"], "lambda", i30["lambda"], "wealth", i30["wealth_cents"])

# (2) seed 49 standard errors at step 1e-5 and 1e-6 from the oracle, at the reference estimate
inst = make_instance(49)
resp = json.loads(inst["responses_json"])
parsed = [parse(r) for r in resp]
est = reference.estimate(resp)
print("seed49 estimate:", {k: round(v, 6) for k, v in est.items()})
g, l, k = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
theta = [math.log(g / (1 - g)), math.log(l), math.log(k)]
def f(t):
    return ll(parsed, 1 / (1 + math.exp(-t[0])), math.exp(t[1]), math.exp(t[2]))
def info(h):
    def at(*moves):
        y = list(theta)
        for idx, amt in moves:
            y[idx] += amt
        return f(y)
    f0 = at()
    M = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        M[i][i] = -(at((i, h)) - 2 * f0 + at((i, -h))) / (h * h)
        for j in range(i + 1, 3):
            v = -(at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h))) / (4 * h * h)
            M[i][j] = M[j][i] = v
    return M
def inv3(M):
    A = [list(r) + [1.0 if i == j else 0.0 for j in range(3)] for i, r in enumerate(M)]
    for c in range(3):
        p = max(range(c, 3), key=lambda r: abs(A[r][c]))
        A[c], A[p] = A[p], A[c]
        d = A[c][c]
        A[c] = [x / d for x in A[c]]
        for r in range(3):
            if r != c:
                fac = A[r][c]
                A[r] = [x - fac * y for x, y in zip(A[r], A[c])]
    return [row[3:] for row in A]
for h in (1e-5, 1e-6):
    C = inv3(info(h))
    se_g = g * (1 - g) * math.sqrt(C[0][0]); se_l = l * math.sqrt(C[1][1]); se_k = k * math.sqrt(C[2][2])
    print(f"step {h:g}: se_gamma={se_g:.5f} se_lambda={se_l:.4f} se_kappa={se_k:.4f}")
    if h == 1e-5:
        base = (se_g, se_l)
    else:
        print(f"  rel change se_lambda 1e-5->1e-6: {100*(se_l-base[1])/base[1]:.2f}%  se_gamma: {100*(se_g-base[0])/base[0]:.2f}%")
