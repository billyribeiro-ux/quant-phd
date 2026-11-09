"""Reference solution for the SC2 project: the Itô derivations engine, ito_checks.py.

Standard library only. All seeded-simulation functions consume random numbers in one fixed order:
path by path (path-major), and within a path step by step, using ``random.Random(seed).gauss(0.0, 1.0)``.
Any implementation following that exact contract reproduces the reference numbers.
"""

from __future__ import annotations

import math
import random
from typing import Any

VALID_TRANSFORMS = frozenset(str(i) for i in range(1, 11))
GBM_TRANSFORMS = frozenset(str(i) for i in range(1, 6))


def value(transform: str, t: float, x: float, instance: dict[str, Any]) -> float:
    """Evaluate the transform function f(t, x) for the specified transform index (1 to 10).

    Transforms 1-5 have base GBM and require x > 0.
    Transforms 6-10 have base OU and accept all real x.
    """
    t_key = str(transform)
    if t_key not in VALID_TRANSFORMS:
        raise ValueError(f"unknown transform {transform!r}; must be one of 1 through 10")
    if t_key in GBM_TRANSFORMS and x <= 0:
        raise ValueError(f"transform {t_key} requires positive state x, got {x}")

    if t_key == "1":
        return math.log(x)
    elif t_key == "2":
        return float(x ** float(instance["p"]))
    elif t_key == "3":
        return 1.0 / x
    elif t_key == "4":
        return math.exp(-float(instance["r"]) * t) * x
    elif t_key == "5":
        a = float(instance["a"])
        return x / (a + x)
    elif t_key == "6":
        return float(instance["c"]) + float(instance["b"]) * x
    elif t_key == "7":
        return x * x
    elif t_key == "8":
        return math.exp(x)
    elif t_key == "9":
        tau = float(instance["tbar"]) - t
        kappa = float(instance["kappa"])
        a0 = float(instance["a0"])
        a1 = float(instance["a1"])
        b_val = (1.0 - math.exp(-kappa * tau)) / kappa
        a_val = a0 * (b_val - tau) - a1 * (b_val**2)
        return math.exp(-a_val - b_val * x)
    elif t_key == "10":
        kappa = float(instance["kappa"])
        return math.exp(kappa * t) * x
    raise ValueError(f"unhandled transform {transform!r}")


def coefficients(transform: str, t: float, x: float, instance: dict[str, Any]) -> tuple[float, float]:
    """Compute the drift mu_Y(t, x) and diffusion sigma_Y(t, x) of the transformed process Y_t = f(t, X_t).

    Returns:
        (drift, diffusion) tuple of floats.
    """
    t_key = str(transform)
    if t_key not in VALID_TRANSFORMS:
        raise ValueError(f"unknown transform {transform!r}; must be one of 1 through 10")
    if t_key in GBM_TRANSFORMS and x <= 0:
        raise ValueError(f"transform {t_key} requires positive state x, got {x}")

    mu = float(instance["mu"])
    sigma = float(instance["sigma"])
    kappa = float(instance["kappa"])
    theta = float(instance["theta"])

    if t_key == "1":
        return mu - 0.5 * sigma * sigma, sigma
    elif t_key == "2":
        p = float(instance["p"])
        val = x**p
        drift = (p * mu + 0.5 * p * (p - 1.0) * sigma * sigma) * val
        diff = p * sigma * val
        return drift, diff
    elif t_key == "3":
        drift = (sigma * sigma - mu) / x
        diff = -sigma / x
        return drift, diff
    elif t_key == "4":
        r = float(instance["r"])
        disc = math.exp(-r * t)
        drift = (mu - r) * disc * x
        diff = sigma * disc * x
        return drift, diff
    elif t_key == "5":
        a = float(instance["a"])
        denom = a + x
        drift = (a * x / (denom * denom)) * (mu - (sigma * sigma * x) / denom)
        diff = a * sigma * x / (denom * denom)
        return drift, diff
    elif t_key == "6":
        b = float(instance["b"])
        drift = b * kappa * (theta - x)
        diff = b * sigma
        return drift, diff
    elif t_key == "7":
        drift = 2.0 * kappa * x * (theta - x) + sigma * sigma
        diff = 2.0 * sigma * x
        return drift, diff
    elif t_key == "8":
        ex = math.exp(x)
        drift = (kappa * (theta - x) + 0.5 * sigma * sigma) * ex
        diff = sigma * ex
        return drift, diff
    elif t_key == "9":
        tau = float(instance["tbar"]) - t
        a0 = float(instance["a0"])
        a1 = float(instance["a1"])
        b_val = (1.0 - math.exp(-kappa * tau)) / kappa
        a_val = a0 * (b_val - tau) - a1 * (b_val**2)
        p_val = math.exp(-a_val - b_val * x)
        exp_kt = math.exp(-kappa * tau)
        db_dtau = exp_kt
        da_dtau = a0 * (exp_kt - 1.0) - 2.0 * a1 * b_val * exp_kt
        drift = p_val * (da_dtau + x * db_dtau - kappa * (theta - x) * b_val + 0.5 * sigma * sigma * b_val * b_val)
        diff = -sigma * b_val * p_val
        return drift, diff
    elif t_key == "10":
        ekt = math.exp(kappa * t)
        drift = kappa * theta * ekt
        diff = sigma * ekt
        return drift, diff
    raise ValueError(f"unhandled transform {transform!r}")


def residual(transform: str, instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    """Compute the mean and standard error of the discrete Itô residual across simulated base paths.

    Residual for path j is:
        R_j = [f(H, x_N) - f(0, x_0)] - sum_{k=0}^{N-1} [mu_Y(t_k, x_k) Delta t + sigma_Y(t_k, x_k) Delta B_k]

    Returns:
        (mean, standard_error) tuple of floats.
    """
    t_key = str(transform)
    if t_key not in VALID_TRANSFORMS:
        raise ValueError(f"unknown transform {transform!r}; must be one of 1 through 10")
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    n_paths = int(instance["n_paths"])
    if n_paths < 2:
        raise ValueError("n_paths must be at least 2")

    horizon = float(instance["H"])
    dt = horizon / n_steps
    sq_dt = math.sqrt(dt)
    mu = float(instance["mu"])
    sigma = float(instance["sigma"])
    kappa = float(instance["kappa"])
    theta = float(instance["theta"])

    is_gbm = t_key in GBM_TRANSFORMS
    gbm_drift = (mu - 0.5 * sigma * sigma) * dt
    gbm_vol = sigma * sq_dt

    rng = random.Random(int(instance["seed"]))
    res_list: list[float] = []

    for _ in range(n_paths):
        x = float(instance["s0"]) if is_gbm else float(instance["x0"])
        t = 0.0
        y0 = value(t_key, 0.0, x, instance)
        ito_sum = 0.0
        for _ in range(n_steps):
            z = rng.gauss(0.0, 1.0)
            db = sq_dt * z
            m, s = coefficients(t_key, t, x, instance)
            ito_sum += m * dt + s * db
            if is_gbm:
                x *= math.exp(gbm_drift + gbm_vol * z)
            else:
                x += kappa * (theta - x) * dt + sigma * db
            t += dt
        yn = value(t_key, horizon, x, instance)
        res_list.append((yn - y0) - ito_sum)

    mean = sum(res_list) / n_paths
    var = sum((r - mean) ** 2 for r in res_list) / (n_paths - 1)
    se = math.sqrt(var / n_paths)
    return mean, se
