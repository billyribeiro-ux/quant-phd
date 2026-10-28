"""CF1 L06 lab 1: Monte Carlo NPV, checked for convergence against a case with a closed form. SIMULATED.

SIMULATED: every receipt is drawn from the seeded generator below. No company, filing or market series is read.

Model. An investment of INVESTMENT cents is made at time zero. Each year t = 1 to YEARS, the receipt is a whole
number of cents drawn uniformly from LOW to HIGH inclusive, independently across years. The net present value (NPV)
of one draw, in cents, is the investment's negative plus the receipts discounted at RATE.

Closed forms, for this model only. The mean receipt is (LOW + HIGH) / 2. The expected NPV is the negative of the
investment plus the mean receipt times the annuity factor (1 - (1 + RATE)**-YEARS) / RATE. The variance of one
discrete uniform receipt on m = HIGH - LOW + 1 values is (m**2 - 1) / 12, and the variance of the NPV is the sum over
years of that variance divided by (1 + RATE)**(2t). The Monte Carlo estimate of the mean has standard error
sd / sqrt(n), where sd is the sample standard deviation of n draws.
"""

from __future__ import annotations

import math
import random
import statistics

SEED = 6  # seed for every draw in this lab
RATE = 0.10  # annual discount rate, a SIMULATED hurdle rate
YEARS = 5  # receipts in years 1 to 5
INVESTMENT = 300_000  # cents paid at time zero
LOW = 50_000  # lowest possible receipt in a year, cents
HIGH = 150_000  # highest possible receipt in a year, cents
N_MAX = 50_000  # draws; the smaller samples are the first n draws of the same run
SAMPLE_SIZES = (100, 1_000, 10_000, 50_000)
QUANTILES = (0.10, 0.50, 0.90)


def annuity_factor(rate: float, years: int) -> float:
    """Present value of 1 per year for the given years at the given rate, a dimensionless number."""
    return (1.0 - (1.0 + rate) ** -years) / rate


def npv_of(receipts: list[int]) -> float:
    """NPV in cents of one draw: the investment is negative, and receipts[t - 1] arrives at the end of year t."""
    return -INVESTMENT + math.fsum(x / (1.0 + RATE) ** (t + 1) for t, x in enumerate(receipts))


def quantile(sorted_values: list[float], p: float) -> float:
    """Nearest-rank quantile of an ascending list: the value at position ceil(p * n) (1-based)."""
    rank = max(1, math.ceil(p * len(sorted_values)))
    return sorted_values[rank - 1]


def main() -> None:
    rng = random.Random(SEED)
    npvs = [npv_of([rng.randint(LOW, HIGH) for _ in range(YEARS)]) for _ in range(N_MAX)]

    m = HIGH - LOW + 1
    receipt_var = (m * m - 1) / 12.0
    mean_receipt = (LOW + HIGH) / 1.0
    expected = -INVESTMENT + mean_receipt * annuity_factor(RATE, YEARS)
    sd_exact = math.sqrt(sum(receipt_var / (1.0 + RATE) ** (2 * t) for t in range(1, YEARS + 1)))

    print(f"seed {SEED} rate {RATE} years {YEARS} investment {INVESTMENT} low {LOW} high {HIGH} draws {N_MAX}")
    print(f"expected_npv_cents_closed_form {expected:.2f}")
    print(f"sd_npv_cents_closed_form {sd_exact:.2f}")
    for n in SAMPLE_SIZES:
        sample = npvs[:n]
        mean_n = math.fsum(sample) / n
        sd_n = statistics.stdev(sample)
        se_n = sd_n / math.sqrt(n)
        z = (mean_n - expected) / se_n
        print(
            f"n {n:>6} mean_npv_cents {mean_n:.2f} se_cents {se_n:.2f} error_in_se {z:+.3f} within_3se {abs(z) <= 3.0}"
        )
    sd_all = statistics.stdev(npvs)
    print(f"n {N_MAX} sd_npv_cents_sample {sd_all:.2f} sd_relative_to_closed_form {sd_all / sd_exact:.4f}")

    ordered = sorted(npvs)
    for p in QUANTILES:
        print(f"quantile_{int(p * 100):02d}_npv_cents {quantile(ordered, p):.2f}")
    negative = sum(1 for x in npvs if x < 0) / N_MAX
    se_negative = math.sqrt(negative * (1.0 - negative) / N_MAX)
    print(f"share_npv_below_zero {negative:.4f} se {se_negative:.4f}")


main()
