"""Witness for test_zero_probability_prize_contributes_nothing_to_the_likelihood: a correct engine (alt4, bisection
inversion of the prospect value, from ledgers/E3/scripts/run_alternatives.py) gives log-likelihoods that differ in the
last bits when a zero-probability prize is present, so the suite's exact equality fails. Usage: python3 zero_prob_witness.py
"""

from __future__ import annotations

import importlib.util
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("run_alternatives", ROOT / "ledgers" / "E3" / "scripts" / "run_alternatives.py")
assert spec is not None and spec.loader is not None
ra = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ra)
import sys  # noqa: E402
sys.path.insert(0, str(ROOT / "course" / "modules" / "E" / "E3" / "grader"))
from instance import make_instance  # noqa: E402

mod = types.ModuleType("alt4")
exec(compile(ra.build("alt4"), "alt4", "exec"), mod.__dict__)
RESPONSES_BASE = {"pair_id": 0, "choice": "A", "prizes_a": [-100, 300], "probs_a": ["1/2", "1/2"],
                  "prizes_b": [200], "probs_b": ["1"]}
for seed in (26, 44, 45):
    params = {"gamma": float(make_instance(seed)["gamma"]), "lambda": float(make_instance(seed)["lambda"]),
              "kappa": float(make_instance(seed)["kappa"])}
    with_zero = [RESPONSES_BASE | {"probs_a": ["0", "1"]}]
    without = [RESPONSES_BASE | {"prizes_a": [300], "probs_a": ["1"]}]
    a = mod.log_likelihood(with_zero, params)
    b = mod.log_likelihood(without, params)
    print(f"seed {seed}: alt4 with_zero={a!r} without={b!r} difference={a - b!r}")
