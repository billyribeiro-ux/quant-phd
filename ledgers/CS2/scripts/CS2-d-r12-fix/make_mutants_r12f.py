"""Write ten single-change student-error mutants of the CS2 reference into ledgers/CS2/mutants/."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = ROOT / "course" / "modules" / "CS" / "CS2" / "grader" / "reference.py"
OUT = ROOT / "ledgers" / "CS2" / "mutants"

# (file stem, first docstring line naming the student error, old text, new text); each old text occurs once.
MUTANTS: list[tuple[str, str, str, str]] = [
    (
        "r12f_01_variance_returns_standard_deviation",
        "variance(1) returns the square root of the sample variance, the standard deviation, not the variance.",
        "            return self._m2 / (self._count - 1)\n",
        "            return math.sqrt(self._m2 / (self._count - 1))\n",
    ),
    (
        "r12f_02_mean_returns_running_sum",
        "mean() returns the running sum of the values instead of their mean.",
        "        return self._mean\n\n    def variance",
        "        return self._mean * self._count\n\n    def variance",
    ),
    (
        "r12f_03_maximum_returns_latest_value",
        "maximum() returns the value pushed last instead of the maximum of the window.",
        "        return self._maxs[0][1]\n",
        "        return self._maxs[-1][1]\n",
    ),
    (
        "r12f_04_quantile_returns_mean_of_stored_values",
        "quantile(q) returns the mean of the stored values for every q, not a stored value at the rank target.",
        "        for value, g in zip(self._values, self._g, strict=True):\n"
        "            rank += g\n"
        "            if rank >= target:\n"
        "                return value\n",
        "        for _value, g in zip(self._values, self._g, strict=True):\n"
        "            rank += g\n"
        "            if rank >= target:\n"
        "                return sum(self._values) / len(self._values)\n",
    ),
    (
        "r12f_05_quantile_reads_the_probability_mirrored",
        "quantile(q) answers for the probability 1 - q, so quantile(0) returns the maximum side of the stream.",
        "        target = max(1, math.ceil(Fraction(q) * self._n - self._exact_epsilon * self._n))\n",
        "        target = max(1, math.ceil(Fraction(1 - q) * self._n - self._exact_epsilon * self._n))\n",
    ),
    (
        "r12f_06_quantile_target_clamped_to_count_minus_one",
        "quantile(q) caps the rank target at n - 1, so the top quantile on a short stream answers one rank low.",
        "        target = max(1, math.ceil(Fraction(q) * self._n - self._exact_epsilon * self._n))\n",
        "        target = min(self._n - 1, max(1, math.ceil(Fraction(q) * self._n - self._exact_epsilon * self._n)))\n",
    ),
    (
        "r12f_07_sketch_ignores_values_after_the_hundredth",
        "add(x) silently drops every value after the hundredth, so the sketch describes only the first hundred values.",
        "        position = bisect_right(self._values, x)\n",
        "        if self._n >= 100:\n            return\n        position = bisect_right(self._values, x)\n",
    ),
    (
        "r12f_08_rolling_block_restarts_every_window_values",
        "push() empties both deques at every multiple of the window, so the minimum and maximum forget earlier values.",
        "        index = self._pushed\n",
        "        if self._pushed % self._window == 0:\n            self._mins.clear()\n            self._maxs.clear()\n"
        "        index = self._pushed\n",
    ),
    (
        "r12f_09_single_value_quantile_is_nan",
        "quantile(q) returns NaN when exactly one value has been added, instead of that value.",
        "        target = max(1, math.ceil(Fraction(q) * self._n - self._exact_epsilon * self._n))\n",
        "        if self._n == 1:\n            return float(\"nan\")\n"
        "        target = max(1, math.ceil(Fraction(q) * self._n - self._exact_epsilon * self._n))\n",
    ),
    (
        "r12f_10_sketch_refuses_negative_values",
        "add(x) raises ValueError for a negative value, although the specification accepts every real number.",
        "        position = bisect_right(self._values, x)\n",
        "        if x < 0:\n            raise ValueError(\"a negative value is outside the domain\")\n"
        "        position = bisect_right(self._values, x)\n",
    ),
]


def main() -> int:
    ref = REF.read_text(encoding="utf-8")
    start = ref.index('"""')
    end = ref.index('"""', start + 3) + 3  # the reference module docstring spans [start, end)
    rest = ref[end:]
    for stem, doc, old, new in MUTANTS:
        assert ref.count(old) == 1, f"{stem}: anchor occurs {ref.count(old)} times"
        body = rest.replace(old, new)
        text = f'"""{doc}"""' + body
        (OUT / f"{stem}.py").write_text(text, encoding="utf-8")
        print("wrote", f"{stem}.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
