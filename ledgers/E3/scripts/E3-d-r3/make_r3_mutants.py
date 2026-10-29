"""Write the round-3 student-error mutants of the E3 engine from the reference solution.

Each mutant is a complete module. Its docstring's first line describes the error; the rest of the module is the
reference with one edit (asserted to match exactly once, so no edit is silent).
"""
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
REF = (REPO / "course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
OUT = REPO / "ledgers/E3/mutants"

MUTANTS = {
    "r3_half_cent_truncated_toward_zero": (
        "Certainty equivalent rounded by truncation toward zero instead of half up, so 2.5 cents gives 2.",
        ("    return math.floor(y + 0.5)\n", "    return int(y)\n"),
    ),
    "r3_kappa_se_is_observed_information_not_inverted": (
        "Standard errors read from the observed information itself, not from its inverse (no inversion before the root).",
        (
            "    cov_diag: list[float] = []\n    for i in range(3):\n        unit = [1.0 if k == i else 0.0 for k in range(3)]\n        cov_diag.append(_solve(lower, unit)[i])\n",
            "    cov_diag: list[float] = [-hess[i][i] for i in range(3)]\n",
        ),
    ),
    "r3_mixed_check_counts_zero_probability_losses": (
        "Mixed-sign identification test counts a loss of probability zero as a loss, so a pure-gain design passes.",
        (
            "    gains = any(x > 0 and p > 0 for x, p in zip(prizes, probs, strict=True))\n    losses = any(x < 0 and p > 0 for x, p in zip(prizes, probs, strict=True))\n    return gains and losses\n\n\ndef _log1pexp",
            "    gains = any(x > 0 and p > 0 for x, p in zip(prizes, probs, strict=True))\n    losses = any(x < 0 for x in prizes)\n    return gains and losses\n\n\ndef _log1pexp",
        ),
    ),
    "r3_estimate_stops_at_grid_start": (
        "Estimate returns the best grid point without running the Newton search, so the score is not zero at the estimate.",
        ("    theta = _maximise(parsed)\n", "    theta = _grid_best(parsed)\n"),
    ),
}

GRID_BEST = '''

def _grid_best(parsed: list[Parsed]) -> list[float]:
    best_t: list[float] = [0.0, 0.0, 0.0]
    best_v = -math.inf
    for gamma in (0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95):
        for lam in (1.0, 1.5, 2.0, 3.0, 4.0, 6.0):
            for kappa in (0.5, 1.0, 2.0, 3.0, 5.0, 8.0):
                t = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]
                v = _objective(t, parsed)
                if v > best_v:
                    best_t, best_v = t, v
    return best_t
'''

for name, (desc, (old, new)) in MUTANTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    text = REF.replace(old, new)
    first, rest = text.split("\n", 1)
    # the module docstring's first line is replaced by the error description
    assert first.startswith('"""Reference solution'), first
    text = '"""' + desc + '\n' + rest
    if name == "r3_estimate_stops_at_grid_start":
        text = text.replace("\ndef estimate(", GRID_BEST + "\n\ndef estimate(", 1)
    (OUT / f"{name}.py").write_text(text, encoding="utf-8")
    print("wrote", name)
