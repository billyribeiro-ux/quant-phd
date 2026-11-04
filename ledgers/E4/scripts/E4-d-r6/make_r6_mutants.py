"""Write ten single-change student-error mutants of the E4 reference solver into ledgers/E4/mutants/.

Each mutant is reference.py with exactly one edit (the replacement must match exactly once). The first docstring line
of each mutant names the student error. Usage: python3 -I make_r6_mutants.py <WORKDIR>
"""

from __future__ import annotations

import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
ref = (root / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")
out_dir = root / "ledgers/E4/mutants"
HEAD = '"""Reference solution for the E4 project'

EDITS: list[tuple[str, str, str, str]] = [
    (
        "mutant_d6_01_zero_cost_rejected",
        "The cost check rejects a zero information cost, although the page accepts zero.",
        "if not (math.isfinite(cost) and cost >= 0.0):",
        "if not (math.isfinite(cost) and cost > 0.0):",
    ),
    (
        "mutant_d6_02_upper_boundary_reversed",
        "The upper boundary is reversed: the fraction is 1 when the gap at 1 is nonpositive.",
        "elif gap_1 >= 0.0:",
        "elif gap_1 <= 0.0:",
    ),
    (
        "mutant_d6_03_lower_boundary_reversed",
        "The lower boundary is reversed: the fraction is 0 when the gap at 0 is nonnegative.",
        "if gap_0 <= 0.0:",
        "if gap_0 >= 0.0:",
    ),
    (
        "mutant_d6_04_cost_sign_flipped_in_gap",
        "The information cost enters the gap with the wrong sign: exp(-a c) multiplies the informed term.",
        "return uninformed_term(lam, noise_sd) - math.exp(RISK_AVERSION * info_cost) * informed_term(lam, noise_sd)",
        "return uninformed_term(lam, noise_sd) - math.exp(-RISK_AVERSION * info_cost) * informed_term(lam, noise_sd)",
    ),
    (
        "mutant_d6_05_absolute_stop_1e-9",
        "The bisection stops at an absolute bracket width of 1e-9 instead of the relative width of 1e-12.",
        "while high - low > BISECTION_TOLERANCE * high and steps < MAX_BISECTION_STEPS:",
        "while high - low > 1e-9 and steps < MAX_BISECTION_STEPS:",
    ),
    (
        "mutant_d6_06_bracket_floor_1e-11",
        "The bracket starts at 1e-11, so a root below 1e-11 is reported as 1e-11.",
        "low, high = 0.0, 1.0  # invariant",
        "low, high = 1e-11, 1.0  # invariant",
    ),
    (
        "mutant_d6_07_noise_message_changed",
        "The message for a bad noise volume is '> 0', which lacks the text the page's table requires.",
        'raise ValueError("noise volume must be positive")',
        'raise ValueError("noise volume must be > 0")',
    ),
    (
        "mutant_d6_08_cost_message_changed",
        "The message for a negative cost says 'positive', which lacks the text the page's table requires.",
        'raise ValueError("information cost must be nonnegative")',
        'raise ValueError("information cost must be positive")',
    ),
    (
        "mutant_d6_09_noise_floor_1e-9",
        "Noise volumes below 1e-9 are rejected, although the page accepts every positive finite noise volume.",
        "if not (math.isfinite(sd) and sd > 0.0):",
        "if not (math.isfinite(sd) and sd > 1e-9):",
    ),
    (
        "mutant_d6_10_uninformed_variance_drops_price_noise",
        "The uninformed conditional variance of y ignores the price noise: Var(y) is taken as 1/tau_v.",
        "return math.pow(1.0 + r * r * (tau_v + tau_y) * (1.0 / tau_v + 1.0 / tau_y), -0.5)",
        "return math.pow(1.0 + r * r * (tau_v + tau_y) * (1.0 / tau_v), -0.5)",
    ),
]

for name, desc, old, new in EDITS:
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new, 1)
    assert body.count(HEAD) == 1
    body = body.replace(HEAD, f'"""{desc}\n\nBuilt from reference.py by one edit.\n\nReference solution', 1)
    (out_dir / f"{name}.py").write_text(body, encoding="utf-8")
    print("wrote", name)
