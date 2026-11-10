"""Mutant 4: DeltaHedger assumes zero transaction costs and ignores transaction cost drag in accounting."""

from __future__ import annotations

import math

import numpy as np
from numpy.typing import NDArray
from scipy.special import erf


def _std_norm_cdf(x: NDArray[np.float64]) -> NDArray[np.float64]:
    res: NDArray[np.float64] = np.asarray(0.5 * (1.0 + erf(x / math.sqrt(2.0))), dtype=np.float64)
    return res


def _std_norm_pdf(x: NDArray[np.float64]) -> NDArray[np.float64]:
    res: NDArray[np.float64] = np.asarray(np.exp(-0.5 * (x**2)) / math.sqrt(2.0 * math.pi), dtype=np.float64)
    return res


def simulate_gbm_paths(
    s0: float,
    mu: float,
    sigma: float,
    t_exp: float,
    n_steps: int,
    n_paths: int,
    rng: np.random.Generator,
) -> NDArray[np.float64]:
    if s0 <= 0.0 or sigma <= 0.0 or t_exp <= 0.0 or n_steps <= 0 or n_paths <= 0:
        raise ValueError("Invalid parameters for GBM simulation")
    dt = t_exp / n_steps
    drift = (mu - 0.5 * sigma**2) * dt
    vol = sigma * math.sqrt(dt)
    shocks = rng.normal(0.0, 1.0, size=(n_paths, n_steps))
    paths = np.zeros((n_paths, n_steps + 1), dtype=np.float64)
    paths[:, 0] = s0
    for step in range(n_steps):
        paths[:, step + 1] = paths[:, step] * np.exp(drift + vol * shocks[:, step])
    return paths


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
    if s0 <= 0.0 or sigma <= 0.0 or t_exp <= 0.0 or n_steps <= 0 or n_paths <= 0:
        raise ValueError("Invalid parameters for Jump-Diffusion simulation")
    if lambda_j < 0.0 or sigma_j <= 0.0:
        raise ValueError("Invalid jump parameters")
    dt = t_exp / n_steps
    drift = (mu - 0.5 * sigma**2) * dt
    vol = sigma * math.sqrt(dt)
    diff_shocks = rng.normal(0.0, 1.0, size=(n_paths, n_steps))
    poisson_counts = rng.poisson(lambda_j * dt, size=(n_paths, n_steps))
    paths = np.zeros((n_paths, n_steps + 1), dtype=np.float64)
    paths[:, 0] = s0
    for step in range(n_steps):
        n_j = poisson_counts[:, step]
        jump_increment = np.zeros(n_paths, dtype=np.float64)
        has_jumps = n_j > 0
        if np.any(has_jumps):
            counts = n_j[has_jumps]
            jump_increment[has_jumps] = rng.normal(mu_j * counts, sigma_j * np.sqrt(counts))
        inc = drift + vol * diff_shocks[:, step] + jump_increment
        paths[:, step + 1] = paths[:, step] * np.exp(inc)
    return paths


def black_scholes_call_price(
    s: NDArray[np.float64],
    k: float,
    tau: NDArray[np.float64],
    sigma: float,
    r: float,
) -> NDArray[np.float64]:
    tau_safe = np.maximum(tau, 1e-8)
    vol_sqrt = sigma * np.sqrt(tau_safe)
    d1 = (np.log(np.maximum(s, 1e-8) / k) + (r + 0.5 * sigma**2) * tau_safe) / vol_sqrt
    d2 = d1 - vol_sqrt
    price = s * _std_norm_cdf(d1) - k * np.exp(-r * tau_safe) * _std_norm_cdf(d2)
    at_maturity = tau <= 1e-8
    if np.any(at_maturity):
        price = np.where(at_maturity, np.maximum(s - k, 0.0), price)
    return np.maximum(price, 0.0)


def black_scholes_call_delta(
    s: NDArray[np.float64],
    k: float,
    tau: NDArray[np.float64],
    sigma: float,
    r: float,
) -> NDArray[np.float64]:
    tau_safe = np.maximum(tau, 1e-8)
    vol_sqrt = sigma * np.sqrt(tau_safe)
    d1 = (np.log(np.maximum(s, 1e-8) / k) + (r + 0.5 * sigma**2) * tau_safe) / vol_sqrt
    delta = _std_norm_cdf(d1)
    at_maturity = tau <= 1e-8
    if np.any(at_maturity):
        delta = np.where(at_maturity, np.where(s > k, 1.0, np.where(s < k, 0.0, 0.5)), delta)
    return np.clip(delta, 0.0, 1.0)


