"""AC3 lab L05: management earnings guidance and information conveyance.

SIMULATED: the management forecasts, consensus analyst expectations, actual earnings realizations,
and abnormal announcement returns are generated under an asymmetric voluntary disclosure model.
All calculations use standard library float and math. Deterministic seed; no network.
"""

from __future__ import annotations

import random

SEED = 20261110
N_FIRMS = 60


def simulate_guidance_and_earnings(
    seed: int,
) -> tuple[list[float], list[float], list[float], list[float], list[bool]]:
    """Simulate guidance surprises, earnings surprises, abnormal returns, and guidance issuance indicators.

    Returns (guidance_surprises, earnings_surprises, car_guidance, car_announcement, issued_guidance).
    """
    rng = random.Random(seed)

    guidance_surprises: list[float] = []
    earnings_surprises: list[float] = []
    car_guidance: list[float] = []
    car_announcement: list[float] = []
    issued_guidance: list[bool] = []

    # GRC (guidance response coefficient) is typically larger than ERC (earnings response coefficient)
    # because guidance conveys forward-looking, persistent operational news.
    true_grc = 0.045
    true_erc = 0.025

    for _ in range(N_FIRMS):
        # Initial consensus expectation E_0 ~ N(2.0, 0.5)
        # Fundamental innovation total_news ~ N(0, 0.4)
        total_news = rng.gauss(0.0, 0.4)

        # Asymmetric guidance probability:
        # Bad news (total_news < -0.1) has 85% probability of early guidance (pre-announcement)
        # Good news (total_news > +0.1) has 50% probability of early guidance
        # Modest news has 30% probability
        if total_news < -0.1:
            p_issue = 0.85
        elif total_news > 0.1:
            p_issue = 0.50
        else:
            p_issue = 0.30

        issues = rng.random() < p_issue
        issued_guidance.append(issues)

        if issues:
            # Management guides ~ 75% of total news in mid-quarter guidance
            guide_news = 0.75 * total_news + rng.gauss(0.0, 0.05)
            rem_news = total_news - guide_news

            car_g = true_grc * guide_news + rng.gauss(0.0, 0.008)
            car_e = true_erc * rem_news + rng.gauss(0.0, 0.008)

            guidance_surprises.append(guide_news)
            earnings_surprises.append(rem_news)
            car_guidance.append(car_g)
            car_announcement.append(car_e)
        else:
            # No guidance: entire total_news lands at official announcement
            guidance_surprises.append(0.0)
            earnings_surprises.append(total_news)
            car_guidance.append(0.0)
            car_e = true_erc * total_news + rng.gauss(0.0, 0.010)
            car_announcement.append(car_e)

    return (
        guidance_surprises,
        earnings_surprises,
        car_guidance,
        car_announcement,
        issued_guidance,
    )


def ols_slope(x: list[float], y: list[float]) -> float:
    """Compute univariate OLS slope coefficient cov(x, y) / var(x)."""
    n = len(x)
    x_bar = sum(x) / n
    y_bar = sum(y) / n
    cov = sum((x[i] - x_bar) * (y[i] - y_bar) for i in range(n))
    var = sum((x[i] - x_bar) ** 2 for i in range(n))
    return cov / var if var > 0 else 0.0


def main() -> None:
    g_surp, e_surp, car_g, car_e, issued = simulate_guidance_and_earnings(SEED)

    # Filter to firms that issued guidance
    g_idxs = [i for i in range(N_FIRMS) if issued[i]]
    no_g_idxs = [i for i in range(N_FIRMS) if not issued[i]]

    # Guidance Response Coefficient (GRC)
    x_g = [g_surp[i] for i in g_idxs]
    y_g = [car_g[i] for i in g_idxs]
    grc = ols_slope(x_g, y_g)

    # Earnings Response Coefficient for guidance firms at official announcement
    x_eg = [e_surp[i] for i in g_idxs]
    y_eg = [car_e[i] for i in g_idxs]
    erc_g = ols_slope(x_eg, y_eg)

    # Earnings Response Coefficient for no-guidance firms
    x_no = [e_surp[i] for i in no_g_idxs]
    y_no = [car_e[i] for i in no_g_idxs]
    erc_no = ols_slope(x_no, y_no)

    print(f"seed {SEED} total_firms {N_FIRMS} firms_guiding {len(g_idxs)} firms_silent {len(no_g_idxs)}")
    print(f"guidance_response_coefficient_GRC: {grc:.4f}")
    print(f"earnings_response_coefficient_guided_firms: {erc_g:.4f}")
    print(f"earnings_response_coefficient_unguided_firms: {erc_no:.4f}")

    # Check that guidance response coefficient exceeds earnings response coefficient
    print(f"grc_exceeds_guided_erc: {grc > erc_g}")
    print(f"grc_exceeds_unguided_erc: {grc > erc_no}")

    # Check guidance asymmetry: fraction of bad-news firms guiding vs good-news firms guiding
    bad_news = [i for i in range(N_FIRMS) if (g_surp[i] + e_surp[i]) < -0.1]
    good_news = [i for i in range(N_FIRMS) if (g_surp[i] + e_surp[i]) > 0.1]

    pct_bad_guided = sum(1 for i in bad_news if issued[i]) / len(bad_news) if bad_news else 0.0
    pct_good_guided = sum(1 for i in good_news if issued[i]) / len(good_news) if good_news else 0.0

    print(f"bad_news_firms {len(bad_news)} pct_guiding {pct_bad_guided:.3f}")
    print(f"good_news_firms {len(good_news)} pct_guiding {pct_good_guided:.3f}")
    print(f"asymmetric_timeliness_observed: {pct_bad_guided > pct_good_guided}")


main()
