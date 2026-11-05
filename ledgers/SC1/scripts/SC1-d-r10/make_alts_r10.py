"""Write five alternative correct bm_checks.py implementations (verifier round 10) from the reference by function swaps."""
from pathlib import Path

REF = Path("/Users/billyribeiro/.fanout/wt/verifyE10-SC1-d/course/modules/SC/SC1/grader/reference.py").read_text(encoding="utf-8")
OUT = Path("/Users/billyribeiro/.fanout/wt/verifyE10-SC1-d/ledgers/SC1/scripts/SC1-d-r10/alternatives")


def replace_def(src: str, name: str, new_def: str) -> str:
    lines = src.split("\n")
    starts = [i for i, line in enumerate(lines) if line.startswith(f"def {name}(")]
    assert len(starts) == 1, (name, starts)
    i = starts[0]
    j = i + 1
    while j < len(lines) and not lines[j].startswith("def "):
        j += 1
    block = "\n".join(lines[:i]) + "\n" + new_def.rstrip("\n") + "\n\n\n" + "\n".join(lines[j:])
    return block


DEF_A = '''def reflection_tail(a: float, t: float) -> float:
    """P(M_t >= a) = 2 (1 - Phi(a / sqrt(t))), from statistics.NormalDist, a different route to erfc."""
    from statistics import NormalDist

    if a <= 0:
        raise ValueError("the level a must be positive for the reflection tail")
    if t <= 0:
        raise ValueError("the time t must be positive for the reflection tail")
    return 2.0 * (1.0 - NormalDist().cdf(a / math.sqrt(t)))
'''

DEF_B = '''def reflection_tail(a: float, t: float) -> float:
    """2 P(B_t >= a) by composite Simpson on the N(0, t) density over [a, a + 12 sqrt(t)]: no closed form used."""
    if a <= 0:
        raise ValueError("the level a must be positive for the reflection tail")
    if t <= 0:
        raise ValueError("the time t must be positive for the reflection tail")
    intervals = 2000
    top = a + 12.0 * math.sqrt(t)
    step = (top - a) / intervals

    def density(x: float) -> float:
        return math.exp(-x * x / (2.0 * t)) / math.sqrt(2.0 * math.pi * t)

    total = density(a) + density(top)
    for k in range(1, intervals):
        total += (4.0 if k % 2 else 2.0) * density(a + k * step)
    return 2.0 * total * step / 3.0
'''

DP_TERMINAL = '''def srw_terminal_count(n: int, a: int) -> int:
    """#{S_n >= a} by dynamic programming over (position, running maximum), exact integers; no binomial sum."""
    if n < 1:
        raise ValueError("the walk needs at least one step")
    if a < 1:
        raise ValueError("the level a must be at least 1")
    states: dict[tuple[int, int], int] = {(0, 0): 1}
    for _ in range(n):
        nxt: dict[tuple[int, int], int] = {}
        for (pos, top), count in states.items():
            for step in (1, -1):
                key = (pos + step, max(top, pos + step))
                nxt[key] = nxt.get(key, 0) + count
        states = nxt
    return sum(count for (pos, _top), count in states.items() if pos >= a)
'''

DP_MAX = '''def srw_max_count(n: int, a: int) -> int:
    """#{max >= a} by the same dynamic programme over (position, running maximum), exact integers."""
    if n < 1:
        raise ValueError("the walk needs at least one step")
    if a < 1:
        raise ValueError("the level a must be at least 1")
    states: dict[tuple[int, int], int] = {(0, 0): 1}
    for _ in range(n):
        nxt: dict[tuple[int, int], int] = {}
        for (pos, top), count in states.items():
            for step in (1, -1):
                key = (pos + step, max(top, pos + step))
                nxt[key] = nxt.get(key, 0) + count
        states = nxt
    return sum(count for (_pos, top), count in states.items() if top >= a)
'''

DEF_D = '''def _grid_paths(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    """Same gauss draws, taken step-major: all paths' step 1, then all paths' step 2, and so on (another draw order)."""
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    n_paths = int(instance["n_paths"])
    positions = [0.0] * n_paths
    paths: list[list[float]] = [[] for _ in range(n_paths)]
    for _ in range(n_steps):
        for i in range(n_paths):
            positions[i] += rng.gauss(0.0, sd)
            paths[i].append(positions[i])
    return paths
'''

DEF_E = '''def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    """Same paths as the reference; the coarse grid is taken by index subsampling of the fine values, not slicing."""
    if n_fine < 1:
        raise ValueError("the fine grid needs at least one step")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("the coarse grid size must divide the fine grid size")
    level = float(instance["a"])
    stride = n_fine // n_coarse
    coarse_index = [k for k in range(n_fine) if (k + 1) % stride == 0]
    paths = _grid_paths(instance, n_fine)
    fine = 0
    coarse = 0
    for values in paths:
        if max(values) >= level:
            fine += 1
        if max(values[i] for i in coarse_index) >= level:
            coarse += 1
    return fine, coarse
'''

PLAN = {
    "alt_r10_a_normaldist_tail.py": [("reflection_tail", DEF_A)],
    "alt_r10_b_quadrature_tail.py": [("reflection_tail", DEF_B)],
    "alt_r10_c_dp_walk_counts.py": [("srw_terminal_count", DP_TERMINAL), ("srw_max_count", DP_MAX)],
    "alt_r10_d_step_major_order.py": [("_grid_paths", DEF_D)],
    "alt_r10_e_index_subsample.py": [("nested_grid_counts", DEF_E)],
}

for name, swaps in PLAN.items():
    text = REF
    for fname, new_def in swaps:
        text = replace_def(text, fname, new_def)
    header = f'"""Alternative correct engine {name} (verifier round 10): the reference with the named functions re-implemented."""\n'
    body = text.split('"""', 2)[2]
    (OUT / name).write_text(header + body, encoding="utf-8")
    print("wrote", name)
