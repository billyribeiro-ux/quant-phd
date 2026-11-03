"""Probe (verifier E3-e round 2; run as: python -I gap_probe_log_likelihood.py PATH_TO_ELICIT): does log_likelihood refuse a response whose probabilities sum to 999/1000 (table row, project.html:225)?"""

import sys
from pathlib import Path

import importlib.util  # noqa: E402

path = sys.argv[1]
spec = importlib.util.spec_from_file_location("elicit_under_test", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
resp = [{"pair_id": 0, "choice": "A", "prizes_a": [-100, 300], "probs_a": ["1/2", "499/1000"],
         "prizes_b": [200], "probs_b": ["1"]}]
try:
    value = mod.log_likelihood(resp, {"gamma": 0.4, "lambda": 2.0, "kappa": 1.5})
    print(path.split("/")[-1], "log_likelihood returned", value)
except ValueError as err:
    print(path.split("/")[-1], "ValueError:", err)
