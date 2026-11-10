"""Grader instance generator for E8 CIP-basis monitor project.

Generates deterministic synthetic market panels for testing.
Different seeds generate materially different quote series and quarter-end distributions.
"""

from __future__ import annotations

import datetime
import functools
import random


def is_quarter_end_date(d: datetime.date) -> bool:
    """Return True if date is the last weekday of March, June, September, or December."""
    if d.month not in (3, 6, 9, 12):
        return False
    max_day = 31 if d.month in (3, 12) else 30
    last_cal_day = datetime.date(d.year, d.month, max_day)
    # 0=Monday, 4=Friday, 5=Saturday, 6=Sunday
    if last_cal_day.weekday() == 5:
        target_day = max_day - 1
    elif last_cal_day.weekday() == 6:
        target_day = max_day - 2
    else:
        target_day = max_day
    return d.day == target_day


@functools.lru_cache(maxsize=128)
def make_instance(seed: int) -> dict[str, object]:
    """Generate a deterministic test instance for seed.

    Generates approximately 60 business days of daily quotes including at least one quarter end.
    """
    rng = random.Random(seed)

    # Base parameters vary with seed
    base_spot = 1.05 + 0.15 * rng.random()  # 1.05 - 1.20
    base_usd_rate = 0.040 + 0.025 * rng.random()  # 4.0% - 6.5%
    base_foreign_rate = 0.020 + 0.020 * rng.random()  # 2.0% - 4.0%
    base_basis_bp = -35.0 + 20.0 * rng.random()  # -35 bp to -15 bp
    quarter_end_spike_bp = -40.0 - 25.0 * rng.random()  # -40 bp to -65 bp

    # Start date varies: spanning Q1/Q2 or Q2/Q3 across 2023-2025
    year = 2024
    start_month = 1 + (seed % 9)  # 1 to 9
    current_date = datetime.date(year, start_month, 1)

    rows: list[dict[str, object]] = []
    # Collect 60 business days
    tau_usd = 90.0 / 360.0
    tau_foreign = 90.0 / 360.0

    spot = base_spot
    usd_rate = base_usd_rate
    foreign_rate = base_foreign_rate

    while len(rows) < 60:
        if current_date.weekday() < 5:  # Monday to Friday
            is_qe = is_quarter_end_date(current_date)

            # Random walk for rates and spot
            spot *= 1.0 + rng.gauss(0.0, 0.003)
            usd_rate = max(0.005, usd_rate + rng.gauss(0.0, 0.0005))
            foreign_rate = max(0.005, foreign_rate + rng.gauss(0.0, 0.0005))

            # Basis: normal vs quarter-end spike
            target_basis = (base_basis_bp + quarter_end_spike_bp) if is_qe else (base_basis_bp + rng.gauss(0.0, 3.0))

            # Forward rate implied by target basis
            # basis = (usd_rate - implied_usd) * 10000 => implied_usd = usd_rate - basis / 10000
            implied_usd = usd_rate - (target_basis / 10000.0)
            # implied_usd = (1 / tau_usd) * [ (spot / forward) * (1 + foreign_rate * tau_foreign) - 1 ]
            # => 1 + implied_usd * tau_usd = (spot / forward) * (1 + foreign_rate * tau_foreign)
            # => forward = spot * (1 + foreign_rate * tau_foreign) / (1 + implied_usd * tau_usd)
            forward = spot * (1.0 + foreign_rate * tau_foreign) / (1.0 + implied_usd * tau_usd)

            rows.append(
                {
                    "date": current_date.isoformat(),
                    "spot": round(spot, 6),
                    "forward": round(forward, 6),
                    "usd_rate": round(usd_rate, 6),
                    "foreign_rate": round(foreign_rate, 6),
                    "tau_usd": tau_usd,
                    "tau_foreign": tau_foreign,
                }
            )

        current_date += datetime.timedelta(days=1)

    return {
        "seed": seed,
        "currency_pair": "EUR/USD",
        "rows": rows,
    }
