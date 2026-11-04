"""Write the four round-6 student-error mutants of the FC2 reference solution into ledgers/FC2/mutants/.

Usage: python3 -I ledgers/FC2/scripts/FC2-d-r6/write_mutants_r6.py <repo_root>
Each mutant is reference.py with exactly one line changed and the first docstring line replaced by the error.
The script asserts that each target line occurs exactly once, so each mutant differs by one line.
"""

import os
import sys

root = sys.argv[1]
ref = os.path.join(root, "course", "modules", "FC", "FC2", "grader", "reference.py")
text = open(ref, encoding="utf-8").read()
ref_first = '"""Reference solution for the FC2 project: the arbitrage scanner (scanner.py).'
assert text.startswith(ref_first)

mutants = {
    "w6_a_convexity_counts_call_on_chord.py": (
        '"""Student error: the convexity test counts a call that lies exactly on the chord as a violation, not only one above it.',
        "    return [j for j in range(1, len(strikes_cents) - 1) if _second_difference(strikes_cents, calls_cents, j) < 0]\n",
        "    return [j for j in range(1, len(strikes_cents) - 1) if _second_difference(strikes_cents, calls_cents, j) <= 0]\n",
    ),
    "w6_b_chord_weights_by_own_distance.py": (
        '"""Student error: the chord weights use the distance from the strike to its own neighbour, not to the other one.',
        "    w_low = Fraction(high - mid, high - low)\n    w_high = Fraction(mid - low, high - low)\n",
        "    w_low = Fraction(mid - low, high - low)\n    w_high = Fraction(high - mid, high - low)\n",
    ),
    "w6_c_finding_kept_when_net_is_zero.py": (
        '"""Student error: a finding is kept when its net amount is zero or more, not only when it is strictly positive.',
        "        if net > 0:\n            findings.append(\n                {\n                    \"kind\": \"parity\",\n",
        "        if net >= 0:\n            findings.append(\n                {\n                    \"kind\": \"parity\",\n",
    ),
    "w6_d_half_spread_charged_once_per_finding.py": (
        '"""Student error: the half-spread is charged once per finding, while the fee is charged on each of the three legs.',
        "    per_finding = LEGS_PER_FINDING * (fee + spread)\n",
        "    per_finding = LEGS_PER_FINDING * fee + spread\n",
    ),
}
for name, (first, old, new) in mutants.items():
    assert text.count(old) == 1, (name, text.count(old))
    body = text.replace(old, new, 1)
    body = body.replace(ref_first, first, 1)
    dest = os.path.join(root, "ledgers", "FC2", "mutants", name)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(body)
    print("wrote", dest)
