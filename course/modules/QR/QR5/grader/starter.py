"""Starter template for QR5 project: Deep Hedging vs. Delta Hedging.

Fill in each function and class to complete the project.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def simulate_gbm_paths(
    s0: float,
    mu: float,
    sigma: float,
    t_exp: float,
    n_steps: int,
    n_paths: int,
    rng: np.random.Generator,
) -> NDArray[np.float64]:
    """Simulate asset price paths under Geometric Brownian Motion."""
    raise NotImplementedError("Implement simulate_gbm_paths")


def simulate_jump_diffusion_paths(
    s0: float,
    mu: float,
    sigma: float,
    lambda_j: float,
    mu_j: float,
    sigma_j: float,
    t_exp: float,
    n_steps: int,
    n_paths: int,
    rng: np.random.Generator,
) -> NDArray[np.float64]:
    """Simulate asset price paths under Merton jump-diffusion dynamics."""
    raise NotImplementedError("Implement simulate_jump_diffusion_paths")


def black_scholes_call_price(
    s: NDArray[np.float64],
    k: float,
    tau: NDArray[np.float64],
    sigma: float,
    r: float,
) -> NDArray[np.float64]:
    """Vectorized Black-Scholes European call option pricing."""
    raise NotImplementedError("Implement black_scholes_call_price")


def black_scholes_call_delta(
    s: NDArray[np.float64],
    k: float,
    tau: NDArray[np.float64],
    sigma: float,
    r: float,
) -> NDArray[np.float64]:
    """Vectorized Black-Scholes European call option delta."""
    raise NotImplementedError("Implement black_scholes_call_delta")


def black_scholes_gamma(
    s: NDArray[np.float64],
    k: float,
    tau: NDArray[np.float64],
    sigma: float,
    r: float,
) -> NDArray[np.float64]:
    """Vectorized Black-Scholes gamma."""
    raise NotImplementedError("Implement black_scholes_gamma")


def whalley_wilmott_bandwidth(
    s: NDArray[np.float64],
    k: float,
    tau: NDArray[np.float64],
    sigma: float,
    r: float,
    cost_rate: float,
    risk_aversion: float,
) -> NDArray[np.float64]:
    """Compute Whalley & Wilmott (1997) asymptotic no-trade band half-width."""
    raise NotImplementedError("Implement whalley_wilmott_bandwidth")


def compute_hedging_pnl(
    paths: NDArray[np.float64],
    deltas: NDArray[np.float64],
    strike: float,
    cost_rate: float,
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Compute hedging P&L, trading gain/loss, and transaction costs for a short call position."""
    raise NotImplementedError("Implement compute_hedging_pnl")


def cvar_loss(loss: NDArray[np.float64], alpha: float = 0.95) -> float:
    """Compute Expected Shortfall (CVaR) of loss distribution at confidence level alpha."""
    raise NotImplementedError("Implement cvar_loss")


def entropic_risk_measure(loss: NDArray[np.float64], risk_aversion: float = 1.0) -> float:
    """Compute Entropic Risk Measure."""
    raise NotImplementedError("Implement entropic_risk_measure")


class DeltaHedger:
    """Standard Black-Scholes continuous/discrete delta hedger."""

    def __init__(self, strike: float, t_exp: float, sigma: float, r: float) -> None:
        self.strike = strike
        self.t_exp = t_exp
        self.sigma = sigma
        self.r = r

    def compute_deltas(self, paths: NDArray[np.float64]) -> NDArray[np.float64]:
        """Compute Black-Scholes delta hedge ratios for each step along paths."""
        raise NotImplementedError("Implement DeltaHedger.compute_deltas")


class WhalleyWilmottHedger:
    """Asymptotic no-trade band hedger of Whalley & Wilmott (1997)."""

    def __init__(
        self,
        strike: float,
        t_exp: float,
        sigma: float,
        r: float,
        cost_rate: float,
        risk_aversion: float,
    ) -> None:
        self.strike = strike
        self.t_exp = t_exp
        self.sigma = sigma
        self.r = r
        self.cost_rate = cost_rate
        self.risk_aversion = risk_aversion

    def compute_deltas(self, paths: NDArray[np.float64]) -> NDArray[np.float64]:
        """Compute delta holdings tracking the Whalley-Wilmott no-trade boundaries."""
        raise NotImplementedError("Implement WhalleyWilmottHedger.compute_deltas")


class DeepHedger:
    """Neural deep hedging policy network (Buehler et al. 2019)."""

    def __init__(
        self,
        strike: float,
        t_exp: float,
        n_steps: int,
        sigma: float,
        r: float,
        cost_rate: float,
        hidden_dim: int = 16,
        seed: int = 42,
    ) -> None:
        self.strike = strike
        self.t_exp = t_exp
        self.n_steps = n_steps
        self.sigma = sigma
        self.r = r
        self.cost_rate = cost_rate
        self.hidden_dim = hidden_dim

    def compute_deltas(self, paths: NDArray[np.float64]) -> NDArray[np.float64]:
        """Compute delta decisions across all paths using current network parameters."""
        raise NotImplementedError("Implement DeepHedger.compute_deltas")

    def fit(
        self,
        train_paths: NDArray[np.float64],
        epochs: int = 25,
        lr: float = 0.02,
        risk_aversion: float = 1.0,
    ) -> list[float]:
        """Train the policy network using gradient descent."""
        raise NotImplementedError("Implement DeepHedger.fit")


def evaluate_hedging_strategies(
    test_paths: NDArray[np.float64],
    strike: float,
    t_exp: float,
    sigma: float,
    r: float,
    cost_rate: float,
    risk_aversion: float,
    deep_hedger: DeepHedger,
    alpha: float = 0.95,
) -> dict[str, dict[str, float]]:
    """Evaluate and compare DeltaHedger, WhalleyWilmottHedger, and DeepHedger on test paths."""
    raise NotImplementedError("Implement evaluate_hedging_strategies")
