"""Verifier round 3, slice c: run the L08 twin's own inversion on the E3 price (0.50 at strike 120).

The twin is read as text, its trailing main() call is removed, and the remaining functions are executed
in a fresh namespace. Usage: python -I -W error recheck_L08_E3.py <path-to-twin>
"""
import sys

with open(sys.argv[1], encoding="utf-8") as fh:
    source = fh.read().replace("\nmain()\n", "\n")
namespace: dict[str, object] = {"__name__": "lab_l08_functions_only"}
exec(compile(source, sys.argv[1], "exec"), namespace)  # noqa: S102
implied_volatility = namespace["implied_volatility"]
bs_call = namespace["bs_call"]
sigma, halvings = implied_volatility(0.50, 120.0)  # type: ignore[operator]
print(f"E3 price 0.50 strike 120: sigma={sigma:.8f} halvings={halvings}")
print(f"check: bs_call at that sigma = {bs_call(100.0, 120.0, 0.05, 1.0, sigma):.8f} (target 0.5)")  # type: ignore[operator]
