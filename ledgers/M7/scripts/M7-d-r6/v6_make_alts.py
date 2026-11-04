"""Round 6 (M7-d): write the five alternative correct allocators from the template (verifier scratch, stdlib only)."""

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = (HERE / "v6_alt_template.txt").read_text(encoding="utf-8")
ALTS = {
    "alt1_exact_tight_most_negative": dict(
        DOC="Alternative 1: exact rational active set, start from the constraints tight at w0, drop the most negative multiplier.",
        EXACT="True", TOL_SLACK="1e-9", TOL_MULT="0.0", ZERO="0.0", START="tight", DROP="most_negative"),
    "alt2_exact_empty_last_added": dict(
        DOC="Alternative 2: exact rational active set, start with no working constraints, drop the latest-added negative multiplier.",
        EXACT="True", TOL_SLACK="0.0", TOL_MULT="0.0", ZERO="0.0", START="empty", DROP="last_added"),
    "alt3_float_tight_1e-12": dict(
        DOC="Alternative 3: float active set with cutoffs 1e-12 on slacks, multipliers and pivots, start tight at w0.",
        EXACT="False", TOL_SLACK="1e-12", TOL_MULT="1e-12", ZERO="1e-12", START="tight", DROP="most_negative"),
    "alt4_float_loose_1e-10": dict(
        DOC="Alternative 4: float active set with looser cutoffs of 1e-10 (a multiplier down to -1e-10 counts as zero), start tight.",
        EXACT="False", TOL_SLACK="1e-10", TOL_MULT="1e-10", ZERO="1e-10", START="tight", DROP="most_negative"),
    "alt5_float_empty_last_added": dict(
        DOC="Alternative 5: float active set, start with no working constraints, cutoffs 1e-13, drop the latest-added negative.",
        EXACT="False", TOL_SLACK="1e-13", TOL_MULT="1e-13", ZERO="1e-13", START="empty", DROP="last_added"),
}
out = HERE / "v6_alts"
out.mkdir(exist_ok=True)
for name, params in ALTS.items():
    text = TEMPLATE
    for key, value in params.items():
        text = text.replace(f"__{key}__", value)
    import re
    assert not re.search(r"__[A-Z_]+__", text), name
    (out / f"{name}.py").write_text(text, encoding="utf-8")
    print("wrote", out / f"{name}.py")
