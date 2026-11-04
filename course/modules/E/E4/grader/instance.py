"""Per-learner instances for the E4 autograder: the price-informativeness model. All values are SIMULATED.

``make_instance(seed)`` is deterministic and uses only the standard library. From the seed alone it draws the two
inputs that the solver takes, the noise-trader volume ``noise_sd`` (the standard deviation sigma_u of the noise supply)
and the information cost ``info_cost`` (c, in units of terminal wealth):

* ``noise_sd`` is drawn uniformly from [0.500, 0.750] and rounded to three decimals;
* ``info_cost`` is drawn uniformly from [0.120, 0.150] and rounded to three decimals.

The other parameters of the model (risk aversion 2, prior precision 1 and signal precision 1) are fixed in solver.py,
so every instance uses them. The box is chosen so that every instance has one interior informed fraction. With these
constants, the interior root is the unique solution of tau_y(lambda) = tau_bar, where tau_bar = 2 exp(-4c) - 1 and tau_y
is strictly increasing in lambda, with tau_y(1) = 1 / (1 + 4 sigma_u^2) (project page, Propositions 3 and 4).
Over the box,
tau_bar lies in (0, 0.2377], because tau_bar(0.120) = 0.2376 and tau_bar(0.150) = 0.0976, while
tau_y(1) >= 1 / (1 + 4 * 0.75^2) = 0.3077. So 0 < tau_bar < tau_y(1) for every instance in the box. The suite re-checks
the interior condition on each seed it runs.

This module does not import the reference solution, which is excluded from deployment. Nothing here is a real market,
a real payoff or a real participant.
"""

from __future__ import annotations

import random

NOISE_SD_RANGE = (0.500, 0.750)
INFO_COST_RANGE = (0.120, 0.150)


def make_instance(seed: int) -> dict[str, float]:
    """The SIMULATED instance for a seed: the noise volume noise_sd and the information cost info_cost."""
    rng = random.Random(seed)
    noise_sd = round(rng.uniform(*NOISE_SD_RANGE), 3)
    info_cost = round(rng.uniform(*INFO_COST_RANGE), 3)
    return {"noise_sd": noise_sd, "info_cost": info_cost}
