"""PC1 Lab L01-1: Section budget and first-number position check on a simulated paper outline.

SIMULATED. Outline and paragraph text are constructed models of an empirical finance paper.
All numbers are verified with exact fractions and integer counts. Standard library only.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class SectionEntry:
    title: str
    words: int
    target_fraction: Fraction


@dataclass(frozen=True)
class PaperOutline:
    sections: list[SectionEntry]

    @property
    def total_words(self) -> int:
        return sum(s.words for s in self.sections)


def check_section_budget(outline: PaperOutline) -> list[tuple[str, int, Fraction, Fraction]]:
    """Return each section with words, actual fraction, and target fraction."""
    total = outline.total_words
    results: list[tuple[str, int, Fraction, Fraction]] = []
    for s in outline.sections:
        actual = Fraction(s.words, total)
        results.append((s.title, s.words, actual, s.target_fraction))
    return results


def find_first_number_sentence(intro_text: str) -> tuple[int, str]:
    """Find the 1-based index and text of the first sentence containing an empirical digit."""
    # Split sentences on periods followed by whitespace
    sentences = [s.strip() for s in re.split(r"\.\s+", intro_text.strip()) if s.strip()]
    for idx, sentence in enumerate(sentences, start=1):
        if re.search(r"\d", sentence):
            return idx, sentence
    return 0, ""


def main() -> None:
    print("PC1 Lab L01-1: Section Budget and First-Number Position Check")
    print("SIMULATED outline and introduction text")

    # Canonical 6-section empirical finance paper structure (10,000 words total)
    sections = [
        SectionEntry("Introduction", 1000, Fraction(1, 10)),
        SectionEntry("Data and Sample Selection", 1500, Fraction(3, 20)),
        SectionEntry("Identification and Model", 2000, Fraction(1, 5)),
        SectionEntry("Core Empirical Results", 3000, Fraction(3, 10)),
        SectionEntry("Robustness and Mechanisms", 2000, Fraction(1, 5)),
        SectionEntry("Conclusion", 500, Fraction(1, 20)),
    ]
    outline = PaperOutline(sections)

    print(f"Total word count: {outline.total_words}")
    budget_checks = check_section_budget(outline)
    all_matched = True
    for title, words, actual, target in budget_checks:
        pct_actual = float(actual) * 100
        pct_target = float(target) * 100
        matched = actual == target
        if not matched:
            all_matched = False
        print(
            f"  {title:30s} | Words: {words:5d} | Actual: {pct_actual:5.1f}% "
            f"({actual}) | Target: {pct_target:5.1f}% ({target}) | Match: {matched}"
        )

    print(f"All section budget shares match targets: {all_matched}")

    # Simulated introduction text
    simulated_intro = (
        "We show that institutional cross-ownership increases five-year physical investment by 14 basis points\n"
        "per standard deviation increase in common ownership across United States manufacturing firms from 1990 to "
        "2020.\n"
        "This effect is concentrated in industries with high product market overlap and persists after instrumenting\n"
        "for ownership using financial institution mergers.\n"
        "In contrast to theories of unilateral market power, the investment response reflects coordinated capital\n"
        "expenditure reductions in duplicate facilities.\n"
        "The remainder of this paper details the sample selection, empirical identification, primary regression "
        "results,\n"
        "battery of robustness checks, and concluding implications for antitrust regulation."
    )

    sent_idx, sent_text = find_first_number_sentence(simulated_intro)
    # Normalize newline to single space for clean display
    clean_sent = " ".join(sent_text.split())
    print(f"First empirical number occurs in sentence: {sent_idx}")
    print(f"First number sentence: {clean_sent}")
    first_sentence_rule = sent_idx == 1
    print(f"First-sentence result requirement satisfied: {first_sentence_rule}")


main()
