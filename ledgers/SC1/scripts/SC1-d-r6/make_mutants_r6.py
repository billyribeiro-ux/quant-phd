"""Verifier round 6 (SC1 slice d): three new student-error mutants of the reference engine, one change each.

Each mutant is written to ledgers/SC1/mutants/ as a complete module. Every replacement must match exactly the
number of times asserted, so the mutant differs from reference.py by exactly the stated change.
"""

from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE6-SC1-d")
REF = (ROOT / "course/modules/SC/SC1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/SC1/mutants"

MUTANTS = {
    "m35_grid_exceedance_strictly_above_level.py": (
        "Strict inequality: discrete_max_exceedance counts a path only when its grid maximum is strictly above a, "
        "so a path whose maximum equals the level is dropped.",
        [("1.0 if max(values) >= level else 0.0", "1.0 if max(values) > level else 0.0", 1)],
    ),
    "m36_nested_counts_strictly_above_level.py": (
        "Strict inequality: nested_grid_counts counts a path only when its fine or coarse maximum is strictly above a, "
        "so a path whose maximum equals the level is dropped from both counts.",
        [
            ("fine = sum(1 for values in paths if max(values) >= level)", "fine = sum(1 for values in paths if max(values) > level)", 1),
            ("coarse = sum(1 for values in paths if max(values[stride - 1 :: stride]) >= level)",
             "coarse = sum(1 for values in paths if max(values[stride - 1 :: stride]) > level)", 1),
        ],
    ),
    "m37_one_path_accepted_with_zero_error.py": (
        "Named condition skipped: discrete_max_exceedance accepts one path and returns a standard error of 0.0 "
        "instead of raising ValueError for n_paths < 2.",
        [
            (
                '    if int(instance["n_paths"]) < 2:\n'
                '        raise ValueError("the estimate needs at least two paths for a standard error")\n',
                "",
                1,
            ),
            (
                "variance = sum((x - mean) ** 2 for x in indicators) / (count - 1)",
                "variance = sum((x - mean) ** 2 for x in indicators) / max(count - 1, 1)",
                1,
            ),
        ],
    ),
}

for name, (description, replacements) in MUTANTS.items():
    text = REF
    for old, new, expected in replacements:
        found = text.count(old)
        assert found == expected, f"{name}: expected {expected} match(es), found {found} for {old!r}"
        text = text.replace(old, new)
    # Replace the module docstring's first line with the description of the student error.
    head, sep, rest = text.partition('"""')
    _, sep2, tail = rest.partition('"""')
    assert sep and sep2, f"{name}: module docstring not found"
    text = head + '"""' + description + "\n\n" + "Mutant of reference.py: exactly one change, as described above.\n" + '"""' + tail
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", OUT / name)
