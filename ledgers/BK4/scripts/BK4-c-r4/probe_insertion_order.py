"""Probe: a valid call whose dictionaries list the members out of id order. Run with the reference and with mutant r4a.

Usage: probe_insertion_order.py <module_path>. The inputs are a valid case of the page's interface: member ids 1 to 4,
defaulter 4 with nothing, a residual of 1 cent, and survivors 3, 1, 2 given in that insertion order.
"""

import importlib.util
import sys

spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
sys.modules["candidate"] = mod
spec.loader.exec_module(mod)
margins = {3: 1, 1: 1, 2: 1, 4: 0}
funds = {3: 1, 1: 1, 2: 1, 4: 0}
got = mod.waterfall(1, 4, margins, funds, 0)
print("survivor_cents", got.survivor_cents, "uncovered", got.uncovered_cents)