def black_scholes_gamma(
    s: NDArray[np.float64],
    k: float,
    tau: NDArray[np.float64],
    sigma: float,
    r: float,
) -> NDArray[np.float64]:
    tau_safe = np.maximum(tau, 1e-8)
    vol_sqrt = sigma * np.sqrt(tau_safe)
    s_safe = np.maximum(s, 1e-8)
    d1 = (np.log(s_safe / k) + (r + 0.5 * sigma**2) * tau_safe) / vol_sqrt
    gamma = _std_norm_pdf(d1) / (s_safe * vol_sqrt)
    at_maturity = tau <= 1e-8
    if np.any(at_maturity):
        gamma = np.where(at_maturity, 0.0, gamma)
    return np.maximum(gamma, 0.0)


def whalley_wilmott_bandwidth(
    s: NDArray[np.float64],
    k: float,
    tau: NDArray[np.float64],
    sigma: float,
    r: float,
    cost_rate: float,
    risk_aversion: float,
) -> NDArray[np.float64]:
    if cost_rate < 0.0 or risk_aversion <= 0.0:
        raise ValueError("Transaction cost must be non-negative and risk aversion positive")
    gamma = black_scholes_gamma(s, k, tau, sigma, r)
    tau_safe = np.maximum(tau, 1e-8)
    s_safe = np.maximum(s, 1e-8)
    inner = (1.5 * cost_rate * np.exp(-r * tau_safe) * s_safe * (gamma**2)) / risk_aversion
    half_width = np.cbrt(np.maximum(inner, 0.0))
    at_maturity = tau <= 1e-8
    if np.any(at_maturity):
        half_width = np.where(at_maturity, 0.0, half_width)
    return np.maximum(half_width, 0.0)


