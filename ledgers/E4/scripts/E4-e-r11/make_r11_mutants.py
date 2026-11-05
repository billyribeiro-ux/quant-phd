"""Round 11: write three new student-error mutants of the E4 reference solver into ledgers/E4/mutants/.

Each mutant is course/modules/E/E4/grader/reference.py with one edit. The script asserts that the edited text occurs
exactly once, so a mutant cannot silently equal the reference. Run from the checkout root."""
from pathlib import Path

REF = Path("course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")
OUT = Path("ledgers/E4/mutants")

EDITS = {
    "mutant_r11_01_cost_factor_first_order_taylor.py": (
        "Student shortcut: the cost factor exp(a c) is replaced by its first-order Taylor term 1 + a c, in both the gap at 0 and the gap at a fraction.",
        "    return uninformed - math.exp(RISK_AVERSION * info_cost) * informed",
        "    return uninformed - (1.0 + RISK_AVERSION * info_cost) * informed",
        "    return uninformed_term(lam, noise_sd) - math.exp(RISK_AVERSION * info_cost) * informed_term(lam, noise_sd)",
        "    return uninformed_term(lam, noise_sd) - (1.0 + RISK_AVERSION * info_cost) * informed_term(lam, noise_sd)",
    ),
    "mutant_r11_02_zero_limit_drops_cost_factor.py": (
        "Student error: the limit of the gap at fraction 0 forgets the information cost (the exp(a c) factor), so the zero-fraction gap ignores the cost.",
        "    return uninformed - math.exp(RISK_AVERSION * info_cost) * informed\n",
        "    return uninformed - informed\n",
        None,
        None,
    ),
    "mutant_r11_03_price_precision_is_signal_precision.py": (
        "Student error: the price is treated as the signal, so the uninformed precision tau_y is the signal precision tau_e, not the precision of the price signal y = p / b_s.",
        "    tau_y = price_precision(lam, noise_sd)\n    return tau_y / (PRIOR_PRECISION + tau_y)",
        "    tau_y = SIGNAL_PRECISION\n    return tau_y / (PRIOR_PRECISION + tau_y)",
        None,
        None,
    ),
}

for name, (doc, old, new, old2, new2) in EDITS.items():
    text = REF
    pairs = [(old, new)] + ([(old2, new2)] if old2 is not None else [])
    for a, b in pairs:
        n = text.count(a)
        assert n == 1, (name, a[:60], n)
        text = text.replace(a, b)
    header = f'"""{doc}\n\nRound-11 verifier mutant (E4 slice e). Derived from grader/reference.py by one edit.\n"""\n'
    body = text.split('"""', 2)[2] if text.startswith('"""') else text
    (OUT / name).write_text(header + body.lstrip("\n"), encoding="utf-8")
    print("wrote", OUT / name)
