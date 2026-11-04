import pathlib
ref = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD7-E3-d/course/modules/E/E3/grader/reference.py")
out = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD7-E3-d/ledgers/E3/mutants")
src = ref.read_text(encoding="utf-8")
specs = {
 "e3d7_01_crra_gamma_zero_expectation_summed_in_float.py": (
  "CRRA at gamma = 0 sums the expected prize in float, so an exact half cent can round down.",
  '            expected_change = sum((p * x for p, x in zip(probs, prizes, strict=True)), Fraction(0))\n            return math.floor(expected_change + Fraction(1, 2))',
  '            expected_change = sum(float(p) * x for p, x in zip(probs, prizes, strict=True))\n            return math.floor(expected_change + 0.5)'),
 "e3d7_02_loss_power_applies_lambda_inside_the_root.py": (
  "Loss value puts lambda inside the power, -(lambda (-x))^(1-gamma), not outside it.",
  '    return -lam * math.pow(float(-x), 1.0 - gamma)',
  '    return -math.pow(lam * float(-x), 1.0 - gamma)'),
 "e3d7_03_prospect_model_refuses_nonpositive_final_wealth.py": (
  "The prospect model refuses wealth plus prize <= 0, although the prospect model does not use wealth.",
  '    lam = float(params["lambda"])\n    _check_prospect(gamma, lam)\n    return _half_up',
  '    lam = float(params["lambda"])\n    _check_prospect(gamma, lam)\n    if any(wealth_cents + x <= 0 for x in prizes):\n        raise ValueError("wealth plus prize must stay positive")\n    return _half_up'),
 "e3d7_04_estimate_returns_the_grid_start_without_refinement.py": (
  "estimate returns the best starting-grid point and never runs the search, so it is a grid point.",
  '    xi = list(best[1])\n    value = best[0]\n',
  '    return list(best[1])\n    xi = list(best[1])\n    value = best[0]\n'),
}
for name, (doc, old, new) in specs.items():
    assert src.count(old) == 1, (name, src.count(old))
    body = src.replace(old, new)
    text = f'"""{doc}\n\nRound-7 verifier (E3-d) student-error mutant: the reference solution with the single change above.\nStandard library only.\n"""\n' + body.split('"""', 2)[2]
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name, len(text))
