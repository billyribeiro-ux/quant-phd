"""Build three alternative correct allocators from the reference (verifier helper, round 10).

Alt A and Alt C: the reference's active-set search in float arithmetic with two different zero cutoffs (1e-12 and
1e-10); the spec tolerances (1e-9 on the start checks) are kept. Alt B: exact Fraction arithmetic, but the working set
starts empty and the negative-multiplier rule drops the LAST negative working row instead of the most negative one.
Run from the checkout root: python ledgers/M7/scripts/M7-d-r10/make_alts.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = (ROOT / "course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M7/scripts/M7-d-r10/alts"


def float_version(eps: str, normalize: bool = False) -> str:
    text = SRC
    if normalize:
        # Solve the problem divided by gamma (gamma = 1, mu / gamma), so the cutoffs see O(1) Hessian entries; the
        # multipliers of the scaled problem are multiplied back by gamma, and the certificate uses the original problem.
        old = "    rows = _inequalities(problem)\n    x, mult, budget_mult = _active_set(problem, rows)"
        assert old in text
        text = text.replace(
            old,
            "    g = problem.gamma\n"
            "    scaled = Problem(problem.n, Fraction(1), [m / g for m in problem.mu], problem.sigma, problem.w0,"
            " problem.lower, problem.upper, problem.sector, problem.caps, problem.tau)\n"
            "    rows = _inequalities(scaled)\n"
            "    x, mult, budget_mult = _active_set(scaled, rows)\n"
            "    mult = {k: v * g for k, v in mult.items()}\n"
            "    budget_mult = budget_mult * g",
        )
    text = text.replace("from fractions import Fraction\n", "Fraction = float  # verifier alternative: float arithmetic\n")
    text = text.replace("TOL = Fraction(1, 10**9)", "TOL = 1e-9")
    text = text.replace("rows[r][col] != 0", f"abs(rows[r][col]) > {eps}")
    text = text.replace("if all(v == 0 for v in p):", f"if all(abs(v) <= {eps} for v in p):")
    text = text.replace("if lam[1 + k] < 0]", f"if lam[1 + k] < -{eps}]")
    text = text.replace("if rate > 0:", f"if rate > {eps}:")
    text = text.replace("if abs(sum(w0, Fraction(0)) - 1) > TOL:", "if abs(sum(w0, 0.0) - 1) > TOL:")
    return text


def exact_empty_start() -> str:
    text = SRC
    text = text.replace(
        "if b - _dot(a, x) <= TOL and _rank([budget, *(rows[k][0] for k in working), a]) > len(working) + 1:",
        "if False:",
    )
    text = text.replace("working.pop(min(negative)[1])", "working.pop(negative[-1][1])")
    return text


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "alt_A_float_cutoff_1e-12.py").write_text(float_version("1e-12"), encoding="utf-8")
    (OUT / "alt_C_float_cutoff_1e-10.py").write_text(float_version("1e-10"), encoding="utf-8")
    (OUT / "alt_D_float_1e-12_gamma_folded.py").write_text(float_version("1e-12", normalize=True), encoding="utf-8")
    (OUT / "alt_E_float_1e-10_gamma_folded.py").write_text(float_version("1e-10", normalize=True), encoding="utf-8")
    (OUT / "alt_B_exact_empty_start_last_drop.py").write_text(exact_empty_start(), encoding="utf-8")
    for name in ("alt_A_float_cutoff_1e-12.py", "alt_C_float_cutoff_1e-10.py", "alt_B_exact_empty_start_last_drop.py",
                 "alt_D_float_1e-12_gamma_folded.py", "alt_E_float_1e-10_gamma_folded.py"):
        print("wrote", OUT / name)


if __name__ == "__main__":
    main()
