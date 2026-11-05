"""Round 10, slice E4-c: the clearing price at the L08 Example 1.1 parameters (a = 2, unit variances, sigma_u^2 = 1)
solved numerically (same solver as independent_L07_L08.py) against the closed form of L08 Proposition 3.1."""
import importlib.util
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("ind", str(Path(__file__).with_name("independent_L07_L08.py")))
src = Path(__file__).with_name("independent_L07_L08.py").read_text(encoding="utf-8").split("# L07 base and an alternative")[0]
ns = {}
exec(compile(src, "independent_L07_L08_head", "exec"), ns)
for lam in (0.5, 1.0):
    prm = {"sv2": 1.0, "se2": 1.0, "a": 2.0, "lam": lam, "su2": 1.0}
    th, cf, worst = ns["check_price"](prm)
    beta_cf = cf[0]
    print(f"Example 1.1 lam {lam}: numeric theta_s {th[0]:.12f} theta_u {th[1]:.12f} | closed form {cf[0]:.12f} {cf[1]:.12f} | max |residual| {worst:.2e}")
