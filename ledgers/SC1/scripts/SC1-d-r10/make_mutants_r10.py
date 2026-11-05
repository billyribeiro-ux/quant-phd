"""Write round-10 student-error mutants of the SC1 reference engine into ledgers/SC1/mutants/."""
from pathlib import Path

REF = Path("/Users/billyribeiro/.fanout/wt/verifyE10-SC1-d/course/modules/SC/SC1/grader/reference.py").read_text(encoding="utf-8")
OUT = Path("/Users/billyribeiro/.fanout/wt/verifyE10-SC1-d/ledgers/SC1/mutants")


def swap(src: str, old: str, new: str) -> str:
    assert src.count(old) == 1, (src.count(old), old[:60])
    return src.replace(old, new)


mutants = {
    "r10_01_srw_max_doubles_the_endpoint_count.py": (
        "Factor 2 carried over from the continuous reflection principle: srw_max_count returns twice the endpoint "
        "count, so the tie at S_n = a is counted twice.",
        ("    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)",
         "    return 2 * srw_terminal_count(n, a)"),
    ),
    "r10_02_last_path_dropped_from_the_count.py": (
        "Loop bound: discrete_max_exceedance tests only the first N - 1 seeded paths, and reports the fraction of those.",
        ("    indicators = [1.0 if max(values) >= level else 0.0 for values in paths]",
         "    indicators = [1.0 if max(values) >= level else 0.0 for values in paths[:-1]]"),
    ),
    "r10_03_bgk_level_shift_on_the_grid.py": (
        "Continuity correction misapplied: discrete_max_exceedance lowers the grid level by 0.5826 sqrt(H / n_steps) "
        "before counting, which is not the fraction the specification defines.",
        ('    level = float(instance["a"])\n    paths = _grid_paths(instance, n_steps)',
         '    level = float(instance["a"]) - 0.5826 * math.sqrt(float(instance["H"]) / n_steps)\n    paths = _grid_paths(instance, n_steps)'),
    ),
    "r10_04_terminal_count_reads_level_one_low.py": (
        "Off-by-one level: srw_terminal_count counts walks with S_n >= a - 1, so the tie at S_n = a - 1 is included.",
        ("    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a)",
         "    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a - 1)"),
    ),
    "r10_05_reflection_tail_ignores_the_horizon.py": (
        "Horizon dropped: reflection_tail evaluates the closed form at t = 1 whatever horizon the caller passes.",
        ("    return math.erfc(a / math.sqrt(2.0 * t))", "    return math.erfc(a / math.sqrt(2.0 * 1.0))"),
    ),
}

for name, (doc, (old, new)) in mutants.items():
    src = swap(REF, old, new)
    # the first docstring of the module is the reference's; the mutant's own docstring is the description
    body = src.split('"""', 2)[2]
    text = f'"""{doc}\n\nSingle-change copy of the reference reference.py (round 10, verifier-written).\n"""' + body
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
