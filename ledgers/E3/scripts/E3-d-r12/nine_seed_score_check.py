"""For the nine non-gradable seeds: the score at the estimate of an alternative (elicit.py in the current directory),
on the own and the second participant, with the suite's own helpers (test_project._largest_score_component).

Run from a directory holding elicit.py, instance.py and test_project.py (QF_SEED is set by the caller).
"""

from __future__ import annotations

import json
import math

import elicit as sol  # type: ignore[import-not-found]
import test_project as tp  # type: ignore[import-not-found]
from instance import make_instance  # type: ignore[import-not-found]

for seed in (14, 89, 110, 235, 373, 108, 157, 165, 269):
    row = []
    for label, s in (("own", seed), ("second", seed + 7_919)):
        resp = json.loads(str(make_instance(s)["responses_json"]))
        parsed = [tp.parse(r) for r in resp]
        try:
            fit = sol.estimate(resp)
        except Exception as error:  # noqa: BLE001
            row.append(f"{label}=RAISES {type(error).__name__}")
            continue
        g, a, k = fit["gamma_hat"], fit["lambda_hat"], fit["kappa_hat"]
        score = min(tp._largest_score_component(parsed, g, a, k, 1e-5), tp._largest_score_component(parsed, g, a, k, 1e-6))
        row.append(f"{label}=ok score={score:.1e} gamma={g:.3g} lambda={a:.3g} kappa={k:.3g}")
    print(f"seed {seed}: " + " | ".join(row), flush=True)
