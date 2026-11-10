"""Lab AP8-project-2: Rung 2 completion problem: cross-examination scoring and Bayesian updating.

SIMULATED: Completed reference solution for scoring adversarial cross-examinations,
evaluating Bayesian posterior odds of market efficiency, and certifying empirical settling conditions.
Standard library only.
"""

from __future__ import annotations


def score_cross_examination(
    attack_vector: str,
    counter_grade: str,
    deconstruction_words: int,
) -> float:
    """Compute the methodological rigor score of an adversarial cross-examination (0.0 to 1.0).

    A doctoral cross-examination must:
    1. Target an approved attack vector (weight 0.40)
    2. Support the critique with Grade A/T (1.0) or Grade B (0.75) counter-evidence (weight 0.35)
    3. Articulate a detailed deconstruction >= 15 words (weight 0.25)
    """
    valid_vectors = {
        "joint_hypothesis_confound",
        "sample_selection_survivorship",
        "implementation_friction_decay",
        "data_mining_multiple_testing",
        "unpriced_tail_risk",
    }

    # Vector score (0.40)
    vector_score = 0.40 if attack_vector in valid_vectors else 0.0

    # Grade score (0.35)
    grade_weights = {"T": 1.0, "A": 1.0, "B": 0.75, "C": 0.40, "D": 0.10}
    grade_score = 0.35 * grade_weights.get(counter_grade, 0.0)

    # Deconstruction depth score (0.25)
    depth_score = 0.25 * min(1.0, deconstruction_words / 15.0)

    return round(vector_score + grade_score + depth_score, 4)


def update_efficiency_posterior_odds(
    prior_prob_emh: float,
    lr_post_publication_decay: float,
    lr_bootstrap_alpha_luck: float,
    lr_survey_expectations_puzzle: float,
) -> tuple[float, float]:
    """Compute posterior odds and posterior probability of market efficiency using Bayes' rule.

    Odds = P(EMH) / (1 - P(EMH))
    Posterior Odds = Prior Odds * LR_1 * LR_2 * LR_3
    Posterior Prob = Posterior Odds / (1 + Posterior Odds)
    """
    prior_odds = prior_prob_emh / (1.0 - prior_prob_emh)
    combined_lr = lr_post_publication_decay * lr_bootstrap_alpha_luck * lr_survey_expectations_puzzle
    posterior_odds = prior_odds * combined_lr
    posterior_prob = posterior_odds / (1.0 + posterior_odds)

    return round(posterior_odds, 4), round(posterior_prob, 4)


def evaluate_settling_condition(text: str) -> bool:
    """Verify whether a proposed settling condition provides operational falsification criteria."""
    operational_keywords = ("structural", "falsif", "wealth-weighted", "micro-data", "margin", "out-of-sample")
    lower = text.lower()
    has_keyword = any(kw in lower for kw in operational_keywords)
    is_sufficient_length = len(text.strip().split()) >= 10
    return has_keyword and is_sufficient_length


def main() -> None:
    # 1. Score cross-examinations
    cxs = [
        ("joint_hypothesis_confound", "A", 22),
        ("unpriced_tail_risk", "B", 18),
        ("implementation_friction_decay", "A", 16),
        ("unsupported_rhetoric", "D", 8),
    ]

    print("================================================================================")
    print("DOCTORAL CROSS-EXAMINATION & BAYESIAN EFFICIENCY EVALUATOR")
    print("================================================================================")
    print(f"{'Attack Vector':>32} | {'Grade':>5} | {'Words':>5} | {'Rigor Score':>11} | {'Status':>6}")
    print("-" * 75)

    scores = []
    for vec, gr, w in cxs:
        sc = score_cross_examination(vec, gr, w)
        scores.append(sc)
        status = "PASS" if sc >= 0.80 else "FAIL"
        print(f"{vec:>32} | {gr:>5} | {w:>5} | {sc:11.4f} | {status:>6}")

    # 2. Bayesian Belief Update
    # Base prior P(EMH) = 0.50 (prior odds = 1.0)
    post_odds, post_prob = update_efficiency_posterior_odds(
        prior_prob_emh=0.50,
        lr_post_publication_decay=1.40,
        lr_bootstrap_alpha_luck=1.60,
        lr_survey_expectations_puzzle=0.45,
    )

    print("-" * 75)
    print("BAYESIAN POSTERIOR SYNTHESIS (Prior P(EMH) = 0.50):")
    print(f"  Combined Evidence Likelihood Ratio:  {1.40 * 1.60 * 0.45:.4f}")
    print(f"  Posterior Odds of Market Efficiency: {post_odds:.4f}")
    print(f"  Posterior Probability of EMH:        {post_prob * 100:.2f}%")

    # 3. Settling conditions check
    cond1 = (
        "Structural estimation of whether post-publication decay matches transaction costs and margin constraints "
        "across out-of-sample micro-data."
    )
    cond2 = "Markets will be proven efficient when prices stop moving irrationally."
    print("-" * 75)
    print("SETTLING CONDITIONS AUDIT:")
    print(f"  Condition 1 Operational: {evaluate_settling_condition(cond1)}")
    print(f"  Condition 2 Operational: {evaluate_settling_condition(cond2)}")
    print("================================================================================")


main()
