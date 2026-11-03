"""Round-2 verifier: three new student-error mutants of the M7 allocator, each a complete module derived from reference.py
by one edit, written to ledgers/M7/mutants/. Each edit is asserted to match exactly once."""
import pathlib

GRADER = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD2-M7-d/course/modules/M/M7/grader")
OUT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD2-M7-d/ledgers/M7/mutants")
REF = (GRADER / "reference.py").read_text(encoding="utf-8")

MUTANTS = {
    "d2_01_sector_membership_taken_from_position_not_label": (
        "Student error d2_01: asset i is placed in sector i mod Z instead of the sector label the case gives it, so every sector cap applies to the wrong assets.",
        "    if any(label not in sector for label in range(len(caps))):\n",
        "    sector = [i % len(caps) for i in range(n)]  # the position, not the label\n    if any(label not in sector for label in range(len(caps))):\n",
    ),
    "d2_02_complementary_slackness_turnover_rows_at_zero_displacement": (
        "Student error d2_02: the complementary-slackness residual evaluates the two turnover rows at t = 0 (d_i and minus d_i) instead of at t_i = |d_i|, so a binding turnover multiplier is reported as a slackness violation.",
        "        *[d[i] - t[i] for i in range(n)],\n                *[-d[i] - t[i] for i in range(n)],\n",
        "        *[d[i] for i in range(n)],\n                *[-d[i] for i in range(n)],\n",
    ),
    "d2_03_negative_turnover_multipliers_never_dropped": (
        "Student error d2_03: the active-set rule drops a working constraint only when its multiplier is negative and it is a bound or sector row, so a negative turnover multiplier stays in the answer.",
        "            negative = [(lam[1 + k], k) for k in range(len(working)) if lam[1 + k] < 0]\n",
        "            negative = [(lam[1 + k], k) for k in range(len(working)) if lam[1 + k] < 0 and rows[working[k]][2][0] != 'turn']\n",
    ),
}

for name, (doc, old, new) in MUTANTS.items():
    body = REF
    assert body.count(old) == 1, (name, body.count(old))
    body = body.replace(old, new)
    # replace the reference's module docstring by the mutant's one-line description (first line)
    start = body.index('"""')
    end = body.index('"""', start + 3) + 3
    body = '"""' + doc + '\n\nVerifier-written wrong solution: reference.py with the single edit described above.\n"""' + body[end:]
    (OUT / f"{name}.py").write_text(body, encoding="utf-8")
    print("wrote", name)
