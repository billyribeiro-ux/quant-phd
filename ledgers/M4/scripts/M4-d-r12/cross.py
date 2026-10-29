import sys, math, random, statistics
sys.path.insert(0, "/tmp/M4-d-r12-scratch/ws")
import tail_risk as sol
from fractions import Fraction

def fsum_var(xs):
    m = math.fsum(xs) / len(xs)
    return math.fsum((x - m) ** 2 for x in xs) / (len(xs) - 1)

NU, DRAWS = 5, 100_000
cov = [[4e-4, 4.8e-4], [4.8e-4, 9e-4]]
L = sol._cholesky(cov, 2)

def sim(pos, seed, mode):
    """mode 'ref' (matched, one chi per draw), 'one_asset' (matched factor on asset 1 only),
    'per_asset_chi' (matched factor, a separate chi-square per asset)."""
    rng = random.Random(seed)
    s = (NU - 2) / NU
    out = []
    for _ in range(DRAWS):
        z = [rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0)]
        if mode == "per_asset_chi":
            c1 = rng.gammavariate(NU / 2, 2.0); c2 = rng.gammavariate(NU / 2, 2.0)
            sc = [math.sqrt(s * NU / c1), math.sqrt(s * NU / c2)]
        else:
            c = rng.gammavariate(NU / 2, 2.0)
            if mode == "one_asset":
                sc = [math.sqrt(s * NU / c), math.sqrt(NU / c)]
            else:
                sc = [math.sqrt(s * NU / c), math.sqrt(s * NU / c)]
        r1 = sc[0] * (L[0][0] * z[0])
        r2 = sc[1] * (L[1][0] * z[0] + L[1][1] * z[1])
        out.append(round(-(pos[0] * r1 + pos[1] * r2)))
    return out

def cross(seed, mode):
    w1, w2 = 1_000_000, 1_000_000
    target = 4.0 * w1 * w2 * cov[0][1]
    plus = sim([w1, w2], seed, mode)
    minus = sim([w1, -w2], seed, mode)
    measured = fsum_var(plus) - fsum_var(minus)
    return abs(measured / target - 1)

ref = []
for seed in range(50):
    ref.append(cross(seed, "ref"))
print("reference cross-term max rel err seeds 0-49:", round(max(ref), 4), "mean", round(sum(ref)/len(ref), 4), flush=True)
for mode in ("one_asset", "per_asset_chi"):
    vals = [cross(seed, mode) for seed in range(10)]
    print(mode, "seeds 0-9 rel dev from target: mean", round(sum(vals)/len(vals), 4), "min", round(min(vals), 4), "max", round(max(vals), 4), flush=True)
print("ref seeds 0-9 values", [round(x, 4) for x in ref[:10]])
# truncation vs rounding variance of a N(0,4) loss (cents), exact quadrature
nd = statistics.NormalDist(0, 2)
def expect(f, lo=-40, hi=40, n=400000):
    h = (hi - lo) / n
    tot = 0.0
    for k in range(n):
        x = lo + (k + 0.5) * h
        tot += f(x) * nd.pdf(x) * h
    return tot
e_trunc2 = expect(lambda x: int(x) ** 2)
e_trunc1 = expect(lambda x: int(x))
print("truncation variance (E[int(X)^2]-E[int(X)]^2):", round(e_trunc2 - e_trunc1**2, 4))
e_round2 = expect(lambda x: round(x) ** 2); e_round1 = expect(lambda x: round(x))
print("rounding variance:", round(e_round2 - e_round1**2, 4), "vs 4+1/12 =", round(4 + 1/12, 4))
