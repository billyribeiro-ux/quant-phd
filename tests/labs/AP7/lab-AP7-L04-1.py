"""Lab AP7-L04-1: Survey Expectations vs Rational Forecasts & Diagnostic Expectations.

SIMULATED: Compares rational model-implied return forecasts with empirical survey
expectations (extrapolative), and tests the diagnostic expectations belief-distortion
equation on corporate earnings forecasts (Greenwood & Shleifer 2014; Bordalo et al. 2019).
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    seed = 42
    rng = np.random.default_rng(seed)
    n_periods = 200

    # 1. State variable: persistent dividend-price ratio / valuation state x_t
    # In rational Campbell-Cochrane / Campbell-Shiller models, high dividend-price ratio
    # implies HIGH rational expected returns (discount-rate variation).
    phi_x = 0.88
    x_val = np.zeros(n_periods)
    shocks = rng.normal(0.0, 1.0, size=n_periods)
    for t in range(1, n_periods):
        x_val[t] = phi_x * x_val[t - 1] + shocks[t]

    # Realized returns: R_{t+1} = mu + beta * x_t + u_{t+1}
    # where u_{t+1} negatively correlates with shock_{t+1} (price dividend ratio drops when returns are bad)
    return_innovations = -0.75 * shocks + rng.normal(0.0, 0.65, size=n_periods)
    returns = 0.008 + 0.015 * x_val + return_innovations

    # Rational return expectation: E_t[R_{t+1}] = mu + beta * x_t
    rational_expectations = 0.008 + 0.015 * x_val

    # 2. Survey return expectations: Greenwood & Shleifer (2014) finding
    # Investors extrapolate recent past returns:
    # E_t^S[R_{t+1}] = c_0 + c_1 * Past_Return_t
    # Because past high returns correspond to low dividend-price ratios (negative shock),
    # survey expectations move in the OPPOSITE direction of rational discount rates!
    past_returns_ewma = np.zeros(n_periods)
    theta_extrap = 0.70
    for t in range(1, n_periods):
        past_returns_ewma[t] = theta_extrap * past_returns_ewma[t - 1] + (1.0 - theta_extrap) * returns[t - 1]

    survey_expectations = 0.008 + 0.85 * past_returns_ewma

    # Correlation between survey expectations and rational expectations
    corr_survey_rational = float(np.corrcoef(survey_expectations[20:], rational_expectations[20:])[0, 1])

    # Predictive regression: Realized returns on Survey Expectations vs Rational Expectations
    y_ret = returns[21:]
    x_survey = survey_expectations[20:-1]
    x_rational = rational_expectations[20:-1]

    slope_survey = float(np.polyfit(x_survey, y_ret, 1)[0])
    slope_rational = float(np.polyfit(x_rational, y_ret, 1)[0])

    # 3. Diagnostic Expectations updating (Bordalo et al. 2019):
    # E_t^theta[g_{t+1}] = E_t[g_{t+1}] + theta * (E_t[g_{t+1}] - E_{t-1}[g_{t+1}])
    theta_diagnostic = 0.50
    earnings_growth_shock = rng.normal(0.0, 0.05, size=n_periods)
    earnings_growth = 0.02 + earnings_growth_shock

    rational_earnings_exp = np.full(n_periods, 0.02)
    # News revision: current shock
    news_innovation = earnings_growth_shock
    diagnostic_earnings_exp = rational_earnings_exp + theta_diagnostic * news_innovation

    # Diagnostic forecast errors: Realized - Expected
    forecast_errors = earnings_growth - diagnostic_earnings_exp
    # Predictability of forecast errors by recent surprise:
    # Under rational expectations, Cov(error_{t+1}, news_t) = 0
    # Under diagnostic expectations, forecast error is negatively predicted by news_t (overreaction reversal)
    corr_error_news = float(np.corrcoef(forecast_errors[1:], news_innovation[:-1])[0, 1])

    print("Greenwood-Shleifer Survey Expectations Analysis:")
    print(f"  Corr(Survey Expectation, Rational Expectation): {corr_survey_rational:+.4f}")
    print(f"  Predictive slope of returns on Survey Expectation: {slope_survey:+.4f}")
    print(f"  Predictive slope of returns on Rational Expectation: {slope_rational:+.4f}")
    print("Bordalo et al. Diagnostic Expectations Analysis:")
    print(f"  Diagnostic distortion coefficient theta:          {theta_diagnostic:.2f}")
    print(f"  Diagnostic forecast error standard deviation:     {float(np.std(forecast_errors)):.4f}")
    print(f"  Corr(Forecast Error t+1, News Innovation t):       {corr_error_news:+.4f}")
    print(f"  Surveys negatively correlate with rational:       {bool(corr_survey_rational < 0)}")


main()
