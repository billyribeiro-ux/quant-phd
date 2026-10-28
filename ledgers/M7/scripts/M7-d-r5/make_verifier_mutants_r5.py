"""Write the verifier's own student-error mutants of the M7 reference (round 5, slice d, verifier).

Each mutant is grader/reference.py with one replaced text; every search text must occur exactly once.
Usage: python3 make_verifier_mutants_r5.py <checkout-root>
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
REFERENCE = ROOT / "course/modules/M/M7/grader/reference.py"
OUT = ROOT / "ledgers/M7/mutants"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "z01_start_box_checked_without_tolerance": (
        "Student error z01: the starting weights are compared with the bounds with no 1e-9 tolerance, so a start "
        "5e-10 outside a bound is refused although the page allows it.",
        [("    if any(w0[i] < lower[i] - TOL or w0[i] > upper[i] + TOL for i in range(n)):",
          "    if any(w0[i] < lower[i] or w0[i] > upper[i] for i in range(n)):")],
    ),
    "z02_start_sector_cap_checked_without_tolerance": (
        "Student error z02: the starting sector sums are compared with the caps with no tolerance, so a start that "
        "sits 5e-10 over a cap is refused although the page allows it.",
        [("        if sum(w0[i] for i in range(n) if sector[i] == k) > cap + TOL:",
          "        if sum(w0[i] for i in range(n) if sector[i] == k) > cap:")],
    ),
    "z03_allocate_prints_a_trace": (
        "Student error z03: allocate prints a progress line before it returns, which the page's silence rule forbids.",
        [("    problem = _parse(instance)\n", "    print('solving')\n    problem = _parse(instance)\n")],
    ),
    "z04_allocate_marks_its_argument": (
        "Student error z04: allocate writes a cache key into the instance it receives, so the argument changes.",
        [("    problem = _parse(instance)\n", "    instance['_cache'] = True\n    problem = _parse(instance)\n")],
    ),
    "z05_certificate_hard_coded_to_zero": (
        "Student error z05: the certificate fields are typed in as zero instead of being computed from the weights "
        "and multipliers.",
        [('        "certificate": _certificate(problem, sol),',
          '        "certificate": {"primal_residual": 0.0, "stationarity_residual": 0.0, '
          '"dual_residual": 0.0, "complementary_slackness": 0.0},')],
    ),
    "z06_sector_multiplier_sign_flipped_in_stationarity": (
        "Student error z06: the sector multiplier enters the weight stationarity with the wrong sign in the certificate.",
        [('+ sol["sector"][problem.sector[i]]', '- sol["sector"][problem.sector[i]]')],
    ),
    "z07_weights_returned_in_reverse_order": (
        "Student error z07: allocate returns the weights in reverse asset order, so each weight is paired with the "
        "wrong asset.",
        [('        "weights": [float(v) for v in sol["w"]],', '        "weights": [float(v) for v in sol["w"][::-1]],')],
    ),
    "z08_turnover_measured_from_uniform_portfolio": (
        "Student error z08: the turnover limit is measured from an equal-weight portfolio instead of the starting "
        "portfolio w0.",
        [("rows.append((a, problem.tau + _dot(a, problem.w0), (\"turn\", signs)))",
          "rows.append((a, problem.tau + _dot(a, [Fraction(1, problem.n)] * problem.n), (\"turn\", signs)))")],
    ),
}


def main() -> None:
    source = REFERENCE.read_text(encoding="utf-8")
    for name, (description, replacements) in MUTANTS.items():
        text = source
        for old, new in replacements:
            count = text.count(old)
            if count != 1:
                raise SystemExit(f"{name}: search text occurs {count} times: {old!r}")
            text = text.replace(old, new)
        _, _, rest = text.partition('"""')
        _, _, body = rest.partition('"""')
        mutant = f'"""{description}\n\nOne change to grader/reference.py, written by the M7 verifier (round 5).\n"""' + body
        (OUT / f"{name}.py").write_text(mutant, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
