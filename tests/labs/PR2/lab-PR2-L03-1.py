"""Lab 3: Leverage aversion and borrowing constraints: The risk-parity Sharpe advantage.

Demonstrates the theoretical mechanism of Asness, Frazzini & Pedersen (2012):
When investors face borrowing constraints (leverage aversion), high-beta assets
are bid up and have lower Sharpe ratios, while low-risk assets offer higher Sharpe ratios.
Leveraging the balanced risk parity portfolio beats the equity/market portfolio.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # Asset 1: Low-risk/bonds (vol = 6%, SR = 0.70, exp return = 4.2% over rf)
    # Asset 2: High-risk/equities (vol = 18%, SR = 0.40, exp return = 7.2% over rf)
    # Correlation rho = 0.15, borrow cost spread c_b = 1.0% (100 bps over rf)
    vol1 = 0.06
    vol2 = 0.18
    sr1 = 0.70
    sr2 = 0.40
    rho = 0.15
    borrow_spread = 0.010

    mu1 = sr1 * vol1
    mu2 = sr2 * vol2
    cov12 = rho * vol1 * vol2
    cov = np.array([[vol1**2, cov12], [cov12, vol2**2]], dtype=np.float64)

    # 1. Market portfolio (equity heavy: 60/40 dollar weights)
    w_mkt = np.array([0.40, 0.60], dtype=np.float64)
    mu_mkt = float(w_mkt @ np.array([mu1, mu2]))
    vol_mkt = float(np.sqrt(w_mkt @ cov @ w_mkt))
    sr_mkt = mu_mkt / vol_mkt

    # 2. Unleveraged Risk Parity (ERC weights)
    # For 2 assets: w1 * (cov @ w)_1 = w2 * (cov @ w)_2
    # w_1 / w_2 = vol2 / vol1 when rho = 0
    w_rp_raw = np.array([1.0 / vol1, 1.0 / vol2], dtype=np.float64)
    w_rp = w_rp_raw / np.sum(w_rp_raw)
    mu_rp = float(w_rp @ np.array([mu1, mu2]))
    vol_rp = float(np.sqrt(w_rp @ cov @ w_rp))
    sr_rp = mu_rp / vol_rp

    # 3. Leveraged Risk Parity scaled to match Market Volatility
    leverage = vol_mkt / vol_rp
    w_lev_rp = leverage * w_rp
    gross_ret_lev = float(w_lev_rp @ np.array([mu1, mu2]))
    borrow_cost = (leverage - 1.0) * borrow_spread
    net_ret_lev = gross_ret_lev - borrow_cost
    vol_lev = float(np.sqrt(w_lev_rp @ cov @ w_lev_rp))
    sr_lev_net = net_ret_lev / vol_lev

    print(f"Asset 1 (Bonds) SR: {sr1:.2f}, Asset 2 (Equities) SR: {sr2:.2f}")
    print(f"Market (60/40) Return: {mu_mkt * 100:.2f}%, Vol: {vol_mkt * 100:.2f}%, SR: {sr_mkt:.4f}")
    print(f"Unleveraged RP Return: {mu_rp * 100:.2f}%, Vol: {vol_rp * 100:.2f}%, SR: {sr_rp:.4f}")
    print(f"Required Leverage for Vol Match: {leverage:.2f}x")
    print(f"Leveraged RP Gross Return: {gross_ret_lev * 100:.2f}%, Borrow Drag: {borrow_cost * 100:.2f}%")
    print(f"Leveraged RP Net Return: {net_ret_lev * 100:.2f}%, Vol: {vol_lev * 100:.2f}%, Net SR: {sr_lev_net:.4f}")
    print(f"Net Sharpe Premium over Market: {sr_lev_net - sr_mkt:+.4f}")


main()
