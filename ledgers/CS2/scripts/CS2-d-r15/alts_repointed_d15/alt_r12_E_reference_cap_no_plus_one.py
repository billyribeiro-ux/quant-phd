"""Alternative E: the reference solution with the compression cap floor(2 epsilon n) (no plus one), everything else reference."""

from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

_SRC = Path("/Users/billyribeiro/.fanout/wt/verifyD15-CS2-d/course/modules/CS/CS2/grader/reference.py")
_text = _SRC.read_text(encoding="utf-8")
assert "cap = math.floor(2 * self._exact_epsilon * self._n) + 1" in _text
_text = _text.replace("cap = math.floor(2 * self._exact_epsilon * self._n) + 1", "cap = math.floor(2 * self._exact_epsilon * self._n)")
exec(compile(_text, "alt_e_reference_cap", "exec"), globals())
