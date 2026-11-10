"""Lab 1 for PM2 L02: Venture Contract Terms, Founder Vesting, and Control Rights.

SIMULATED: A venture capital contract governing 10,000,000 founder shares with a standard
4-year vesting schedule and 1-year cliff (12-month cliff with 25% vesting, then 1/48th per month).
Evaluates founder vested equity and liquidation value across departure events at month 6, month 18,
and an acquisition event at month 30 under:
(A) No acceleration (standard reverse vesting).
(B) Single-trigger acceleration (100% vesting upon change of control).
(C) Double-trigger acceleration (100% vesting upon change of control + termination without cause).
Also tracks board control switch triggered by milestone covenants (Kaplan & Strömberg 2003).

Standard library and NumPy only; fully deterministic.
"""

from __future__ import annotations


def compute_vested_fraction(month: int) -> float:
    """Standard 4-year monthly vesting schedule with 12-month cliff."""
    if month < 12:
        return 0.0
    if month >= 48:
        return 1.0
    # 25% at month 12, then additional 1/48th per month for months 13 to 48
    return month / 48.0


def main() -> None:
    total_founder_shares = 10_000_000
    exit_share_price = 5.00  # $5.00 per share acquisition price

    # 1. Vesting Milestones
    vested_m06 = compute_vested_fraction(6)
    vested_m18 = compute_vested_fraction(18)
    vested_m30 = compute_vested_fraction(30)

    shares_vested_m06 = int(total_founder_shares * vested_m06)
    shares_vested_m18 = int(total_founder_shares * vested_m18)
    shares_vested_m30 = int(total_founder_shares * vested_m30)

    # 2. Acquisition Event at Month 30 ($50M company exit)
    # Scenario A: No acceleration (founder terminated, unvested shares repurchased at par)
    payoff_unaccelerated = shares_vested_m30 * exit_share_price

    # Scenario B: Single-trigger acceleration on change of control (100% immediate vesting)
    shares_single_trigger = total_founder_shares
    payoff_single_trigger = shares_single_trigger * exit_share_price

    # Scenario C1: Double-trigger without termination (retained by acquirer -> no acceleration)
    payoff_double_retained = shares_vested_m30 * exit_share_price

    # Scenario C2: Double-trigger with involuntary termination (triggers full acceleration)
    payoff_double_terminated = total_founder_shares * exit_share_price

    # 3. Contingent Board Control (Aghion & Bolton 1992 / Kaplan & Strömberg 2003)
    # 5-seat board: Founders hold 3 seats (60%), VC holds 2 seats (40%) in base state.
    # Covenant: If trailing 12-month revenue < $5.0M threshold, VC gains 1 seat from founders.
    rev_actual_q1 = 6.2  # Meets milestone -> Founder control retained
    rev_actual_q4 = 4.1  # Breaches milestone -> VC gains control (3 VC vs 2 Founder)

    vc_board_seats_q1 = 2 if rev_actual_q1 >= 5.0 else 3
    vc_board_seats_q4 = 2 if rev_actual_q4 >= 5.0 else 3
    vc_has_control_q4 = vc_board_seats_q4 >= 3

    print(f"Month 6 Cliff Check: {shares_vested_m06:,} shares vested ({vested_m06 * 100:.1f}%)")
    print(f"Month 18 Vested: {shares_vested_m18:,} shares ({vested_m18 * 100:.1f}%)")
    print(f"Month 30 Base Vested: {shares_vested_m30:,} shares ({vested_m30 * 100:.2f}%)")
    print(f"Acquisition at Month 30 Payoff (No Acceleration): ${payoff_unaccelerated / 1e6:.2f}M")
    print(f"Acquisition at Month 30 Payoff (Single Trigger): ${payoff_single_trigger / 1e6:.2f}M")
    print(f"Acquisition at Month 30 Payoff (Double Trigger Retained): ${payoff_double_retained / 1e6:.2f}M")
    print(f"Acquisition at Month 30 Payoff (Double Trigger Terminated): ${payoff_double_terminated / 1e6:.2f}M")
    print(
        f"VC Board Seats (Q1 / Q4): {vc_board_seats_q1} / {vc_board_seats_q4} (VC Control in Q4: {vc_has_control_q4})"
    )


main()
