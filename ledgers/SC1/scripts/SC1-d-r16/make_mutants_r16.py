"""Write four round-16 student-error mutants: single-change copies of grader/reference.py.
Usage: make_mutants_r16.py <checkout root>. Each replacement must match exactly once, or the script stops."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref_path = root / "course/modules/SC/SC1/grader/reference.py"
ref = ref_path.read_text(encoding="utf-8")
old_doc = '"""Reference solution for the SC1 project: the reflection-principle engine, bm_checks.py.'
assert ref.count(old_doc) == 1
MUTANTS = {
    "r16_01_srw_max_shifts_the_level_down_by_one.py": (
        "Student error: srw_max_count adds the endpoint count at a - 1 instead of a + 1 in the reflection identity.",
        "    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)",
        "    return srw_terminal_count(n, a) + srw_terminal_count(n, a - 1)",
    ),
    "r16_02_standard_error_missing_root_n.py": (
        "Student error: discrete_max_exceedance returns the sample sd of the indicators, not divided by sqrt(N).",
        "    return mean, math.sqrt(variance) / math.sqrt(count)",
        "    return mean, math.sqrt(variance)",
    ),
    "r16_03_reflection_tail_rounds_the_level_to_two_places.py": (
        "Student error: reflection_tail rounds the level to two decimals before it evaluates erfc.",
        "    return math.erfc(a / math.sqrt(2.0 * t))",
        "    return math.erfc(round(a, 2) / math.sqrt(2.0 * t))",
    ),
    "r16_04_one_path_divides_by_zero_instead_of_valueerror.py": (
        "Student error: discrete_max_exceedance omits the n_paths check, so one path raises ZeroDivisionError.",
        '    if int(instance["n_paths"]) < 2:\n        raise ValueError("the estimate needs at least two paths for a standard error")\n',
        "",
    ),
}
for name, (description, old, new) in MUTANTS.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    text = ref.replace(old, new, 1)
    head, sep, tail = text.partition("from __future__ import annotations")
    assert sep and head.startswith('"""Reference solution'), name
    text = f'"""{description}\n\nSingle-change copy of grader/reference.py (round 16, verifier-written).\n"""\n\n' + sep + tail
    (root / "ledgers/SC1/mutants" / name).write_text(text, encoding="utf-8")
    print("wrote", name)
