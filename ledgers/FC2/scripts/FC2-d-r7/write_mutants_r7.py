"""Write four round-7 student-error mutants of the FC2 reference solution into ledgers/FC2/mutants/.

Usage: python3 -I ledgers/FC2/scripts/FC2-d-r7/write_mutants_r7.py <repo_root>
Each mutant is reference.py with exactly one line changed (the target text is asserted to occur once) and the first
docstring line replaced by the error description.
"""

import os
import sys

root = sys.argv[1]
ref = os.path.join(root, "course", "modules", "FC", "FC2", "grader", "reference.py")
text = open(ref, encoding="utf-8").read()
ref_first = '"""Reference solution for the FC2 project: the arbitrage scanner (scanner.py).'
assert text.startswith(ref_first)

mutants = {
    "s7_a_parity_gap_discounts_the_spot.py": (
        '"""Student error: the parity gap discounts the spot price (S df - K) instead of the strike (S - K df).',
        "    return _half_up(gap)\n",
        "    return _half_up(gap)\n",
        "(Fraction(spot_cents) - Fraction(strike_cents * df_ppm, PPM))",
        "(Fraction(spot_cents * df_ppm, PPM) - Fraction(strike_cents))",
    ),
    "s7_b_convexity_loop_runs_past_last_strike.py": (
        '"""Student error: the convexity scan runs over every index after the first, including the last strike.',
        "    return [j for j in range(1, len(strikes_cents) - 1) if _second_difference(strikes_cents, calls_cents, j) < 0]\n",
        "    return [j for j in range(1, len(strikes_cents)) if _second_difference(strikes_cents, calls_cents, j) < 0]\n",
        None,
        None,
    ),
    "s7_c_convexity_net_omits_half_spread.py": (
        '"""Student error: a convexity finding is netted against three legs at the fee only, without the half-spread.',
        "        gross = _half_up(-_second_difference(strikes, calls, j))\n        net = gross - per_finding\n",
        "        gross = _half_up(-_second_difference(strikes, calls, j))\n        net = gross - LEGS_PER_FINDING * fee\n",
        None,
        None,
    ),
    "s7_d_parity_gap_floors_the_signed_gap.py": (
        '"""Student error: the signed parity gap is rounded down (floor), so a negative gap rounds away from zero.',
        "    return _half_up(gap)\n",
        "    return gap.numerator // gap.denominator\n",
        None,
        None,
    ),
}
for name, (first, old, new, old2, new2) in mutants.items():
    if old2 is not None:
        assert text.count(old2) == 1, (name, "old2", text.count(old2))
        body = text.replace(old2, new2, 1)
    else:
        body = text
    assert body.count(old) == 1, (name, "old", body.count(old))
    body = body.replace(old, new, 1)
    body = body.replace(ref_first, first, 1)
    dest = os.path.join(root, "ledgers", "FC2", "mutants", name)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(body)
    print("wrote", dest)
