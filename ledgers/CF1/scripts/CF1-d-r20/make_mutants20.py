"""Round 20 new student-error mutants of the CF1 engine, derived from the reference by exact text replacement."""
import pathlib
import sys

REF = pathlib.Path("/tmp/verify20-CF1-d/course/modules/CF/CF1/grader/reference.py")
OUT = pathlib.Path("/tmp/verify20-CF1-d/ledgers/CF1/mutants")
src = REF.read_text()

MUTANTS = {
    "r20d_01_payback_discounted_fraction_uses_undiscounted_flow.py": (
        "A discounted payback accumulates discounted flows but divides the fraction by the undiscounted flow at year t.",
        [("            return (t - 1) + (-cumulative) / discounted[t]", "            return (t - 1) + (-cumulative) / flows[t]")],
    ),
    "r20d_02_irr_grid_evenly_spaced_in_x.py": (
        "The IRR scan places its 4,001 samples evenly in the discount factor x, not evenly in log x, so the samples are 2.5 apart.",
        [
            (
                "        math.exp(math.log(_X_LOW) + (math.log(_X_HIGH) - math.log(_X_LOW)) * k / (_GRID_POINTS - 1))\n        for k in range(_GRID_POINTS)",
                "        _X_LOW + (_X_HIGH - _X_LOW) * k / (_GRID_POINTS - 1)\n        for k in range(_GRID_POINTS)",
            )
        ],
    ),
    "r20d_03_irr_refuses_flows_that_sum_to_zero.py": (
        "An IRR request whose flows sum to zero, such as -100 and 100, is refused: the all-zero test is written as a sum test.",
        [
            (
                "    if all(cf == 0 for cf in flows):",
                "    if sum(flows) == 0:",
            )
        ],
    ),
    "r20d_04_monte_carlo_one_gauss_per_year_not_per_draw.py": (
        "A Monte Carlo draw takes one standard normal per year of life instead of one per draw, so the draws do not follow the specified stream.",
        [
            (
                "        z = rng.gauss(0.0, 1.0)\n        m = math.exp(volatility * z - volatility * volatility / 2.0)\n        scaled = dict(project)\n        scaled[\"revenue\"] = [m * float(x) for x in project[\"revenue\"]]",
                "        scaled = dict(project)\n        ms = []\n        for _year in project[\"revenue\"]:\n            z = rng.gauss(0.0, 1.0)\n            ms.append(math.exp(volatility * z - volatility * volatility / 2.0))\n        scaled[\"revenue\"] = [m * float(x) for m, x in zip(ms, project[\"revenue\"], strict=True)]",
            )
        ],
    ),
    "r20d_05_working_capital_balance_uses_next_years_revenue.py": (
        "The working-capital balance at the end of year t is set from the revenue of year t+1 instead of year t.",
        [
            (
                "    for t in range(1, life):\n        nwc[t] = share * revenue[t - 1]",
                "    for t in range(1, life):\n        nwc[t] = share * revenue[t]",
            )
        ],
    ),
    "r20d_06_monte_carlo_scales_cash_costs_too.py": (
        "A Monte Carlo draw multiplies cash costs by the same multiplier as revenue, so the operating line scales with m.",
        [
            (
                "        scaled[\"revenue\"] = [m * float(x) for x in project[\"revenue\"]]\n",
                "        scaled[\"revenue\"] = [m * float(x) for x in project[\"revenue\"]]\n        scaled[\"cash_costs\"] = [m * float(x) for x in project[\"cash_costs\"]]\n",
            )
        ],
    ),
    "r20d_07_monte_carlo_multiplier_without_mean_one_correction.py": (
        "A Monte Carlo multiplier is exp(volatility * z) with no correction, so its mean is exp(volatility squared / 2), not one.",
        [
            (
                "        m = math.exp(volatility * z - volatility * volatility / 2.0)\n        scaled",
                "        m = math.exp(volatility * z)\n        scaled",
            )
        ],
    ),
}

for name, (doc, edits) in MUTANTS.items():
    text = src
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            sys.exit(f"{name}: expected one occurrence, found {n}")
        text = text.replace(old, new)
    body = text.split('"""', 2)[2]
    (OUT / name).write_text(f'"""{doc}"""' + body)
    print("wrote", name)
