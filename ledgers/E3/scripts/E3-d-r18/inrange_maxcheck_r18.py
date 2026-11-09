"""Ruling 32 check (verifier, round 18): simulated participants whose reference estimate lies in the stated range
[0.001, 0.99] (and just above it, for contrast) are put through the suite's own shared checks,
tests/_assert_estimate_is_a_maximum (score, reported likelihood, 0.1 percent local-maximum move), imported from the
pinned test_project.py. A failing in-range estimate would contradict the page's stated range.

Usage (repo root): .venv/bin/python -I ledgers/E3/scripts/E3-d-r18/inrange_maxcheck_r18.py <out.txt>
"""

import concurrent.futures as cf
import itertools
import math
import os
import random
import shutil
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

ROOT = Path(os.getcwd()).resolve()
GRADER = ROOT / "course/modules/E/E3/grader"
W = Path(tempfile.mkdtemp(prefix="e3d-r18-inrange-"))
for name in ("test_project.py", "instance.py"):
    shutil.copy(GRADER / name, W / name)
shutil.copy(GRADER / "reference.py", W / "elicit.py")
sys.path.insert(0, str(W))
os.environ["QF_SEED"] = "0"
os.environ["PYTHONHASHSEED"] = "0"
import elicit as ref  # noqa: E402
import test_project as tp  # noqa: E402


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


def job(cfg: tuple[float, float, float, int, int]) -> str:
    g, lam, k, n, seed = cfg
    recs = sim(seed, g, lam, k, n)
    tag = f"truth={g} lam={lam} kappa={k} n={n} seed={seed}"
    try:
        r = ref.estimate(recs)
    except Exception as err:  # the reference raises on some participants: no estimate, nothing to check
        return f"ERR {tag} {type(err).__name__}"
    gh = r["gamma_hat"]
    if not (0.97 <= gh <= 1.0):
        return f"OUT {tag} gamma_hat={gh:.6f}"
    zone = "IN" if gh <= 0.99 else "ABOVE"
    try:
        tp._assert_estimate_is_a_maximum(recs)
        verdict = "PASS"
    except BaseException as err:  # pytest.fail raises a Failed exception
        verdict = "FAIL " + str(getattr(err, "msg", err))[:120]
    return f"{zone} {verdict} {tag} gamma_hat={gh:.6f} lam_hat={r['lambda_hat']:.4f} kappa_hat={r['kappa_hat']:.4f}"


if __name__ == "__main__":
    out = sys.argv[1]
    truths = (0.96, 0.975, 0.98, 0.985, 0.99, 0.995)
    cfgs = list(itertools.product(truths, (1.0, 2.0), (5.0, 20.0, 50.0), (12, 26), range(1, 41)))
    with cf.ProcessPoolExecutor(max_workers=24) as ex:
        lines = list(ex.map(job, cfgs, chunksize=4))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    shutil.rmtree(W, ignore_errors=True)
    print("rows", len(lines))
