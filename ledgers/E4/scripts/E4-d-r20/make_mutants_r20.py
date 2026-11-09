"""Round-20 verifier: write three new student-error mutants of the E4 reference (each a complete solve_model module).

Each edit is a plausible student error that is outside the 1e-14 accuracy tolerance (ruling 25 is not engaged).
Usage: python3 make_mutants_r20.py <checkout-root>
"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
ref_text = (root / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")
out_dir = root / "ledgers/E4/mutants"


def edit(text, old, new):
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new)


# 1. Closed-form interior root with a sign slip in the denominator, used instead of bisection.
m1 = ref_text.replace('"""Reference solution', '"""Interior root taken from the closed form a sd sqrt(tb / (tau_e (tau_e + tb))): a sign slip in Proposition 4.\n\nReference solution', 1)
m1 = edit(m1, "        low, high = 0.0, 1.0  # invariant: the gap is positive at low (its limit, at 0) and negative at high\n        steps = 0\n        while high - low > BISECTION_TOLERANCE * high and steps < MAX_BISECTION_STEPS:\n            mid = 0.5 * (low + high)\n            if indifference_gap(mid, sd, cost) > 0.0:\n                low = mid\n            else:\n                high = mid\n            steps += 1\n        lam = 0.5 * (low + high)\n",
          "        tb = (TAU_V + TAU_E) * math.exp(-2.0 * RISK_AVERSION * cost) - TAU_V\n        lam = RISK_AVERSION * sd * math.sqrt(tb / (TAU_E * (TAU_E + tb)))\n")
# the variable names used above must exist in solve_model's scope
m1 = edit(m1, "    sd, cost = _check_inputs(noise_sd, info_cost)\n", "    sd, cost = _check_inputs(noise_sd, info_cost)\n    TAU_V, TAU_E = PRIOR_PRECISION, SIGNAL_PRECISION\n")
(out_dir / "mutant_d20_01_closed_form_root_denominator_sign_slip.py").write_text(m1, encoding="utf-8")

# 2. Reports the squared correlation of the payoff with the signal, not with the price.
m2 = ref_text.replace('"""Reference solution', '"""Reports Corr(v, s)^2 = tau_e / (tau_v + tau_e), the payoff-signal correlation, as the informativeness.\n\nReference solution', 1)
m2 = edit(m2, '        "price_informativeness": price_informativeness(lam, sd),',
          '        "price_informativeness": SIGNAL_PRECISION / (PRIOR_PRECISION + SIGNAL_PRECISION),')
(out_dir / "mutant_d20_02_informativeness_is_payoff_signal_correlation.py").write_text(m2, encoding="utf-8")

# 3. Uninformed conditional mean drops the price term: r = tau_y / (tau_v + tau_y), with no -b_s.
m3 = ref_text.replace('"""Reference solution', '"""Uninformed term drops the price slope: r = tau_y / (tau_v + tau_y) without subtracting b_s.\n\nReference solution', 1)
m3 = edit(m3, "    r = tau_y / (tau_v + tau_y) - b_s\n", "    r = tau_y / (tau_v + tau_y)\n")
(out_dir / "mutant_d20_03_uninformed_slope_drops_price_term.py").write_text(m3, encoding="utf-8")
print("written")
