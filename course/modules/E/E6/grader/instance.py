"""Per-learner instances for the E6 New Keynesian model solver (nk_solver.py).

make_instance(seed) is deterministic. It returns a SIMULATED case of the three-equation New Keynesian model:
structural parameters beta (discount factor), sigma (intertemporal elasticity / CRRA risk aversion),
kappa (slope of the NK Phillips curve), phi_pi (Taylor rule inflation coefficient), phi_y (Taylor rule
output gap coefficient), rho (shock persistence), and the impulse response horizon.

The instances are regime-balanced: approximately half the seeds produce determinate equilibria where the
generalized Taylor principle holds, and approximately half produce indeterminate equilibria.
"""

from __future__ import annotations

import json
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic, regime-balanced New Keynesian model parameter instance."""
    rng = random.Random(f"E6-nk-solver/{int(seed)}")
    beta = round(rng.uniform(0.96, 0.995), 4)
    sigma = round(rng.uniform(0.5, 3.0), 3)
    kappa = round(rng.uniform(0.05, 0.35), 3)
    rho = round(rng.uniform(-0.75, 0.75), 3)
    horizon = rng.choice([10, 15, 20, 25])

    # Balanced determinacy: even seeds produce determinate equilibria, odd seeds indeterminate
    if seed % 2 == 0:
        phi_y = round(rng.uniform(0.1, 0.8), 3)
        crit = 1.0 - (1.0 - beta) * phi_y / kappa
        phi_pi = round(crit + rng.uniform(0.2, 1.5), 3)
    else:
        phi_y = round(rng.uniform(0.0, 0.4), 3)
        crit = 1.0 - (1.0 - beta) * phi_y / kappa
        phi_pi = round(max(0.0, crit - rng.uniform(0.1, 0.6)), 3)

    det_metric = kappa * (phi_pi - 1.0) + (1.0 - beta) * phi_y
    is_det = bool(det_metric > 1e-12)

    case: dict[str, Any] = {
        "label": f"SIMULATED NK model instance, seed {int(seed)}",
        "beta": beta,
        "sigma": sigma,
        "kappa": kappa,
        "phi_pi": phi_pi,
        "phi_y": phi_y,
        "rho": rho,
        "horizon": horizon,
        "is_determinate": is_det,
    }
    return {
        "seed": int(seed),
        "label": case["label"],
        "payload": json.dumps(case, sort_keys=True),
    }
