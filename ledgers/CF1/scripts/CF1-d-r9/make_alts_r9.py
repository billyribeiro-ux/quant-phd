"""Write round-9 alternative correct engines (different numerics and algorithms) from the reference."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
SRC = (ROOT / "course/modules/CF/CF1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/CF1/scripts/CF1-d-r9/alts"
EDITS = {
    "alt_r9_1_irr_finer_grid_tighter_bisection.py": [
        ("_GRID_POINTS = 4001", "_GRID_POINTS = 30001"),
        ("if hi - lo <= 1e-15 * hi:", "if hi - lo <= 1e-13 * hi:"),
    ],
    "alt_r9_2_payback_discount_by_multiplication.py": [
        ("discounted = [cf / (1.0 + rate) ** t for t, cf in enumerate(flows)]",
         "discounted = [cf * (1.0 + rate) ** (-t) for t, cf in enumerate(flows)]"),
    ],
    "alt_r9_3_fisher_by_log_identity.py": [
        ("    return (1.0 + real) * (1.0 + inflation) - 1.0",
         "    return math.expm1(math.log1p(real) + math.log1p(inflation))"),
    ],
    "alt_r9_4_npv_horner_and_mc_ratio_multiplier.py": [
        ("    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))",
         "    total = 0.0\n    for cf in reversed(flows):\n        total = total / (1.0 + rate) + cf\n    return total"),
        ("m = math.exp(volatility * z - volatility * volatility / 2.0)",
         "m = math.exp(volatility * z) / math.exp(volatility * volatility / 2.0)"),
    ],
}
OUT.mkdir(parents=True, exist_ok=True)
for name, edits in EDITS.items():
    text = SRC
    for old, new in edits:
        assert text.count(old) == 1, (name, old[:50], text.count(old))
        text = text.replace(old, new, 1)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
