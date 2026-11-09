"""Build the round-17 verifier mutants of the FC2 reference (run from the checkout root)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/FC/FC2/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/FC2/mutants"

HEADER_OLD = '"""Reference solution for the FC2 project: the arbitrage scanner (scanner.py).'

MUTANTS = {
    "r17_a_convexity_one_strike_returns_before_validation.py": (
        "Convexity returns no violation for a one-strike chain before it checks df_ppm or the strikes.",
        [
            (
                "    _check_df(df_ppm)\n    _check_strikes(strikes_cents)\n    _check_lengths(strikes_cents, calls_cents, None)\n"
                "    return [j for j in range(1, len(strikes_cents) - 1)",
                "    if len(strikes_cents) < 2:\n        return []\n"
                "    _check_df(df_ppm)\n    _check_strikes(strikes_cents)\n    _check_lengths(strikes_cents, calls_cents, None)\n"
                "    return [j for j in range(1, len(strikes_cents) - 1)",
            ),
        ],
    ),
    "r17_c_convexity_skips_length_check_for_one_strike.py": (
        "Convexity checks the quote count only when the chain has at least two strikes.",
        [
            (
                "    _check_lengths(strikes_cents, calls_cents, None)\n    return [j",
                "    if len(strikes_cents) > 1:\n        _check_lengths(strikes_cents, calls_cents, None)\n    return [j",
            ),
        ],
    ),
}

for name, (description, edits) in MUTANTS.items():
    text = REF
    for old, new in edits:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    assert text.count(HEADER_OLD) == 1, name
    header = (
        f'"""{description}\n\n'
        "Round-17 verifier mutant of the FC2 reference (grader/reference.py); otherwise identical.\n\n"
        "Reference solution for the FC2 project: the arbitrage scanner (scanner.py)."
    )
    text = text.replace(HEADER_OLD, header, 1)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)


# Round-17 addition: a plain-float convexity computation (no Fraction anywhere in the chord or its rounding).
FLOAT_CHORD = {
    "r17_d_convexity_chord_and_gross_in_plain_float.py": (
        "Convexity chord and its gross are computed in plain float arithmetic, not in exact fractions.",
        [
            (
                "    low, mid, high = strikes[j - 1], strikes[j], strikes[j + 1]\n"
                "    w_low = Fraction(high - mid, high - low)\n"
                "    w_high = Fraction(mid - low, high - low)\n"
                "    return w_low * calls[j - 1] + w_high * calls[j + 1] - calls[j]",
                "    low, mid, high = strikes[j - 1], strikes[j], strikes[j + 1]\n"
                "    w_low = (high - mid) / (high - low)\n"
                "    w_high = (mid - low) / (high - low)\n"
                "    return w_low * calls[j - 1] + w_high * calls[j + 1] - calls[j]",
            ),
            (
                "        gross = _half_up(-_second_difference(strikes, calls, j))",
                "        gross = int((-_second_difference(strikes, calls, j) + 0.5) // 1)",
            ),
        ],
    ),
}

for name, (description, edits) in FLOAT_CHORD.items():
    text = REF
    for old, new in edits:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    assert text.count(HEADER_OLD) == 1, name
    header = (
        f'"""{description}\n\n'
        "Round-17 verifier mutant of the FC2 reference (grader/reference.py); otherwise identical.\n\n"
        "Reference solution for the FC2 project: the arbitrage scanner (scanner.py)."
    )
    text = text.replace(HEADER_OLD, header, 1)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)


# Round-17 addition: a plain-float parity computation (no Fraction in the gap or its rounding).
PLAIN_PARITY = {
    "r17_e_parity_gap_in_plain_float.py": (
        "Parity gap and its gross are computed in plain float arithmetic, not in exact fractions.",
        [
            (
                "    gap = Fraction(call_cents) - Fraction(put_cents) - (Fraction(spot_cents) - Fraction(strike_cents * df_ppm, PPM))\n    return _half_up(gap)",
                "    gap = call_cents - put_cents - (spot_cents - strike_cents * (df_ppm / PPM))\n    return int((gap + 0.5) // 1)",
            ),
        ],
    ),
}

for name, (description, edits) in PLAIN_PARITY.items():
    text = REF
    for old, new in edits:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    assert text.count(HEADER_OLD) == 1, name
    header = (
        f'"""{description}\n\n'
        "Round-17 verifier mutant of the FC2 reference (grader/reference.py); otherwise identical.\n\n"
        "Reference solution for the FC2 project: the arbitrage scanner (scanner.py)."
    )
    text = text.replace(HEADER_OLD, header, 1)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
