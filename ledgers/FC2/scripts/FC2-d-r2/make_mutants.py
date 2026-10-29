"""Write six round-2 student-error mutants (m41-m46) from the reference solution, one replacement each.

Each replacement must match exactly once in the reference, or the script stops.
Usage: python3 ledgers/FC2/scripts/FC2-d-r2/make_mutants.py <checkout>
"""

from __future__ import annotations

import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/FC/FC2/grader/reference.py").read_text(encoding="utf-8")

MUTANTS = {
    "m41_cost_charged_on_two_legs": (
        "Student error: each finding is charged two legs of fee plus half-spread instead of three.",
        [("per_finding = LEGS_PER_FINDING * (fee + spread)", "per_finding = 2 * (fee + spread)")],
    ),
    "m42_convexity_gross_floored": (
        "Student error: the convexity gross is floored, so a 0.5-cent or 1.5-cent violation loses its half cent.",
        [
            (
                "gross = _half_up(-_second_difference(strikes, calls, j))",
                "gross = (-_second_difference(strikes, calls, j)) // 1",
            )
        ],
    ),
    "m43_convexity_findings_reversed": (
        "Student error: convexity findings are emitted in reverse strike order (the loop walks the indices backwards).",
        [
            (
                "for j in convexity_violations(strikes, calls, df_ppm):",
                "for j in reversed(convexity_violations(strikes, calls, df_ppm)):",
            )
        ],
    ),
    "m44_convexity_explanation_without_P1": (
        "Student error: the convexity explanation omits the European-exercise label P1 it depends on.",
        [('"convexity in strike (P1 European exercise, P2 one expiry, "', '"convexity in strike (P2 one expiry, "')],
    ),
    "m45_call_discounted_in_parity": (
        "Student error: the call is discounted by df in the parity gap, as if it were a payment at expiry.",
        [
            (
                "gap = Fraction(calls[k]) - Fraction(puts[k])",
                "gap = Fraction(calls[k]) * Fraction(df_ppm, PPM) - Fraction(puts[k])",
            )
        ],
    ),
    "m46_spread_charged_once": (
        "Student error: the half-spread is charged once per finding while the fee is charged on each of three legs.",
        [("per_finding = LEGS_PER_FINDING * (fee + spread)", "per_finding = LEGS_PER_FINDING * fee + spread")],
    ),
}

out_dir = root / "ledgers/FC2/mutants"
for name, (doc, replacements) in MUTANTS.items():
    text = ref
    for old, new in replacements:
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"{name}: expected one match for {old!r}, found {count}")
        text = text.replace(old, new)
    end = text.index('"""', 3) + 3  # the reference module docstring is replaced by the mutant description
    text = f'"""{doc}\n"""' + text[end:]
    (out_dir / f"{name}.py").write_text(text, encoding="utf-8")
    print("wrote", name)
