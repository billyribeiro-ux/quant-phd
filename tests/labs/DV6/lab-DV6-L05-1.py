"""Lab 5 · Market Footprint of Dealer Hedging Flows & Intraday Momentum.

Simulates the market footprint of endogenous dealer delta rebalancing flows,
demonstrating the Baltussen, Da, Lammers & Martens (2021) empirical finding that
dealer hedging demand induces strong intraday momentum near the market close
on seed 42 (SIMULATED).
"""

from __future__ import annotations

import math

import numpy as np


def simulate_intraday_hedging_momentum(
    n_days: int = 10000,
    dealer_gamma_regime: str = "short",  # "neutral", "long", or "short"
    feedback_strength: float = 0.35,
    sigma_daily: float = 0.012,
    seed: int = 42,
) -> dict[str, float]:
    """Simulate intraday morning vs late-afternoon return correlation under dealer hedging.

    Following Baltussen et al. (2021):
    Divide trading day into Period 1 (Open to 3:30 PM, fraction 11/12) and
    Period 2 (3:30 PM to 4:00 PM close, fraction 1/12).
    In Period 2, dealers execute delta-hedging rebalancing orders proportional
    to the accumulated Period 1 market move:
    Flow_dealer = Gamma_dealer * Return_Period1.
    Market impact creates end-of-day price pressure:
    Return_Period2 = Exogenous_Shock2 + Feedback_Coefficient * Return_Period1.
    """
    rng = np.random.default_rng(seed)

    t1_frac = 11.0 / 12.0
    t2_frac = 1.0 / 12.0

    vol_1 = sigma_daily * math.sqrt(t1_frac)
    vol_2 = sigma_daily * math.sqrt(t2_frac)

    # Exogenous innovations
    z1 = rng.standard_normal(n_days)
    z2 = rng.standard_normal(n_days)

    ret_period1 = vol_1 * z1

    if dealer_gamma_regime == "neutral":
        coeff = 0.0
    elif dealer_gamma_regime == "long":
        # Long gamma: dealers buy when down, sell when up (stabilizing / negative feedback)
        coeff = -feedback_strength
    elif dealer_gamma_regime == "short":
        # Short gamma: dealers sell when down, buy when up (trend-reinforcing / momentum)
        coeff = feedback_strength
    else:
        raise ValueError(f"Unknown regime: {dealer_gamma_regime}")

    # Period 2 return includes endogenous hedging flow footprint
    ret_period2 = vol_2 * z2 + coeff * ret_period1

    # Statistical evaluation
    corr = float(np.corrcoef(ret_period1, ret_period2)[0, 1])

    # Momentum strategy: take position in Period 2 with sign of Period 1
    # PnL = sign(ret_period1) * ret_period2
    strat_returns = np.sign(ret_period1) * ret_period2
    mean_strat_bps = float(np.mean(strat_returns) * 10000.0)
    win_rate = float(np.mean(strat_returns > 0))
    t_stat = float(np.mean(strat_returns) / (np.std(strat_returns, ddof=1) / math.sqrt(n_days)))

    return {
        "correlation": corr,
        "mean_strat_bps": mean_strat_bps,
        "win_rate": win_rate,
        "t_stat": t_stat,
    }


def main() -> None:
    n_days = 20000

    # 1. Neutral Market (No Dealer Hedging Flows)
    res_neutral = simulate_intraday_hedging_momentum(n_days=n_days, dealer_gamma_regime="neutral", seed=42)

    # 2. Long Gamma Market (Overwriting / Structured Note Issuance Dampening)
    res_long = simulate_intraday_hedging_momentum(n_days=n_days, dealer_gamma_regime="long", seed=42)

    # 3. Short Gamma Market (Baltussen et al. 2021 Intraday Momentum Footprint)
    res_short = simulate_intraday_hedging_momentum(n_days=n_days, dealer_gamma_regime="short", seed=42)

    print("=== Lab 5: Hedging Flow Footprint & Intraday Momentum ===")
    print("Regime: Neutral (Martingale Benchmark):")
    print(f"  Intraday Return Correlation (P1 vs P2): {res_neutral['correlation']:.4f}")
    ret_neu, t_neu = res_neutral["mean_strat_bps"], res_neutral["t_stat"]
    print(f"  End-of-Day Momentum Return:             {ret_neu:.2f} bps (t-stat: {t_neu:.2f})")
    print(f"  Momentum Win Rate:                      {res_neutral['win_rate'] * 100.0:.2f}%")

    print("\nRegime: Dealer Long Gamma (Volatility Dampening):")
    print(f"  Intraday Return Correlation (P1 vs P2): {res_long['correlation']:.4f}")
    ret_long, t_long = res_long["mean_strat_bps"], res_long["t_stat"]
    print(f"  End-of-Day Momentum Return:             {ret_long:.2f} bps (t-stat: {t_long:.2f})")
    print(f"  Reversal Win Rate:                      {(1.0 - res_long['win_rate']) * 100.0:.2f}%")

    print("\nRegime: Dealer Short Gamma (Baltussen et al. 2021 Momentum Footprint):")
    print(f"  Intraday Return Correlation (P1 vs P2): {res_short['correlation']:.4f}")
    ret_sh, t_sh = res_short["mean_strat_bps"], res_short["t_stat"]
    print(f"  End-of-Day Momentum Return:             {ret_sh:.2f} bps (t-stat: {t_sh:.2f})")
    print(f"  Momentum Win Rate:                      {res_short['win_rate'] * 100.0:.2f}%")


main()
