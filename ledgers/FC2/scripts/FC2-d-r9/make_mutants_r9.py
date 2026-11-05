"""Write round-9 student-error mutants of the FC2 reference into ledgers/FC2/mutants/ (each exactly one edit)."""

import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref = (root / "course/modules/FC/FC2/grader/reference.py").read_text(encoding="utf-8")
out = root / "ledgers/FC2/mutants"

EDITS = {
    "y9_a_discounted_strike_rounded_to_cent.py": (
        "Student error: the discounted strike K df is rounded to a whole cent before the parity gap is formed, so the gap is rounded twice.",
        [
            (
                '    gap = Fraction(call_cents) - Fraction(put_cents) - (Fraction(spot_cents) - Fraction(strike_cents * df_ppm, PPM))',
                '    gap = Fraction(call_cents) - Fraction(put_cents) - (Fraction(spot_cents) - _half_up(Fraction(strike_cents * df_ppm, PPM)))',
            ),
            (
                '        gap = Fraction(calls[k]) - Fraction(puts[k]) - (Fraction(spot) - Fraction(strike * df_ppm, PPM))',
                '        gap = Fraction(calls[k]) - Fraction(puts[k]) - (Fraction(spot) - _half_up(Fraction(strike * df_ppm, PPM)))',
            ),
        ],
    ),
    "y9_b_convexity_chord_rounded_before_comparison.py": (
        "Student error: the chord is rounded to a whole cent before the call is compared with it, so the convexity gross is taken from a rounded chord.",
        [
            (
                '    return [j for j in range(1, len(strikes_cents) - 1) if _second_difference(strikes_cents, calls_cents, j) < 0]',
                '    return [j for j in range(1, len(strikes_cents) - 1) if _half_up(_second_difference(strikes_cents, calls_cents, j)) < 0]',
            ),
        ],
    ),
    "y9_c_convexity_trades_two_legs.py": (
        "Student error: a convexity finding is charged two legs of cost, as if the wings were one call, instead of three calls.",
        [
            (
                '        net = gross - per_finding\n        if net > 0:\n            findings.append(\n                {\n                    "kind": "convexity"',
                '        net = gross - 2 * (fee + spread)\n        if net > 0:\n            findings.append(\n                {\n                    "kind": "convexity"',
            ),
        ],
    ),
    "y9_d_convexity_kept_at_zero_net.py": (
        "Student error: a convexity finding is kept when its net amount is zero, while parity findings still need a strictly positive net.",
        [
            (
                '        net = gross - per_finding\n        if net > 0:\n            findings.append(\n                {\n                    "kind": "convexity"',
                '        net = gross - per_finding\n        if net >= 0:\n            findings.append(\n                {\n                    "kind": "convexity"',
            ),
        ],
    ),
}

for name, (doc, edits) in EDITS.items():
    text = ref
    for old, new in edits:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    body = text.split('"""', 2)
    assert body[0] == "" and len(body) >= 3
    text = '"""' + doc + '"""' + body[2]
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name)
