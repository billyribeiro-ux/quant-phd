"""Write the round-12 student-error mutants as single-change copies of the reference solution (asserts each edit once)."""
from pathlib import Path
import sys

root = Path(sys.argv[1])
ref = (root / "course/modules/SC/SC1/grader/reference.py").read_text(encoding="utf-8")
out = root / "ledgers/SC1/mutants"

def edit(name: str, doc: str, pairs: list[tuple[str, str]]) -> None:
    text = ref
    for old, new in pairs:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    (out / name).write_text(f'"""{doc}\n\nSingle-change copy of the reference (round 12, verifier-written)."""\n' + text.split('"""', 2)[2], encoding="utf-8")

# 1. step-major draw order, which the page names as the wrong order
edit(
    "r12_01_step_major_draw_order.py",
    "Draw order: _grid_paths draws step 1 of every path before step 2 of any path, so the same seed gives other paths than Lab 3's.",
    [(
        '''    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    paths: list[list[float]] = []
    for _ in range(int(instance["n_paths"])):
        position = 0.0
        values: list[float] = []
        for _ in range(n_steps):
            position += rng.gauss(0.0, sd)
            values.append(position)
        paths.append(values)
    return paths''',
        '''    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    n_paths = int(instance["n_paths"])
    positions = [0.0] * n_paths
    paths: list[list[float]] = [[] for _ in range(n_paths)]
    for _ in range(n_steps):
        for p in range(n_paths):
            positions[p] += rng.gauss(0.0, sd)
            paths[p].append(positions[p])
    return paths''',
    )],
)

# 2. a probability returned where a count is specified
edit(
    "r12_02_terminal_count_is_a_probability.py",
    "Probability instead of count: srw_terminal_count returns the fraction of the 2**n walks, not their number.",
    [(
        "    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a)",
        "    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a) / 2**n",
    )],
)

# 3. over-constraint: a level above the walk length is rejected instead of counting zero walks
edit(
    "r12_03_level_above_length_rejected.py",
    "Over-constraint: srw_terminal_count raises ValueError for a level above the walk length, a valid input whose count is zero.",
    [(
        "    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a)",
        '    if a > n:\n        raise ValueError("the level exceeds the walk length")\n'
        "    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a)",
    )],
)

# 4. coarse grid maximum taken over the first n_coarse fine points, not over every stride-th point
edit(
    "r12_04_coarse_maximum_over_first_points.py",
    "Coarse grid truncated: nested_grid_counts takes the coarse maximum over the first n_coarse fine points, not over every stride-th point.",
    [(
        "    coarse = sum(1 for values in paths if max(values[stride - 1 :: stride]) >= level)",
        "    coarse = sum(1 for values in paths if max(values[:n_coarse]) >= level)",
    )],
)
print("written")
