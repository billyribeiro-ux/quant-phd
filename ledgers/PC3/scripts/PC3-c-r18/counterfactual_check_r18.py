"""Round 18, PC3 slice c. Independent recomputation of Lab 1 and Lab 3 numbers with the grader engine and reference replay."""

from __future__ import annotations

import sys

sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyE18-PC3-c/course/modules/PC/PC3/grader")

import engine  # noqa: E402
import reference  # noqa: E402


def rule(half_spread: int):  # type: ignore[no-untyped-def]
    def quote(state: dict[str, object]) -> tuple[int, int, int]:
        mid = 10_000
        for record in state["history"]:  # type: ignore[attr-defined]
            if record["filled"] is True:  # type: ignore[index]
                mid = record["fill_price_cents"]  # type: ignore[index]
        return mid - half_spread, mid + half_spread, 1

    return quote


for hs in (10, 15):
    log = engine.play(rule(hs), 0)
    fills = sum(1 for t in log["turns"] if t["filled"])
    res = reference.replay(log)
    print(f"half-spread {hs}: fills {fills}, settlement {log['settlement_cents']}, replay {res}")
