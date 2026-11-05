"""Write round-10 student-error mutants of the FC2 reference into ledgers/FC2/mutants/ (each exactly one edit)."""

import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref = (root / "course/modules/FC/FC2/grader/reference.py").read_text(encoding="utf-8")
out = root / "ledgers/FC2/mutants"

EDITS = {
    "z10_a_strike_of_one_cent_rejected.py": (
        "Student error: parity_gap_cents rejects a strike of 1 cent, using strike < 2 as the test for a positive strike.",
        [
            (
                "    if isinstance(strike_cents, bool) or not isinstance(strike_cents, int) or strike_cents <= 0:",
                "    if isinstance(strike_cents, bool) or not isinstance(strike_cents, int) or strike_cents < 2:",
            ),
        ],
    ),
    "z10_b_df_upper_bound_exclusive.py": (
        "Student error: df_ppm = 1000000 is rejected, because the upper bound test uses < instead of <= (the range is 1 to 1000000).",
        [
            (
                "    if isinstance(df_ppm, bool) or not isinstance(df_ppm, int) or not DF_MIN <= df_ppm <= DF_MAX:",
                "    if isinstance(df_ppm, bool) or not isinstance(df_ppm, int) or not DF_MIN <= df_ppm < DF_MAX:",
            ),
        ],
    ),
    "z10_c_zero_half_spread_rejected.py": (
        "Student error: a half-spread of exactly zero is rejected, because the cost check tests for a positive half-spread.",
        [
            (
                "    if fee < 0 or spread < 0:",
                "    if fee < 0 or spread <= 0:",
            ),
        ],
    ),
    "z10_d_convexity_flags_call_below_chord.py": (
        "Student error: convexity_violations flags a call strictly below the chord, reversing the sign of the test.",
        [
            (
                "    return [j for j in range(1, len(strikes_cents) - 1) if _second_difference(strikes_cents, calls_cents, j) < 0]",
                "    return [j for j in range(1, len(strikes_cents) - 1) if _second_difference(strikes_cents, calls_cents, j) > 0]",
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
