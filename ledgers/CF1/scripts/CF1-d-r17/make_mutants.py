"""Write four round-17 student-error mutants of the CF1 reference solution into ledgers/CF1/mutants/."""

import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/CF/CF1/grader/reference.py").read_text(encoding="utf-8")
ref = "from __future__" + ref.split("from __future__", 1)[1]
out = root / "ledgers/CF1/mutants"


def swap(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, old[:60]
    return text.replace(old, new)


mutants = {
    "r17_01_fisher_checks_only_the_real_rate.py": (
        "The student validates the real rate in fisher_nominal but not the inflation rate, so an inflation of -1 "
        "returns -1 instead of raising ValueError.",
        swap(ref, "    _check_rate(real)\n    _check_rate(inflation)\n", "    _check_rate(real)\n"),
    ),
    "r17_02_payback_zero_recovery_needs_strictly_positive_cumulative.py": (
        "The student tests recovery with a strict inequality, so a cumulative flow of exactly zero before the final "
        "year is not taken as payback.",
        swap(ref, "        if cumulative + discounted[t] >= 0.0:", "        if cumulative + discounted[t] > 0.0:"),
    ),
    "r17_03_irr_grid_evenly_spaced_in_discount_factor.py": (
        "The student spaces the IRR search grid evenly in the discount factor x, not in log x as the page specifies, "
        "so the window is sampled at intervals of about 2.5 in x.",
        swap(
            ref,
            """    xs = [
        math.exp(math.log(_X_LOW) + (math.log(_X_HIGH) - math.log(_X_LOW)) * k / (_GRID_POINTS - 1))
        for k in range(_GRID_POINTS)
    ]
""",
            """    xs = [_X_LOW + (_X_HIGH - _X_LOW) * k / (_GRID_POINTS - 1) for k in range(_GRID_POINTS)]
""",
        ),
    ),
    "r17_04_monte_carlo_correction_uses_volatility_not_its_square.py": (
        "The student writes the lognormal correction as volatility / 2 instead of volatility squared / 2, so E[m] is "
        "not one and the draws do not center on the deterministic NPV.",
        swap(
            ref,
            "        m = math.exp(volatility * z - volatility * volatility / 2.0)",
            "        m = math.exp(volatility * z - volatility / 2.0)",
        ),
    ),
}
for name, (desc, text) in mutants.items():
    body = f'"""{desc}"""\n' + text
    (out / name).write_text(body, encoding="utf-8")
    print("wrote", name)
