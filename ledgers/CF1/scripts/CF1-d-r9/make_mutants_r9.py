"""Write round-9 student-error mutants of the CF1 reference (each edit must match exactly once)."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
REF = ROOT / "course/modules/CF/CF1/grader/reference.py"
OUT = ROOT / "ledgers/CF1/mutants"
src = REF.read_text(encoding="utf-8")
HEAD = '"""Reference solution for the CF1 capital-budgeting engine (capbudget.py).'
assert src.count(HEAD) == 1

EDITS = {
    "m48_volatility_taken_as_variance.py": (
        "A student reads volatility as a variance: the draw multiplier uses sqrt(volatility) as the standard deviation.",
        [("m = math.exp(volatility * z - volatility * volatility / 2.0)",
          "m = math.exp(math.sqrt(volatility) * z - volatility / 2.0)")],
    ),
    "m49_one_normal_reused_for_every_draw.py": (
        "The student draws one standard normal number and reuses it for every draw, so all draws are identical.",
        [("    rng = random.Random(seed)\n    out: list[float] = []\n    for _ in range(n_draws):\n        z = rng.gauss(0.0, 1.0)\n",
          "    rng = random.Random(seed)\n    out: list[float] = []\n    z = rng.gauss(0.0, 1.0)\n    for _ in range(n_draws):\n")],
    ),
    "m50_irr_returns_discount_factor.py": (
        "irr_roots reports the discount factor x = 1 / (1 + r) instead of the rate r.",
        [("return sorted(1.0 / x - 1.0 for x in roots_x)", "return sorted(roots_x)")],
    ),
    "m51_irr_grid_point_without_refinement.py": (
        "irr_roots reports the grid sample nearest the sign change and never bisects, so roots are only grid-accurate.",
        [("            roots_x.append(0.5 * (lo + hi))", "            roots_x.append(lo)")],
    ),
    "m52_depreciation_over_life_plus_one.py": (
        "Straight-line depreciation is spread over life + 1 years, an off-by-one in the schedule.",
        [("    depreciation = capex / life\n", "    depreciation = capex / (life + 1)\n")],
    ),
    "m53_discounted_payback_rate_as_percent.py": (
        "Discounted payback divides each flow by (1 + rate / 100) to the power t, reading the rate as a percentage.",
        [("    discounted = [cf / (1.0 + rate) ** t for t, cf in enumerate(flows)]",
          "    discounted = [cf / (1.0 + rate / 100.0) ** t for t, cf in enumerate(flows)]")],
    ),
}
for name, (desc, edits) in EDITS.items():
    text = src.replace(HEAD, '"""' + desc + "\n\nReference solution for the CF1 capital-budgeting engine (capbudget.py).", 1)
    for old, new in edits:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new, 1)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
