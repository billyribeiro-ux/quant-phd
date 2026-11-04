# ruff: noqa: E501
"""Round-5 verifier (CS2-d): writes three student-error mutants as complete modules, derived from the reference.

Each mutant is the reference solution with one plausible student error applied. Every replacement must match
exactly once, or the script stops, so no mutant silently equals the reference.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
REF = ROOT / "course/modules/CS/CS2/grader/reference.py"
OUT = ROOT / "ledgers/CS2/mutants"

MUTANTS = {
    "r5v_01_sketch_compression_folds_maximum_into_predecessor.py": (
        "QuantileSketch._compress also folds the last (maximum) tuple into its predecessor, so the maximum is not stored.",
        [
            (
                "                del self._values[i]\n                del self._g[i]\n                del self._delta[i]\n",
                "                del self._values[i]\n                del self._g[i]\n                del self._delta[i]\n"
                "        if len(self._values) >= 2 and self._g[-2] + self._g[-1] + self._delta[-1] <= cap:\n"
                "            self._g[-2] += self._g[-1]\n"
                "            del self._values[-1]\n"
                "            del self._g[-1]\n"
                "            del self._delta[-1]\n",
            ),
        ],
    ),
    "r5v_02_empty_sketch_quantile_returns_nan.py": (
        "QuantileSketch.quantile returns NaN on an empty sketch instead of raising ValueError.",
        [
            (
                '        if self._n == 0:\n            raise ValueError("the sketch is empty, so it has no quantiles")\n',
                '        if self._n == 0:\n            return float("nan")\n',
            ),
        ],
    ),
    "r5v_03_variance_uses_last_five_values.py": (
        "WelfordAccumulator.variance is computed over the last five values only, not over every value added.",
        [
            (
                "        self._count += 1\n        delta = x - self._mean\n",
                "        self._count += 1\n        self._recent = (getattr(self, '_recent', []) + [x])[-5:]\n        delta = x - self._mean\n",
            ),
            (
                '        if ddof == 0:\n            return self._m2 / self._count\n        if ddof == 1:\n            if self._count < 2:\n                raise ValueError("the sample variance needs at least two values")\n            return self._m2 / (self._count - 1)\n',
                '        if ddof == 0:\n            return self._m2 / self._count\n        if ddof == 1:\n            if self._count < 2:\n                raise ValueError("the sample variance needs at least two values")\n'
                "            recent = self._recent\n            mu = sum(recent) / len(recent)\n            return sum((v - mu) ** 2 for v in recent) / (len(recent) - 1) if len(recent) >= 2 else 0.0\n",
            ),
        ],
    ),
}

if __name__ == "__main__":
    source = REF.read_text(encoding="utf-8")
    for name, (doc, edits) in MUTANTS.items():
        text = source
        for old, new in edits:
            assert text.count(old) == 1, f"{name}: replacement target found {text.count(old)} times"
            text = text.replace(old, new)
        head, sep, rest = text.partition('"""')
        _, sep2, tail = rest.partition('"""')
        text = head + '"""' + doc + '\n"""' + tail
        (OUT / name).write_text(text, encoding="utf-8")
        print("wrote", name)
