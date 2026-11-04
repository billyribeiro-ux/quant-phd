"""Probe: one input where the page requires ValueError (defaulter 3 is in the margins, not in the default funds)."""
import sys
sys.path.insert(0, sys.argv[1])
import clearing_house as sol  # noqa: E402

try:
    print("result:", sol.waterfall(10, 3, {1: 500, 2: 500, 3: 100}, {1: 40, 2: 60}, 30))
except Exception as exc:  # report the exception type
    print("raised", type(exc).__name__, str(exc))
