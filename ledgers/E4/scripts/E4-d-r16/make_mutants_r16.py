"""Write four new student-error mutants of the E4 reference (round 16 verifier).

Each mutant is grader/reference.py with exactly one replaced block; the script asserts each old block occurs once.
Usage: python -I make_mutants_r16.py <checkout-root>
"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")
out_dir = root / "ledgers/E4/mutants"

MUTANTS = [
    (
        "mutant_v16_01_boundary_zero_uses_exp_minus_ac_threshold.py",
        "Boundary at zero decided by the sign of (tau_v + tau_e) exp(-a c) - tau_v, a cost factor with a once, not the gap at 0.",
        "    if gap_0 <= 0.0:\n        lam = 0.0\n",
        "    if (PRIOR_PRECISION + SIGNAL_PRECISION) * math.exp(-RISK_AVERSION * cost) - PRIOR_PRECISION <= 0.0:\n"
        "        lam = 0.0\n",
    ),
    (
        "mutant_v16_02_uninformed_term_reads_price_precision_at_one.py",
        "Uninformed term reads the price precision at informed fraction 1 for every fraction, as if the price were fully revealing.",
        "    b_s, _, tau_y = price_coefficients(lam, noise_sd)\n    r = tau_y / (tau_v + tau_y) - b_s\n",
        "    b_s, _, tau_y = price_coefficients(lam, noise_sd)\n    tau_y = price_precision(1.0, noise_sd)\n"
        "    r = tau_y / (tau_v + tau_y) - b_s\n",
    ),
    (
        "mutant_v16_03_unit_informativeness_uses_noise_volume_once.py",
        "Informativeness at informed fraction 1 uses the noise volume once, not squared, in the price precision.",
        "    tau_y = price_precision(lam, noise_sd)\n    return tau_y / (PRIOR_PRECISION + tau_y)\n",
        "    tau_y = price_precision(lam, noise_sd)\n"
        "    if lam == 1.0:\n"
        "        tau_y = lam * lam * SIGNAL_PRECISION * SIGNAL_PRECISION / (lam * lam * SIGNAL_PRECISION + RISK_AVERSION**2 * noise_sd)\n"
        "    return tau_y / (PRIOR_PRECISION + tau_y)\n",
    ),
    (
        "mutant_v16_04_informed_slope_uses_uninformed_precision.py",
        "Informed slope uses the uninformed posterior precision tau_v + tau_y where the informed precision tau_v + tau_e belongs.",
        "    slope = tau_e / precision - b_s\n",
        "    slope = tau_e / (tau_v + price_precision(lam, noise_sd)) - b_s\n",
    ),
]

for name, doc, old, new in MUTANTS:
    assert ref.count(old) == 1, (name, ref.count(old))
    text = ref.replace(old, new, 1)
    body = text.split('"""', 2)[2]  # keep everything after the module docstring
    header = f'"""{doc}\n\nSingle-change copy of grader/reference.py (verifier round 16). Original docstring follows.\n'
    original_doc = text.split('"""', 2)[1]
    out = header + original_doc + '"""' + body
    (out_dir / name).write_text(out, encoding="utf-8")
    print("wrote", name)
