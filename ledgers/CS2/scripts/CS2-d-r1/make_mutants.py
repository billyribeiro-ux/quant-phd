"""Write the verifier's CS2 project mutants as complete streamstats.py modules (CS2-d round 1).

Each mutant is the reference solution with exactly one student-style change. Every replacement must match once.
Usage: python -I make_mutants.py <checkout>
"""

from __future__ import annotations

import sys
from pathlib import Path

NAIVE_WELFORD = '''class WelfordAccumulator:
    """Naive sum-of-squares variance: sum(x*x) - n*mean*mean, no Welford update."""

    def __init__(self) -> None:
        self._count = 0
        self._sum = 0.0
        self._sumsq = 0.0

    def update(self, x: float) -> None:
        if math.isnan(x):
            raise ValueError("a NaN value is not a number and cannot be added")
        self._count += 1
        self._sum += x
        self._sumsq += x * x

    @property
    def count(self) -> int:
        return self._count

    def mean(self) -> float:
        if self._count == 0:
            raise ValueError("the mean is undefined before the first value")
        return self._sum / self._count

    def variance(self, ddof: int = 1) -> float:
        if self._count == 0:
            raise ValueError("the variance is undefined before the first value")
        if ddof == 1 and self._count < 2:
            raise ValueError("the sample variance needs at least two values")
        m2 = self._sumsq - self._count * self.mean() * self.mean()
        return m2 / (self._count - ddof)


'''

DESCRIPTIONS = {
    "m01_naive_sum_of_squares": "Naive sum-of-squares variance (sum x*x minus n*mean*mean), not Welford's update.",
    "m02_population_divisor_for_sample": "Sample variance divides by n (population divisor) instead of n - 1.",
    "m03_window_one_value_too_long": "Rolling window keeps window + 1 values (expiry off by one).",
    "m04_rank_target_rounds_down": "Quantile rank target is floor(q n), which drops the epsilon n slack and rounds the rank down.",
    "m05_m2_increment_uses_delta_squared": "Welford M2 increment is delta squared, the deviation from the old mean, not delta times the new deviation.",
    "m06_sketch_accepts_nan_silently": "Quantile sketch add() accepts NaN without raising ValueError.",
    "m07_two_values_rejected_for_sample_variance": "variance(1) raises with two values and only accepts three or more (edge case at count 2).",
    "m08_deque_never_expires_from_front": "Monotonic deque never removes expired indices from its front, so expired extremes stay reported.",
}

REPLACEMENTS: list[tuple[str, str, str]] = [
    ("m01_naive_sum_of_squares", "", ""),  # whole-class replacement, handled below
    (
        "m02_population_divisor_for_sample",
        "            return self._m2 / (self._count - 1)",
        "            return self._m2 / self._count",
    ),
    (
        "m03_window_one_value_too_long",
        "        oldest = index - self._window + 1",
        "        oldest = index - self._window",
    ),
    (
        "m04_rank_target_rounds_down",
        "        target = max(1, math.ceil(Fraction(q) * self._n - self._exact_epsilon * self._n))",
        "        target = max(1, math.floor(Fraction(q) * self._n))",
    ),
    (
        "m05_m2_increment_uses_delta_squared",
        "        self._m2 += delta * (x - self._mean)",
        "        self._m2 += delta * delta",
    ),
    (
        "m06_sketch_accepts_nan_silently",
        "        if math.isnan(x):\n            raise ValueError(\"a NaN value is not a number and cannot be added\")\n        position = bisect_right",
        "        position = bisect_right",
    ),
    (
        "m07_two_values_rejected_for_sample_variance",
        "            if self._count < 2:\n                raise ValueError(\"the sample variance needs at least two values\")",
        "            if self._count < 3:\n                raise ValueError(\"the sample variance needs at least two values\")",
    ),
    (
        "m08_deque_never_expires_from_front",
        "        while self._mins[0][0] < oldest:",
        "        while self._mins[0][0] < oldest and False:",
    ),
]


def main() -> int:
    ref = (Path(sys.argv[1]) / "course/modules/CS/CS2/grader/reference.py").read_text(encoding="utf-8")
    out = Path(sys.argv[1]) / "ledgers/CS2/mutants"
    out.mkdir(parents=True, exist_ok=True)
    welford_start = ref.index("class WelfordAccumulator:")
    rolling_start = ref.index("class RollingMinMax:")
    for name, old, new in REPLACEMENTS:
        if name.startswith("m01"):
            text = ref[:welford_start] + NAIVE_WELFORD + ref[rolling_start:]
        else:
            if ref.count(old) != 1:
                raise SystemExit(f"{name}: pattern found {ref.count(old)} times, expected 1")
            text = ref.replace(old, new)
        description = DESCRIPTIONS[name]
        text = '"""' + description + '\n\nVerifier mutant (CS2-d round 1): one student-style change to reference.py.\n"""\n\n' + text[text.index("from __future__"):]
        (out / f"{name}.py").write_text(text, encoding="utf-8")
        print("wrote", name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
