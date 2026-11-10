"""PC2 Lab Project-3: Rung 3 independent project verification for two pitches and IC defenses.

SIMULATED. Audits structural completeness, valuation asymmetry, catalyst specifications,
pre-mortem quantitative tripwires, and 3-step adversarial IC defense dialogues across
both the Long Equity pitch (A16) and Macro Trade pitch (A20).
Standard library only.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PitchSubmission:
    asset_class: str  # "Equity" or "Macro"
    trade_name: str
    current_level: float
    base_target: float
    bull_target: float
    bear_target: float
    asymmetry_ratio: float
    expected_gain_pct: float
    catalyst_count: int
    premortem_tripwire_count: int
    sizing_weight_pct: float
    ic_dialogues: list[tuple[str, str, str]]


def verify_pitch_submission(p: PitchSubmission) -> dict[str, bool]:
    """Verify compliance across all professional pitch and defense standards."""
    has_asymmetry = p.asymmetry_ratio >= 2.0
    has_gain = p.expected_gain_pct >= 10.0
    has_catalysts = p.catalyst_count >= 2
    has_premortem = p.premortem_tripwire_count >= 3
    has_ic_dialogues = len(p.ic_dialogues) >= 5

    # Check 3-step defense structure in all dialogues
    dialogues_structured = True
    for _vec, _q, ans in p.ic_dialogues:
        has_ack = "acknowledge" in ans.lower() or "bound" in ans.lower() or "concede" in ans.lower()
        has_evid = "evidence" in ans.lower() or "historical" in ans.lower() or "data" in ans.lower()
        has_exit = "tripwire" in ans.lower() or "liquidate" in ans.lower() or "exit" in ans.lower()
        if not (has_ack and has_evid and has_exit):
            dialogues_structured = False

    all_ok = (
        has_asymmetry and has_gain and has_catalysts and has_premortem and has_ic_dialogues and dialogues_structured
    )

    return {
        "asymmetry_ok": has_asymmetry,
        "gain_ok": has_gain,
        "catalysts_ok": has_catalysts,
        "premortem_ok": has_premortem,
        "ic_dialogues_ok": has_ic_dialogues,
        "dialogues_structured": dialogues_structured,
        "all_compliant": all_ok,
    }


def main() -> None:
    print("PC2 Lab Project-3: Rung 3 Independent Project Structural Self-Check")
    print("SIMULATED submission audit for two investment pitches and IC defenses")

    # Pitch 1: Long Equity Pitch (Enterprise Infrastructure Cloud - from A16 Valuation Engine)
    equity_pitch = PitchSubmission(
        asset_class="Equity",
        trade_name="Enterprise Infrastructure Cloud (EIC)",
        current_level=72.00,
        base_target=112.00,
        bull_target=155.00,
        bear_target=54.00,
        asymmetry_ratio=2.22,
        expected_gain_pct=47.36,
        catalyst_count=2,
        premortem_tripwire_count=3,
        sizing_weight_pct=3.5,
        ic_dialogues=[
            (
                "Terminal Value Dominance",
                "Question on TV share...",
                "We acknowledge TV share is 72.8%. Empirical stress test evidence shows value holds at $84.50. "
                "Our tripwire liquidates if ROIC falls below WACC.",
            ),
            (
                "Hedge Fund Float Crowding",
                "Question on crowding...",
                "We acknowledge institutional float concentration of 38%. Historical trading evidence proves low "
                "beta. Our liquidation tripwire triggers on 5% float selling.",
            ),
            (
                "Competitive Encroachment",
                "Question on hyperscalers...",
                "We acknowledge hyperscaler competition. Historical contract data shows 30% multi-cloud premium. "
                "Our tripwire mandates liquidation if gross margin drops below 71%.",
            ),
            (
                "CAC Payback Blowout",
                "Question on sales efficiency...",
                "We acknowledge sales investment. Empirical cohort data shows CAC payback at 14.8 months. "
                "Our tripwire exits if payback exceeds 19 months.",
            ),
            (
                "Macro IT Budget Freeze",
                "Question on macro slowdown...",
                "We acknowledge enterprise software cyclicality. Empirical evidence shows 97% contract renewals. "
                "Our tripwire cuts sizing if budget surveys turn negative.",
            ),
        ],
    )

    # Pitch 2: Macro Trade Pitch (US 2s10s Curve Steepener - from A20 Macro Engine)
    macro_pitch = PitchSubmission(
        asset_class="Macro",
        trade_name="US 2s10s Yield Curve Steepener (DV01 Neutral)",
        current_level=-35.0,
        base_target=30.0,
        bull_target=75.0,
        bear_target=-65.0,
        asymmetry_ratio=2.17,
        expected_gain_pct=143.4,  # Percent gain relative to risk budget
        catalyst_count=2,
        premortem_tripwire_count=3,
        sizing_weight_pct=4.0,
        ic_dialogues=[
            (
                "Negative Carry Drag",
                "Question on roll drag...",
                "We acknowledge negative carry of 3.8 bps/month. Historical easing evidence shows 145 bps steepening. "
                "Our tripwire exits if carry drag exceeds 18 bps.",
            ),
            (
                "Sticky Service Inflation",
                "Question on wage inflation...",
                "We acknowledge service inflation persistence. Empirical Phillips-curve data confirms wage slowdown. "
                "Our macro tripwire exit halves size if payrolls exceed 250k.",
            ),
            (
                "Long-End Foreign Buying",
                "Question on bull-flattening...",
                "We acknowledge foreign reserve flows. Empirical TIC flow data confirms $1.8T Treasury issuance. "
                "Our tripwire liquidates if term premium drops below -50 bps.",
            ),
            (
                "Convexity Hedge Drift",
                "Question on DV01 drift...",
                "We acknowledge second-order duration drift. Empirical gamma evidence bounds drift under 2.8%. "
                "Our tripwire re-hedges if mismatch exceeds 3%.",
            ),
            (
                "Global Central Bank Divergence",
                "Question on foreign bond yields...",
                "We acknowledge G10 yield co-movement. Empirical regression evidence shows 82% domestic determination. "
                "Our exit tripwire triggers if transatlantic spread divergence exceeds 45 bps.",
            ),
        ],
    )

    submissions = [equity_pitch, macro_pitch]
    all_passed = True

    print("-" * 80)
    for p in submissions:
        res = verify_pitch_submission(p)
        if not res["all_compliant"]:
            all_passed = False
        print(f"Asset Class:                          {p.asset_class} ({p.trade_name})")
        print(f"  - Asymmetry Ratio (>= 2.0x):         {p.asymmetry_ratio:.2f}x -> {res['asymmetry_ok']}")
        print(f"  - Expected Gain Threshold:           {p.expected_gain_pct:.1f}% -> {res['gain_ok']}")
        print(f"  - Catalysts Specified (>= 2):        {p.catalyst_count} -> {res['catalysts_ok']}")
        print(f"  - Pre-Mortem Tripwires (>= 3):       {p.premortem_tripwire_count} -> {res['premortem_ok']}")
        print(f"  - IC Adversarial Dialogues (>= 5):   {len(p.ic_dialogues)} -> {res['ic_dialogues_ok']}")
        print(f"  - 3-Step Defense Structure Verified: {res['dialogues_structured']}")
        print(f"  - Pitch Submission Status:           {'PASS' if res['all_compliant'] else 'FAIL'}")
        print("-" * 80)

    print(f"\nAll Project Submissions Compliant:     {all_passed}")


main()
