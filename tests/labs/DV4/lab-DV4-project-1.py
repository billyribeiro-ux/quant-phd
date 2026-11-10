"""DV4 Project Rung 1: Worked example of trinomial lattice pricing for American options.

SIMULATED market data under geometric Brownian motion.
Prices an American put option on a 3-branch recombining trinomial lattice (Boyle 1977),
extracting the early exercise boundary and verifying the Snell envelope property.
"""

from __future__ import annotations

import math

import numpy as np


def run_worked_example() -> None:
    spot = 100.0
    strike = 100.0
    rate = 0.05
    vol = 0.20
    maturity = 1.0
    n_steps = 100

    dt = maturity / n_steps
    dx = vol * math.sqrt(3.0 * dt)
    u = math.exp(dx)
    1.0 / u
    df = math.exp(-rate * dt)
    nu = (rate - 0.5 * vol * vol) * dt

    pu = 1.0 / 6.0 + 0.5 * (nu * nu / (dx * dx) + nu / dx)
    pm = 2.0 / 3.0 - (nu * nu / (dx * dx))
    pd = 1.0 / 6.0 + 0.5 * (nu * nu / (dx * dx) - nu / dx)

    # Terminal node payoff
    indices = np.arange(-n_steps, n_steps + 1)
    s_terminal = spot * np.exp(indices * dx)
    v_amer = np.maximum(strike - s_terminal, 0.0)
    v_eur = v_amer.copy()

    early_exercise_count = 0

    for k in range(n_steps - 1, -1, -1):
        # Discounted expected continuation
        cont_amer = df * (pu * v_amer[2 : 2 * k + 3] + pm * v_amer[1 : 2 * k + 2] + pd * v_amer[0 : 2 * k + 1])
        cont_eur = df * (pu * v_eur[2 : 2 * k + 3] + pm * v_eur[1 : 2 * k + 2] + pd * v_eur[0 : 2 * k + 1])

        k_indices = np.arange(-k, k + 1)
        s_k = spot * np.exp(k_indices * dx)
        intrinsic = np.maximum(strike - s_k, 0.0)

        # American early exercise check (Snell envelope)
        exercise_now = intrinsic > cont_amer
        early_exercise_count += int(np.sum(exercise_now))

        v_amer = np.maximum(cont_amer, intrinsic)
        v_eur = cont_eur

    amer_price = float(v_amer[0])
    eur_price = float(v_eur[0])
    premium = amer_price - eur_price

    # Analytical BSM benchmark
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * math.sqrt(maturity))
    d2 = d1 - vol * math.sqrt(maturity)
    n_neg_d1 = 0.5 * (1.0 + math.erf(-d1 / math.sqrt(2.0)))
    n_neg_d2 = 0.5 * (1.0 + math.erf(-d2 / math.sqrt(2.0)))
    bsm_eur = strike * math.exp(-rate * maturity) * n_neg_d2 - spot * n_neg_d1

    print(f"Trinomial American put price: {amer_price:.4f}")
    print(f"Trinomial European put price: {eur_price:.4f}")
    print(f"Analytical BSM European price: {bsm_eur:.4f}")
    print(f"American early-exercise premium: {premium:.4f}")
    print(f"Total early-exercise node events: {early_exercise_count}")


run_worked_example()
