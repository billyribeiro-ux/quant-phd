"""Re-derive Theorem 2.3 hypothesis counterexample and L02 numbers from the L02 twin (no edits to the twin)."""

import math
import pathlib

src = pathlib.Path("tests/labs/E5/lab-E5-L02-1.py").read_text(encoding="utf-8")
assert src.rstrip().endswith("main()")
ns: dict[str, object] = {"__name__": "twin_defs"}
exec(compile(src.rstrip()[: -len("main()")], "lab-E5-L02-1-defs", "exec"), ns)
simulate_economy = ns["simulate_economy"]
log_growth = ns["log_growth"]
residual_growth = ns["residual_growth"]
mean = ns["mean"]

a, k, l, y = simulate_economy(2026, 40)  # type: ignore[operator]
dln_a = log_growth(a)  # type: ignore[operator]
dln_k = log_growth(k)  # type: ignore[operator]
dln_l = log_growth(l)  # type: ignore[operator]
dln_y = log_growth(y)  # type: ignore[operator]
for alpha_chosen in (0.3, 0.5):
    res = residual_growth(dln_y, dln_k, dln_l, alpha_chosen)  # type: ignore[operator]
    gap = max(abs(r - x) for r, x in zip(res, dln_a, strict=True))
    print(f"chosen alpha {alpha_chosen}: max_t |Res_t - dlnA_t| = {gap:.6f}; mean residual {mean(res):.6f}")  # type: ignore[operator]
print(f"mean dlnA = {mean(dln_a):.6f}")  # type: ignore[operator]
print(f"0.016254 - 0.010665 = {0.016254 - 0.010665:.6f}")
