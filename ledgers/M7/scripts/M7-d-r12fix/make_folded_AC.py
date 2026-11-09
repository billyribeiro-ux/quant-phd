"""Second repair for alternatives A and C: fold gamma into the linear term, as alternatives D and E already do.

Usage: python -I make_folded_AC.py <repo_root>
Reads the refined copies written by make_repaired_AF.py and writes *_gamma_folded.py next to them. With gamma = 1e-9
the Hessian entries are of order 1e-11, below the absolute cutoffs of A (1e-12) and C (1e-10); folding divides the
linear term by gamma so the solved system has unit Hessian scale, and the multipliers are multiplied back by gamma.
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
out_dir = root / "ledgers/M7/scripts/M7-d-r12fix/alts_repaired"
OLD = (
    "def _solve(problem: Problem) -> dict[str, Any]:\n"
    "    n = problem.n\n"
    "    rows = _inequalities(problem)\n"
    "    x, mult, budget_mult = _active_set(problem, rows)\n"
)
NEW = (
    "def _solve(problem: Problem) -> dict[str, Any]:\n"
    "    n = problem.n\n"
    "    g = problem.gamma\n"
    "    # gamma folded into the linear term: the scaled problem has unit Hessian scale; multipliers scale back by gamma.\n"
    "    scaled = Problem(\n"
    "        problem.n, Fraction(1), [m / g for m in problem.mu], problem.sigma, problem.w0, problem.lower, problem.upper,\n"
    "        problem.sector, problem.caps, problem.tau,\n"
    "    )\n"
    "    rows = _inequalities(scaled)\n"
    "    x, mult, budget_mult = _active_set(scaled, rows)\n"
    "    mult = {k: v * g for k, v in mult.items()}\n"
    "    budget_mult = budget_mult * g\n"
)
for name in ("alt_A_r12fix_float_cutoff_1e-12_refined.py", "alt_C_r12fix_float_cutoff_1e-10_refined.py"):
    text = (out_dir / name).read_text(encoding="utf-8")
    assert text.count(OLD) == 1, name
    out = out_dir / name.replace("_refined.py", "_refined_gamma_folded.py")
    out.write_text(text.replace(OLD, NEW), encoding="utf-8")
    print(out.name)
