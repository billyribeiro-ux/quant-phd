"""Rung 2 completion problem: the rung 1 scan with its parity-gap line and its cost-netting lines left blank.

This twin is the completed solution, so it runs as written. Standard library only. The chain is SIMULATED and is
not a market quote. Money is integer cents, rounded once from exact Fractions, a tie going toward plus infinity.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any

# SIMULATED chain: one expiry, six strikes, quotes in integer cents (not a market quote).
CHAIN: dict[str, Any] = {
    "spot_cents": 10_000,
    "df_ppm": 990_000,  # the discount factor to expiry, 0.990000, in parts per million
    "strikes_cents": [9_000, 9_500, 10_000, 10_500, 11_000, 11_500],
    "call_cents": [1_500, 1_100, 800, 700, 450, 350],
    "put_cents": [410, 385, 700, 1_095, 1_360, 1_735],
    "cost": {"fee_cents_per_contract": 5, "half_spread_cents": 10},
}
LEGS = 3  # every finding trades three legs


def round_cents(x: Fraction) -> int:
    """The nearest whole cent of an exact amount, a tie going toward plus infinity: floor(x + 1/2)."""
    return (2 * x.numerator + x.denominator) // (2 * x.denominator)


def parity_gap(call: int, put: int, spot: int, strike: int, df_ppm: int) -> Fraction:
    """The exact parity gap C - P - (S - K df) in cents, with df = df_ppm / 1e6. The caller rounds it."""
    return Fraction(call) - Fraction(put) - (Fraction(spot) - Fraction(strike * df_ppm, 1_000_000))


def chord_less_call(strikes: list[int], calls: list[int], j: int) -> Fraction:
    """The chord through the two neighbours of strike j, evaluated at strike j, less the call at j, in cents.

    A negative value is a convexity violation: the call sits above the chord. The weights are the distances to the
    other neighbour, divided by the distance between the two neighbours, so unequal spacing is handled exactly.
    """
    low, mid, high = strikes[j - 1], strikes[j], strikes[j + 1]
    w_low = Fraction(high - mid, high - low)
    w_high = Fraction(mid - low, high - low)
    return w_low * calls[j - 1] + w_high * calls[j + 1] - calls[j]


def main() -> None:
    strikes = CHAIN["strikes_cents"]
    calls = CHAIN["call_cents"]
    puts = CHAIN["put_cents"]
    spot = CHAIN["spot_cents"]
    df_ppm = CHAIN["df_ppm"]
    cost = LEGS * (CHAIN["cost"]["fee_cents_per_contract"] + CHAIN["cost"]["half_spread_cents"])
    print(f"cost per finding: {LEGS} legs x (fee + half-spread) = {cost} cents")

    print("step 1: parity gap C - P - (S - K df) at each strike")
    findings: list[tuple[str, int, int, int]] = []
    for k, strike in enumerate(strikes):
        gap = parity_gap(calls[k], puts[k], spot, strike, df_ppm)
        gross = round_cents(abs(gap))
        net = gross - cost
        verdict = "kept" if net > 0 else "dropped, net not positive"
        print(f"  strike {strike}: gap {round_cents(gap)}, gross {gross}, net {net}: {verdict}")
        if net > 0:
            findings.append(("parity", strike, gross, net))

    print("step 2: convexity in strike, the call against the chord of its neighbours")
    for j in range(1, len(strikes) - 1):
        diff = chord_less_call(strikes, calls, j)
        if diff >= 0:
            print(f"  strike {strikes[j]}: chord less call {diff}, no violation")
            continue
        gross = round_cents(-diff)
        net = gross - cost
        verdict = "kept" if net > 0 else "dropped, net not positive"
        print(f"  strike {strikes[j]}: chord less call {diff}, gross {gross}, net {net}: {verdict}")
        if net > 0:
            findings.append(("convexity", strikes[j], gross, net))

    print(f"findings kept: {len(findings)}")
    for kind, strike, gross, net in findings:
        why = (
            "parity: the call less the put differs from the synthetic forward"
            if kind == "parity"
            else ("convexity in strike: the call sits above the chord of its neighbours")
        )
        print(f"  {kind} at strike {strike}: gross {gross}, net {net}; {why}")


main()
