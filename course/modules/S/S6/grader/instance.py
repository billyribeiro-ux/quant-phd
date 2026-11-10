"""Deterministic instance generator for S6 project autograder.

Generates simulated market return series, stock returns, event calendar,
announcement clusters, and exact reference values.
All data is SIMULATED.
"""

from __future__ import annotations

import math
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic, valid instance from seed (SIMULATED data)."""
    rng = random.Random(seed)

    # 1. Timeline configuration
    calendar_length = 260
    est_len = 50
    window = (-1, 1)

    # 2. Market model structural parameters
    alpha_true = round(0.0002 + 0.00008 * (seed % 5), 6)
    beta_true = round(0.80 + 0.06 * (seed % 7), 4)
    sigma_true = round(0.008 + 0.001 * (seed % 4), 4)

    # 3. Simulate market returns
    market: list[float] = []
    for _ in range(calendar_length):
        r_m = rng.gauss(0.0004, 0.011)
        market.append(round(r_m, 6))

    # 4. Generate 8 spaced event days
    base_events = [65, 90, 115, 140, 165, 190, 215, 240]
    shift = seed % 4
    event_days = [d + shift for d in base_events]

    # 5. Clusters (4 distinct clusters across the 8 events)
    clusters = ["q1", "q1", "q2", "q2", "q3", "q3", "q4", "q4"]

    # 6. Simulate stock returns with planted event shocks
    planted_shock = round(0.035 + 0.005 * (seed % 5), 4)
    stock: list[float] = []
    for t in range(calendar_length):
        eps = rng.gauss(0.0, sigma_true)
        ret = alpha_true + beta_true * market[t] + eps
        if t in event_days:
            # Positive announcement surprise on day 0 of event window
            ret += planted_shock
        stock.append(round(ret, 6))

    # 7. Compute ground-truth values via direct exact arithmetic
    # For each event, evaluate estimation window and event window
    cars: list[float] = []
    car_vars: list[float] = []
    a, b = window
    for ev in event_days:
        s_est = ev + a - est_len
        e_est = ev + a - 1
        est_stock = stock[s_est : e_est + 1]
        est_mkt = market[s_est : e_est + 1]

        # OLS on estimation window
        n_est = len(est_stock)
        m_bar = sum(est_mkt) / n_est
        s_bar = sum(est_stock) / n_est
        ss_m = sum((m - m_bar) ** 2 for m in est_mkt)
        sp_ms = sum((m - m_bar) * (s - s_bar) for m, s in zip(est_mkt, est_stock, strict=True))
        b_hat = sp_ms / ss_m
        a_hat = s_bar - b_hat * m_bar
        ss_res = sum((s - (a_hat + b_hat * m)) ** 2 for s, m in zip(est_stock, est_mkt, strict=True))
        sig2 = ss_res / (n_est - 2)

        # Event window abnormal returns and variance
        s_ev = ev + a
        e_ev = ev + b
        ev_stock = stock[s_ev : e_ev + 1]
        ev_mkt = market[s_ev : e_ev + 1]

        ev_cars = [s - (a_hat + b_hat * m) for s, m in zip(ev_stock, ev_mkt, strict=True)]
        c_val = sum(ev_cars)
        cars.append(c_val)

        c_var = sum(sig2 * (1.0 + 1.0 / n_est + ((m - m_bar) ** 2) / ss_m) for m in ev_mkt)
        car_vars.append(c_var)

    # Event cross-sectional t-stat
    k_events = len(cars)
    mean_car = sum(cars) / k_events
    s_car = math.sqrt(sum((c - mean_car) ** 2 for c in cars) / (k_events - 1))
    t_stat = mean_car / (s_car / math.sqrt(k_events))

    # Clustered t-stat
    g_clusters = 4
    cluster_devs: dict[str, float] = {c: 0.0 for c in set(clusters)}
    for c_val, cl in zip(cars, clusters, strict=True):
        cluster_devs[cl] += c_val - mean_car
    v_cr1 = (g_clusters / (g_clusters - 1)) * (sum(d**2 for d in cluster_devs.values()) / (k_events**2))
    clustered_t = mean_car / math.sqrt(v_cr1)

    return {
        "seed": seed,
        "calendar_length": calendar_length,
        "est_len": est_len,
        "window": window,
        "market": market,
        "stock": stock,
        "event_days": event_days,
        "clusters": clusters,
        "alpha_true": alpha_true,
        "beta_true": beta_true,
        "sigma_true": sigma_true,
        "planted_shock": planted_shock,
        "cars": cars,
        "car_vars": car_vars,
        "t_stat": t_stat,
        "clustered_t": clustered_t,
        "placebo_count": 6,
        "placebo_half_window": 4,
    }
