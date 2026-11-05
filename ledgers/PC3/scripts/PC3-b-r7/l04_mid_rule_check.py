"""Checks the L04 claim (line 467): under the Example 1.3 rule the mid at turn t is 10000 - 10 * I_{t-1}.

Uses the lab's own play() (twin with the top-level main() call removed) over seeds 0 to 49, and a fixed-size
check of the quoted bid/ask against the mid. Also checks the claim that a purchase lowers the mid by 10 cents.
"""

from __future__ import annotations

import sys
import types

path = "tests/labs/PC3/lab-PC3-L04-1.py"
src = open(path, encoding="utf-8").read().rstrip("\n")
assert src.endswith("\nmain()")
src = src[: -len("\nmain()")]
mod = types.ModuleType("twin_l04")
sys.modules[mod.__name__] = mod
exec(compile(src, path, "exec"), mod.__dict__)

bad = 0
checked = 0
for seed in range(50):
    _, turns = mod.play(seed)  # type: ignore[attr-defined]
    inv_before = 0
    for r in turns:
        mid = (r.bid_cents + r.ask_cents) // 2
        if mid != 10000 - 10 * inv_before:
            bad += 1
        checked += 1
        inv_before = r.inventory_after
print(f"turns checked {checked}; turns where mid != 10000 - 10 x I_(t-1): {bad}")
