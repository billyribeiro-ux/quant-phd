"""Witness for mutant e3d5_01: a set with no lottery that mixes a gain and a loss, where a zero prize is the 'gain'.

Run from a directory holding ref.py and mut.py (copies of the reference and the mutant): python3 -I v5_zero_prize_witness.py
"""
import importlib
import os
import sys

sys.path.insert(0, os.path.abspath('.'))
for modname in ("ref", "mut"):
    sol = importlib.import_module(modname)
    responses = [
        {"pair_id": 0, "choice": "A", "prizes_a": [0, -100], "probs_a": ["1/2", "1/2"], "prizes_b": [200], "probs_b": ["1"]},
        {"pair_id": 1, "choice": "B", "prizes_a": [500], "probs_a": ["1"], "prizes_b": [50, 900], "probs_b": ["1/2", "1/2"]},
    ]
    try:
        out = sol.estimate(responses)
        print(modname, "accepted the set; keys:", len(out))
    except ValueError as err:
        print(modname, "ValueError:", err)
    except RuntimeError as err:
        print(modname, "accepted the set (no ValueError) and then failed in the optimiser:", err)
