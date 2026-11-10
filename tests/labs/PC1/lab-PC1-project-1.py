"""PC1 Lab Project-1: Rung 1 worked example: rewrite verification and annotation checker for H1.

SIMULATED. Hypothetical introduction H1 and its reference rewrite.
All numbers and text metrics are deterministic. Standard library only.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Annotation:
    original_text: str
    rewritten_text: str
    rule_applied: str


@dataclass(frozen=True)
class IntroMetrics:
    word_count: int
    sentence_count: int
    first_number_sentence: int
    has_unit: bool
    has_sample: bool
    has_roadmap: bool


def check_introduction_structure(text: str) -> IntroMetrics:
    """Evaluate structural properties of an empirical introduction."""
    sentences = [s.strip() for s in re.split(r"\.\s+", text.strip()) if s.strip()]
    first_num_sentence = 0
    for idx, s in enumerate(sentences, start=1):
        if re.search(r"\d", s):
            first_num_sentence = idx
            break

    words = len(text.split())
    has_unit = any(
        u in text.lower() for u in ["basis points", "percent", "%", "dollars", "cents", "standard deviation"]
    )
    has_sample = "1990" in text and "2020" in text and "manufacturing" in text.lower()
    has_roadmap = "section" in text.lower() or "remainder of this paper" in text.lower()

    return IntroMetrics(
        word_count=words,
        sentence_count=len(sentences),
        first_number_sentence=first_num_sentence,
        has_unit=has_unit,
        has_sample=has_sample,
        has_roadmap=has_roadmap,
    )


def main() -> None:
    print("PC1 Lab Project-1: Rung 1 Worked Example (Introduction H1 Rewrite)")
    print("SIMULATED text from hypothetical paper H1")

    # Weak H1: literature opener, late unscaled result, generic roadmap
    weak_h1 = (
        "The relationship between corporate ownership structure and physical capital investment has long "
        "interested financial economists. Many studies examine whether concentrated institutional holdings "
        "alleviate agency frictions or foster anti-competitive coordination across product markets. "
        "Theoretical models offer conflicting predictions regarding whether common owners encourage managers "
        "to curtail redundant capacity or stimulate aggressive expansion. "
        "Prior empirical literature presents mixed findings across diverse historical samples and industries. "
        "In this paper, we explore the empirical linkage using a broad dataset. "
        "We hypothesize that cross-ownership exerts a material impact on firm capital outlays. "
        "Empirically, our regression analysis shows an increase of 14 across manufacturing firms. "
        "Section 2 describes the data. Section 3 presents the methodology. "
        "Section 4 reports the empirical results. Section 5 concludes."
    )

    # Rewritten H1: result in sentence 1, explicit unit, bounded sample, informative roadmap (162 words)
    rewritten_h1 = (
        "We show that institutional cross-ownership increases five-year physical investment by 14 basis points "
        "per standard deviation increase in common ownership across United States manufacturing firms from 1990 to "
        "2020. "
        "This economic response is concentrated in industries characterized by high product-market overlap and "
        "remains statistically robust when instrumenting for institutional holdings using financial institution "
        "mergers as exogenous ownership shocks. "
        "In contrast to unilateral theories of corporate governance, the investment response reflects coordinated "
        "capital expenditure reductions in duplicate manufacturing facilities rather than broad-based expansion. "
        "Economically, a 14 basis point change represents 6.8 percent of median capital expenditure, suggesting "
        "that common portfolio allocations generate measurable real efficiency gains across overlapping product "
        "markets without depressing firm profitability. "
        "Furthermore, we establish that these physical capital adjustments are not explained by differences in "
        "leverage, firm size, or growth opportunities across treatment cohorts. "
        "The remainder of this paper details the sample selection criteria, the quasi-experimental identification "
        "strategy, primary regression results, extensive robustness checks, and concluding implications for "
        "financial regulation."
    )

    annotations = [
        Annotation(
            original_text="The relationship between corporate ownership structure...",
            rewritten_text="We show that institutional cross-ownership increases...",
            rule_applied="Result First: Replaced literature opener with headline finding and unit in Sentence 1.",
        ),
        Annotation(
            original_text="...shows an increase of 14 across manufacturing firms.",
            rewritten_text="...by 14 basis points per standard deviation increase... 1990 to 2020.",
            rule_applied="Explicit Unit and Sample: Attached basis point unit, standardized shift, and sample dates.",
        ),
        Annotation(
            original_text="We hypothesize that cross-ownership exerts a material impact...",
            rewritten_text="The response reflects coordinated reductions in duplicate facilities...",
            rule_applied="Mechanism and Scope: Clarified economic channel without generalizing beyond manufacturing.",
        ),
        Annotation(
            original_text="Section 2 describes the data. Section 3 presents the methodology...",
            rewritten_text="The remainder of this paper details the sample selection criteria...",
            rule_applied="Informative Roadmap: Replaced bare section numbers with content-descriptive signposts.",
        ),
    ]

    before = check_introduction_structure(weak_h1)
    after = check_introduction_structure(rewritten_h1)

    print("\n--- Structural Comparison ---")
    print(f"{'Metric':26s} | {'Weak H1':12s} | {'Rewritten H1':12s} | {'Target Requirement':25s}")
    print("-" * 83)
    print(f"{'Word count':26s} | {before.word_count:12d} | {after.word_count:12d} | {'150 to 250 words':25s}")
    print(
        f"{'First number sentence':26s} | {before.first_number_sentence:12d} | "
        f"{after.first_number_sentence:12d} | {'Sentence 1 (or <= 2)':25s}"
    )
    print(f"{'Explicit unit present':26s} | {before.has_unit!s:12s} | {after.has_unit!s:12s} | {'True':25s}")
    print(f"{'Sample & dates present':26s} | {before.has_sample!s:12s} | {after.has_sample!s:12s} | {'True':25s}")
    print(
        f"{'Roadmap present':26s} | {before.has_roadmap!s:12s} | "
        f"{after.has_roadmap!s:12s} | {'True (content signposts)':25s}"
    )
    print("-" * 83)

    print(f"\nTotal annotations provided: {len(annotations)}")
    for idx, ann in enumerate(annotations, start=1):
        print(f"Annotation {idx}: {ann.rule_applied}")

    all_criteria_met = (
        150 <= after.word_count <= 250
        and after.first_number_sentence == 1
        and after.has_unit
        and after.has_sample
        and after.has_roadmap
        and len(annotations) >= 4
    )
    print(f"\nAll Rung 1 rewrite criteria satisfied: {all_criteria_met}")


main()
