"""Write four new student-error mutants (round 18) as single-change copies of grader/reference.py.
Each replacement must match exactly once, or the script fails. Usage: python3 -I make_mutants_r18.py <checkout root>"""
import sys

root = sys.argv[1]
ref = open(f"{root}/course/modules/SC/SC1/grader/reference.py", encoding="utf-8").read()
header_old = '"""Reference solution for the SC1 project: the reflection-principle engine, bm_checks.py.\n'
assert ref.count(header_old) == 1
MUTANTS = {
    "r18_01_reflection_tail_swaps_level_and_time": (
        "Student error: reflection_tail swaps the level and the time in the erfc argument, erfc(t / sqrt(2 a)).",
        ("    return math.erfc(a / math.sqrt(2.0 * t))", "    return math.erfc(t / math.sqrt(2.0 * a))"),
    ),
    "r18_02_horizon_capped_at_one_in_the_tail": (
        "Student error: reflection_tail caps the horizon at one time unit before the closed form, so horizons above 1 are wrong.",
        ("    return math.erfc(a / math.sqrt(2.0 * t))", "    return math.erfc(a / math.sqrt(2.0 * min(t, 1.0)))"),
    ),
    "r18_03_grid_maximum_stops_at_half_the_grid": (
        "Student error: discrete_max_exceedance takes the grid maximum over the first half of the grid only, dropping later steps.",
        (
            "    indicators = [1.0 if max(values) >= level else 0.0 for values in paths]",
            "    indicators = [1.0 if max(values[: max(1, n_steps // 2)]) >= level else 0.0 for values in paths]",
        ),
    ),
    "r18_04_estimate_adds_one_path_smoothing": (
        "Student error: discrete_max_exceedance adds one phantom path reaching the level (Laplace smoothing) to the estimate.",
        ("    mean = sum(indicators) / count\n    variance", "    mean = (sum(indicators) + 1.0) / (count + 1.0)\n    variance"),
    ),
}
for name, (first_line, (old, new)) in MUTANTS.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new).replace(header_old, f'"""{first_line}\n\nSingle-change copy of grader/reference.py (round 18, verifier-written).\n', 1)
    open(f"{root}/ledgers/SC1/mutants/{name}.py", "w", encoding="utf-8").write(body)
    print("wrote", name)
