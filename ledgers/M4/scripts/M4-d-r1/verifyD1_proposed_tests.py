"""Verifier round-1 proposed grader tests for the M4 suite (NOT added to the grader; the verifier may not edit it).

Each test is stream-free: it checks a closed-form or distributional property that every conforming implementation
satisfies whatever random stream it uses, and it is run against the reference, the five alternatives and the
survivors of mutate_graders.py. Usage (from the checkout root):

    .venv/bin/python ledgers/M4/scripts/M4-d-r1/verifyD1_proposed_tests.py <solution.py> --seeds 0-49

It prints PASS or FAIL per test per seed window, so a proposed test is accepted only if it passes the reference and
all five alternatives, and fails the mutant it is meant to kill.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import os
import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/M/M4/grader"
sys.path.insert(0, str(GRADER))
from instance import make_instance  # noqa: E402


def load_solution(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("tail_risk_under_test", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def mean_abs_t(nu: int) -> float:
    """E|T| for a Student-t with nu > 1 degrees of freedom: 2 sqrt(nu) Gamma((nu+1)/2) / (sqrt(pi) (nu-1) Gamma(nu/2))."""
    return 2.0 * math.sqrt(nu) * math.gamma((nu + 1) / 2) / (math.sqrt(math.pi) * (nu - 1) * math.gamma(nu / 2))


def proposed_student_t_mean_absolute_loss(sol: ModuleType, seed: int) -> None:
    """For every nu of 3 to 8, E|loss| = w sigma sqrt(s) E|T_nu| with s = (nu - 2) / nu (matched scale), within 5 %."""
    w = 1_000_000
    sigma = math.sqrt(4e-4)
    for nu in range(3, 9):
        target = w * sigma * math.sqrt((nu - 2) / nu) * mean_abs_t(nu)
        losses = sol.simulate_losses([w], [[4e-4]], 20_000, seed, "student_t", nu)
        measured = sum(abs(x) for x in losses) / len(losses)
        check(abs(measured / target - 1.0) <= 0.05, f"student_t |loss| at nu={nu} misses the matched-scale value")


def proposed_student_t_draws_do_not_share_chi_square(sol: ModuleType, seed: int) -> None:
    """Draws (2k, 2k+1) and (2k+1, 2k+2) are independent: P(both |loss| above the median) is 1/4 within 5 SE."""
    n = 40_000
    losses = sol.simulate_losses([1_000_000], [[4e-4]], n, seed, "student_t", 3)
    magnitudes = [abs(x) for x in losses]
    median = sorted(magnitudes)[n // 2]
    above = [m > median for m in magnitudes]
    se = math.sqrt(0.25 * 0.75 / (n // 2))
    for offset in (0, 1):
        pairs = [(above[i], above[i + 1]) for i in range(offset, n - 1, 2)]
        share = sum(a and b for a, b in pairs) / len(pairs)
        check(abs(share - 0.25) <= 5 * se, f"draws at offset {offset} share a chi-square variable (dependent scales)")


def proposed_quantile_index_is_exact_for_instance_draws(sol: ModuleType, seed: int) -> None:
    """Sanity: round-1 proposal for the index check on every instance draw count (not needed for the kills)."""
    for n in (6_003, 8_001, 9_997, 12_011, 15_013, 19_987):
        losses = list(range(1, n + 1))
        check(sol.quantile_99(losses) == (99 * n + 99) // 100, "quantile index differs at an instance draw count")


TESTS: list[tuple[str, Callable[[ModuleType, int], None]]] = [
    ("proposed_student_t_mean_absolute_loss", proposed_student_t_mean_absolute_loss),
    ("proposed_student_t_draws_do_not_share_chi_square", proposed_student_t_draws_do_not_share_chi_square),
    ("proposed_quantile_index_is_exact_for_instance_draws", proposed_quantile_index_is_exact_for_instance_draws),
]


def parse_seeds(text: str) -> list[int]:
    lo, _, hi = text.partition("-")
    return list(range(int(lo), int(hi or lo) + 1))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("solution", type=Path)
    parser.add_argument("--seeds", default="0-9")
    args = parser.parse_args()
    sol = load_solution(args.solution)
    failing: dict[str, list[int]] = {}
    for seed in parse_seeds(args.seeds):
        make_instance(seed)  # the instance module is used only to confirm the seed is valid for the grader
        for name, test in TESTS:
            try:
                test(sol, seed)
            except AssertionError:
                failing.setdefault(name, []).append(seed)
    for name, _ in TESTS:
        seeds = failing.get(name, [])
        print(f"{name}: {'FAIL' if seeds else 'PASS'} ({len(parse_seeds(args.seeds)) - len(seeds)}/{len(parse_seeds(args.seeds))} seeds ok)")
    print(f"solution {args.solution.name}: {'REJECTED by a proposed test' if failing else 'ACCEPTED by all proposed tests'}")
    return 0


if __name__ == "__main__":
    os.environ.setdefault("PYTHONHASHSEED", "0")
    raise SystemExit(main())
