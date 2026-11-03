"""Probe the r10n06 survivor and the reference at a valid large kappa (verifier E3-e round 2).

Usage: python -I ledgers/E3/scripts/E3-e-r2/probe_r10n06_large_kappa.py PATH_TO_MUTANT PATH_TO_REFERENCE
One response: pair 0 choice A, CE_A - CE_B = 500 cents (probs 1/2, 1/2), kappa = 1e5 (valid: kappa > 0, project.html:212).
"""

import importlib.util
import sys


def load(path: str, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


resp = [{"pair_id": 0, "choice": "A", "prizes_a": [1000, 0], "probs_a": ["1/2", "1/2"], "prizes_b": [500], "probs_b": ["1"]}]
params = {"gamma": 0.4, "lambda": 2.0, "kappa": 1e5}
for label, path in (("mutant", sys.argv[1]), ("reference", sys.argv[2])):
    mod = load(path, label)
    try:
        print(label, "log_likelihood =", mod.log_likelihood(resp, params))
    except Exception as err:  # the probe reports every exception type
        print(label, "raised", type(err).__name__, err)
