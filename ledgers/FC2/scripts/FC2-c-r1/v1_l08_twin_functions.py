"""Round 1 verifier: call the L08 twin's own functions (its module body minus the top-level main() call).

Checks the Problem E3 claims (price 0.50 at strike 120 is accepted, volatility 0.102077, 37 halvings),
the E2 claim (price 0.462497 at strike 120 for sigma 0.10), and the bounds message rule.
Run from the checkout root: .venv/bin/python -I ledgers/FC2/scripts/FC2-c-r1/v1_l08_twin_functions.py
"""

from __future__ import annotations

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
src = (ROOT / "tests" / "labs" / "FC2" / "lab-FC2-L08-1.py").read_text(encoding="utf-8")
body = src.rsplit("\nmain()", 1)[0]
ns: dict[str, object] = {"__name__": "twin_l08"}
exec(compile(body, "lab-FC2-L08-1-body", "exec"), ns)  # the twin's own definitions only
implied_volatility = ns["implied_volatility"]
bs_call = ns["bs_call"]
lower_bound = ns["lower_bound"]

vol, n = implied_volatility(0.50, 120.0)  # type: ignore[operator]
print(f"E3 price 0.50 strike 120: accepted, sigma={vol:.6f} halvings={n} residual={bs_call(100.0, 120.0, 0.05, 1.0, vol) - 0.50:.3e}")  # type: ignore[operator]
print(f"E2 call K=120 sigma=0.10: {bs_call(100.0, 120.0, 0.05, 1.0, 0.10):.7f} currency units")  # type: ignore[operator]
print(f"lower bound K=120: {lower_bound(100.0, 120.0, 0.05, 1.0):.6f}")  # type: ignore[operator]
for price in (0.0, 0.5, 99.999, 100.0):
    try:
        v, k = implied_volatility(price, 120.0)  # type: ignore[operator]
        print(f"price {price}: accepted sigma={v:.6f} halvings={k}")
    except ValueError as exc:
        print(f"price {price}: rejected: {str(exc)[:70]}")
print(f"log2(1e11)={math.log2(1e11):.4f}")
