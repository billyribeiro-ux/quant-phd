"""Round 1 verifier: does the L08 twin's bracket check ever reject a price near the LOWER bound?

Page L08 Lab 1 (line 121) says the bracket [1e-6, 10] check fails 'when the price is too close to the lower
bound or to the spot'. This script tests both ends with the twin's own functions.
Run from the checkout root: .venv/bin/python -I ledgers/FC2/scripts/FC2-c-r1/v1_l08_lower_bracket.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
src = (ROOT / "tests" / "labs" / "FC2" / "lab-FC2-L08-1.py").read_text(encoding="utf-8")
ns: dict[str, object] = {"__name__": "twin_l08"}
exec(compile(src.rsplit("\nmain()", 1)[0], "twin", "exec"), ns)
bs_call = ns["bs_call"]
lower_bound = ns["lower_bound"]
implied_volatility = ns["implied_volatility"]

for K in (80.0, 100.0, 120.0):
    L = lower_bound(100.0, K, 0.05, 1.0)  # type: ignore[operator]
    c_low = bs_call(100.0, K, 0.05, 1.0, 1e-6)  # type: ignore[operator]
    print(f"K={K:.0f}: L={L!r} C(1e-6)={c_low!r} C(1e-6)-L={c_low - L:.3e}")
for eps in (1e-7, 1e-10, 1e-13):
    p = 4.877057549928594 + eps
    try:
        v, n = implied_volatility(p, 100.0)  # type: ignore[operator]
        print(f"K=100 price=L+{eps:g}: accepted sigma={v:.6f} halvings={n}")
    except ValueError as exc:
        print(f"K=100 price=L+{eps:g}: rejected: {str(exc)[:60]}")
