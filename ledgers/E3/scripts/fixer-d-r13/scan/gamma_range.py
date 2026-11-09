"""Gamma-hat range of the reference over a chunk of generator seeds (own and second participant)."""
import json
import sys

import elicit as sol  # type: ignore[import-not-found]
from instance import make_instance  # type: ignore[import-not-found]

lo, hi = int(sys.argv[1]), int(sys.argv[2])
lows, highs = [], []
for seed in range(lo, hi + 1):
    for s in (seed, seed + 7_919):
        try:
            fit = sol.estimate(json.loads(str(make_instance(s)["responses_json"])))
        except Exception:  # noqa: BLE001
            continue
        lows.append((fit["gamma_hat"], s))
        highs.append((fit["gamma_hat"], s))
print("min", min(lows), "max", max(highs), "count", len(lows), flush=True)
