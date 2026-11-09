"""Largest reference gamma_hat over generator seeds 0-399 (own and second participant), and the fixed participants.

Shows whether any participant the suite can draw reaches gamma_hat above 0.999 (the clamp of mutant r11_03).
Run from a directory holding elicit.py (= grader/reference.py), instance.py and test_project.py.
"""

from __future__ import annotations

import json
import math

import elicit as sol  # type: ignore[import-not-found]
import test_project as tp  # type: ignore[import-not-found]
from instance import make_instance  # type: ignore[import-not-found]

best = (-1.0, None)
for seed in range(400):
    for s in (seed, seed + 7_919):
        try:
            fit = sol.estimate(json.loads(str(make_instance(s)["responses_json"])))
        except Exception:  # noqa: BLE001
            continue
        if fit["gamma_hat"] > best[0]:
            best = (fit["gamma_hat"], s)
print("max gamma_hat over own and second participants of seeds 0-399:", best)
resp26 = [{"pair_id": i, "choice": c, "prizes_a": pa, "probs_a": qa, "prizes_b": pb, "probs_b": qb} for i, c, pa, qa, pb, qb in tp.FIXED_26_ANSWERS]
print("fixed 26-response participant gamma_hat:", sol.estimate(resp26)["gamma_hat"])
print("fixed seed-49 participant gamma_hat:", sol.estimate(json.loads(str(tp.LARGE_LAMBDA["responses_json"])))["gamma_hat"])
print("math.log(999) =", math.log(999))
