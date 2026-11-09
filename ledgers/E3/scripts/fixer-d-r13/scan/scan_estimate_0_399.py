"""Estimate-level scan of the reference over generator seeds: own participant (seed) and second participant (seed+7919).

Run from a directory holding elicit.py (= grader/reference.py) and instance.py. Prints, for each seed in the range,
whether elicit.estimate returns on the own and on the second participant, and the exception message if not.
usage: scan_estimate_0_399.py <lo> <hi>
"""

from __future__ import annotations

import json
import sys

import elicit as sol  # type: ignore[import-not-found]
from instance import make_instance  # type: ignore[import-not-found]

lo, hi = int(sys.argv[1]), int(sys.argv[2])
for seed in range(lo, hi + 1):
    row = []
    for label, s in (("own", seed), ("second", seed + 7_919)):
        responses = json.loads(str(make_instance(s)["responses_json"]))
        try:
            sol.estimate(responses)
            row.append(f"{label}=ok")
        except Exception as error:  # noqa: BLE001 - the scan records every failure mode
            row.append(f"{label}={type(error).__name__}: {str(error)[:120]}")
    if any("=ok" not in r for r in row):
        print(f"seed {seed}: " + " | ".join(row), flush=True)
print(f"scanned {lo}-{hi}", flush=True)
