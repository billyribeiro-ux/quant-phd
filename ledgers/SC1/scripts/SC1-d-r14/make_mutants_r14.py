"""Write round-14 student-error mutants as complete bm_checks.py modules, each a single change of grader/reference.py.

Each replacement must match exactly once in the reference, so every mutant differs from it by one edit.
Usage: make_mutants_r14.py <checkout root>
"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref = (root / "course/modules/SC/SC1/grader/reference.py").read_text(encoding="utf-8")
out = root / "ledgers/SC1/mutants"

MUTANTS = {
    "r14_01_path_seeded_by_path_index.py": (
        "Seed per path: _grid_paths seeds each path with the instance seed plus its path index, so paths are not the "
        "seeded stream of the page.",
        "    rng = random.Random(int(instance[\"seed\"]))\n    sd = math.sqrt(float(instance[\"H\"]) / n_steps)\n    paths: list[list[float]] = []\n    for _ in range(int(instance[\"n_paths\"])):\n",
        "    sd = math.sqrt(float(instance[\"H\"]) / n_steps)\n    paths: list[list[float]] = []\n    for path_index in range(int(instance[\"n_paths\"])):\n        rng = random.Random(int(instance[\"seed\"]) + path_index)\n",
    ),
    "r14_02_nested_fine_drops_the_horizon_point.py": (
        "Fine grid truncated: nested_grid_counts takes the fine maximum over the first n_fine - 1 grid points, so the "
        "horizon point t_H is left out of the fine count.",
        "    fine = sum(1 for values in paths if max(values) >= level)\n",
        "    fine = sum(1 for values in paths if max(values[:-1]) >= level)\n",
    ),
    "r14_03_terminal_count_compares_the_up_count.py": (
        "Up-count for endpoint: srw_terminal_count compares the number of up-steps j with a, not the endpoint 2j - n "
        "with a, so the level is read in the wrong units.",
        "    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a)\n",
        "    return sum(math.comb(n, j) for j in range(n + 1) if j >= a)\n",
    ),
}

for name, (doc, old, new) in MUTANTS.items():
    assert ref.count(old) == 1, f"{name}: the replaced text must occur exactly once in the reference"
    body = ref.replace(old, new, 1)
    head_end = body.index('"""', 3) + 3
    body = f'"""{doc}\n\nWritten by the verifier, round 14, as a single change of grader/reference.py.\n"""' + body[head_end:]
    (out / name).write_text(body, encoding="utf-8")
    print("wrote", name)
