"""Diagnose the float alternatives on the gamma boundary cases: prints the exception message, or the budget gap.

Usage: python -I diagnose_gamma_r12.py <repo_root> <alt_file> <seed> <gamma>
"""

import json
import sys
from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

repo, alt, seed, gamma = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
sys.path.insert(0, str(repo / "course/modules/M/M7/grader"))
from instance import make_instance  # noqa: E402

case = json.loads(make_instance(seed)["payload"])
case["gamma"] = gamma
spec = spec_from_file_location("alt", alt)
mod = module_from_spec(spec)
sys.modules["alt"] = mod
spec.loader.exec_module(mod)
try:
    out = mod.allocate(case)
    w = out["weights"]
    print("ok: budget gap", float(sum(Fraction(x) for x in w) - 1), "min weight", min(w), "certificate", out["certificate"])
except Exception as exc:  # noqa: BLE001
    print("raised", type(exc).__name__, str(exc)[:200])
