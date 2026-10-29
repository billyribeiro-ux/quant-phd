"""Round-4 verifier student-error mutants of the FC2 reference scanner (one change each)."""
import pathlib
import sys

REF = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
OUT = pathlib.Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

MUTANTS = {
    "n01_convexity_explanation_omits_P6": (
        "Convexity explanation omits the cost label P6 that every cost depends on.",
        [("f\"the chord weights; net {net} cents after {LEGS_PER_FINDING} legs at fee {fee} plus half-spread {spread} (P6).\"",
          "f\"the chord weights; net {net} cents after {LEGS_PER_FINDING} legs at fee {fee} plus half-spread {spread}.\"")],
    ),
    "n02_parity_strike_divided_by_df": (
        "Parity gap discounts the strike by dividing by the discount factor instead of multiplying.",
        [("        gap = Fraction(calls[k]) - Fraction(puts[k]) - (Fraction(spot) - Fraction(strike * df_ppm, PPM))\n",
          "        gap = Fraction(calls[k]) - Fraction(puts[k]) - (Fraction(spot) - Fraction(strike * PPM, df_ppm))\n")],
    ),
    "n03_negative_parity_gaps_skipped": (
        "Negative parity gaps are skipped, so only calls rich to the synthetic forward are reported.",
        [("        gross = _half_up(abs(gap))\n", "        if gap < 0:\n            continue\n        gross = _half_up(abs(gap))\n")],
    ),
    "n04_convexity_charged_one_leg_less": (
        "Convexity net charges two legs instead of three, so a finding one cost-leg too rich is kept.",
        [("        gross = _half_up(-_second_difference(strikes, calls, j))\n        net = gross - per_finding\n",
          "        gross = _half_up(-_second_difference(strikes, calls, j))\n        net = gross - (per_finding - spread)\n")],
    ),
    "n05_findings_sorted_by_net_descending": (
        "Findings returned sorted by net amount, largest first, instead of parity then convexity in strike order.",
        [("    return findings\n", "    return sorted(findings, key=lambda record: -record[\"net_cents\"])\n")],
    ),
}

for name, (doc, pairs) in MUTANTS.items():
    src = REF
    for old, new in pairs:
        assert src.count(old) == 1, (name, old[:60], src.count(old))
        src = src.replace(old, new)
    header = f'"""{doc}\n\nMutant of the reference scanner: one change, everything else as in reference.py.\n"""\n'
    body = src.split('"""', 2)[2]
    (OUT / f"{name}.py").write_text(header + body, encoding="utf-8")
    print("wrote", name)
