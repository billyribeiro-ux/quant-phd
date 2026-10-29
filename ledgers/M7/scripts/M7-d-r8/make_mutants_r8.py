"""Write the round-8 verifier mutants from the alt_nullspace solver; each replacement must match exactly once."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
BASE = (ROOT / "ledgers/M7/scripts/M7-d-r8/alt/alt_nullspace.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M7/mutants"
FIRST = '"""Alternative A2 for the M7 project suite: the exact active-set method, with a null-space step.'
MUTANTS = {
    "r8_m01_start_sum_checked_one_sided.py": (
        "Student error r8m01: the starting-sum check refuses only a sum above one, so a start 2e-9 below one is accepted.",
        ("    if abs(sum(w0, Fraction(0)) - 1) > TOL:", "    if sum(w0, Fraction(0)) - 1 > TOL:"),
    ),
    "r8_m02_equal_bounds_refused_as_out_of_order.py": (
        "Student error r8m02: a lower bound equal to its upper bound is refused as out of order, so the boundary is rejected.",
        ("    if any(lower[i] > upper[i] for i in range(n)):", "    if any(lower[i] >= upper[i] for i in range(n)):"),
    ),
    "r8_m03_weights_rounded_to_six_places.py": (
        "Student error r8m03: the returned weights are rounded to six decimals, so the stationarity residual is about 1e-7.",
        ('        "weights": [float(v) for v in sol["w"]],', '        "weights": [round(float(v), 6) for v in sol["w"]],'),
    ),
    "r8_m04_turnover_measured_from_zero.py": (
        "Student error r8m04: the turnover rows measure the change from zero (sum of signed weights at most tau), not from w0.",
        ("        rows.append((a, problem.tau + _dot(a, problem.w0), (\"turn\", signs)))", "        rows.append((a, problem.tau, (\"turn\", signs)))"),
    ),
    "r8_m05_sector_cap_applied_per_asset.py": (
        "Student error r8m05: each sector cap is applied to every asset of the sector separately, not to the sector sum.",
        (
            '    for k, cap in enumerate(problem.caps):\n        rows.append(([Fraction(1) if problem.sector[j] == k else Fraction(0) for j in range(n)], cap, ("sector", k)))',
            '    for k, cap in enumerate(problem.caps):\n        for i in range(n):\n            if problem.sector[i] == k:\n                rows.append(([Fraction(1) if j == i else Fraction(0) for j in range(n)], cap, ("sector", k)))',
        ),
    ),
    "r8_m06_zero_risk_aversion_accepted.py": (
        "Student error r8m06: a risk aversion of exactly zero is accepted, although the page requires gamma to be positive.",
        ("    if gamma <= 0:", "    if gamma < 0:"),
    ),
}
for name, (doc, (old, new)) in MUTANTS.items():
    assert BASE.count(old) == 1, (name, BASE.count(old))
    text = BASE.replace(old, new, 1)
    assert text.count(FIRST) == 1, name
    text = text.replace(FIRST, '"""' + doc, 1)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
