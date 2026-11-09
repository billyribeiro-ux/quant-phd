"""Probe for ruling 32: converged fits with gamma_hat in [LO, HI] and their local-maximum check (0.1 percent moves,
no gain above 1e-9).

Usage (repo root): .venv/bin/python -I <this file> <grader directory> LO HI TRUTH,TRUTH,...
"""

import itertools
import math
import os
import random
import sys
from fractions import Fraction

sys.path.insert(0, sys.argv[1])
LO, HI = float(sys.argv[2]), float(sys.argv[3])
TRUTHS = tuple(float(t) for t in sys.argv[4].split(","))
import reference as ref  # noqa: E402


def lottery(rng: random.Random, mixed: bool) -> tuple[list[int], list[Fraction]]:
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


def sim(seed: int, gamma: float, lam: float, kappa: float, n: int) -> list[dict[str, object]]:
    rng = random.Random(seed)
    recs: list[dict[str, object]] = []
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


rows = []
for g, lam, k, n, seed in itertools.product(TRUTHS, (1.0, 2.0, 4.0), (1.0, 5.0, 20.0), (12, 26), (1, 2)):
    recs = sim(seed, g, lam, k, n)
    try:
        r = ref.estimate(recs)
    except Exception as err:
        rows.append(("ERR", g, lam, k, n, seed, type(err).__name__))
        continue
    gh, lh, kh = r["gamma_hat"], r["lambda_hat"], r["kappa_hat"]
    if not LO <= gh <= HI:
        rows.append(("OUT", g, lam, k, n, seed, round(gh, 6)))
        continue
    here = ref.log_likelihood(recs, {"gamma": gh, "lambda": lh, "kappa": kh})
    worst = -math.inf
    for step in (1e-3, -1e-3):
        for dg, dl, dk in ((gh * (1 + step), lh, kh), (gh, lh * (1 + step), kh), (gh, lh, kh * (1 + step))):
            if not 0 < dg < 1:
                continue
            worst = max(worst, ref.log_likelihood(recs, {"gamma": dg, "lambda": dl, "kappa": dk}) - here)
    rows.append(("FIT", g, lam, k, n, seed, round(gh, 6), f"{worst:.3e}", "PASS" if worst <= 1e-9 else "FAIL"))

for row in rows:
    print(*row)
fits = [r for r in rows if r[0] == "FIT"]
print(
    f"in-range fits (gamma_hat in [{LO}, {HI}]):",
    len(fits),
    "| local-max PASS:",
    sum(r[-1] == "PASS" for r in fits),
    "| FAIL:",
    sum(r[-1] == "FAIL" for r in fits),
    "| errors:",
    sum(r[0] == "ERR" for r in rows),
    "| outside:",
    sum(r[0] == "OUT" for r in rows),
    "| pid",
    os.getpid(),
)
