"""Write the round-12 student-error mutants of grader/reference.py into ledgers/E4/mutants/ (one replacement each, asserted unique)."""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/E4/mutants"

DOC_OLD = REF[: REF.index('"""', 3) + 3]
MUTANTS = {
    "mutant_r12_01_informed_cost_factor_squared.py": (
        "Informed cost enters the gap as exp(2 a c), the cost counted twice in the exponent.",
        "    return uninformed_term(lam, noise_sd) - math.exp(RISK_AVERSION * info_cost) * informed_term(lam, noise_sd)",
        "    return uninformed_term(lam, noise_sd) - math.exp(2.0 * RISK_AVERSION * info_cost) * informed_term(lam, noise_sd)",
    ),
    "mutant_r12_02_uninformed_pays_cost.py": (
        "The uninformed investor pays the information cost too: the uninformed term is scaled by exp(a c).",
        "    return uninformed_term(lam, noise_sd) - math.exp(RISK_AVERSION * info_cost) * informed_term(lam, noise_sd)",
        "    return math.exp(RISK_AVERSION * info_cost) * uninformed_term(lam, noise_sd) - math.exp(RISK_AVERSION * info_cost) * informed_term(lam, noise_sd)",
    ),
    "mutant_r12_03_informed_variance_uses_bs_for_price_noise.py": (
        "The informed agent's price-noise variance uses the weight b_s where b_u belongs.",
        "    var_gap = slope * slope * var_signal + b_u * b_u * noise_sd * noise_sd",
        "    var_gap = slope * slope * var_signal + b_s * b_s * noise_sd * noise_sd",
    ),
    "mutant_r12_04_stops_when_midpoint_gap_is_tiny.py": (
        "Bisection stops when the gap at the midpoint is within 1e-12 of zero, not when the bracket is narrow.",
        "        while high - low > BISECTION_TOLERANCE * high and steps < MAX_BISECTION_STEPS:\n            mid = 0.5 * (low + high)",
        "        while abs(indifference_gap(0.5 * (low + high), sd, cost)) > BISECTION_TOLERANCE and steps < MAX_BISECTION_STEPS:\n            mid = 0.5 * (low + high)",
    ),
}
for name, (doc, old, new) in MUTANTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    body = REF.replace(old, new, 1)
    body = body.replace(DOC_OLD, f'"""{doc}"""\n', 1)
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)
