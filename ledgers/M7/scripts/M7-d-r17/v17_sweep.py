"""Verifier sweep (round 17): run the M7 reference on page-valid cases and recheck every output from the definitions.

Independent of reference._certificate: residuals are recomputed here from the weights and multipliers the reference
returns, in exact Fraction arithmetic on the decimal inputs. Usage: python -I v17_sweep.py <repo_root> <n_random> <n_seeds>
"""

import importlib.util
import json
import random
import sys
from fractions import Fraction
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
N_RANDOM = int(sys.argv[2])
N_SEEDS = int(sys.argv[3])
GRADER = ROOT / "course/modules/M/M7/grader"
spec = importlib.util.spec_from_file_location("ref17", GRADER / "reference.py")
ref = importlib.util.module_from_spec(spec)
sys.modules["ref17"] = ref
spec.loader.exec_module(ref)  # type: ignore[union-attr]
sys.path.insert(0, str(GRADER))
from instance import make_instance  # noqa: E402

TOL = 1e-8
AGREE = 1e-9


def F(x):
    return Fraction(repr(float(x)))


def check(case, out):
    """Return a list of failure strings (empty when the output passes every definition)."""
    fails = []
    n = len(case["mu"])
    w = out["weights"]
    m = out["multipliers"]
    c = out["certificate"]
    w0 = [F(v) for v in case["w0"]]
    lo = [F(v) for v in case["lower"]]
    up = [F(v) for v in case["upper"]]
    caps = [F(v) for v in case["sector_caps"]]
    sec = case["sector"]
    tau = F(case["turnover_limit"])
    gamma = F(case["gamma"])
    sigma = [[F(v) for v in row] for row in case["sigma"]]
    mu = [F(v) for v in case["mu"]]
    wf = [Fraction(v) for v in w]
    d = [wf[i] - w0[i] for i in range(n)]
    t = [abs(v) for v in d]
    sums = [sum((wf[i] for i in range(n) if sec[i] == k), Fraction(0)) for k in range(len(caps))]
    gaps = []
    for i in range(n):
        gaps += [lo[i] - wf[i], wf[i] - up[i], d[i] - t[i], -d[i] - t[i]]
    gaps += [sums[k] - caps[k] for k in range(len(caps))]
    gaps.append(sum(t, Fraction(0)) - tau)
    primal = max([Fraction(0), abs(sum(wf) - 1), *gaps])
    lower_m, upper_m, sector_m = [Fraction(v) for v in m["lower"]], [Fraction(v) for v in m["upper"]], [Fraction(v) for v in m["sector"]]
    plus_m, minus_m = [Fraction(v) for v in m["turnover_plus"]], [Fraction(v) for v in m["turnover_minus"]]
    kappa = Fraction(m["turnover_total"])
    budget = Fraction(m["budget"])
    ineq_m = [*lower_m, *upper_m, *sector_m, *plus_m, *minus_m, kappa]
    ineq_g = [*[lo[i] - wf[i] for i in range(n)], *[wf[i] - up[i] for i in range(n)],
              *[sums[k] - caps[k] for k in range(len(caps))], *[d[i] - t[i] for i in range(n)],
              *[-d[i] - t[i] for i in range(n)], sum(t, Fraction(0)) - tau]
    dual = max(Fraction(0), -min(ineq_m))
    comp = max(abs(a * b) for a, b in zip(ineq_m, ineq_g, strict=True))
    stat = Fraction(0)
    for i in range(n):
        grad = gamma * sum((sigma[i][j] * wf[j] for j in range(n)), Fraction(0)) - mu[i]
        r_w = grad + budget - lower_m[i] + upper_m[i] + sector_m[sec[i]] + plus_m[i] - minus_m[i]
        r_t = kappa - plus_m[i] - minus_m[i]
        stat = max(stat, abs(r_w), abs(r_t))
    if float(primal) > TOL: fails.append(f"primal {float(primal):.3e}")
    if float(stat) > TOL: fails.append(f"stationarity {float(stat):.3e}")
    if float(dual) > TOL: fails.append(f"dual {float(dual):.3e}")
    if float(comp) > TOL: fails.append(f"comp {float(comp):.3e}")
    if any(float(v) < -TOL for v in ineq_m): fails.append("negative multiplier beyond tol")
    for key, val in (("primal_residual", primal), ("stationarity_residual", stat), ("dual_residual", dual),
                     ("complementary_slackness", comp)):
        if abs(c[key] - float(val)) > AGREE: fails.append(f"agree {key} {c[key]} vs {float(val):.3e}")
    return fails


