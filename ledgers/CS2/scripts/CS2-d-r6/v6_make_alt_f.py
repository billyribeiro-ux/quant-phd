"""Round-6 alternative F (correct by the spec's allowance): every argument is coerced with float() first, so strings
and booleans are read as the numbers they denote; a window is coerced and refused unless it is a whole number >= 1;
ddof is coerced and refused unless it denotes 0 or 1. None, and every non-whole window, must still raise.
Run: python3 v6_make_alt_f.py <root>"""

import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref = (root / "course/modules/CS/CS2/grader/reference.py").read_text(encoding="utf-8")
body = ref[ref.index('"""', 3) + 3 :]


def rep(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, old[:60]
    return text.replace(old, new)


s = body
s = rep(s, "    def update(self, x: float) -> None:\n        if math.isnan(x):",
        "    def update(self, x: float) -> None:\n        x = float(x)\n        if math.isnan(x):")
s = rep(s, "    def variance(self, ddof: int = 1) -> float:\n        if self._count == 0:",
        "    def variance(self, ddof: int = 1) -> float:\n        d = float(ddof)\n        if self._count == 0:")
s = rep(s, "        if ddof == 0:\n            return self._m2 / self._count\n        if ddof == 1:\n            if self._count < 2:",
        "        if d == 0:\n            return self._m2 / self._count\n        if d == 1:\n            if self._count < 2:")
s = rep(s, "        if window < 1:\n            raise ValueError(\"the window must hold at least one value\")\n        if window != int(window):\n            raise ValueError(\"the window must be a whole number of values\")\n        self._window = window",
        "        w = float(window)\n        if math.isnan(w) or math.isinf(w) or w < 1:\n            raise ValueError(\"the window must hold at least one value\")\n        if w != int(w):\n            raise ValueError(\"the window must be a whole number of values\")\n        self._window = int(w)")
s = rep(s, "    def push(self, x: float) -> None:\n        if math.isnan(x):",
        "    def push(self, x: float) -> None:\n        x = float(x)\n        if math.isnan(x):")
s = rep(s, "    def add(self, x: float) -> None:\n        if math.isnan(x):",
        "    def add(self, x: float) -> None:\n        x = float(x)\n        if math.isnan(x):")
header = ('"""Alternative F (correct by the spec allowance): every argument is coerced with float() first, so strings and '
          'booleans are read as the numbers they denote; windows and ddof are refused unless they denote a whole number of the '
          'allowed value."""')
(root / "ledgers/CS2/scripts/CS2-d-r6/alts_v6/alt_v6_f_float_coercion_of_arguments.py").write_text(header + s, encoding="utf-8")
print("wrote alternative F")
