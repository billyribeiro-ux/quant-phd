"""Lab SR3-project-1 (Rung 1 Worked Example): Full Systemic Risk Monitor Pipeline.

SIMULATED: fully solved instance of the Atlas A19 Systemic Risk Monitor (`atlas.systemic`),
incorporating CoVaR, Marginal Expected Shortfall, SRISK capital shortfall index,
Eisenberg-Noe network clearing, and prudential alert monitoring.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import linprog


def fit_quantile_reg(y: np.ndarray, x: np.ndarray, q: float) -> np.ndarray:
    t_obs, k_vars = x.shape
    c = np.concatenate([np.zeros(k_vars), q * np.ones(t_obs), (1.0 - q) * np.ones(t_obs)])
    eye_t = np.eye(t_obs)
    res = linprog(
        c,
        A_eq=np.hstack([x, eye_t, -eye_t]),
        b_eq=y,
        bounds=[(None, None)] * k_vars + [(0.0, None)] * (2 * t_obs),
        method="highs",
    )
    return np.asarray(res.x[:k_vars], dtype=np.float64)


def main() -> None:
    rng = np.random.default_rng(303)
    t_obs = 500

    # Macro volatility state M_t
    vol_state = np.zeros(t_obs)
    for t in range(1, t_obs):
        vol_state[t] = 0.60 * vol_state[t - 1] + rng.normal(0.0, 0.01)

    # Market returns R_sys
    scale = np.sqrt(rng.chisquare(df=4, size=t_obs) / 4.0)
    r_sys = 0.0003 - 0.20 * vol_state + rng.normal(0.0, 0.011, size=t_obs) / np.maximum(scale, 1e-4)

    # 4 Institutions: returns, equities, debts
    names = ["Bank 1", "Bank 2", "Bank 3", "Bank 4"]
    betas = [1.50, 1.20, 0.90, 0.70]
    equities = np.array([120.0, 85.0, 210.0, 55.0])
    debts = np.array([850.0, 620.0, 1600.0, 440.0])

    r_insts: list[np.ndarray] = []
    for b in betas:
        noise = rng.normal(0.0, 0.012, size=t_obs)
        r_insts.append(b * r_sys + 0.05 * vol_state + noise)

    # 1. CoVaR and Delta-CoVaR
    ones = np.ones((t_obs, 1))
    delta_covars: list[float] = []
    for r_i in r_insts:
        # Static institution VaR
        var_i_05 = float(np.quantile(r_i, 0.05))
        var_i_50 = float(np.quantile(r_i, 0.50))
        x_sys = np.column_stack([ones, r_i])
        b_sys = fit_quantile_reg(r_sys, x_sys, q=0.05)
        d_cov = float(b_sys[1] * (var_i_05 - var_i_50))
        delta_covars.append(d_cov)

    # 2. MES and LRMES
    var_sys_05 = float(np.quantile(r_sys, 0.05))
    crisis_mask = r_sys <= var_sys_05
    mes_values = [float(-np.mean(r_i[crisis_mask])) for r_i in r_insts]
    var_s = float(np.var(r_sys, ddof=1))
    lrmes_values = [float(1.0 - (1.0 - 0.40) ** (np.cov(r_i, r_sys, ddof=1)[0, 1] / var_s)) for r_i in r_insts]

    # 3. SRISK Panel
    k = 0.08
    cs = k * debts - (1.0 - k) * (1.0 - np.array(lrmes_values)) * equities
    srisks = np.maximum(0.0, cs)
    total_srisk = float(np.sum(srisks))
    srisk_pcts = (srisks / total_srisk * 100.0) if total_srisk > 0 else np.zeros_like(srisks)

    # 4. Network Clearing under targeted shock
    l_mat = np.array(
        [
            [0.0, 20.0, 15.0, 10.0],
            [15.0, 0.0, 20.0, 15.0],
            [20.0, 15.0, 0.0, 15.0],
            [10.0, 20.0, 15.0, 0.0],
        ]
    )
    p_bar = np.sum(l_mat, axis=1)
    z_external = np.array([0.0, 25.0, 35.0, 20.0])  # Bank 1 wiped out
    b_senior = np.array([12.0, 10.0, 15.0, 8.0])

    pi = l_mat / p_bar[:, None]
    p = p_bar.copy()
    for _ in range(500):
        p_next = np.minimum(p_bar, np.maximum(0.0, z_external + pi.T @ p - b_senior))
        if np.max(np.abs(p_next - p)) < 1e-10:
            break
        p = p_next
    defaults = (p < p_bar - 1e-7).astype(int)

    # 5. Alert Monitor
    monitor_thresholds = {"delta_covar": -0.015, "mes": 0.035, "srisk_pct": 30.0, "network_defaults": 1}
    breaches = {
        "delta_covar": any(dc < monitor_thresholds["delta_covar"] for dc in delta_covars),
        "mes": any(m > monitor_thresholds["mes"] for m in mes_values),
        "srisk_pct": any(sp > monitor_thresholds["srisk_pct"] for sp in srisk_pcts),
        "network_defaults": int(np.sum(defaults)) >= monitor_thresholds["network_defaults"],
    }
    severity = "CRITICAL" if sum(breaches.values()) >= 3 else "WARNING"

    print("=== Atlas A19 Systemic-Risk Monitor (Full Pipeline) ===")
    print(f"Systemic SRISK (Total): ${total_srisk:.2f}B")
    print("-" * 75)
    print(f"{'Bank':<10} {'Delta-CoVaR':<15} {'MES (5%)':<12} {'LRMES':<10} {'SRISK ($B)':<12} {'Share (%)':<10}")
    print("-" * 75)
    for i, name in enumerate(names):
        mes_str = f"{mes_values[i] * 100:<11.2f}%"
        lrmes_str = f"{lrmes_values[i] * 100:<9.1f}%"
        srisk_str = f"${srisks[i]:<11.2f}"
        pct_str = f"{srisk_pcts[i]:<9.1f}%"
        print(f"{name:<10} {delta_covars[i]:<15.4f} {mes_str} {lrmes_str} {srisk_str} {pct_str}")
    print("-" * 75)
    print(f"Network Cascade: {int(np.sum(defaults))}/4 defaults. Clearing shortfall: ${np.sum(p_bar - p):.1f}B")
    print(f"Alert Monitor Status: {severity} ({sum(breaches.values())}/4 indicators breached)")


main()
