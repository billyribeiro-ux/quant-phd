"""BK4 L04 lab 1: reserve coverage of a stablecoin under a seeded SIMULATED redemption path, in exact arithmetic.

SIMULATED. The claims, the reserve ratios and the redemption path are illustrative inputs. They describe no issuer and
no market. The path is drawn from random.Random with a fixed seed, so every run prints the same lines.

The model is the one in Section 2 of the lesson. Claims outstanding are C_0 integer cents. Reserves at the start are
rho times C_0, where rho is the reserve-to-claims ratio. A cumulative redemption share x satisfies 0 <= x < 1 and
x <= rho. Under the lesson's assumptions (redemptions paid at par from reserves, no new issuance, no fees), the reserves
left are C_0 (rho - x) and the claims left are C_0 (1 - x), so the coverage is (rho - x) / (1 - x).

The cents columns are integers. The coverage is an exact Fraction. Its value in basis points is the floor of 10000 times
the coverage, taken exactly. A share with x greater than rho is not computed, because the reserves would be negative and
no par payment exists; the lab counts those shares and prints the count.

The lab checks three statements on the computed rows: the identity coverage = (rho - x) / (1 - x), the sign rule
(coverage is below 1 exactly when rho is below 1), and the difference identity for two shares x < y. It prints each
check's result; it does not assert them.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from fractions import Fraction

SEED = 7
PATH_LENGTH = 6
CLAIMS_CENTS = 2_000_000  # C_0: 20,000.00 of the reference unit, in cents
RHOS = (Fraction(95, 100), Fraction(105, 100))  # reserve-to-claims ratios below and above 1, exact
BPS = 10_000
HAIRCUT = Fraction(1, 20)  # h, the haircut in the valuation convention of Section 4 of the lesson


@dataclass(frozen=True)
class Row:
    """The state after one cumulative redemption share on a reserve path. Amounts are integer cents."""

    share: Fraction
    reserves_left_cents: int
    claims_left_cents: int
    coverage: Fraction
    coverage_bps: int


def cents(value: Fraction) -> int:
    """Return the amount in cents as an int. Raise ValueError if the exact amount is not a whole number of cents."""
    if value.denominator != 1:
        raise ValueError(f"amount {value} is not a whole number of cents")
    return value.numerator


def coverage_of(rho: Fraction, share: Fraction) -> Fraction:
    """The coverage (rho - x) / (1 - x) after a cumulative redemption share x, for 0 <= x < 1 and x <= rho."""
    if not 0 <= share < 1 or share > rho:
        raise ValueError("the share must satisfy 0 <= x < 1 and x <= rho")
    return (rho - share) / (1 - share)


def seeded_path(seed: int, length: int) -> list[Fraction]:
    """Return `length` distinct cumulative shares k/100 with k in 1 to 99, in increasing order.

    The fixed share 99/100 is appended as the last point of the path, so that the path reaches a share above both
    reserve ratios of this lab and the omission rule is exercised.
    """
    rng = random.Random(seed)
    hundredths = sorted(rng.sample(range(1, 100), length))
    return [Fraction(k, 100) for k in hundredths] + [Fraction(99, 100)]


def state_after(rho: Fraction, share: Fraction) -> Row:
    """The reserves and claims in integer cents after redeeming `share` of C_0, and the coverage they give.

    Reserves start at rho times C_0 and fall by the redeemed claims, which are paid at par. Claims fall by the same
    amount. Both amounts are whole cents for the share grid of this lab.
    """
    reserves_start = cents(rho * CLAIMS_CENTS)
    redeemed = cents(share * CLAIMS_CENTS)
    reserves_left = reserves_start - redeemed
    claims_left = CLAIMS_CENTS - redeemed
    coverage = Fraction(reserves_left, claims_left)
    return Row(share, reserves_left, claims_left, coverage, math.floor(BPS * coverage))


def print_path_table(rho: Fraction, path: list[Fraction]) -> list[Row]:
    """Print one row per share on the path that the model can compute, and return those rows."""
    reserves_start = cents(rho * CLAIMS_CENTS)
    print(f"rho {rho} reserves_0 {reserves_start} claims_0 {CLAIMS_CENTS} rho_below_1 {rho < 1}")
    rows: list[Row] = []
    omitted = 0
    for share in path:
        if share > rho:
            omitted += 1
            print(f"  x {share} omitted: x exceeds rho, so the reserves would be negative")
            continue
        row = state_after(rho, share)
        rows.append(row)
        print(
            f"  x {share} reserves_left {row.reserves_left_cents} claims_left {row.claims_left_cents} "
            f"coverage {row.coverage} bps {row.coverage_bps} below_1 {row.coverage < 1}"
        )
    below = sum(1 for row in rows if row.coverage < 1)
    identity = all(row.coverage == coverage_of(rho, row.share) for row in rows)
    sign_rule = all((row.coverage < 1) == (rho < 1) for row in rows)
    print(f"  computed rows {len(rows)} omitted rows {omitted} coverage below 1 in {below} computed rows")
    print(f"  identity (rho - x) / (1 - x) equals reserves over claims in all computed rows: {identity}")
    print(f"  coverage below 1 exactly when rho is below 1, in all computed rows: {sign_rule}")
    return rows


def check_differences(rho: Fraction, rows: list[Row]) -> None:
    """Check the difference identity and the direction of change for every pair of computed shares x < y."""
    pairs = [(a, b) for i, a in enumerate(rows) for b in rows[i + 1 :]]
    identity = all(
        b.coverage - a.coverage == (b.share - a.share) * (rho - 1) / ((1 - a.share) * (1 - b.share)) for a, b in pairs
    )
    direction = all((b.coverage - a.coverage) * (rho - 1) > 0 for a, b in pairs)
    print(f"  pairs of computed shares {len(pairs)}")
    print(f"  difference identity (y - x)(rho - 1) / ((1 - x)(1 - y)) holds in all pairs: {identity}")
    print(
        "  coverage falls as the share rises when rho is below 1, and rises when rho is above 1, "
        f"in all pairs: {direction}"
    )


def haircut_check() -> None:
    """Print the full-cover threshold 1/(1 - h) under the valuation convention, and coverage on either side of it.

    The convention values the reserves at (1 - h) of face value, so the effective ratio is rho times (1 - h). The
    coverage at share 1/2 is the same formula with the effective ratio in place of rho.
    """
    threshold = Fraction(1) / (1 - HAIRCUT)
    print(f"haircut h {HAIRCUT} full-cover threshold 1/(1 - h) {threshold}")
    for rho in (Fraction(21, 20), threshold):
        effective = rho * (1 - HAIRCUT)
        value = coverage_of(effective, Fraction(1, 2))
        print(f"rho {rho} effective {effective} x 1/2 coverage {value} bps {math.floor(BPS * value)}")


def main() -> None:
    """Run the seeded path for two reserve ratios, the difference checks, the worked values and the haircut check."""
    path = seeded_path(SEED, PATH_LENGTH)
    print(f"SIMULATED: seed {SEED}, claims C_0 {CLAIMS_CENTS} cents, cumulative shares x in the lesson's model")
    print("path " + " ".join(str(share) for share in path))
    for rho in RHOS:
        rows = print_path_table(rho, path)
        check_differences(rho, rows)
    print("worked values, exact")
    for rho, share in (
        (Fraction(19, 20), Fraction(1, 2)),
        (Fraction(21, 20), Fraction(1, 2)),
        (Fraction(19, 20), Fraction(1, 7)),
    ):
        value = coverage_of(rho, share)
        print(f"rho {rho} x {share} coverage {value} bps {math.floor(BPS * value)}")
    print("haircut valuation convention, exact")
    haircut_check()


main()
