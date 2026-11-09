"""Build the round-16 verifier mutants of the FC2 reference (run from the checkout root)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/FC/FC2/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/FC2/mutants"

HEADER_OLD = '"""Reference solution for the FC2 project: the arbitrage scanner (scanner.py).'

MUTANTS = {
    "r16_a_parity_explanation_names_P5_too.py": (
        "Parity explanation also names P5 (present-value quotes), which a parity finding does not list.",
        [("P3 no income, P4 the supplied", "P3 no income, P5 present-value quotes, P4 the supplied")],
    ),
    "r16_b_convexity_explanation_states_chord_rule_without_the_word.py": (
        "Convexity explanation names the rule as a chord test and never names convexity.",
        [('"convexity in strike (P1 European exercise, P2 one expiry, "', '"chord test on the strikes (P1 European exercise, P2 one expiry, "')],
    ),
    "r16_c_convexity_chord_weights_as_float_fractions.py": (
        "Convexity chord weights are float quotients passed to Fraction, so a tie at a half cent is not exact.",
        [
            ("w_low = Fraction(high - mid, high - low)", "w_low = Fraction((high - mid) / (high - low))"),
            ("w_high = Fraction(mid - low, high - low)", "w_high = Fraction((mid - low) / (high - low))"),
        ],
    ),
}

for name, (description, edits) in MUTANTS.items():
    text = REF
    for old, new in edits:
        assert text.count(old) == 1, (name, old, text.count(old))
        text = text.replace(old, new)
    assert text.count(HEADER_OLD) == 1, name
    header = (
        f'"""{description}\n\n'
        "Round-16 verifier mutant of the FC2 reference (grader/reference.py); otherwise identical.\n\n"
        "Reference solution for the FC2 project: the arbitrage scanner (scanner.py)."
    )
    text = text.replace(HEADER_OLD, header, 1)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
