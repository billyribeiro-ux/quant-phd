"""Verifier round-1: check the grader comment's cross-term numbers (test_project.py lines 43-48).

The comment says: "A matched factor applied to one asset only, or one chi-square variable per asset, moves the cross term
by about 29 % and 15 % (measured at seeds 0 to 9). The tolerance 0.05 lies between them." This script measures the
relative change of the cross term (the same statistic the suite uses: w1 = w2 = 10^6, cov 4e-4, 4.8e-4, 9e-4, nu = 5,
100,000 draws, same seed) for the two variants, at seeds 0 to 9, and for the reference's own error.
Run from the checkout root: .venv/bin/python -I ledgers/M4/scripts/M4-d-r1/verifyD1_cross_term_effect.py
"""

from __future__ import annotations

import importlib.util
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/M/M4/grader"
spec = importlib.util.spec_from_file_location("reference", GRADER / "reference.py")
assert spec is not None and spec.loader is not None
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)
sys.path.insert(0, str(GRADER))


def sample_variance(xs: list[int]) -> float:
    mean = math.fsum(xs) / len(xs)
    return math.fsum((x - mean) ** 2 for x in xs) / (len(xs) - 1)


def one_chi_per_asset(positions: list[int], cov: list[list[float]], n_draws: int, seed: int, nu: int) -> list[int]:
    """Reference model except each asset draws its own chi-square variable (the variant named in the comment)."""
    factor = ref._cholesky(cov, 2)
    rng = random.Random(seed)
    matched = (nu - 2) / nu
    out: list[int] = []
    for _ in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(2)]
        total = 0.0
        for i in range(2):
            chi = rng.gammavariate(nu / 2, 2.0)
            scale = math.sqrt(matched * nu / chi)
            ret = scale * sum(factor[i][k] * z[k] for k in range(i + 1))
            total += positions[i] * ret
        out.append(round(-total))
    return out


def matched_on_asset_one_only(positions: list[int], cov: list[list[float]], n_draws: int, seed: int, nu: int) -> list[int]:
    """Reference model except the matched factor is applied to asset 1 only (asset 2 is left unmatched)."""
    factor = ref._cholesky(cov, 2)
    rng = random.Random(seed)
    matched = (nu - 2) / nu
    out: list[int] = []
    for _ in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(2)]
        chi = rng.gammavariate(nu / 2, 2.0)
        base = math.sqrt(nu / chi)
        rets = [
            math.sqrt(matched) * base * factor[0][0] * z[0],
            base * (factor[1][0] * z[0] + factor[1][1] * z[1]),
        ]
        out.append(round(-(positions[0] * rets[0] + positions[1] * rets[1])))
    return out


def cross_term_ratio(make) -> float:  # type: ignore[no-untyped-def]
    w1 = w2 = 1_000_000
    cov = [[4e-4, 4.8e-4], [4.8e-4, 9e-4]]
    target = 4.0 * w1 * w2 * cov[0][1]
    plus = make([w1, w2], cov, 100_000, seed, 5)
    minus = make([w1, -w2], cov, 100_000, seed, 5)
    return (sample_variance(plus) - sample_variance(minus)) / target


def reference_model(positions: list[int], cov: list[list[float]], n_draws: int, seed: int, nu: int) -> list[int]:
    return ref.simulate_losses(positions, cov, n_draws, seed, "student_t", nu)


def main() -> int:
    variants = {
        "reference": reference_model,
        "one chi-square per asset": one_chi_per_asset,
        "matched factor on asset 1 only": matched_on_asset_one_only,
    }
    for name, make in variants.items():
        ratios = []
        for seed in range(10):
            globals()["seed"] = seed
            ratios.append(cross_term_ratio(make))
        worst = max(abs(r - 1.0) for r in ratios)
        print(f"{name}: cross-term ratio to target over seeds 0-9: min {min(ratios):.4f} max {max(ratios):.4f}; "
              f"largest |ratio - 1| {worst:.4f}")
    return 0


seed = 0

if __name__ == "__main__":
    raise SystemExit(main())
