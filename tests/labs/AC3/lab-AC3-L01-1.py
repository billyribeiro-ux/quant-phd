"""AC3 lab L01: event study cumulative abnormal returns around earnings announcements.

SIMULATED: the firm return series, market index returns, and earnings announcement dates are
generated from a seeded pseudo-random number generator. They do not represent real market prices.
The market model is estimated on the pre-event window [-120, -21]; abnormal returns are computed
on the event window [-20, +20]. All calculations use exact floats.
"""

from __future__ import annotations

import random

SEED = 20261110
N_FIRMS = 40
EST_LEN = 100  # days -120 to -21
EVENT_LEN = 41  # days -20 to +20 (day 0 is announcement)


def simulate_market_and_firms(seed: int) -> tuple[list[float], list[list[float]], list[float]]:
    """Generate simulated market returns, firm returns, and earnings surprises.

    Returns (market_returns, firm_returns, surprises).
    Total days = 141 (-120 to +20).
    """
    rng = random.Random(seed)
    total_days = EST_LEN + EVENT_LEN
    mkt = [rng.gauss(0.0004, 0.010) for _ in range(total_days)]

    firm_returns: list[list[float]] = []
    surprises: list[float] = []

    for _ in range(N_FIRMS):
        beta = rng.uniform(0.7, 1.4)
        alpha = rng.uniform(-0.0001, 0.0001)
        sigma_e = rng.uniform(0.012, 0.025)

        # Standardized surprise in [-3, 3]
        sue = rng.gauss(0.0, 1.0)
        surprises.append(sue)

        # Daily returns
        rets: list[float] = []
        for t in range(total_days):
            event_day = t - 120  # day index relative to announcement at 120
            ret = alpha + beta * mkt[t] + rng.gauss(0.0, sigma_e)
            # Information leakage during [-10, -1]
            if -10 <= event_day < 0:
                ret += 0.0010 * sue
            # Announcement day reaction at day 0
            elif event_day == 0:
                ret += 0.0150 * sue
            # Modest post-announcement drift during [+1, +20]
            elif 1 <= event_day <= 20:
                ret += 0.0005 * sue
            rets.append(ret)
        firm_returns.append(rets)

    return mkt, firm_returns, surprises


def estimate_market_model(mkt: list[float], firm_ret: list[float]) -> tuple[float, float]:
    """Fit market model R_it = alpha + beta * R_mt on estimation window [0:EST_LEN].

    Returns (alpha, beta).
    """
    n = EST_LEN
    x = mkt[:n]
    y = firm_ret[:n]

    x_bar = sum(x) / n
    y_bar = sum(y) / n

    cov_xy = sum((x[i] - x_bar) * (y[i] - y_bar) for i in range(n))
    var_x = sum((x[i] - x_bar) ** 2 for i in range(n))

    beta = cov_xy / var_x if var_x > 0 else 1.0
    alpha = y_bar - beta * x_bar
    return alpha, beta


def compute_car_series(mkt: list[float], firm_ret: list[float], alpha: float, beta: float) -> list[float]:
    """Compute cumulative abnormal return over the event window [-20, +20].

    Returns list of 41 CAR values from day -20 to day +20.
    """
    cars: list[float] = []
    cum = 0.0
    for t in range(EST_LEN, EST_LEN + EVENT_LEN):
        ar = firm_ret[t] - (alpha + beta * mkt[t])
        cum += ar
        cars.append(cum)
    return cars


def main() -> None:
    mkt, firm_returns, surprises = simulate_market_and_firms(SEED)

    good_news_cars: list[list[float]] = []
    bad_news_cars: list[list[float]] = []

    for i in range(N_FIRMS):
        alpha, beta = estimate_market_model(mkt, firm_returns[i])
        car = compute_car_series(mkt, firm_returns[i], alpha, beta)
        if surprises[i] >= 0:
            good_news_cars.append(car)
        else:
            bad_news_cars.append(car)

    # Average CAR at selected event days: -20, -10, -1, 0, +1, +10, +20
    # Day indices in 0..40: -20 -> 0, -10 -> 10, -1 -> 19, 0 -> 20, +1 -> 21, +10 -> 30, +20 -> 40
    check_days = [(-20, 0), (-10, 10), (-1, 19), (0, 20), (1, 21), (10, 30), (20, 40)]

    print(f"seed {SEED} firms {N_FIRMS} good_news {len(good_news_cars)} bad_news {len(bad_news_cars)}")

    for day_label, idx in check_days:
        mean_good = sum(c[idx] for c in good_news_cars) / len(good_news_cars)
        mean_bad = sum(c[idx] for c in bad_news_cars) / len(bad_news_cars)
        spread = mean_good - mean_bad
        print(f"day {day_label:+3d} : good_CAR {mean_good:+.4f} | bad_CAR {mean_bad:+.4f} | spread {spread:+.4f}")

    # Verify Ball & Brown (1968) properties:
    # 1. Pre-announcement drift: spread is positive before day 0
    car_pre_spread = sum(c[19] for c in good_news_cars) / len(good_news_cars) - sum(c[19] for c in bad_news_cars) / len(
        bad_news_cars
    )
    # 2. Announcement jump: spread increases noticeably at day 0
    mean_good_0 = sum(c[20] for c in good_news_cars) / len(good_news_cars)
    mean_bad_0 = sum(c[20] for c in bad_news_cars) / len(bad_news_cars)
    car_jump = (mean_good_0 - mean_bad_0) - car_pre_spread
    # 3. Post-announcement spread at day +20
    car_post_spread = sum(c[40] for c in good_news_cars) / len(good_news_cars) - sum(
        c[40] for c in bad_news_cars
    ) / len(bad_news_cars)

    print("ball_brown_properties:")
    print(f"pre_announcement_spread_positive: {car_pre_spread > 0}")
    print(f"announcement_jump_positive: {car_jump > 0}")
    print(f"post_announcement_spread_positive: {car_post_spread > car_pre_spread}")


main()
