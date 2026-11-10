"""Lab F3-L01-1: Cross-Asset Value and Momentum Sorts & 50/50 Combo Diversification.

Simulates monthly returns and signals across four asset classes (Equities, Bonds,
Currencies, Commodities) to construct value and momentum factor portfolios,
measure within-asset negative correlations, and verify Sharpe ratio expansion
under equal-risk combination following Asness, Moskowitz & Pedersen (2013).
"""

from __future__ import annotations

import numpy as np


def simulate_cross_asset_valmom(seed: int = 42) -> dict[str, object]:
    """Simulate value and momentum factor returns across four asset classes."""
    rng = np.random.default_rng(seed)
    n_months = 240
    asset_classes = ["Equities", "Bonds", "Currencies", "Commodities"]

    # Target annualized annualized statistics:
    # Individual factors: ~4% to 5% excess return, ~10% annual vol (Sharpe ~0.40 - 0.50)
    # Negative correlation within each asset class ~ -0.45 to -0.55
    dt = 1.0 / 12.0
    vol_mth = 0.10 * np.sqrt(dt)

    class_stats: dict[str, dict[str, float]] = {}
    all_val: list[np.ndarray] = []
    all_mom: list[np.ndarray] = []

    for ac in asset_classes:
        # Generate correlated bivariate normal returns for Value and Momentum
        # Base correlation -0.50
        rho = -0.50 + rng.uniform(-0.05, 0.05)
        cov = np.array([[vol_mth**2, rho * vol_mth**2], [rho * vol_mth**2, vol_mth**2]])
        mean = np.array([0.045 * dt, 0.048 * dt])

        ret = rng.multivariate_normal(mean, cov, size=n_months)
        val_ret = ret[:, 0]
        mom_ret = ret[:, 1]

        all_val.append(val_ret)
        all_mom.append(mom_ret)

        # 50/50 combo
        combo_ret = 0.5 * val_ret + 0.5 * mom_ret

        # Annualized statistics
        sr_val = float((np.mean(val_ret) / np.std(val_ret, ddof=1)) * np.sqrt(12))
        sr_mom = float((np.mean(mom_ret) / np.std(mom_ret, ddof=1)) * np.sqrt(12))
        sr_combo = float((np.mean(combo_ret) / np.std(combo_ret, ddof=1)) * np.sqrt(12))
        corr_vm = float(np.corrcoef(val_ret, mom_ret)[0, 1])

        class_stats[ac] = {
            "sr_val": round(sr_val, 2),
            "sr_mom": round(sr_mom, 2),
            "sr_combo": round(sr_combo, 2),
            "corr": round(corr_vm, 2),
        }

    # Global cross-asset diversified factor portfolios
    global_val = np.mean(all_val, axis=0)
    global_mom = np.mean(all_mom, axis=0)
    global_combo = 0.5 * global_val + 0.5 * global_mom

    sr_g_val = float((np.mean(global_val) / np.std(global_val, ddof=1)) * np.sqrt(12))
    sr_g_mom = float((np.mean(global_mom) / np.std(global_mom, ddof=1)) * np.sqrt(12))
    sr_g_combo = float((np.mean(global_combo) / np.std(global_combo, ddof=1)) * np.sqrt(12))
    corr_g = float(np.corrcoef(global_val, global_mom)[0, 1])

    return {
        "classes": class_stats,
        "global_sr_val": round(sr_g_val, 2),
        "global_sr_mom": round(sr_g_mom, 2),
        "global_sr_combo": round(sr_g_combo, 2),
        "global_corr": round(corr_g, 2),
    }


def main() -> None:
    print("Lab F3-L01-1 | Cross-Asset Value & Momentum Everywhere (AMP 2013)")
    print("-----------------------------------------------------------------")
    res = simulate_cross_asset_valmom(seed=42)
    classes = res["classes"]
    assert isinstance(classes, dict)

    print(f"{'Asset Class':<14} | {'SR(Val)':<8} | {'SR(Mom)':<8} | {'Corr(V,M)':<10} | {'SR(Combo)':<8}")
    print("-" * 60)
    for ac, st in classes.items():
        assert isinstance(st, dict)
        sr_v, sr_m = st["sr_val"], st["sr_mom"]
        cvm, src = st["corr"], st["sr_combo"]
        print(f"{ac:<14} | {sr_v:<8.2f} | {sr_m:<8.2f} | {cvm:<10.2f} | {src:<8.2f}")
    print("-" * 60)
    gsr_v, gsr_m = res["global_sr_val"], res["global_sr_mom"]
    g_corr, gsr_c = res["global_corr"], res["global_sr_combo"]
    print(f"{'Global All':<14} | {gsr_v:<8.2f} | {gsr_m:<8.2f} | {g_corr:<10.2f} | {gsr_c:<8.2f}")
    print("Negative correlation within every asset class doubles the combined Sharpe ratio.")


main()
