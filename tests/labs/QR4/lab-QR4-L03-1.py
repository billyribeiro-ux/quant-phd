"""Lab QR4-L03-1: Financial Domain Lexicons vs General Dictionaries (Loughran-McDonald 2011).

Demonstrates why general-purpose sentiment dictionaries (such as Harvard IV-4) fail in finance
by misclassifying standard business accounting terms as negative, whereas the domain-specific
Loughran & McDonald (2011) financial lexicon isolates genuine operational distress.
"""

from __future__ import annotations

import re


def tokenize(text: str) -> list[str]:
    """Tokenize text into lowercase alphabetic words."""
    return re.findall(r"\b[a-z]{2,}\b", text.lower())


def score_sentiment(
    tokens: list[str],
    pos_words: set[str],
    neg_words: set[str],
) -> dict[str, float]:
    """Score sentiment tone: net = (pos - neg) / total_tokens."""
    total = len(tokens)
    if total == 0:
        return {"pos_count": 0.0, "neg_count": 0.0, "net_tone": 0.0, "polarity": 0.0}

    pos_count = sum(1 for t in tokens if t in pos_words)
    neg_count = sum(1 for t in tokens if t in neg_words)
    net_tone = (pos_count - neg_count) / float(total)
    polarity = (pos_count - neg_count) / float(pos_count + neg_count) if (pos_count + neg_count) > 0 else 0.0

    return {
        "pos_count": float(pos_count),
        "neg_count": float(neg_count),
        "net_tone": float(net_tone),
        "polarity": float(polarity),
    }


def main() -> None:
    # Loughran-McDonald (2011) financial domain word sets (representative subsets)
    lm_positive = {"gain", "profitable", "exceeded", "strong", "improved", "expansion", "growth"}
    lm_negative = {"loss", "default", "restructuring", "impairment", "litigation", "adverse", "recession", "breach"}

    # Harvard-IV-4 / General Inquirer general dictionary (contains ordinary accounting nouns as negative)
    # Harvard IV-4 notoriously classifies 'tax', 'cost', 'liability', 'foreign', 'depreciation' as negative.
    gi_positive = {"gain", "profitable", "exceeded", "strong", "improved", "expansion", "growth", "share"}
    gi_negative = {
        "loss",
        "default",
        "restructuring",
        "impairment",
        "litigation",
        "adverse",
        "recession",
        "breach",
        "liability",
        "cost",
        "tax",
        "depreciation",
        "expense",
        "board",
    }

    # Two 10-K disclosures:
    # Doc A: Normal healthy balance sheet description with routine accounting terminology
    doc_a = (
        "Total liabilities increased due to deferred tax obligations and routine cost of goods sold. "
        "Depreciation expense remained steady as the board approved the annual capital allocation. "
        "Operating growth and profitable expansion exceeded our previous multi-year guidance."
    )

    # Doc B: Genuinely distressed filing describing default, breach, and litigation
    doc_b = (
        "The company incurred severe operating loss and remains in breach of debt covenants. "
        "Adverse macroeconomic headwinds prompted restructuring and asset impairment charges. "
        "Ongoing litigation poses material risk of accelerated default."
    )

    tokens_a = tokenize(doc_a)
    tokens_b = tokenize(doc_b)

    lm_a = score_sentiment(tokens_a, lm_positive, lm_negative)
    gi_a = score_sentiment(tokens_a, gi_positive, gi_negative)

    lm_b = score_sentiment(tokens_b, lm_positive, lm_negative)
    gi_b = score_sentiment(tokens_b, gi_positive, gi_negative)

    print("--- Document A: Healthy 10-K Balance Sheet Description ---")
    print(f"Total tokens: {len(tokens_a)}")
    print(
        f"Loughran-McDonald (2011): Pos={lm_a['pos_count']:.0f}, Neg={lm_a['neg_count']:.0f} | "
        f"Tone={lm_a['net_tone']:+.4f} | Polarity={lm_a['polarity']:+.2f}"
    )
    print(
        f"General Inquirer (Harvard): Pos={gi_a['pos_count']:.0f}, Neg={gi_a['neg_count']:.0f} | "
        f"Tone={gi_a['net_tone']:+.4f} | Polarity={gi_a['polarity']:+.2f}"
    )

    print("\n--- Document B: Material Distress Disclosure ---")
    print(f"Total tokens: {len(tokens_b)}")
    print(
        f"Loughran-McDonald (2011): Pos={lm_b['pos_count']:.0f}, Neg={lm_b['neg_count']:.0f} | "
        f"Tone={lm_b['net_tone']:+.4f} | Polarity={lm_b['polarity']:+.2f}"
    )
    print(
        f"General Inquirer (Harvard): Pos={gi_b['pos_count']:.0f}, Neg={gi_b['neg_count']:.0f} | "
        f"Tone={gi_b['net_tone']:+.4f} | Polarity={gi_b['polarity']:+.2f}"
    )

    # Accounting term false-negative analysis
    accounting_words = ["liability", "tax", "cost", "depreciation", "expense", "board"]
    misclassified = [w for w in accounting_words if w in gi_negative and w not in lm_negative]
    print(f"\nRoutine accounting words misclassified as negative by General Inquirer: {misclassified}")
    print(
        "Verification Invariant: LM classifies healthy disclosure as net positive; "
        "Harvard misclassifies it as net negative."
    )


main()
