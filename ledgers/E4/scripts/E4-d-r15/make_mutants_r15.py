"""Round-15 verifier mutants: single-change copies of grader/reference.py (VERIFIER section 2.6 item 3).

Each mutant's first docstring line names the student error. Each replacement must occur exactly once.
Usage: python -I make_mutants_r15.py   (writes ledgers/E4/mutants/mutant_r15_*.py)
"""
from pathlib import Path

ROOT = Path(".")
SRC = (ROOT / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/E4/mutants"

MUTANTS = {
    "mutant_r15_01_noise_coefficient_forgets_informed_fraction.py": (
        "Noise coefficient of the price taken as -a b_s / tau_e, forgetting the informed fraction lambda.",
        "    b_u = -RISK_AVERSION * b_s / (lam * tau_e)\n",
        "    b_u = -RISK_AVERSION * b_s / tau_e\n",
    ),
    "mutant_r15_02_signal_variance_is_posterior_variance.py": (
        "Informed term uses the posterior variance 1/(tau_v + tau_e) where the signal variance 1/tau_v + 1/tau_e belongs.",
        "    var_signal = 1.0 / tau_v + 1.0 / tau_e\n",
        "    var_signal = 1.0 / (tau_v + tau_e)\n",
    ),
    "mutant_r15_03_gap_at_zero_power_minus_one.py": (
        "Gap at fraction 0 raises the informed Gaussian term to the power -1 instead of -1/2.",
        "    informed = math.pow(1.0 + tau_e / tau_v + (tau_v + tau_e) * a2 / (tau_v * tau_v), -0.5)\n",
        "    informed = math.pow(1.0 + tau_e / tau_v + (tau_v + tau_e) * a2 / (tau_v * tau_v), -1.0)\n",
    ),
    "mutant_r15_04_bracket_starts_at_half.py": (
        "Bisection starts from the bracket [0, 0.5], so a root in (0.5, 1) is never bracketed.",
        "        low, high = 0.0, 1.0  # invariant",
        "        low, high = 0.0, 0.5  # invariant",
    ),
}

for name, (error, old, new) in MUTANTS.items():
    assert SRC.count(old) == 1, (name, SRC.count(old))
    text = SRC.replace(old, new, 1)
    first, rest = text.split("\n", 1)
    assert first.startswith('"""Reference solution for the E4 project'), first[:60]
    doc_rest = first[len('"""'):]
    body = f'"""{error}\n\nSingle-change copy of grader/reference.py (verifier round 15). Original docstring:\n{doc_rest}\n{rest}'
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)