def compute_hedging_pnl(
    paths: NDArray[np.float64],
    deltas: NDArray[np.float64],
    strike: float,
    cost_rate: float,
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    # MUTATION: Costs are zeroed out!
    n_paths, n_steps_plus_1 = paths.shape
    n_steps = n_steps_plus_1 - 1
    if deltas.shape != (n_paths, n_steps):
        raise ValueError(f"deltas shape {deltas.shape} must match (n_paths, n_steps) = {(n_paths, n_steps)}")
    price_diffs = paths[:, 1:] - paths[:, :-1]
    trading_gains = np.sum(deltas * price_diffs, axis=1)
    costs = np.zeros(n_paths, dtype=np.float64)
    terminal_payoff = np.maximum(paths[:, -1] - strike, 0.0)
    total_pnl = trading_gains - terminal_payoff - costs
    return total_pnl, trading_gains, costs


def cvar_loss(loss: NDArray[np.float64], alpha: float = 0.95) -> float:
    if not (0.0 < alpha < 1.0):
        raise ValueError(f"Confidence level alpha must be in (0, 1), got {alpha}")
    loss_arr = np.asarray(loss, dtype=np.float64)
    if loss_arr.size == 0:
        return 0.0
    sorted_loss = np.sort(loss_arr)
    cutoff_idx = math.ceil(alpha * len(sorted_loss))
    if cutoff_idx >= len(sorted_loss):
        cutoff_idx = len(sorted_loss) - 1
    return float(np.mean(sorted_loss[cutoff_idx:]))


def entropic_risk_measure(loss: NDArray[np.float64], risk_aversion: float = 1.0) -> float:
    if risk_aversion <= 0.0:
        raise ValueError("Risk aversion must be positive for entropic risk measure")
    loss_arr = np.asarray(loss, dtype=np.float64)
    m = loss_arr.size
    if m == 0:
        return 0.0
    max_val = float(np.max(risk_aversion * loss_arr))
    log_sum = max_val + math.log(float(np.mean(np.exp(risk_aversion * loss_arr - max_val))))
    return float(log_sum / risk_aversion)


class DeltaHedger:
    def __init__(self, strike: float, t_exp: float, sigma: float, r: float) -> None:
        self.strike = strike
        self.t_exp = t_exp
        self.sigma = sigma
        self.r = r

    def compute_deltas(self, paths: NDArray[np.float64]) -> NDArray[np.float64]:
        n_paths, n_steps_plus_1 = paths.shape
        n_steps = n_steps_plus_1 - 1
        dt = self.t_exp / n_steps
        deltas = np.zeros((n_paths, n_steps), dtype=np.float64)
        for step in range(n_steps):
            tau = max(self.t_exp - step * dt, 1e-8)
            s_t = paths[:, step]
            deltas[:, step] = black_scholes_call_delta(s_t, self.strike, np.full(n_paths, tau), self.sigma, self.r)
        return deltas


class WhalleyWilmottHedger:
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
        n_paths, n_steps_plus_1 = paths.shape
        n_steps = n_steps_plus_1 - 1
        dt = self.t_exp / n_steps
        deltas = np.zeros((n_paths, n_steps), dtype=np.float64)
        curr_delta = np.zeros(n_paths, dtype=np.float64)
        for step in range(n_steps):
            tau = max(self.t_exp - step * dt, 1e-8)
            s_t = paths[:, step]
            tau_vec = np.full(n_paths, tau)
            bs_delta = black_scholes_call_delta(s_t, self.strike, tau_vec, self.sigma, self.r)
            bandwidth = whalley_wilmott_bandwidth(
                s_t, self.strike, tau_vec, self.sigma, self.r, self.cost_rate, self.risk_aversion
            )
            lower_band = np.clip(bs_delta - bandwidth, 0.0, 1.0)
            upper_band = np.clip(bs_delta + bandwidth, 0.0, 1.0)
            next_delta = np.where(
                curr_delta < lower_band,
                lower_band,
                np.where(curr_delta > upper_band, upper_band, curr_delta),
            )
            deltas[:, step] = next_delta
            curr_delta = next_delta
        return deltas


def _sigmoid(x: NDArray[np.float64]) -> NDArray[np.float64]:
    clipped = np.clip(x, -20.0, 20.0)
    return 1.0 / (1.0 + np.exp(-clipped))


class DeepHedger:
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
        self.dt = t_exp / n_steps
        rng = np.random.default_rng(seed)
        input_dim = 4
        scale1 = math.sqrt(2.0 / (input_dim + hidden_dim))
        scale2 = math.sqrt(2.0 / (hidden_dim + 1))
        self.w1 = rng.normal(0.0, scale1, (input_dim, hidden_dim))
        self.b1 = np.zeros(hidden_dim, dtype=np.float64)
        self.w2 = rng.normal(0.0, scale2, (hidden_dim, 1))
        self.b2 = np.zeros(1, dtype=np.float64)

    def _step_policy(
        self,
        s_t: NDArray[np.float64],
        tau: float,
        prev_delta: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        n_paths = s_t.shape[0]
        bs_d = black_scholes_call_delta(s_t, self.strike, np.full(n_paths, tau), self.sigma, self.r)
        features = np.column_stack([s_t / self.strike, np.full(n_paths, tau), prev_delta, bs_d])
        hidden = np.tanh(features @ self.w1 + self.b1)
        z = (hidden @ self.w2 + self.b2).ravel()
        delta = _sigmoid(z)
        return delta, hidden, features

    def compute_deltas(self, paths: NDArray[np.float64]) -> NDArray[np.float64]:
        n_paths, n_steps_plus_1 = paths.shape
        n_steps = n_steps_plus_1 - 1
        deltas = np.zeros((n_paths, n_steps), dtype=np.float64)
        prev_delta = np.zeros(n_paths, dtype=np.float64)
        for step in range(n_steps):
            tau = max(self.t_exp - step * self.dt, 1e-8)
            delta, _, _ = self._step_policy(paths[:, step], tau, prev_delta)
            deltas[:, step] = delta
            prev_delta = delta
        return deltas

    def fit(
        self,
        train_paths: NDArray[np.float64],
        epochs: int = 25,
        lr: float = 0.02,
        risk_aversion: float = 1.0,
    ) -> list[float]:
        n_paths, n_steps_plus_1 = train_paths.shape
        n_steps = n_steps_plus_1 - 1
        history: list[float] = []
        for _ in range(epochs):
            deltas = np.zeros((n_paths, n_steps), dtype=np.float64)
            h_list: list[NDArray[np.float64]] = []
            x_list: list[NDArray[np.float64]] = []
            prev_delta = np.zeros(n_paths, dtype=np.float64)
            for step in range(n_steps):
                tau = max(self.t_exp - step * self.dt, 1e-8)
                delta, hidden, features = self._step_policy(train_paths[:, step], tau, prev_delta)
                deltas[:, step] = delta
                h_list.append(hidden)
                x_list.append(features)
                prev_delta = delta
            pnl, _, _ = compute_hedging_pnl(train_paths, deltas, self.strike, self.cost_rate)
            loss = -pnl
            current_risk = entropic_risk_measure(loss, risk_aversion)
            history.append(current_risk)
            scaled_loss = risk_aversion * loss
            shift_loss = scaled_loss - np.max(scaled_loss)
            exp_loss = np.exp(shift_loss)
            weights = exp_loss / np.sum(exp_loss)
            d_loss_ddelta = -(train_paths[:, 1:] - train_paths[:, :-1])
            smooth_eps = 1e-4
            d_loss_ddelta[:, 0] += (
                self.cost_rate * train_paths[:, 0] * (deltas[:, 0] / np.sqrt(deltas[:, 0] ** 2 + smooth_eps))
            )
            for step in range(1, n_steps):
                diff = deltas[:, step] - deltas[:, step - 1]
                sign_diff = diff / np.sqrt(diff**2 + smooth_eps)
                d_loss_ddelta[:, step] += self.cost_rate * train_paths[:, step] * sign_diff
                d_loss_ddelta[:, step - 1] -= self.cost_rate * train_paths[:, step] * sign_diff
            d_loss_ddelta[:, -1] += (
                self.cost_rate * train_paths[:, -1] * (deltas[:, -1] / np.sqrt(deltas[:, -1] ** 2 + smooth_eps))
            )
            d_risk_ddelta = weights[:, None] * d_loss_ddelta
            grad_w2 = np.zeros_like(self.w2)
            grad_b2 = np.zeros_like(self.b2)
            grad_w1 = np.zeros_like(self.w1)
            grad_b1 = np.zeros_like(self.b1)
            for step in range(n_steps):
                d_t = deltas[:, step]
                dz = d_risk_ddelta[:, step] * d_t * (1.0 - d_t)
                grad_w2 += h_list[step].T @ dz[:, None]
                grad_b2 += np.sum(dz, keepdims=True)
                dh = dz[:, None] @ self.w2.T * (1.0 - h_list[step] ** 2)
                grad_w1 += x_list[step].T @ dh
                grad_b1 += np.sum(dh, axis=0)
            self.w2 -= lr * np.clip(grad_w2, -1.0, 1.0)
            self.b2 -= lr * np.clip(grad_b2, -1.0, 1.0)
            self.w1 -= lr * np.clip(grad_w1, -1.0, 1.0)
            self.b1 -= lr * np.clip(grad_b1, -1.0, 1.0)
        return history


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
    delta_hedger = DeltaHedger(strike, t_exp, sigma, r)
    ww_hedger = WhalleyWilmottHedger(strike, t_exp, sigma, r, cost_rate, risk_aversion)
    policies = {
        "DeltaHedging": delta_hedger.compute_deltas(test_paths),
        "WhalleyWilmott": ww_hedger.compute_deltas(test_paths),
        "DeepHedging": deep_hedger.compute_deltas(test_paths),
    }
    results: dict[str, dict[str, float]] = {}
    for name, deltas in policies.items():
        total_pnl, _trading_gains, costs = compute_hedging_pnl(test_paths, deltas, strike, cost_rate)
        loss = -total_pnl
        results[name] = {
            "mean_pnl": float(np.mean(total_pnl)),
            "std_pnl": float(np.std(total_pnl)),
            "cvar_95": float(cvar_loss(loss, alpha=alpha)),
            "entropic_risk": float(entropic_risk_measure(loss, risk_aversion=risk_aversion)),
            "mean_costs": float(np.mean(costs)),
            "total_turnover": float(np.mean(np.sum(np.abs(np.diff(deltas, axis=1)), axis=1))),
        }
    return results
