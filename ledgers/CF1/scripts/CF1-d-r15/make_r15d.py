"""Write ten student-error mutants of the CF1 reference into ledgers/CF1/mutants (round 15, slice d).

Each mutant is the reference with one exact replacement; the script asserts that the replacement matches once.
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path("/Users/billyribeiro/dev/quant-phd")
REF = ROOT / "course/modules/CF/CF1/grader/reference.py"
OUT = ROOT / "ledgers/CF1/mutants"

MUTANTS: list[tuple[str, str, str, str]] = [
    (
        "r15d_01_irr_reports_interior_zero_samples",
        "A student reports every interior grid sample that is exactly zero as a root, on top of the sign changes.",
        "    # Only a sign change between two samples inside the window is reported.",
        "    for k in range(1, _GRID_POINTS - 1):\n"
        "        if values[k] == 0.0:\n"
        "            roots_x.append(xs[k])\n"
        "    # Only a sign change between two samples inside the window is reported.",
    ),
    (
        "r15d_02_payback_recovery_needs_strictly_positive",
        "A student counts a cumulative flow of exactly zero as not yet recovered (strict inequality in payback).",
        "        if cumulative + discounted[t] >= 0.0:",
        "        if cumulative + discounted[t] > 0.0:",
    ),
    (
        "r15d_03_payback_refuses_a_tiny_outlay",
        "A student refuses a first payback flow above -1e-6 cents, so an outlay of -1e-9 is wrongly refused.",
        "    if not flows[0] < 0:",
        "    if not flows[0] < -1e-6:",
    ),
    (
        "r15d_04_monte_carlo_refuses_zero_volatility",
        "A student treats zero volatility as an error (strict inequality on the volatility guard).",
        "    if not _finite(volatility) or volatility < 0.0:",
        "    if not _finite(volatility) or volatility <= 0.0:",
    ),
    (
        "r15d_05_monte_carlo_accepts_one_draw",
        "A student accepts a Monte Carlo request with one draw, which has no standard error.",
        "    if not isinstance(n_draws, int) or isinstance(n_draws, bool) or n_draws < 2:",
        "    if not isinstance(n_draws, int) or isinstance(n_draws, bool) or n_draws < 1:",
    ),
    (
        "r15d_06_working_capital_share_of_one_accepted",
        "A student accepts a working-capital share of exactly 100 percent (inclusive upper bound).",
        "    if not _finite(share) or not 0.0 <= share < 1.0:",
        "    if not _finite(share) or not 0.0 <= share <= 1.0:",
    ),
    (
        "r15d_07_zero_revenue_refused",
        "A student refuses a revenue of zero, which the specification names as valid.",
        "    if not all(_finite(x) and x >= 0 for x in revenue):",
        "    if not all(_finite(x) and x > 0 for x in revenue):",
    ),
    (
        "r15d_08_fisher_adds_the_two_rates",
        "A student uses the rule of thumb nominal = real + inflation instead of the exact Fisher form.",
        "    return (1.0 + real) * (1.0 + inflation) - 1.0",
        "    return real + inflation",
    ),
    (
        "r15d_09_npv_drops_the_outlay",
        "A student sums the discounted flows from t = 1, so the outlay at t = 0 is left out of the NPV.",
        "    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))",
        "    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows) if t > 0)",
    ),
    (
        "r15d_10_payback_in_whole_years",
        "A student returns payback in whole years by dropping the fraction of the recovery year.",
        "            return (t - 1) + (-cumulative) / discounted[t]",
        "            return float(t - 1)",
    ),
]


def main() -> None:
    base = REF.read_text(encoding="utf-8")
    head_end = base.index('"""', base.index('"""') + 3) + 3
    for name, description, old, new in MUTANTS:
        assert base.count(old) == 1, (name, base.count(old))
        text = base.replace(old, new, 1)
        text = f'"""{description}"""' + text[head_end:]
        (OUT / f"{name}.py").write_text(text, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
