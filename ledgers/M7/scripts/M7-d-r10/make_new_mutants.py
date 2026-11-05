"""Write the verifier's new student-error mutants for M7-d (round 10) as complete solution modules.

Each mutant is the reference solution with one plausible student error. Written to ledgers/M7/mutants/r10_*.py.
Run from the checkout root: python ledgers/M7/scripts/M7-d-r10/make_new_mutants.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = (ROOT / "course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M7/mutants"

MUTANTS: dict[str, tuple[str, str, str]] = {
    "r10_01_sector_multipliers_divided_by_sector_size.py": (
        "Student error r10_01: the sector multipliers are reported divided by the number of assets in their sector, "
        "a per-asset convention the page does not use.",
        '        "sector": [float(v) for v in sol["sector"]],',
        '        "sector": [float(v) / max(1, sum(1 for s in problem_sector(sol) if s == k)) '
        'for k, v in enumerate(sol["sector"])],',
    ),
    "r10_02_budget_multiplier_read_from_asset_zero.py": (
        "Student error r10_02: the budget multiplier is read off asset 0 alone, as mu[0] minus gamma times the first row "
        "of Sigma times w, ignoring every other multiplier in that row.",
        '        "budget": float(sol["budget"]),',
        '        "budget": float(sol["budget_from_asset_zero"]),',
    ),
    "r10_03_lower_multipliers_reported_as_zero.py": (
        "Student error r10_03: the lower-bound multipliers are never reported; the output lists zero for every asset, "
        "so the weight stationarity fails wherever a lower bound binds.",
        '        "lower": [float(v) for v in sol["lower"]],',
        '        "lower": [0.0 for _ in sol["lower"]],',
    ),
}

HELPERS = '''

def problem_sector(sol: dict[str, Any]) -> list[int]:
    return list(sol["sector_of_asset"])


def budget_from_asset_zero(problem: Problem, w: list[Fraction], sol: dict[str, Any]) -> Fraction:
    grad0 = problem.gamma * _dot(problem.sigma[0], w) - problem.mu[0]
    return -grad0
'''


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (doc, old, new) in MUTANTS.items():
        text = SRC.replace('"""Reference solution', f'"""{doc}\n\nReference solution', 1)
        assert old in text, name
        text = text.replace(old, new)
        if "problem_sector" in new:
            text = text.replace("def _solve(problem: Problem) -> dict[str, Any]:", HELPERS.strip() + "\n\n\ndef _solve(problem: Problem) -> dict[str, Any]:", 1)
            text = text.replace('        "w": x,', '        "w": x,\n        "sector_of_asset": problem.sector,', 1)
        if "budget_from_asset_zero" in new:
            text = text.replace("def _solve(problem: Problem) -> dict[str, Any]:", HELPERS.strip() + "\n\n\ndef _solve(problem: Problem) -> dict[str, Any]:", 1)
            text = text.replace('        "w": x,', '        "w": x,\n        "budget_from_asset_zero": budget_from_asset_zero(problem, x, {}),', 1)
        (OUT / name).write_text(text, encoding="utf-8")
        print("wrote", OUT / name)


if __name__ == "__main__":
    main()
