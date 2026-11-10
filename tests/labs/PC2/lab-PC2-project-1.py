"""PC2 Lab Project-1: Rung 1 worked example: equity pitch and IC adversarial defense validator.

SIMULATED. Validates structural and quantitative integrity of a long equity pitch
derived from an A16 discounted cash flow model, together with its 5-part scripted IC defense.
Standard library only.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EquityPitchModel:
    ticker: str
    current_price: float
    base_target: float
    bull_target: float
    bear_target: float
    base_prob: float
    bull_prob: float
    bear_prob: float
    catalysts: list[str]
    premortem_tripwires: list[str]
    sizing_weight_nav: float
    ic_defense_dialogues: list[tuple[str, str, str]]  # (Attack Vector, Question, 3-Step Defense)


def validate_equity_pitch(pitch: EquityPitchModel) -> dict[str, bool | float | str]:
    """Validate completeness and financial metrics of an institutional equity pitch."""
    prob_sum = pitch.base_prob + pitch.bull_prob + pitch.bear_prob
    probs_valid = abs(prob_sum - 1.0) < 1e-6

    exp_price = (
        pitch.base_prob * pitch.base_target + pitch.bull_prob * pitch.bull_target + pitch.bear_prob * pitch.bear_target
    )
    exp_return = (exp_price - pitch.current_price) / pitch.current_price

    upside = (pitch.base_target - pitch.current_price) / pitch.current_price
    downside = (pitch.current_price - pitch.bear_target) / pitch.current_price
    asymmetry = upside / downside if downside > 0 else 0.0

    has_catalysts = len(pitch.catalysts) >= 2
    has_premortem = len(pitch.premortem_tripwires) >= 3
    has_ic_defense = len(pitch.ic_defense_dialogues) >= 5

    # Check 3-step defense structure in every dialogue: must contain acknowledge, evidence, invalidation
    valid_defense_steps = True
    for _vector, _q, defense in pitch.ic_defense_dialogues:
        has_ack = "acknowledge" in defense.lower() or "concede" in defense.lower() or "bound" in defense.lower()
        has_evid = "evidence" in defense.lower() or "historical" in defense.lower() or "data" in defense.lower()
        has_exit = "tripwire" in defense.lower() or "exit" in defense.lower() or "liquidate" in defense.lower()
        if not (has_ack and has_evid and has_exit):
            valid_defense_steps = False

    is_compliant = (
        probs_valid
        and asymmetry >= 2.0
        and exp_return >= 0.15
        and has_catalysts
        and has_premortem
        and has_ic_defense
        and valid_defense_steps
    )

    return {
        "probs_valid": probs_valid,
        "expected_price": exp_price,
        "expected_return": exp_return,
        "asymmetry_ratio": asymmetry,
        "has_catalysts": has_catalysts,
        "has_premortem": has_premortem,
        "has_ic_defense": has_ic_defense,
        "valid_defense_steps": valid_defense_steps,
        "is_compliant": is_compliant,
    }


def main() -> None:
    print("PC2 Lab Project-1: Rung 1 Worked Example (Long Equity Pitch & IC Defense)")
    print("SIMULATED institutional equity pitch: Enterprise Infrastructure Cloud (EIC)")

    sample_pitch = EquityPitchModel(
        ticker="EIC",
        current_price=72.00,
        base_target=112.00,
        bull_target=155.00,
        bear_target=54.00,
        base_prob=0.55,
        bull_prob=0.20,
        bear_prob=0.25,
        catalysts=[
            "Q3 Earnings Release (Nov 18): Operating margin expansion toward 24% as R&D capitalization stabilizes.",
            "Annual Customer Conference (Jan 15): Launch of GenAI inference pipeline with consumption billing.",
        ],
        premortem_tripwires=[
            "Net Expansion Rate drops below 108% for two consecutive quarters (mandatory liquidation).",
            "Sales cycle length elongates beyond 120 days across Tier-1 enterprise accounts.",
            "Operating cash flow conversion falls below 80% of reported GAAP operating income.",
        ],
        sizing_weight_nav=0.035,  # 3.5% NAV
        ic_defense_dialogues=[
            (
                "Terminal Value Sensitivity",
                "Your A16 DCF assigns 74% of Enterprise Value to the terminal value. How can we deploy capital "
                "when a 50 bps increase in WACC erases the entire margin of safety?",
                "We acknowledge that terminal value represents 72.8% of operating enterprise value under baseline "
                "parameters. However, our empirical stress-test evidence shows that even under a punitive 10.5% WACC "
                "(up 150 bps) and 2.0% terminal growth, fair value is $84.50 (+17.4% above market). "
                "Our binding exit tripwire mandates immediate liquidation if return on incremental invested capital "
                "falls below WACC in any four-quarter trailing window.",
            ),
            (
                "Crowding and Institutional Concentration",
                "Top-10 hedge funds hold 38% of the free float. If the tech factor rotates, won't liquidation cascades "
                "crush the stock?",
                "We acknowledge that institutional float concentration is elevated at 38%. Empirical trading evidence "
                "from the 2022 factor drawdown demonstrates that EIC's 90-day realized beta to software momentum "
                "was 0.72 due to high net cash balances ($14/share). "
                "Our liquidation tripwire triggers automatic de-risking if 13F filings reveal aggregate top-10 selling "
                "exceeding 5% of float in a single quarter.",
            ),
            (
                "Competitive Encroachment",
                "Hyperscalers are bundling competing database optimization tools. Why won't gross margins compress?",
                "We acknowledge hyperscaler competition in baseline storage. Historical contract data shows that "
                "multi-cloud clients pay a 30% premium to avoid vendor lock-in, with gross margins stable at 76.2%. "
                "If gross margin degrades below our 71.0% tripwire threshold, we liquidate the position immediately.",
            ),
            (
                "Execution and CAC Blowout",
                "Customer acquisition costs rose 14% last quarter. What if sales productivity fails to inflect?",
                "We acknowledge the recent uptick in acquisition spending during EMEA expansion. Empirical cohort data "
                "shows CAC payback remaining healthy at 14.8 months with net retention at 121%. "
                "Our operational tripwire requires CAC payback under 19 months; any breach triggers immediate sizing "
                "reduction by 50%.",
            ),
            (
                "Macro Recession Sensitivity",
                "If corporate IT budgets freeze next fiscal year, software multiples will compress by 30%.",
                "We acknowledge enterprise software cyclicality during broader GDP contractions. Empirical evidence "
                "from the 2020 downturn proves EIC's mission-critical data governance contracts maintained 97% renewal "
                "rates with zero customer churn. "
                "If corporate software spending surveys indicate net negative budget revisions, our macro tripwire "
                "cuts position sizing to 1.5% NAV.",
            ),
        ],
    )

    val = validate_equity_pitch(sample_pitch)

    print("-" * 75)
    print(
        f"Target Valuation: Base ${sample_pitch.base_target:.2f} | "
        f"Bull ${sample_pitch.bull_target:.2f} | Bear ${sample_pitch.bear_target:.2f}"
    )
    print(f"Expected Valuation Price:              ${val['expected_price']:.2f}")
    print(f"Expected Return:                       {float(val['expected_return']) * 100:.2f}%")
    print(f"Upside/Downside Asymmetry Ratio:       {val['asymmetry_ratio']:.2f}x (Hurdle >= 2.0x)")
    print(f"Catalysts Specified:                   {len(sample_pitch.catalysts)} discrete events")
    print(f"Pre-Mortem Quantitative Tripwires:     {len(sample_pitch.premortem_tripwires)} thresholds")
    print(f"IC Adversarial Q&A Dialogues:          {len(sample_pitch.ic_defense_dialogues)} attack vectors")
    print(f"3-Step Defense Structure Compliant:    {val['valid_defense_steps']}")
    print(f"Overall Pitch Compliance:              {val['is_compliant']}")
    print("-" * 75)


main()
