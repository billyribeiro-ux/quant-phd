"""Lab AP7-L01-1: DSSW (1990) Noise Trader Risk and Limits to Arbitrage.

SIMULATED: Simulates an overlapping generations economy with rational arbitrageurs
and noise traders with stochastic sentiment shocks, evaluating price volatility,
arbitrageur demand, and expected returns (De Long, Shleifer, Summers & Waldmann 1990).
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    seed = 42
    rng = np.random.default_rng(seed)
    n_periods = 1000

    # Model parameters
    risk_free_rate = 0.05  # r = 5% per period
    risk_aversion = 1.0  # gamma = 1.0 (CARA utility)
    dividend = 1.0  # constant dividend d = 1.0
    mu_sentiment = 0.10  # average noise-trader bullish sentiment
    sigma_sentiment = 0.25  # volatility of sentiment shocks
    noise_trader_share = 0.30  # fraction mu of noise traders in population

    # Fundamental value: V = d / r = 1.0 / 0.05 = 20.0
    fundamental_value = dividend / risk_free_rate

    # Generate i.i.d. sentiment shocks rho_t ~ N(mu_sentiment, sigma_sentiment^2)
    sentiment_shocks = rng.normal(mu_sentiment, sigma_sentiment, size=n_periods)

    # Analytical DSSW equilibrium price formula:
    # P_t = 1 + (d - r)/r + (mu*(rho_t - mu_s))/(1+r) + (mu*mu_s)/r - (2 * gamma * mu^2 * sigma_s^2) / (r * (1+r)^2)
    # For normalized asset with dividend d and risk-free return r:
    # Fundamental P* = d / r
    # Mispricing components:
    # 1. Average sentiment shift: (noise_trader_share * mu_sentiment) / risk_free_rate
    # 2. Resale price risk discount:
    #    -(2 * gamma * mu^2 * sigma^2) / (r * (1 + r)^2)
    # 3. Fluctuating sentiment shock: (noise_trader_share * (sentiment_shocks - mu_sentiment)) / (1 + risk_free_rate)

    avg_sentiment_shift = (noise_trader_share * mu_sentiment) / risk_free_rate
    risk_discount = (2.0 * risk_aversion * (noise_trader_share**2) * (sigma_sentiment**2)) / (
        risk_free_rate * ((1.0 + risk_free_rate) ** 2)
    )
    fluctuation = (noise_trader_share * (sentiment_shocks - mu_sentiment)) / (1.0 + risk_free_rate)

    prices = fundamental_value + avg_sentiment_shift - risk_discount + fluctuation

    # Arbitrageur and noise trader portfolio holdings
    # Arbitrageur demand: q_a,t = (d + E_t[P_{t+1}] - (1+r)P_t) / (2 * gamma * Var_t(P_{t+1}))
    # Var_t(P_{t+1}) = (noise_trader_share^2 * sigma_sentiment^2) / (1 + r)^2
    var_future_price = ((noise_trader_share**2) * (sigma_sentiment**2)) / ((1.0 + risk_free_rate) ** 2)
    expected_future_price = fundamental_value + avg_sentiment_shift - risk_discount

    arb_demand = (dividend + expected_future_price - (1.0 + risk_free_rate) * prices) / (
        2.0 * risk_aversion * var_future_price
    )
    noise_demand = arb_demand + sentiment_shocks / (2.0 * risk_aversion * var_future_price)

    # Calculate returns and performance metrics
    total_returns = (dividend + prices[1:]) / prices[:-1] - 1.0
    excess_returns = total_returns - risk_free_rate

    mean_price = float(np.mean(prices))
    price_volatility = float(np.std(prices, ddof=1))
    mean_excess_return = float(np.mean(excess_returns))
    mean_arb_demand = float(np.mean(arb_demand))
    mean_noise_demand = float(np.mean(noise_demand))

    print(f"Fundamental value V:               ${fundamental_value:.2f}")
    print(f"Mean equilibrium price:            ${mean_price:.2f}")
    print(f"Average sentiment price markup:    ${avg_sentiment_shift:.2f}")
    print(f"Noise trader risk price discount:  ${risk_discount:.4f}")
    print(f"Equilibrium price volatility:      ${price_volatility:.4f}")
    print(f"Mean asset excess return:          {mean_excess_return * 100:.2f}%")
    print(f"Mean arbitrageur share demand:     {mean_arb_demand:.4f}")
    print(f"Mean noise trader share demand:    {mean_noise_demand:.4f}")


main()
