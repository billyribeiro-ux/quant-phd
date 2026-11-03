"""Run one alternative from ledgers/E3/scripts/run_alternatives.py over a seed window (verifier E3-e round 2).

Usage (from the checkout root): python -I ledgers/E3/scripts/E3-e-r2/run_alt_one_r2.py alt1 0-49
The five alternatives are run as five processes so the window finishes sooner; each prints one line like the original.
"""

import importlib.util
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("run_alternatives", "ledgers/E3/scripts/run_alternatives.py")
mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
spec.loader.exec_module(mod)  # type: ignore[union-attr]
name, window = sys.argv[1], sys.argv[2]
mod.ALTERNATIVES = {name: mod.ALTERNATIVES[name]}
sys.argv = ["run_alternatives.py", "--seeds", window]
sys.exit(mod.main())
