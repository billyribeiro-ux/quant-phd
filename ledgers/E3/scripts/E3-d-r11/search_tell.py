"""Round-11: random participants (own generator, seeded) to search for an input where a mutant's estimate fails the
page's score tolerance (2e-5 at step 1e-5 or 1e-6) while the reference passes. usage: search_tell.py <dir> <n> <rng-seed>"""
import importlib.util
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

work, n, rseed = Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
sys.path.insert(0, str(work))
import test_project as tp  # noqa: E402

rng = random.Random(rseed)


def lottery(k_max: int):
    k = rng.randint(1, k_max)
    prizes = rng.sample(range(-20000, 20001, 100), k)
    cuts = sorted(rng.sample(range(1, 20), k - 1)) if k > 1 else []
    nums = [b - a for a, b in zip([0] + cuts, cuts + [20])]
    probs = [Fraction(x, 20) for x in nums]
    return prizes, [str(p) for p in probs]


def make(nq: int):
    out = []
    for i in range(nq):
        pa, qa = lottery(3)
        pb, qb = lottery(3)
        out.append({"pair_id": i, "prizes_a": pa, "probs_a": qa, "prizes_b": pb, "probs_b": qb, "choice": "A"})
    return out


worst_bad = []
for trial in range(n):
    nq = rng.randint(12, 40)
    resp = make(nq)
    gamma, lam, kappa = rng.uniform(0.05, 0.9), rng.uniform(0.5, 8.0), rng.uniform(0.2, 30.0)
    for r in resp:
        pa, qa, pb, qb = tp.parse(r)[:4]
        ce = tp.oracle_prospect(pa, qa, gamma, lam) - tp.oracle_prospect(pb, qb, gamma, lam)
        z = kappa * ce / 10_000.0
        r["choice"] = "A" if rng.random() < 1.0 / (1.0 + math.exp(-max(-50, min(50, z)))) else "B"
    parsed = [tp.parse(r) for r in resp]
    if not any(tp.mixed(pa, qa) or tp.mixed(pb, qb) for pa, qa, pb, qb, _ in parsed):
        continue
    try:
        est = tp.sol.estimate(resp)
    except Exception as err:  # the suite does not check these; record and move on
        print("trial", trial, "raised", type(err).__name__, flush=True)
        continue
    g, l, k = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
    score = min(tp._largest_score_component(parsed, g, l, k, 1e-5), tp._largest_score_component(parsed, g, l, k, 1e-6))
    if score > 2e-5:
        worst_bad.append((trial, nq, score, g, l, k))
        print("BAD trial", trial, "nq", nq, f"score {score:.3e}", f"g {g:.4f} l {l:.4f} k {k:.4f}", flush=True)
print("done", n, "bad", len(worst_bad), flush=True)
