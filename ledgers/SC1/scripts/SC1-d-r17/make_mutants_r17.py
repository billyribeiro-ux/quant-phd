"""Write four round-17 student-error mutants: single-change copies of grader/reference.py.
Usage: make_mutants_r17.py <checkout root>. Each replacement must match exactly once, or the script stops."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref_path = root / "course/modules/SC/SC1/grader/reference.py"
ref = ref_path.read_text(encoding="utf-8")
old_doc = '"""Reference solution for the SC1 project: the reflection-principle engine, bm_checks.py.'
assert ref.count(old_doc) == 1
MUTANTS = {
    "r17_01_erfc_argument_halved_root_t.py": (
        "Student error: reflection_tail divides the level by 2 sqrt(t) instead of sqrt(2 t) inside erfc.",
        "    return math.erfc(a / math.sqrt(2.0 * t))",
        "    return math.erfc(a / (2.0 * math.sqrt(t)))",
    ),
    "r17_02_only_zero_level_guarded.py": (
        "Student error: reflection_tail rejects a = 0 but accepts a negative level and returns erfc of a negative value.",
        '    if a <= 0:\n        raise ValueError("the level a must be positive for the reflection tail")',
        '    if a == 0:\n        raise ValueError("the level a must be positive for the reflection tail")',
    ),
    "r17_03_reflection_tail_returns_twice_erfc.py": (
        "Student error: reflection_tail applies the factor 2 twice, returning 2 erfc(a / sqrt(2 t)).",
        "    return math.erfc(a / math.sqrt(2.0 * t))",
        "    return 2.0 * math.erfc(a / math.sqrt(2.0 * t))",
    ),
    "r17_04_terminal_threshold_floors_half.py": (
        "Student error: srw_terminal_count takes j >= (n + a) // 2, which counts S_n = a - 1 when n + a is odd.",
        "    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a)",
        "    return sum(math.comb(n, j) for j in range(n + 1) if j >= (n + a) // 2)",
    ),
}
for name, (description, old, new) in MUTANTS.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    text = ref.replace(old, new, 1)
    head, sep, tail = text.partition("from __future__ import annotations")
    assert sep and head.startswith('"""Reference solution'), name
    text = f'"""{description}\n\nSingle-change copy of grader/reference.py (round 17, verifier-written).\n"""\n\n' + sep + tail
    (root / "ledgers/SC1/mutants" / name).write_text(text, encoding="utf-8")
    print("wrote", name)
