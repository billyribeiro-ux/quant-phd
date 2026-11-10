"""Lab AP8-project-1: Rung 1 worked example: debate brief structural validator.

SIMULATED: Validates the structural completeness, evidence grading, citation integrity,
and cross-examination symmetry of an institutional debate brief on market efficiency.
Standard library only.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceClaim:
    claim_id: str
    side: str  # "affirmative" or "negative"
    statement: str
    grade: str  # "T", "A", "B", "C", "D"
    registry_keys: tuple[str, ...]
    locator: str
    methodology: str


@dataclass(frozen=True)
class CrossExaminationPoint:
    target_claim_id: str
    attack_vector: str
    counter_grade: str
    counter_registry_key: str
    deconstruction: str


@dataclass(frozen=True)
class DebateBrief:
    resolution: str
    affirmative_claims: tuple[EvidenceClaim, ...]
    negative_claims: tuple[EvidenceClaim, ...]
    cross_examinations: tuple[CrossExaminationPoint, ...]
    settling_conditions: tuple[str, ...]


VALID_GRADES = frozenset({"T", "A", "B", "C", "D"})
ALLOWED_ATTACK_VECTORS = frozenset(
    {
        "joint_hypothesis_confound",
        "sample_selection_survivorship",
        "implementation_friction_decay",
        "data_mining_multiple_testing",
        "unpriced_tail_risk",
    }
)


def validate_debate_brief(brief: DebateBrief) -> dict[str, bool | int | str]:
    """Validate completeness and doctoral rigor of an EMH debate brief."""
    # Check resolution
    has_res = len(brief.resolution.strip()) > 10

    # Check claims
    n_aff = len(brief.affirmative_claims)
    n_neg = len(brief.negative_claims)
    claims_balanced = n_aff >= 3 and n_neg >= 3

    # Check grades and locators
    all_claims = brief.affirmative_claims + brief.negative_claims
    grades_valid = all(c.grade in VALID_GRADES for c in all_claims)
    locators_valid = all(len(c.locator.strip()) > 0 for c in all_claims if c.grade != "T")
    cites_valid = all(len(c.registry_keys) > 0 for c in all_claims if c.grade != "T")

    # Check cross-examinations: at least 3 distinct opposing targets
    n_cx = len(brief.cross_examinations)
    cx_targets = {cx.target_claim_id for cx in brief.cross_examinations}
    cx_sufficient = n_cx >= 3 and len(cx_targets) >= 3
    cx_vectors_valid = all(cx.attack_vector in ALLOWED_ATTACK_VECTORS for cx in brief.cross_examinations)

    # Check settling conditions
    settling_valid = len(brief.settling_conditions) >= 2

    overall_pass = (
        has_res
        and claims_balanced
        and grades_valid
        and locators_valid
        and cites_valid
        and cx_sufficient
        and cx_vectors_valid
        and settling_valid
    )

    return {
        "overall_pass": overall_pass,
        "n_affirmative": n_aff,
        "n_negative": n_neg,
        "n_cross_examinations": n_cx,
        "n_settling_conditions": len(brief.settling_conditions),
        "grades_valid": grades_valid,
        "locators_valid": locators_valid,
        "cx_vectors_valid": cx_vectors_valid,
    }


def make_sample_brief() -> DebateBrief:
    """Instantiate a model doctoral debate brief."""
    aff_claims = (
        EvidenceClaim(
            claim_id="AFF-01",
            side="affirmative",
            statement=(
                "Mutual funds exhibit zero aggregate net alpha; top-decile performance is indistinguishable "
                "from sampling luck under cross-sectional bootstrap."
            ),
            grade="A",
            registry_keys=("fama2010luck",),
            locator="Table 2, Panel A (p. 1928)",
            methodology="Cross-sectional bootstrap with contemporaneous residual resampling (3,156 funds, 1984-2006).",
        ),
        EvidenceClaim(
            claim_id="AFF-02",
            side="affirmative",
            statement=(
                "Active management equilibrium dictates that competitive capital flows drive expected net alpha "
                "to zero while skilled managers extract rents via fund size."
            ),
            grade="A",
            registry_keys=("berk2015measuring", "berk2004mutual"),
            locator="Section 4, Table 1 (p. 8)",
            methodology="Structural value-added estimation on 5,974 funds; average gross value added is $3.2M/year.",
        ),
        EvidenceClaim(
            claim_id="AFF-03",
            side="affirmative",
            statement=(
                "Anomalies attenuate by ~58% post-publication, demonstrating active capital deployment that "
                "eliminates detectable pricing errors."
            ),
            grade="A",
            registry_keys=("fama1970efficient",),
            locator="Table 3, Panel B",
            methodology="Out-of-sample and post-publication decay analysis across 97 published anomalies.",
        ),
    )

    neg_claims = (
        EvidenceClaim(
            claim_id="NEG-01",
            side="negative",
            statement=(
                "Investor survey return expectations are negatively correlated with rational model discount rates, "
                "proving market valuations reflect extrapolative errors."
            ),
            grade="A",
            registry_keys=("greenwood2014expectations",),
            locator="Table 2, p. 726",
            methodology="Survey analysis across Gallup, CFO, and Shiller surveys against macro discount models.",
        ),
        EvidenceClaim(
            claim_id="NEG-02",
            side="negative",
            statement=(
                "Performance-based arbitrage creates severe resale-price risk: capital outflows during dislocations "
                "force arbitrageurs to liquidate at fire-sale discounts."
            ),
            grade="B",
            registry_keys=("shleifer1997limits",),
            locator="Section 2, Proposition 1",
            methodology="Analytical model of delegated portfolio management with performance-responsive investors.",
        ),
        EvidenceClaim(
            claim_id="NEG-03",
            side="negative",
            statement=(
                "Characteristic sorts dominate factor loadings: firm size and book-to-market explain cross-sectional "
                "returns even after controlling for beta covariance."
            ),
            grade="B",
            registry_keys=("fama1993common",),
            locator="Table 1, pp. 11-18",
            methodology="Independent double sorts decoupling factor loadings from observable firm characteristics.",
        ),
    )

    cross_examinations = (
        CrossExaminationPoint(
            target_claim_id="NEG-01",
            attack_vector="joint_hypothesis_confound",
            counter_grade="B",
            counter_registry_key="fama1991efficient",
            deconstruction=(
                "Surveys capture retail sentiments rather than marginal investor pricing kernels; "
                "wealth-weighted asset prices reflect institutional SDF."
            ),
        ),
        CrossExaminationPoint(
            target_claim_id="NEG-02",
            attack_vector="unpriced_tail_risk",
            counter_grade="B",
            counter_registry_key="fama1993common",
            deconstruction=(
                "Intermediary balance-sheet contractions during panics reflect fundamental macroeconomic "
                "distress risk rather than irrational mispricing."
            ),
        ),
        CrossExaminationPoint(
            target_claim_id="NEG-03",
            attack_vector="data_mining_multiple_testing",
            counter_grade="A",
            counter_registry_key="fama2010luck",
            deconstruction=(
                "Characteristics without factor spanning represent data-snooped in-sample patterns that "
                "fail out-of-sample replication tests."
            ),
        ),
    )

    settling = (
        "Empirical identification of marginal investor wealth-weighted discount rate vs. survey expectations.",
        "Structural estimation of whether post-publication decay matches transaction costs and margin constraints.",
    )

    return DebateBrief(
        resolution="Resolved: Liquid capital markets are informationally efficient in equilibrium.",
        affirmative_claims=aff_claims,
        negative_claims=neg_claims,
        cross_examinations=cross_examinations,
        settling_conditions=settling,
    )


def main() -> None:
    brief = make_sample_brief()
    res = validate_debate_brief(brief)

    print("================================================================================")
    print("DOCTORAL DEBATE BRIEF VALIDATION REPORT")
    print("================================================================================")
    print(f"Resolution:                  {brief.resolution}")
    print(f"Affirmative Claims:          {res['n_affirmative']} (Hurdle >= 3)")
    print(f"Negative Claims:             {res['n_negative']} (Hurdle >= 3)")
    print(f"Cross-Examinations:          {res['n_cross_examinations']} (Hurdle >= 3)")
    print(f"Settling Conditions:         {res['n_settling_conditions']} (Hurdle >= 2)")
    print(f"All Grades Grounded:         {res['grades_valid']}")
    print(f"Locators Specified:          {res['locators_valid']}")
    print(f"Attack Vectors Compliant:    {res['cx_vectors_valid']}")
    print("-" * 80)
    print(f"Overall Validation Status:   {'PASS' if res['overall_pass'] else 'FAIL'}")
    print("================================================================================")


main()
