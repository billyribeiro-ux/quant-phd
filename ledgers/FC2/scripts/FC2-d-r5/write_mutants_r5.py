"""Write the three round-5 student-error mutants of the FC2 reference solution into ledgers/FC2/mutants/.

Usage: python3 -I ledgers/FC2/scripts/FC2-d-r5/write_mutants_r5.py <repo_root>
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
    "w5_a_parity_gap_truncated_toward_zero.py": (
        '"""Student error: the parity gap is cut to whole cents by int(), which truncates toward zero, not rounded.',
        "    return _half_up(gap)\n",
        "    return int(gap)\n",
    ),
    "w5_b_length_check_rejects_only_short_lists.py": (
        '"""Student error: the length check rejects a quote list that is shorter than the strikes, but not a longer one.',
        "    if len(calls) != len(strikes) or (puts is not None and len(puts) != len(strikes)):\n",
        "    if len(calls) < len(strikes) or (puts is not None and len(puts) < len(strikes)):\n",
    ),
    "w5_c_gross_rounded_up_to_ceiling.py": (
        '"""Student error: the gross amount of a finding is rounded up to the next whole cent, not to the nearest.',
        "        gross = _half_up(abs(gap))\n",
        "        gross = -(-abs(gap).numerator // abs(gap).denominator)\n",
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
