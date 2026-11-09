"""Exercise the L08 twin's own functions (its trailing main() call removed) on the prices the page discusses.

Run: .venv/bin/python -I ledgers/FC2/scripts/FC2-c-r4/twin_claims.py
"""

from __future__ import annotations

import math
from pathlib import Path

src = Path("tests/labs/FC2/lab-FC2-L08-1.py").read_text(encoding="utf-8")
assert src.rstrip().endswith("\nmain()"), "twin must end with an unconditional main() call"
ns: dict[str, object] = {"__name__": "twin_L08"}
exec(compile(src.rstrip()[: -len("\nmain()")], "lab-FC2-L08-1-noMain", "exec"), ns)
implied_volatility = ns["implied_volatility"]
bs_call = ns["bs_call"]
lower_bound = ns["lower_bound"]


def attempt(label: str, price: float, strike: float) -> None:
    try:
        sig, halv = implied_volatility(price, strike)  # type: ignore[operator]
        print(f"{label}: accepted sigma={sig:.8f} halvings={halv} err_vs_truth=n/a")
    except ValueError as exc:
        print(f"{label}: rejected: {exc}")


print("C(10) K=100:", repr(bs_call(100.0, 100.0, 0.05, 1.0, 10.0)))
attempt("K=100 price 99.99995", 99.99995, 100.0)
print("C(10) K=120:", repr(bs_call(100.0, 120.0, 0.05, 1.0, 10.0)))
attempt("K=120 price 99.99995", 99.99995, 120.0)
attempt("K=120 price 0.50", 0.50, 120.0)
attempt("K=120 price 0.00", 0.0, 120.0)
attempt("K=120 price 100.00", 100.0, 120.0)
K_fwd = 100.0 * math.exp(0.05)
print("K=Se^(r tau)=", repr(K_fwd), "L=", repr(lower_bound(100.0, K_fwd, 0.05, 1.0)), "C(1e-6)=", repr(bs_call(100.0, K_fwd, 0.05, 1.0, 1e-6)))
attempt("K=Se^(rt) price 0.00001", 0.00001, K_fwd)
for K in (80.0, 100.0, 120.0):
    L = lower_bound(100.0, K, 0.05, 1.0)
    c = bs_call(100.0, K, 0.05, 1.0, 1e-6)
    print(f"K={K}: L={L!r} C(1e-6)={c!r} equal_as_doubles={L == c}")
# Window (L, C(1e-6)] for Lab 1's strikes
for K in (80.0, 100.0, 120.0):
    L = lower_bound(100.0, K, 0.05, 1.0)
    c = bs_call(100.0, K, 0.05, 1.0, 1e-6)
    print(f"K={K}: window nonempty={L < c}")
# Bisection halvings for E3 and the twin cases
