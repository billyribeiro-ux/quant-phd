"""Reference solution for BK2: Berk-Green Fund Economics Model.

Implements the dynamic rational equilibrium model of active mutual fund management
developed by Berk & Green (2004, JPE 112(6)):
1. Decreasing returns to scale in active asset management.
2. Bayesian updating of manager skill from noisy portfolio returns.
3. Rational capital flows driving expected net investor alpha to zero.
4. Equilibrium fund capacity and manager fee rent extraction.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FundParameters:
    """Parameters governing a mutual fund under the Berk-Green model."""

    prior_mean: float
    prior_variance: float
    noise_variance: float
    fee_rate: float
    cost_parameter: float
    initial_aum: float


def update_belief(
    prior_mean: float,
    prior_variance: float,
    signal: float,
    noise_variance: float,
) -> tuple[float, float]:
    """Update Gaussian beliefs N(mu, sigma^2) given an observed signal.

    signal = true_skill + epsilon, where epsilon ~ N(0, noise_variance).

    Parameters
    ----------
    prior_mean : float
        Prior expected skill mu_{t-1}.
    prior_variance : float
        Prior variance of skill sigma_{t-1}^2.
    signal : float
        Observed signal s_t.
    noise_variance : float
        Variance of idiosyncratic observation noise sigma_epsilon^2.

    Returns
    -------
    tuple[float, float]
        (posterior_mean, posterior_variance)
    """
    if prior_variance <= 0.0:
        raise ValueError("prior_variance must be strictly positive")
    if noise_variance <= 0.0:
        raise ValueError("noise_variance must be strictly positive")

    prior_prec = 1.0 / prior_variance
    noise_prec = 1.0 / noise_variance
    post_prec = prior_prec + noise_prec
    post_variance = 1.0 / post_prec
    post_mean = (prior_prec * prior_mean + noise_prec * signal) / post_prec
    return post_mean, post_variance


def capacity_aum(
    expected_skill: float,
    fee_rate: float,
    cost_parameter: float,
) -> float:
    """Compute rational equilibrium capacity AUM where expected net alpha is zero.

    E[R_net] = expected_skill - cost_parameter * AUM - fee_rate = 0
    => AUM* = max(0, (expected_skill - fee_rate) / cost_parameter)

    Parameters
    ----------
    expected_skill : float
        Expected manager skill (mu_t).
    fee_rate : float
        Annual management fee rate (f).
    cost_parameter : float
        Scale cost parameter (lambda > 0).

    Returns
    -------
    float
        Equilibrium capacity AUM in millions.
    """
    if cost_parameter <= 0.0:
        raise ValueError("cost_parameter must be strictly positive")
    if fee_rate < 0.0:
        raise ValueError("fee_rate must be non-negative")

    net_expected = expected_skill - fee_rate
    if net_expected <= 0.0:
        return 0.0
    return net_expected / cost_parameter


def gross_alpha(skill: float, aum: float, cost_parameter: float) -> float:
    """Compute fund gross alpha before management fees.

    alpha_gross(q) = skill - cost_parameter * aum
    """
    if cost_parameter <= 0.0:
        raise ValueError("cost_parameter must be strictly positive")
    if aum < 0.0:
        raise ValueError("aum must be non-negative")
    return skill - cost_parameter * aum


def net_alpha(
    skill: float,
    aum: float,
    cost_parameter: float,
    fee_rate: float,
) -> float:
    """Compute fund net alpha delivered to investors after fees.

    alpha_net(q) = skill - cost_parameter * aum - fee_rate
    """
    return gross_alpha(skill, aum, cost_parameter) - fee_rate


def extract_signal(gross_return: float, aum: float, cost_parameter: float) -> float:
    """Extract signal of skill from realized gross return and fund scale.

    Since R_gross = skill - lambda * aum + epsilon,
    signal = R_gross + lambda * aum = skill + epsilon.
    """
    if cost_parameter <= 0.0:
        raise ValueError("cost_parameter must be strictly positive")
    if aum < 0.0:
        raise ValueError("aum must be non-negative")
    return gross_return + cost_parameter * aum


def manager_rent_share(total_fees: float, investor_profit: float) -> float:
    """Compute the fraction of economic surplus captured by fund managers.

    In the Berk-Green equilibrium, expected investor excess profit is zero,
    meaning managers capture 100% of economic rents in expectation.
    """
    if total_fees <= 0.0:
        return 0.0
    if investor_profit <= 0.0:
        return 1.0
    return total_fees / (total_fees + investor_profit)


def simulate_fund_lifecycle(
    params: FundParameters,
    true_skill: float,
    noise_shocks: list[float],
) -> dict[str, Any]:
    """Simulate the multi-period Berk-Green fund lifecycle.

    Parameters
    ----------
    params : FundParameters
        Fund and market prior parameters.
    true_skill : float
        True unobserved manager skill.
    noise_shocks : list[float]
        Sequence of zero-mean noise shocks epsilon_t for each period.

    Returns
    -------
    dict[str, Any]
        Time series of AUM, returns, beliefs, capacities, flows, and fee revenues.
    """
    current_aum = max(0.0, params.initial_aum)
    current_mu = params.prior_mean
    current_var = params.prior_variance

    aum_series: list[float] = []
    gross_returns: list[float] = []
    net_returns: list[float] = []
    signals: list[float] = []
    posterior_means: list[float] = []
    posterior_variances: list[float] = []
    target_capacities: list[float] = []
    net_flows: list[float] = []
    manager_fees: list[float] = []
    investor_profits: list[float] = []

    for shock in noise_shocks:
        aum_series.append(current_aum)

        if current_aum <= 0.0:
            # Fund is shuttered / zero size
            gross_ret = 0.0
            net_ret = 0.0
            sig = current_mu
            fees = 0.0
            inv_profit = 0.0
            post_mu, post_var = current_mu, current_var
            target_cap = 0.0
            flow = 0.0
        else:
            # Fund operates at current_aum
            alpha_g = gross_alpha(true_skill, current_aum, params.cost_parameter)
            gross_ret = alpha_g + shock
            net_ret = gross_ret - params.fee_rate
            fees = params.fee_rate * current_aum
            inv_profit = current_aum * net_ret

            sig = extract_signal(gross_ret, current_aum, params.cost_parameter)
            post_mu, post_var = update_belief(
                current_mu,
                current_var,
                sig,
                params.noise_variance,
            )

            target_cap = capacity_aum(post_mu, params.fee_rate, params.cost_parameter)

            # Assets before external net flows: A_end = max(0, current_aum * (1 + net_ret))
            assets_end = max(0.0, current_aum * (1.0 + net_ret))
            flow = target_cap - assets_end

        gross_returns.append(gross_ret)
        net_returns.append(net_ret)
        signals.append(sig)
        posterior_means.append(post_mu)
        posterior_variances.append(post_var)
        target_capacities.append(target_cap)
        net_flows.append(flow)
        manager_fees.append(fees)
        investor_profits.append(inv_profit)

        # Update state for next period
        current_aum = target_cap
        current_mu = post_mu
        current_var = post_var

    cum_fees = sum(manager_fees)
    cum_inv_profit = sum(investor_profits)
    rent_share = manager_rent_share(cum_fees, cum_inv_profit)

    return {
        "aum": aum_series,
        "gross_returns": gross_returns,
        "net_returns": net_returns,
        "signals": signals,
        "posterior_means": posterior_means,
        "posterior_variances": posterior_variances,
        "target_capacities": target_capacities,
        "net_flows": net_flows,
        "manager_fees": manager_fees,
        "investor_profits": investor_profits,
        "cumulative_fees": cum_fees,
        "cumulative_investor_profit": cum_inv_profit,
        "rent_share": rent_share,
    }
