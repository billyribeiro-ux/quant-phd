"""Measures the local-maximum check of one converged fit above 0.99 (gamma truth 0.99, lambda 1, kappa 20, 26 answers,
simulation seed 2) with the reference, and prints the largest increase from a 0.1 percent move.

Usage (repo root): .venv/bin/python -I ledgers/E3/scripts/fixer-d-r15/fit_0994_localmax.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "course/modules/E/E3/grader"))
import math  # noqa: E402
import random  # noqa: E402
from fractions import Fraction  # noqa: E402

import reference as ref  # noqa: E402


def lottery(rng, mixed):  # type: ignore[no-untyped-def]
    count = rng.choice((2, 3))
    d = rng.choice((4, 5, 10, 20))
    cuts = sorted(rng.sample(range(1, d), count - 1))
    b = [0, *cuts, d]
    probs = [Fraction(b[k + 1] - b[k], d) for k in range(count)]
    mags = [rng.randrange(500, 50001) for _ in range(count)]
    if mixed:
        signs = [1, -1, *(rng.choice((1, -1)) for _ in range(count - 2))]
        rng.shuffle(signs)
    else:
        signs = [1] * count
    return [s * m for s, m in zip(signs, mags, strict=True)], probs


def sim(seed, gamma, lam, kappa, n):  # type: ignore[no-untyped-def]
    rng = random.Random(seed)
    recs = []
    for i in range(n):
        pa, qa = lottery(rng, rng.random() < 0.6)
        ce_a = ref._prospect_ce(pa, qa, gamma, lam)
        cands = [lottery(rng, rng.random() < 0.6) for _ in range(30)]
        target = ce_a + rng.uniform(-5000, 5000)
        pb, qb = min(cands, key=lambda c: abs(ref._prospect_ce(c[0], c[1], gamma, lam) - target))
        ce_b = ref._prospect_ce(pb, qb, gamma, lam)
        p = 1 / (1 + math.exp(-kappa * (ce_a - ce_b) / 10000.0))
        choice = "A" if rng.random() < p else "B"
        recs.append(
            {
                "pair_id": i,
                "choice": choice,
                "prizes_a": pa,
                "probs_a": [str(q) for q in qa],
                "prizes_b": pb,
                "probs_b": [str(q) for q in qb],
            }
        )
    return recs


recs = sim(2, 0.99, 1.0, 20.0, 26)
r = ref.estimate(recs)
gh, lh, kh = r["gamma_hat"], r["lambda_hat"], r["kappa_hat"]
here = ref.log_likelihood(recs, {"gamma": gh, "lambda": lh, "kappa": kh})
worst = {}
for step in (1e-3, -1e-3):
    moves = {
        "gamma": {"gamma": gh * (1 + step), "lambda": lh, "kappa": kh},
        "lambda": {"gamma": gh, "lambda": lh * (1 + step), "kappa": kh},
        "kappa": {"gamma": gh, "lambda": lh, "kappa": kh * (1 + step)},
    }
    for name, p in moves.items():
        d = ref.log_likelihood(recs, p) - here
        worst[name] = max(worst.get(name, -1e300), d)
print(f"gamma_hat {gh:.6f} lambda_hat {lh:.4f} kappa_hat {kh:.4f}")
print("largest increase from a 0.1 percent move:", {k: f"{v:.3e}" for k, v in worst.items()})
print("bound 1e-9; local-maximum check fails:", max(worst.values()) > 1e-9)
