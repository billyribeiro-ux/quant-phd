"""Verifier check (FC2 slice c, round 3): run the L08 twin's own implied_volatility() on the claimed inputs.

Loads the twin source without its trailing top-level main() call, then calls the twin's functions directly.
Run: .venv/bin/python -I ledgers/FC2/scripts/FC2-c-r3/twin_claims.py
"""

from __future__ import annotations

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
src = (ROOT / "tests/labs/FC2/lab-FC2-L08-1.py").read_text(encoding="utf-8")
assert src.rstrip().endswith("main()"), "twin must end with a top-level main() call"
body = src.rstrip()[: -len("main()")]
ns: dict[str, object] = {"__name__": "twin_import"}
exec(compile(body, "lab-FC2-L08-1-no-main.py", "exec"), ns)  # noqa: S102 - local verifier check on a repo file

implied_volatility = ns["implied_volatility"]
lower_bound = ns["lower_bound"]
bs_call = ns["bs_call"]
K_STATE = 100.0 * math.exp(0.05)  # strike with K e^{-r tau} = S


def attempt(label: str, price: float, strike: float) -> None:
    try:
        sig, hal = implied_volatility(price, strike)  # type: ignore[operator]
        print(f"{label}: accepted sigma={sig:.8f} halvings={hal}")
    except ValueError as exc:
        print(f"{label}: ValueError: {exc}")


print("K=Se^{r tau} =", repr(K_STATE), "L =", repr(lower_bound(100.0, K_STATE, 0.05, 1.0)))  # type: ignore[operator]
print("C(1e-6) at K=Se^{r tau} =", repr(bs_call(100.0, K_STATE, 0.05, 1.0, 1e-6)))  # type: ignore[operator]
attempt("lower-end: price 0.00001 at K=Se^{r tau}", 0.00001, K_STATE)
attempt("lower-end: price 0.00004 at K=Se^{r tau} (above C(1e-6))", 0.00004, K_STATE)
attempt("upper-end: price 99.99995 at K=100", 99.99995, 100.0)
attempt("E3: price 0.50 at K=120", 0.50, 120.0)
for pr in (0.0, 4.0, 100.0, 120.0):
    attempt(f"rejected-list: price {pr} at K=100", pr, 100.0)
# Lab-1 strikes: is there any price in (L, C(1e-6)] ?
for K in (80.0, 100.0, 120.0):
    L = lower_bound(100.0, K, 0.05, 1.0)  # type: ignore[operator]
    c = bs_call(100.0, K, 0.05, 1.0, 1e-6)  # type: ignore[operator]
    print(f"Lab-1 strike {K}: L={L!r} C(1e-6)={c!r} window nonempty={c > L}")
