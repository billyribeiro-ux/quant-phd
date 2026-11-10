"""PC1 Lab L02-1: Result sentence formatting and exact rounding check.

SIMULATED. Illustrative regression estimates and standardized sentence builder.
All arithmetic uses exact fractions and explicit rounding rules. Standard library only.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class RegressionEstimate:
    variable_name: str
    beta_exact: Fraction
    se_exact: Fraction
    unit: str
    sample_universe: str
    sample_period: str


def compute_t_stat(est: RegressionEstimate) -> Fraction:
    """Compute exact t-statistic as beta / se."""
    return est.beta_exact / est.se_exact


def round_half_to_even(val: Fraction, decimal_places: int) -> Fraction:
    """Exact decimal rounding to stated places using round-half-to-even."""
    factor = 10**decimal_places
    scaled = val * factor
    # Floor integer part and remainder
    int_part = int(scaled)
    rem = scaled - int_part
    if rem > Fraction(1, 2):
        rounded_int = int_part + 1
    elif rem < Fraction(1, 2):
        rounded_int = int_part
    else:
        # Halfway: round to even
        rounded_int = int_part if int_part % 2 == 0 else int_part + 1
    return Fraction(rounded_int, factor)


def build_result_sentence(est: RegressionEstimate, rounded_bp: int) -> str:
    """Assemble a standardized results-first sentence from exact fields and rounded magnitude."""
    return (
        f"We find that {est.variable_name} increases physical investment by {rounded_bp} basis points "
        f"per standard deviation increase in common ownership across {est.sample_universe} from {est.sample_period}."
    )


def main() -> None:
    print("PC1 Lab L02-1: Result Sentence Formatting and Exact Rounding Check")
    print("SIMULATED estimates from empirical corporate finance model")

    # Raw estimates in percentage points (1 percentage point = 100 basis points)
    # beta = 0.1437 percentage points = 14.37 basis points = 1437/10000
    # se = 0.0410 percentage points = 41/1000
    estimate = RegressionEstimate(
        variable_name="institutional cross-ownership",
        beta_exact=Fraction(1437, 10000),
        se_exact=Fraction(41, 1000),
        unit="basis points",
        sample_universe="United States manufacturing firms",
        sample_period="1990 to 2020",
    )

    t_stat = compute_t_stat(estimate)
    # Convert beta to basis points (multiply by 100)
    beta_bp = estimate.beta_exact * 100  # 1437/100 = 14.37
    rounded_bp_frac = round_half_to_even(beta_bp, 0)
    rounded_bp = int(rounded_bp_frac)
    t_stat_rounded = round_half_to_even(t_stat, 2)

    rounding_error = abs(beta_bp - rounded_bp)
    max_allowed_error = Fraction(1, 2)  # Half a basis point

    print(f"Raw beta (percentage points): {estimate.beta_exact} ({float(estimate.beta_exact):.4f})")
    print(f"Raw standard error: {estimate.se_exact} ({float(estimate.se_exact):.4f})")
    print(f"Exact t-statistic: {t_stat} ({float(t_stat):.4f})")
    print(f"Rounded t-statistic (2 decimal places): {float(t_stat_rounded):.2f}")
    print(f"Raw effect in basis points: {beta_bp} ({float(beta_bp):.2f} bp)")
    print(f"Rounded effect for prose: {rounded_bp} bp")
    print(f"Rounding error: {rounding_error} bp (<= 0.5 bp: {rounding_error <= max_allowed_error})")

    sentence = build_result_sentence(estimate, rounded_bp)
    print("Standardized result sentence:")
    print(f'  "{sentence}"')

    # Verify presence of the 5 mandatory elements
    elements = {
        "Mechanism/Subject": estimate.variable_name in sentence,
        "Direction (increases)": "increases" in sentence,
        "Magnitude with unit": f"{rounded_bp} basis points" in sentence,
        "Standardized shift": "per standard deviation increase" in sentence,
        "Sample and Period": f"{estimate.sample_universe} from {estimate.sample_period}" in sentence,
    }
    for elem, present in elements.items():
        print(f"Element check: {elem:30s} -> {present}")


main()
