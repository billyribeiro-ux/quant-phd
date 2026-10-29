import pathlib
src = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB7-M7-d/course/modules/M/M7/grader/reference.py").read_text()
out = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB7-M7-d/ledgers/M7/mutants")
specs = {
 "r01_stationarity_lower_upper_signs_swapped.py": ("Student error r01: the lower and upper bound multipliers enter the weight stationarity with swapped signs.",
    '        r_w = gradient + sol["budget"] - sol["lower"][i] + sol["upper"][i] + sol["sector"][problem.sector[i]]',
    '        r_w = gradient + sol["budget"] + sol["lower"][i] - sol["upper"][i] + sol["sector"][problem.sector[i]]'),
 "r02_turnover_total_residual_dropped_from_primal.py": ("Student error r02: the turnover limit is left out of the primal residual of the certificate.",
    "    gaps.append(sum(t, Fraction(0)) - problem.tau)\n",
    "    gaps.append(Fraction(0))\n"),
 "r03_turnover_t_stationarity_plus_sign.py": ("Student error r03: the plus multiplier enters the turnover-variable stationarity with a plus sign.",
    '        r_t = sol["kappa"] - sol["plus"][i] - sol["minus"][i]',
    '        r_t = sol["kappa"] + sol["plus"][i] - sol["minus"][i]'),
 "r04_budget_left_out_of_primal_residual.py": ("Student error r04: the budget violation is left out of the primal residual of the certificate.",
    "abs(sum(w, Fraction(0)) - 1), *gaps])",
    "*gaps])"),
 "r05_turnover_total_slackness_term_zeroed.py": ("Student error r05: the turnover-total complementary slackness term uses a constraint value of zero.",
    "                sum(t, Fraction(0)) - problem.tau,\n            ],",
    "                Fraction(0),\n            ],"),
}
for name, (doc, old, new) in specs.items():
    assert src.count(old) == 1, (name, src.count(old))
    text = src.replace(old, new, 1)
    text = '"""' + doc + '\n\nReference solution with one planted error (see the docstring line above).\n"""\n' + text.split('"""', 2)[2]
    (out / name).write_text(text)
    print("wrote", name)
