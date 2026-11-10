"""PC2 Lab Project-2: Rung 2 completion problem: completed solution for macro trade pitch and IC defense.

SIMULATED. Completed reference solution for a US Treasury 2Y/10Y yield curve steepener pitch
derived from the A20 macro trade-construction engine, including DV01 neutral weighting,
fractional Kelly sizing, and a 5-step scripted IC adversarial defense.
Standard library only.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CurveSteepenerPitch:
    trade_name: str
    current_spread_bps: float
    base_target_bps: float
    bull_target_bps: float
    bear_target_bps: float
    dv01_2y: float
    dv01_10y: float
    dv01_hedge_ratio: float
    win_probability: float
    quarter_kelly_weight: float
    catalysts: list[str]
    premortem_tripwires: list[str]
    ic_defense_dialogues: list[tuple[str, str, str]]


def calculate_dv01_hedge_ratio(dv01_leg1: float, dv01_leg2: float) -> float:
    """Calculate duration-neutral hedge ratio: contracts of leg2 per contract of leg1."""
    if dv01_leg2 <= 0:
        msg = "Leg 2 DV01 must be strictly positive"
        raise ValueError(msg)
    return dv01_leg1 / dv01_leg2


def evaluate_macro_pitch(pitch: CurveSteepenerPitch) -> dict[str, bool | float]:
    """Verify quantitative parameters and IC defense completeness of macro curve pitch."""
    # Compute basis point payoff asymmetry
    upside_bps = pitch.base_target_bps - pitch.current_spread_bps
    downside_bps = pitch.current_spread_bps - pitch.bear_target_bps
    asymmetry = upside_bps / downside_bps if downside_bps > 0 else 0.0

    expected_bps = 0.55 * pitch.base_target_bps + 0.20 * pitch.bull_target_bps + 0.25 * pitch.bear_target_bps
    expected_gain_bps = expected_bps - pitch.current_spread_bps

    # Verify DV01 hedge ratio consistency: 2Y contracts per 10Y contract = dv01_10y / dv01_2y
    expected_ratio = pitch.dv01_10y / pitch.dv01_2y
    ratio_valid = abs(pitch.dv01_hedge_ratio - expected_ratio) < 1e-4

    has_catalysts = len(pitch.catalysts) >= 2
    has_tripwires = len(pitch.premortem_tripwires) >= 3
    has_ic_defense = len(pitch.ic_defense_dialogues) >= 5

    valid_defense_steps = True
    for _vec, _q, defense in pitch.ic_defense_dialogues:
        has_ack = "acknowledge" in defense.lower() or "concede" in defense.lower() or "bound" in defense.lower()
        has_evid = "evidence" in defense.lower() or "historical" in defense.lower() or "data" in defense.lower()
        has_exit = "tripwire" in defense.lower() or "exit" in defense.lower() or "liquidate" in defense.lower()
        if not (has_ack and has_evid and has_exit):
            valid_defense_steps = False

    is_compliant = (
        ratio_valid
        and asymmetry >= 2.0
        and expected_gain_bps >= 25.0
        and has_catalysts
        and has_tripwires
        and has_ic_defense
        and valid_defense_steps
    )

    return {
        "asymmetry_ratio": asymmetry,
        "expected_gain_bps": expected_gain_bps,
        "ratio_valid": ratio_valid,
        "has_catalysts": has_catalysts,
        "has_tripwires": has_tripwires,
        "has_ic_defense": has_ic_defense,
        "valid_defense_steps": valid_defense_steps,
        "is_compliant": is_compliant,
    }


def main() -> None:
    print("PC2 Lab Project-2: Rung 2 Completed Solution (Macro Curve Steepener Pitch)")
    print("SIMULATED macro trade construction from A20 engine")

    # Leg parameters: Long 2Y Treasury (DV01 = $42.50 per contract), Short 10Y (DV01 = $85.00 per contract)
    dv01_2y = 42.50
    dv01_10y = 85.00
    hedge_ratio = calculate_dv01_hedge_ratio(dv01_10y, dv01_2y)  # 2.0 contracts of 2Y per 10Y contract

    # Trade: Long 2Y / Short 10Y Steepener (Current 2s10s spread = -35 bps inverted)
    pitch = CurveSteepenerPitch(
        trade_name="US 2s10s Yield Curve Steepener (DV01 Neutral)",
        current_spread_bps=-35.0,
        base_target_bps=30.0,  # +65 bps steepening to positive slope
        bull_target_bps=75.0,  # +110 bps deep disinversion
        bear_target_bps=-65.0,  # -30 bps further inversion to stop-loss
        dv01_2y=dv01_2y,
        dv01_10y=dv01_10y,
        dv01_hedge_ratio=hedge_ratio,
        win_probability=0.62,
        quarter_kelly_weight=0.04,  # 4.0% NAV risk allocation
        catalysts=[
            "FOMC Meeting (Sep 18): Shift in policy dots acknowledging cooling labor demand and initiating easing.",
            "Treasury Refunding Announcement (Nov 1): Shift in issuance duration toward longer-dated coupon supply.",
        ],
        premortem_tripwires=[
            "2s10s spread inverts past -65 bps for 3 consecutive closes (mandatory stop-loss liquidation).",
            "Core PCE inflation re-accelerates above 3.5% annualized on 3-month trailing basis.",
            "Negative carry / roll drag exceeds 18 bps over any 90-day holding window.",
        ],
        ic_defense_dialogues=[
            (
                "Negative Carry Drag",
                "The curve is inverted by 35 bps. You are bleeding 4 bps a month in negative carry. "
                "How long can you hold before roll drag eats your alpha?",
                "We acknowledge that carrying an inverted 2s10s position bleeds 3.8 bps monthly in financing. "
                "Historical rate-cycle evidence from 1989, 2000, 2007, and 2019 proves that once easing cycles begin, "
                "steepening averages 145 bps in 6 months, dwarfing 12-month carry drag by 3.5x. "
                "Our strict invalidation tripwire liquidates the position if total cumulative carry drag hits 18 bps "
                "before the first Fed rate cut.",
            ),
            (
                "Sticky Wage Inflation",
                "What if wage growth remains stubborn and the Fed holds rates higher for another 18 months?",
                "We acknowledge sticky service inflation risks. Empirical Phillips-curve data from the Atlanta Fed "
                "shows non-supervisory wage deceleration from 6.1% to 4.2%. "
                "If non-farm payroll additions exceed 250k for two consecutive prints, our macro tripwire exit rule "
                "halves the position size.",
            ),
            (
                "Long-End Supply Absorption",
                "Foreign central banks and pension funds could buy the 10Y, causing a bull-flattener instead.",
                "We acknowledge foreign reserve rebalancing dynamics. Empirical TIC flow data confirms that "
                "Treasury net issuance of $1.8T will flood dealer balance sheets, anchoring term premia. "
                "If 10Y Treasury term premium drops below -50 bps, our curve model invalidates the thesis and triggers "
                "orderly tripwire liquidation.",
            ),
            (
                "DV01 Instability Across Convexity",
                "Your 2.0x contract ratio is calculated at current yields. In a 100 bps bond rally, negative convexity "
                "breaks your hedge.",
                "We acknowledge second-order dollar duration drift under large parallel shifts. Empirical evidence and "
                "gamma analysis show DV01 drift is bounded under 2.8% for +/- 75 bps shocks. "
                "Our risk model runs weekly DV01 rebalancing with an execution tripwire triggering re-hedging "
                "whenever leg mismatch exceeds 3.0%.",
            ),
            (
                "Global Rate Spillovers",
                "If the ECB or Bank of Japan hikes rates aggressively, European bond yields could invert US spreads.",
                "We acknowledge sovereign bond co-movement across G10 markets. Empirical regression evidence over "
                "20 years shows US 2s10s slope is driven 82% by domestic policy and only 18% by global factors. "
                "If transatlantic spread divergence exceeds 45 bps, our exit tripwire protocol mandates liquidation.",
            ),
        ],
    )

    metrics = evaluate_macro_pitch(pitch)

    print(f"Trade:                                {pitch.trade_name}")
    print(f"Current Spread:                       {pitch.current_spread_bps:+.1f} bps")
    print(
        f"Targets (Base / Bull / Bear):         {pitch.base_target_bps:+.1f} / "
        f"{pitch.bull_target_bps:+.1f} / {pitch.bear_target_bps:+.1f} bps"
    )
    print(f"DV01 Hedge Ratio (2Y contracts/10Y):  {pitch.dv01_hedge_ratio:.2f}x (Consistent: {metrics['ratio_valid']})")
    print(f"Upside/Downside Asymmetry:            {float(metrics['asymmetry_ratio']):.2f}x (Hurdle >= 2.0x)")
    print(f"Probability-Weighted Expected Gain:   {float(metrics['expected_gain_bps']):+.1f} bps")
    print(f"Pre-Mortem Quantitative Tripwires:    {len(pitch.premortem_tripwires)} thresholds")
    print(f"IC Defense Dialogues:                 {len(pitch.ic_defense_dialogues)} attack vectors")
    print(f"3-Step Defense Structure Verified:    {metrics['valid_defense_steps']}")
    print(f"Macro Pitch Full Compliance:          {metrics['is_compliant']}")


main()
