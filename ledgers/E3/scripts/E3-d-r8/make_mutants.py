# Builds round-8 student-error mutants of the reference engine (each a complete elicit.py).
import pathlib
REF = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-E3-d/course/modules/E/E3/grader/reference.py")
OUT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-E3-d/ledgers/E3/mutants")
src = REF.read_text(encoding="utf-8")

def make(name, description, pairs):
    text = src
    for old, new in pairs:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    end = text.index('"""', 3) + 3
    body = f'"""{description}"""' + text[end:]
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)

make("e8_01_se_from_inverse_of_the_diagonal_only.py",
     "Standard errors take 1/sqrt of each diagonal entry of the information, ignoring the off-diagonal terms.",
     [("    cov_diag: list[float] = []\n    for i in range(3):\n        unit = [1.0 if k == i else 0.0 for k in range(3)]\n        cov_diag.append(_solve(lower, unit)[i])\n",
       "    cov_diag: list[float] = [1.0 / (-hess[i][i]) for i in range(3)]\n")])

make("e8_02_crra_allows_final_wealth_of_exactly_zero.py",
     "CRRA refuses final wealth below zero but accepts exactly zero, so a prize that takes wealth to zero is not refused.",
     [('        if any(wealth_cents + x <= 0 for x in prizes):', '        if any(wealth_cents + x < 0 for x in prizes):')])

make("e8_03_prospect_loss_weight_also_scales_the_gain_branch.py",
     "The loss weight lambda multiplies the gain branch of the value function as well as the loss branch.",
     [("    if x >= 0:\n        return math.pow(float(x), 1.0 - gamma)\n    return -lam * math.pow(float(-x), 1.0 - gamma)",
       "    if x >= 0:\n        return lam * math.pow(float(x), 1.0 - gamma)\n    return -lam * math.pow(float(-x), 1.0 - gamma)")])

make("e8_04_prospect_model_adds_wealth_to_each_prize.py",
     "The prospect model values the lottery on final wealth (wealth plus each prize) instead of on the change from 0.",
     [("    gamma = float(params[\"gamma\"])\n    if name == \"crra\":",
       "    gamma = float(params[\"gamma\"])\n    if name == \"prospect\":\n        prizes_final = [x + wealth_cents for x in prizes]\n        lam_f = float(params[\"lambda\"])\n        _check_prospect(gamma, lam_f)\n        return _half_up(_prospect_ce(prizes_final, probs, gamma, lam_f) - wealth_cents)\n    if name == \"crra\":")])

make("e8_05_model_name_error_raises_type_error.py",
     "An unknown model name raises TypeError, where the specification names ValueError.",
     [('        raise ValueError(\'model must be "crra" or "prospect"\')', '        raise TypeError(\'model must be "crra" or "prospect"\')')])