def random_case(rng):
    n = rng.randint(1, 5)
    z = rng.randint(1, min(2, n))
    sector = [rng.randrange(z) for _ in range(n)]
    for k in range(z):
        if k not in sector:
            sector[rng.randrange(n)] = k
    # start: thousandths summing exactly to 1000
    while True:
        cuts = sorted(rng.randint(0, 1000) for _ in range(n - 1))
        parts = [b - a for a, b in zip([0, *cuts], [*cuts, 1000], strict=True)]
        if all(p >= 0 for p in parts):
            break
    w0k = parts
    w0 = [k / 1000 for k in w0k]
    lower = [round(rng.choice([-1.0, -0.5, -0.1, 0.0, rng.randint(-300, 100) / 1000]), 3) for _ in range(n)]
    upper = [round(max(w0[i], rng.choice([2.0, 1.0, w0[i], w0[i] + 0.001 * rng.randint(0, 50)])), 3) for i in range(n)]
    lower = [min(lower[i], w0[i]) for i in range(n)]
    upper = [max(upper[i], w0[i]) for i in range(n)]
    caps = []
    for k in range(z):
        s_k = sum(w0k[i] for i in range(n) if sector[i] == k)
        caps.append(round((s_k + rng.choice([0, 0, 1, 50, 300])) / 1000, 3) if rng.random() < 0.7 else 2.0)
    # keep caps at or above the start sums (exact)
    caps = [max(c, sum(w0k[i] for i in range(n) if sector[i] == k) / 1000) for k, c in enumerate(caps)]
    a = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n + rng.randint(0, 2))]
    sigma = [[sum(a[r][i] * a[r][j] for r in range(len(a))) / 1000 + (1 / 1000 if i == j else 0) for j in range(n)] for i in range(n)]
    sigma = [[round(v, 6) for v in row] for row in sigma]
    mu = [rng.randint(-1000, 1000) / 1000 for _ in range(n)]
    gamma = rng.choice([1e-9, 1e-6, 0.5, 1.0, 3.0, 1000.0, 1e6, rng.uniform(0.01, 10)])
    tau = rng.choice([0.0, 1e-9, 1e-6, 0.05, 0.5, 2.0, round(rng.uniform(0, 1), 3)])
    case = {"gamma": gamma, "mu": mu, "sigma": sigma, "w0": w0, "lower": lower, "upper": upper,
            "sector": sector, "sector_caps": caps, "turnover_limit": tau}
    return case


def run_case(item):
    tag, case = item
    try:
        out = ref.allocate(json.loads(json.dumps(case)))
    except Exception as exc:  # the reference must not raise on a page-valid case
        return tag, [f"raised {type(exc).__name__}: {exc}"], case
    return tag, check(case, out), case


if __name__ == "__main__":
    rng = random.Random(1717)
    items = [(f"seed{s}", json.loads(make_instance(s)["payload"])) for s in range(N_SEEDS)]
    items += [(f"rand{i}", random_case(rng)) for i in range(N_RANDOM)]
    with Pool(20) as pool:
        results = pool.map(run_case, items, chunksize=8)
    bad = [(tag, f) for tag, f, _ in results if f]
    n_seed = sum(1 for tag, _ in items if tag.startswith("seed"))
    print(f"cases {len(items)} (generator seeds {n_seed}, random {len(items) - n_seed}); failing {len(bad)}")
    for tag, f in bad[:25]:
        print("FAIL", tag, f)
