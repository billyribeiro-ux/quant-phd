"""Round-6 verifier mutants for CS2 slice d: each is the reference with one student error, written as a complete module.
Run from the checkout root: python3 ledgers/CS2/scripts/CS2-d-r6/v6_make_mutants.py <checkout-root>"""

import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref = (root / "course/modules/CS/CS2/grader/reference.py").read_text(encoding="utf-8")
out = root / "ledgers/CS2/mutants"


def swap(text: str, old: str, new: str, docstring: str) -> str:
    assert text.count(old) == 1, f"anchor not unique or missing: {old[:60]!r}"
    body = text.replace(old, new)
    body = body.split('"""', 2)  # drop the reference module docstring, replace with the mutant's first line
    return f'"""{docstring}"""' + body[2]


# v6_01: the default ddof is 0, so variance() with no argument answers the population variance.
m1 = swap(
    ref,
    "def variance(self, ddof: int = 1) -> float:",
    "def variance(self, ddof: int = 0) -> float:",
    "WelfordAccumulator.variance defaults to ddof 0 (population), so variance() with no argument is not the sample variance.",
)
(out / "v6_01_variance_default_ddof_is_population.py").write_text(m1, encoding="utf-8")

# v6_02: RollingMinMax keeps its deques as class attributes, so every object shares one window.
m2 = swap(
    ref,
    """        self._window = window
        self._pushed = 0
        self._mins: deque[tuple[int, float]] = deque()
        self._maxs: deque[tuple[int, float]] = deque()
""",
    """        self._window = window
        self._pushed = 0
""",
    "RollingMinMax keeps its two deques at class level, so every RollingMinMax shares one window of values.",
)
m2 = m2.replace(
    "class RollingMinMax:\n",
    "class RollingMinMax:\n    _mins: deque[tuple[int, float]] = deque()\n    _maxs: deque[tuple[int, float]] = deque()\n\n",
    1,
)
m2 = m2.replace(
    "        if self._pushed == 0:\n            raise ValueError(\"no value has been pushed, so there is no minimum\")",
    "        if not self._mins:\n            raise ValueError(\"no value has been pushed, so there is no minimum\")",
    1,
)
(out / "v6_02_rolling_deques_shared_at_class_level.py").write_text(m2, encoding="utf-8")

# v6_03: the rank target counts n + 1 values where it should count the n values added.
m3 = swap(
    ref,
    "target = max(1, math.ceil(Fraction(q) * self._n - self._exact_epsilon * self._n))",
    "target = max(1, math.ceil(Fraction(q) * (self._n + 1) - self._exact_epsilon * self._n))",
    "QuantileSketch.quantile takes the rank target from q times (n + 1), an off-by-one in the count of values.",
)
(out / "v6_03_quantile_target_uses_n_plus_one.py").write_text(m3, encoding="utf-8")

# v6_04: the sketch keeps its tuples in insertion order (append), so quantile scans an unsorted list.
m4 = swap(
    ref,
    "        position = bisect_right(self._values, x)\n        delta = 0 if position == 0 or position == len(self._values) else self._g[position] + self._delta[position] - 1\n",
    "        position = len(self._values)\n        delta = 0\n",
    "QuantileSketch.add appends in arrival order and never keeps the stored values sorted, so quantile reads an unsorted list.",
)
(out / "v6_04_sketch_stores_arrival_order_unsorted.py").write_text(m4, encoding="utf-8")
print("wrote 4 mutants")
