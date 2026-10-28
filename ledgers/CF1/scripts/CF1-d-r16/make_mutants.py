"""Write three round-16 student-error mutants of the CF1 reference solution into ledgers/CF1/mutants/."""

import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/CF/CF1/grader/reference.py").read_text(encoding="utf-8")
# Drop the reference module docstring so the one-line mutant docstring can precede the future import.
ref = "from __future__" + ref.split("from __future__", 1)[1]
out = root / "ledgers/CF1/mutants"


def swap(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, old[:60]
    return text.replace(old, new)


irr_block = """    xs = [
        math.exp(math.log(_X_LOW) + (math.log(_X_HIGH) - math.log(_X_LOW)) * k / (_GRID_POINTS - 1))
        for k in range(_GRID_POINTS)
    ]
    xs[0], xs[-1] = _X_LOW, _X_HIGH
"""
m1 = swap(
    ref,
    irr_block,
    """    xs = sorted(
        1.0 / (1.0 + (-0.9999 + (9999.0 + 0.9999) * k / (_GRID_POINTS - 1))) for k in range(_GRID_POINTS)
    )
""",
)
m1 = '"""The student spaces the IRR search grid evenly in the rate r, so the samples are not evenly spaced in log x as the page specifies."""\n' + m1

mc_old = """        z = rng.gauss(0.0, 1.0)
        m = math.exp(volatility * z - volatility * volatility / 2.0)
        scaled = dict(project)
        scaled["revenue"] = [m * float(x) for x in project["revenue"]]
"""
mc_new = """        scaled = dict(project)
        scaled["revenue"] = [
            math.exp(volatility * rng.gauss(0.0, 1.0) - volatility * volatility / 2.0) * float(x)
            for x in project["revenue"]
        ]
"""
m2 = swap(ref, mc_old, mc_new)
m2 = '"""The student draws one standard normal per year of revenue instead of one per draw, so the seeded stream is consumed in a different order."""\n' + m2

m3 = swap(
    ref,
    "    return sorted(1.0 / x - 1.0 for x in roots_x)",
    "    return sorted(round(1.0 / x - 1.0, 6) for x in roots_x)",
)
m3 = '"""The student rounds each IRR root to six decimals, so a root is no longer within the required 1e-7 of the true rate."""\n' + m3

for name, text in [
    ("r16_01_irr_grid_evenly_spaced_in_rate.py", m1),
    ("r16_02_monte_carlo_one_normal_per_revenue_year.py", m2),
    ("r16_03_irr_roots_rounded_to_six_decimals.py", m3),
]:
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name)
