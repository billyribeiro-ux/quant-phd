"""Write the round-11 verifier's student-error mutants into ledgers/E4/mutants (one edit of reference.py each).
Usage: python3 -I make_mutants_r11.py <root>"""
import sys

root = sys.argv[1]
ref = open(f"{root}/course/modules/E/E4/grader/reference.py", encoding="utf-8").read()
edits = {
    "mutant_r11_01_price_noise_drops_the_square_on_risk_aversion.py": (
        "Price precision uses a sd^2 for the price noise, not a^2 sd^2 (the risk aversion is not squared).",
        "    return lam * lam * tau_e * tau_e / (lam * lam * tau_e + a * a * noise_sd * noise_sd)",
        "    return lam * lam * tau_e * tau_e / (lam * lam * tau_e + a * noise_sd * noise_sd)",
    ),
    "mutant_r11_02_zero_limit_uses_minus_cost_sign.py": (
        "The limit at fraction 0 uses exp(-a c) for the cost factor, so the cost enters with the wrong sign.",
        "    return uninformed - math.exp(RISK_AVERSION * info_cost) * informed\n",
        "    return uninformed - math.exp(-RISK_AVERSION * info_cost) * informed\n",
    ),
    "mutant_r11_03_fraction_clipped_below_one.py": (
        "Clips the informed fraction to 1 - 1e-12 to avoid the boundary, so a unit fraction is never reported.",
        "    if gap_0 <= 0.0:\n        lam = 0.0\n    elif gap_1 >= 0.0:\n        lam = 1.0",
        "    if gap_0 <= 0.0:\n        lam = 0.0\n    elif gap_1 >= 0.0:\n        lam = 1.0 - 1e-12",
    ),
    "mutant_r11_04_informed_mean_forgets_the_precision_weight.py": (
        "Informed conditional mean is the signal itself: the precision weight tau_e / (tau_v + tau_e) is dropped from the slope.",
        "    slope = tau_e / precision - b_s",
        "    slope = tau_e - b_s",
    ),
}
for name, (doc, old, new) in edits.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    text = ref.replace(old, new)
    # replace the module docstring with the one-line error description, as the gate reads it
    start = text.index('"""')
    end = text.index('"""', start + 3) + 3
    text = f'"""{doc}\n\nRound-11 verifier mutant (E4 slice d). Derived from grader/reference.py by one edit.\n"""' + text[end:]
    open(f"{root}/ledgers/E4/mutants/{name}", "w", encoding="utf-8").write(text)
    print("wrote", name)
