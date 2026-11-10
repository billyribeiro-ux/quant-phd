"""PC1 Lab Project-2: Rung 2 completion problem: completed solution for introduction H2 rewrite.

SIMULATED. Hypothetical paper H2 on sovereign debt restructuring.
All numbers and text metrics are deterministic. Standard library only.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


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
    has_sample = "1980" in text and "2018" in text and "emerging market" in text.lower()
    has_roadmap = "section" in text.lower() or "remainder of this paper" in text.lower()

    return IntroMetrics(
        word_count=words,
        sentence_count=len(sentences),
        first_number_sentence=first_num_sentence,
        has_unit=has_unit,
        has_sample=has_sample,
        has_roadmap=has_roadmap,
    )


def assemble_h2_rewrite(result_sentence: str, roadmap_sentence: str) -> str:
    """Combine completed sentences with the middle body to form the full rewrite."""
    middle_body = (
        "This borrowing cost reduction is persistent, lasting at least four years following renegotiation closure, "
        "and is robust to controlling for contemporaneous macroeconomic adjustments, initial debt-to-GDP ratios, "
        "and global commodity price cycles. "
        "By contrast, reprofiling operations that lengthen maturities without nominal face-value relief fail to "
        "lower secondary market yields, leaving countries vulnerable to repeated default distress within three years. "
        "Cross-sectional sample splits indicate that spread relief is strongest among debtor nations with diversified "
        "export bases and transparent fiscal accounting. "
        "These debt sustainability improvements operate primarily through reduced domestic banking sector distress "
        "and restored international capital market access for domestic private firms. "
    )
    return f"{result_sentence} {middle_body}{roadmap_sentence}"


def main() -> None:
    print("PC1 Lab Project-2: Rung 2 Completed Solution (Introduction H2 Rewrite)")
    print("SIMULATED text from hypothetical paper H2")

    # In the completion problem on the page, these two lines are blanked with ___
    result_sentence = "We show that sovereign debt restructuring agreements with face-value haircuts exceeding 30 percent reduce post-restructuring five-year sovereign bond spreads by 185 basis points across 48 emerging market sovereign default episodes from 1980 to 2018."  # noqa: E501
    roadmap_sentence = "The remainder of this paper details the default database construction, the restructuring event-study identification, panel regression estimates across haircut bins, robustness tests for omitted restructuring terms, and implications for multilateral debt renegotiations."  # noqa: E501

    rewritten_h2 = assemble_h2_rewrite(result_sentence, roadmap_sentence)
    metrics = check_introduction_structure(rewritten_h2)

    print(f"Total word count: {metrics.word_count}")
    print(f"Total sentence count: {metrics.sentence_count}")
    print(f"First empirical number sentence: {metrics.first_number_sentence}")
    print(f"Explicit unit present: {metrics.has_unit}")
    print(f"Sample and dates present: {metrics.has_sample}")
    print(f"Informative roadmap present: {metrics.has_roadmap}")

    all_criteria_met = (
        150 <= metrics.word_count <= 250
        and metrics.first_number_sentence == 1
        and metrics.has_unit
        and metrics.has_sample
        and metrics.has_roadmap
    )
    print(f"All Rung 2 rewrite criteria satisfied: {all_criteria_met}")


main()
