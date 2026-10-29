"""Write the round-24 student-error mutants of the CF1 reference engine into ledgers/CF1/mutants/ (each edit must match once)."""
import pathlib
ROOT = pathlib.Path("/tmp/verify24-CF1-d")
REF = (ROOT / "course/modules/CF/CF1/grader/reference.py").read_text(encoding="utf-8")
MUTANTS = {
    "v24d_01_last_year_working_capital_not_recovered.py": (
        "        working_capital = -(nwc[t] - nwc[t - 1])\n",
        "        working_capital = -(nwc[t] - nwc[t - 1]) if t < life else 0.0\n",
        "v24d_01: the working capital is never recovered: the year-life working-capital flow is zero (Convention 'Working capital').",
    ),
    "v24d_02_monte_carlo_fresh_generator_each_draw.py": (
        "        z = rng.gauss(0.0, 1.0)\n",
        "        z = random.Random(seed).gauss(0.0, 1.0)\n",
        "v24d_02: a new generator is seeded inside the loop, so every draw is the same number.",
    ),
    "v24d_03_monte_carlo_normalvariate_not_gauss.py": (
        "        z = rng.gauss(0.0, 1.0)\n",
        "        z = rng.normalvariate(0.0, 1.0)\n",
        "v24d_03: the standard normal is drawn with normalvariate, not gauss, so the stated draw method is not followed.",
    ),
    "v24d_04_irr_root_left_grid_point_not_refined.py": (
        "            roots_x.append(0.5 * (lo + hi))\n",
        "            roots_x.append(xs[k1])\n",
        "v24d_04: the IRR root is reported at the left grid point of the sign-change bracket, with no bisection.",
    ),
    "v24d_05_npv_discounts_outlay_one_period.py": (
        "    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))\n",
        "    return sum(cf / (1.0 + rate) ** (t + 1) for t, cf in enumerate(flows))\n",
        "v24d_05: npv discounts every flow one period too far, including the outlay at t = 0.",
    ),
}
for name, (old, new, desc) in MUTANTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    text = REF.replace(old, new)
    body = f'"""{desc}\n\nMutant of the reference solution for the CF1 capital-budgeting engine (capbudget.py).\n"""\n'
    out = ROOT / "ledgers/CF1/mutants" / name
    out.write_text(body + text.split('"""', 2)[2], encoding="utf-8")
    print("wrote", name)
