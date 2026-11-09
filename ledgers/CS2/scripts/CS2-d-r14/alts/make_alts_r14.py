"""Builds alternatives C, D and E from the grader's reference.py by one textual change each (asserted to match once)."""

from __future__ import annotations

import sys
from pathlib import Path

REF = Path(sys.argv[1])
src = REF.read_text(encoding="utf-8")


def swap(text: str, old: str, new: str, head: str) -> str:
    assert text.count(old) == 1, (head, text.count(old))
    return text.replace(old, new)


# C: sketch cap floor(2 eps n) with no +1 (a different numerical cutoff)
c = swap(
    src,
    "cap = math.floor(2 * self._exact_epsilon * self._n) + 1",
    "cap = math.floor(2 * self._exact_epsilon * self._n)",
    "C",
)
c = '"""Alternative C (correct): reference sketch with compression cap floor(2 eps n), no plus one."""\n' + c.split('"""', 2)[2]
Path("alt_r14_C_reference_cap_floor_2en.py").write_text(c, encoding="utf-8")

# D: Welford with exact Fraction state, converted to float on output
d = swap(
    src,
    "        self._count += 1\n        delta = x - self._mean\n        self._mean += delta / self._count\n        self._m2 += delta * (x - self._mean)",
    "        self._count += 1\n        fx = Fraction(x)\n        self._exact_sum = getattr(self, '_exact_sum', Fraction(0)) + fx\n        self._exact_sq = getattr(self, '_exact_sq', Fraction(0)) + fx * fx\n        self._mean = float(self._exact_sum / self._count)\n        self._m2 = float(self._exact_sq - self._exact_sum * self._exact_sum / self._count)",
    "D",
)
d = '"""Alternative D (correct): reference with Welford state computed in exact Fraction sums, rounded on output."""\n' + d.split('"""', 2)[2]
Path("alt_r14_D_exact_fraction_sums.py").write_text(d, encoding="utf-8")

# E: rolling minimum and maximum by brute force over the last window values (no deques)
e = swap(
    src,
    "        self._pushed = 0\n        self._mins: deque[tuple[int, float]] = deque()\n        self._maxs: deque[tuple[int, float]] = deque()",
    "        self._pushed = 0\n        self._recent: list[float] = []",
    "E1",
)
e = swap(
    e,
    "    def push(self, x: float) -> None:\n        if math.isnan(x):\n            raise ValueError(\"a NaN value is not a number and cannot be pushed\")\n        index = self._pushed\n        self._pushed += 1\n        while self._mins and self._mins[-1][1] >= x:\n            self._mins.pop()\n        self._mins.append((index, x))\n        while self._maxs and self._maxs[-1][1] <= x:\n            self._maxs.pop()\n        self._maxs.append((index, x))\n        oldest = index - self._window + 1\n        while self._mins[0][0] < oldest:\n            self._mins.popleft()\n        while self._maxs[0][0] < oldest:\n            self._maxs.popleft()",
    "    def push(self, x: float) -> None:\n        if math.isnan(x):\n            raise ValueError(\"a NaN value is not a number and cannot be pushed\")\n        self._pushed += 1\n        self._recent.append(x)\n        self._recent = self._recent[-self._window :]",
    "E2",
)
e = swap(
    e,
    "        return self._mins[0][1]\n",
    "        return min(self._recent)\n",
    "E3",
)
e = swap(
    e,
    "        return self._maxs[0][1]\n",
    "        return max(self._recent)\n",
    "E4",
)
e = '"""Alternative E (correct): reference with the rolling minimum and maximum by brute force over the window."""\n' + e.split('"""', 2)[2]
Path("alt_r14_E_brute_window.py").write_text(e, encoding="utf-8")
print("built C, D, E")
