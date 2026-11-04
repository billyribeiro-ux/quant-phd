"""Build the five alternative correct implementations of the SC1 engine from grader/reference.py (VERIFIER_RULES 2.6 item 3; plan 5.7).

Each alternative is the reference with one function replaced. Replacements must match exactly once.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
REF = (ROOT / "course/modules/SC/SC1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/SC1/scripts/SC1-d-r1/alternatives"


def build(name: str, doc: str, edits: list[tuple[str, str]]) -> None:
    text = REF
    for old, new in edits:
        if text.count(old) != 1:
            raise SystemExit(f"{name}: '{old[:50]}' matched {text.count(old)} times")
        text = text.replace(old, new)
    body = text.split('"""', 2)[2]  # drop the reference module docstring
    (OUT / f"{name}.py").write_text(f'"""{doc}\n"""' + body, encoding="utf-8")
    print("wrote", name)


OUT.mkdir(parents=True, exist_ok=True)
REFLECTION_OLD = "    return math.erfc(a / math.sqrt(2.0 * t))"

# Alt 1: closed form through statistics.NormalDist, 2 (1 - Phi(a / sqrt t)).
build(
    "alt1_reflection_normaldist",
    "Alternative 1: reflection_tail by statistics.NormalDist and 2(1 - Phi(a / sqrt t)); the rest is the reference.",
    [(REFLECTION_OLD, "    from statistics import NormalDist\n\n    return 2.0 * (1.0 - NormalDist().cdf(a / math.sqrt(t)))")],
)

# Alt 2: quadrature only, Simpson on the N(0, t) density, no closed form.
build(
    "alt2_reflection_quadrature",
    "Alternative 2: reflection_tail by Simpson quadrature of the N(0, t) density only, 4000 intervals; no closed form.",
    [
        (
            REFLECTION_OLD,
            """    top = a + 12.0 * math.sqrt(t)
    intervals = 4000
    step = (top - a) / intervals

    def density(x: float) -> float:
        return math.exp(-x * x / (2.0 * t)) / math.sqrt(2.0 * math.pi * t)

    total = density(a) + density(top)
    for k in range(1, intervals):
        total += (4.0 if k % 2 else 2.0) * density(a + k * step)
    return 2.0 * total * step / 3.0""",
        )
    ],
)

# Alt 3: srw counts by dynamic programming over (position, running maximum), integer counts.
build(
    "alt3_srw_dynamic_programming",
    "Alternative 3: srw_max_count and srw_terminal_count by dynamic programming over (position, running maximum); exact ints.",
    [
        (
            "    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a)",
            """    states: dict[tuple[int, int], int] = {(0, 0): 1}
    for _ in range(n):
        nxt: dict[tuple[int, int], int] = {}
        for (pos, top), c in states.items():
            for d in (1, -1):
                key = (pos + d, max(top, pos + d))
                nxt[key] = nxt.get(key, 0) + c
        states = nxt
    return sum(c for (pos, _top), c in states.items() if pos >= a)""",
        ),
        (
            "    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)",
            """    states: dict[tuple[int, int], int] = {(0, 0): 1}
    for _ in range(n):
        nxt: dict[tuple[int, int], int] = {}
        for (pos, top), c in states.items():
            for d in (1, -1):
                key = (pos + d, max(top, pos + d))
                nxt[key] = nxt.get(key, 0) + c
        states = nxt
    return sum(c for (_pos, top), c in states.items() if top >= a)""",
        ),
    ],
)

# Alt 4: Box-Muller Gaussians, a different draw order (both values of each pair are used, in pair order).
BM_OLD_DRAW = "            position += rng.gauss(0.0, sd)"
build(
    "alt4_box_muller_draws",
    "Alternative 4: discrete_max_exceedance with Box-Muller Gaussians from rng.random(), a different draw order.",
    [
        (
            "    rng = random.Random(int(instance[\"seed\"]))\n    sd = math.sqrt(float(instance[\"H\"]) / n_steps)\n    paths: list[list[float]] = []",
            """    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    pending: list[float] = []

    def gauss_bm() -> float:
        if pending:
            return pending.pop() * sd
        u1 = 1.0 - rng.random()
        u2 = rng.random()
        radius = math.sqrt(-2.0 * math.log(u1))
        pending.append(radius * math.sin(2.0 * math.pi * u2))
        return radius * math.cos(2.0 * math.pi * u2) * sd

    paths: list[list[float]] = []""",
        ),
        (BM_OLD_DRAW, "            position += gauss_bm()"),
    ],
)

# Alt 5: cumulative-sum construction with itertools.accumulate; nested coarse grid by index subsampling.
build(
    "alt5_cumsum_and_index_subsampling",
    "Alternative 5: paths by itertools.accumulate of the increments; coarse grid by index subsampling, not slicing.",
    [
        (
            """        position = 0.0
        values: list[float] = []
        for _ in range(n_steps):
            position += rng.gauss(0.0, sd)
            values.append(position)
        paths.append(values)""",
            """        increments = [rng.gauss(0.0, sd) for _ in range(n_steps)]
        paths.append(list(itertools.accumulate(increments)))""",
        ),
        (
            "    coarse = sum(1 for values in paths if max(values[stride - 1 :: stride]) >= level)",
            "    coarse = sum(1 for values in paths if max(values[i] for i in range(stride - 1, n_fine, stride)) >= level)",
        ),
        ("import math\n", "import itertools\nimport math\n"),
    ],
)
