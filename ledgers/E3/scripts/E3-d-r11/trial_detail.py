"""Round-11: regenerate the search_tell.py participants (same rng seed) and report, for trials 8, 31, 47, the engine's output or error."""
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

work = Path(sys.argv[1])
sys.path.insert(0, str(work))
import test_project as tp  # noqa: E402

rng = random.Random(11)


def lottery(k_max):
    k = rng.randint(1, k_max)
    prizes = rng.sample(range(-20000, 20001, 100), k)
    cuts = sorted(rng.sample(range(1, 20), k - 1)) if k > 1 else []
    nums = [b - a for a, b in zip([0] + cuts, cuts + [20])]
    return prizes, [str(Fraction(x, 20)) for x in nums]


def make(nq):
    out = []
    for i in range(nq):
        pa, qa = lottery(3)
        pb, qb = lottery(3)
        out.append({"pair_id": i, "prizes_a": pa, "probs_a": qa, "prizes_b": pb, "probs_b": qb, "choice": "A"})
    return out


for trial in range(60):
    nq = rng.randint(12, 40)
    resp = make(nq)
    gamma, lam, kappa = rng.uniform(0.05, 0.9), rng.uniform(0.5, 8.0), rng.uniform(0.2, 30.0)
    for r in resp:
        pa, qa, pb, qb = tp.parse(r)[:4]
        ce = tp.oracle_prospect(pa, qa, gamma, lam) - tp.oracle_prospect(pb, qb, gamma, lam)
        z = kappa * ce / 10_000.0
        r["choice"] = "A" if rng.random() < 1.0 / (1.0 + math.exp(-max(-50, min(50, z)))) else "B"
    if trial not in (8, 31, 47):
        continue
    parsed = [tp.parse(r) for r in resp]
    print("trial", trial, "nq", nq, "true gamma %.4f lambda %.4f kappa %.4f" % (gamma, lam, kappa))
    try:
        est = tp.sol.estimate(resp)
        g, l, k = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
        s = min(tp._largest_score_component(parsed, g, l, k, 1e-5), tp._largest_score_component(parsed, g, l, k, 1e-6))
        print("   estimate g %r l %r k %r score %.3e se_l %.4g" % (g, l, k, s, est["se_lambda"]))
        here = tp.oracle_loglik(parsed, g, l, k)
        lm = max(tp.oracle_loglik(parsed, g * (1 + d), l, k) - here for d in (1e-3, -1e-3))
        lm = max(lm, max(tp.oracle_loglik(parsed, g, l * (1 + d), k) - here for d in (1e-3, -1e-3)))
        lm = max(lm, max(tp.oracle_loglik(parsed, g, l, k * (1 + d)) - here for d in (1e-3, -1e-3)))
        print("   local-max excess (must be <= 1e-9): %.3e" % lm)
    except Exception as err:
        print("   raised", type(err).__name__, str(err)[:120])
