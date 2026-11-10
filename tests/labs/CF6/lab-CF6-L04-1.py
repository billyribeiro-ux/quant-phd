"""CF6 Lesson 4 Inline Lab 1: Myers-Majluf Adverse Selection and SEO Pricing.

Holdings to BUILDER_RULES §6: deterministic, self-contained, standard library.
"""

from __future__ import annotations


def evaluate_myers_majluf(
    v_good: float,
    v_bad: float,
    prob_good: float,
    proj_cost: float,
    proj_npv: float,
    slack: float,
) -> dict[str, float | str | bool]:
    e_req = max(0.0, proj_cost - slack)
    if e_req == 0.0:
        return {
            "decision": "issue",
            "dilution": 0.0,
            "threshold": 0.0,
            "pooling_price": v_good + slack + proj_npv,
            "ann_ret": 0.0,
            "slack_sufficient": True,
        }

    a_bar = prob_good * v_good + (1.0 - prob_good) * v_bad
    v_pool = a_bar + proj_cost + proj_npv
    alpha = e_req / v_pool
    v_good_true = v_good + proj_cost + proj_npv
    dilution = alpha * v_good_true - e_req

    net_benefit_good = (1.0 - alpha) * v_good_true - (v_good + slack)
    decision = "issue" if net_benefit_good >= -1e-9 else "pass"
    threshold = e_req * (1.0 - prob_good) * (v_good - v_bad) / v_pool

    p_pre = a_bar + slack
    p_post_existing = v_pool - e_req
    ann_ret = (p_post_existing - p_pre) / p_pre if decision == "issue" else 0.0

    return {
        "decision": decision,
        "dilution": dilution,
        "threshold": threshold,
        "pooling_price": v_pool,
        "ann_ret": ann_ret,
        "slack_sufficient": False,
    }


def main() -> None:
    # Baseline firm parameters ($M)
    v_assets_good = 220.0  # High-quality assets in place
    v_assets_bad = 100.0  # Low-quality assets in place
    prob_good = 0.50  # Symmetric prior
    project_cost = 40.0  # Capital required for positive-NPV project
    project_npv = 8.0  # Project true NPV ($8M)

    print("=== Myers-Majluf (1984) SEO Adverse Selection Model ===")
    print(f"Good Assets: ${v_assets_good:.1f}M | Bad Assets: ${v_assets_bad:.1f}M | Prior P(Good): {prob_good:.0%}")
    print(f"Project Cost: ${project_cost:.1f}M | Project NPV: ${project_npv:.1f}M\n")

    # Scenario 1: Zero cash slack (equity issue required)
    s1 = evaluate_myers_majluf(v_assets_good, v_assets_bad, prob_good, project_cost, project_npv, slack=0.0)
    print("--- Scenario 1: Zero Internal Cash Slack (Full Equity Issue $40M) ---")
    print(f"  Old Shareholder Dilution Cost: ${s1['dilution']:.2f}M")
    print(f"  Required Project NPV Threshold: ${s1['threshold']:.2f}M")
    print(f"  Good Firm Investment Decision:  {str(s1['decision']).upper()}")
    print(f"  Announcement Return Delta P:    {float(s1['ann_ret']) * 100:.2f}%")
    if s1["decision"] == "pass":
        print("  Outcome: UNDERINVESTMENT! Good firm passes up a +$8M NPV project due to dilution.\n")
    else:
        print("  Outcome: Pooling issue proceeds.\n")

    # Scenario 2: Partial cash slack ($20M internal cash, $20M equity issue)
    s2 = evaluate_myers_majluf(v_assets_good, v_assets_bad, prob_good, project_cost, project_npv, slack=20.0)
    print("--- Scenario 2: Partial Cash Slack ($20M Cash, $20M Equity Issue) ---")
    print(f"  Old Shareholder Dilution Cost: ${s2['dilution']:.2f}M")
    print(f"  Required Project NPV Threshold: ${s2['threshold']:.2f}M")
    print(f"  Good Firm Investment Decision:  {str(s2['decision']).upper()}")
    print(f"  Announcement Return Delta P:    {float(s2['ann_ret']) * 100:.2f}%\n")

    # Scenario 3: Full cash slack ($40M internal cash, zero equity issue)
    s3 = evaluate_myers_majluf(v_assets_good, v_assets_bad, prob_good, project_cost, project_npv, slack=40.0)
    print("--- Scenario 3: Sufficient Cash Slack ($40M Cash, No Equity Dilution) ---")
    print(f"  Old Shareholder Dilution Cost: ${s3['dilution']:.2f}M")
    print(f"  Good Firm Investment Decision:  {str(s3['decision']).upper()}")
    print("  Outcome: Full investment achieved; financial slack eliminates adverse selection.")


main()
