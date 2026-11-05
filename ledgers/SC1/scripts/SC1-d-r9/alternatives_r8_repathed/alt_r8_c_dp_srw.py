"""Alternative C (round 8): srw counts by dynamic programming over (position, running maximum capped at a)."""
from __future__ import annotations

import importlib.util

_spec = importlib.util.spec_from_file_location("ref_r8c", "/Users/billyribeiro/.fanout/wt/verifyE9-SC1-d/course/modules/SC/SC1/grader/reference.py")
_ref = importlib.util.module_from_spec(_spec)
assert _spec is not None and _spec.loader is not None
_spec.loader.exec_module(_ref)


def _dp(n: int, a: int) -> tuple[int, int]:
    # state: (position, min(running max, a)) -> number of walks; returns (#{max >= a}, #{S_n >= a})
    states: dict[tuple[int, int], int] = {(0, 0): 1}
    for _ in range(n):
        nxt: dict[tuple[int, int], int] = {}
        for (pos, top), w in states.items():
            for step in (1, -1):
                p2 = pos + step
                t2 = min(max(top, p2), a)
                nxt[(p2, t2)] = nxt.get((p2, t2), 0) + w
        states = nxt
    max_hits = sum(w for (_, top), w in states.items() if top >= a)
    end_hits = sum(w for (pos, _), w in states.items() if pos >= a)
    return max_hits, end_hits


def srw_max_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return _dp(n, a)[0]


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return _dp(n, a)[1]


reflection_tail = _ref.reflection_tail
discrete_max_exceedance = _ref.discrete_max_exceedance
nested_grid_counts = _ref.nested_grid_counts
