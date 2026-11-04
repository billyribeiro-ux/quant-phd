"""Round-7 experiment: a valid hand case whose inequality multipliers are all positive, so the dual-residual floor
changes the value and an unfloored report is distinguishable (project.html:320). Also runs the unfloored-dual mutant.
Case: two assets, lower = upper = starting weights (valid: a bound equal to the start), turnover limit 0 (valid), sector
cap equal to the starting sector weight (valid, one sector holds both assets). Usage: python -I floor_degenerate_r7.py <grader_dir> <mutant_dir_out>
"""
import copy
import sys
from pathlib import Path

grader = Path(sys.argv[1])
sys.path.insert(0, str(grader))
import reference as ref  # noqa: E402

case = {
    "label": "SIMULATED degenerate hand case for the floor check, not a real portfolio",
    "gamma": 1.0, "mu": [0.3, 0.1], "sigma": [[1.0, 0.0], [0.0, 1.0]], "w0": [0.5, 0.5],
    "lower": [0.5, 0.5], "upper": [0.5, 0.5], "sector": [0, 0], "sector_caps": [1.0], "turnover_limit": 0.0,
}
out = ref.allocate(copy.deepcopy(case))
m = out["multipliers"]
ineq = {"lower": m["lower"], "upper": m["upper"], "sector": m["sector"], "turnover_plus": m["turnover_plus"],
        "turnover_minus": m["turnover_minus"], "turnover_total": [m["turnover_total"]]}
print("weights", out["weights"])
print("multipliers", {k: v for k, v in m.items()})
print("certificate", out["certificate"])
smallest = min(v for vals in ineq.values() for v in vals)
print("smallest inequality multiplier", smallest, "all positive:", smallest > 0)
print("reference dual residual", out["certificate"]["dual_residual"])
print("unfloored report would be", -smallest, "; agreement |unfloored - floored| =", abs(-smallest - max(0.0, -smallest)))
