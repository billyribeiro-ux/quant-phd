"""Build wrong-solution mutants and alternative correct implementations from the reference (scratch, verifier d)."""
import pathlib, sys
REF = pathlib.Path("/tmp/verifyC1-E3-d/course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")

def sub(src, old, new, name):
    assert src.count(old) == 1, (name, src.count(old))
    return src.replace(old, new)

def mutant(name, pairs, doc):
    src = REF
    for old, new in pairs:
        src = sub(src, old, new, name)
    return f'"""{doc}\n\nSingle-change copy of the reference solution (verifier d).\n"""\n' + src.split('"""', 2)[2]

def alt(name, pairs):
    src = REF
    for old, new in pairs:
        src = sub(src, old, new, name)
    return src

MUT = {
 "v01_se_without_delta_method.py": mutant("v01", [(
  '"se_gamma": gamma * (1.0 - gamma) * math.sqrt(cov_diag[0]),',
  '"se_gamma": math.sqrt(cov_diag[0]),')],
  "Standard error of gamma reported in the transformed coordinate c, without the delta-method factor gamma(1 - gamma)."),
 "v02_prospect_inverse_forgets_lambda.py": mutant("v02", [(
  "return -math.pow(-total / lam, 1.0 / (1.0 - gamma))",
  "return -math.pow(-total, 1.0 / (1.0 - gamma))")],
  "Prospect certainty equivalent for a negative lottery value divides no loss weight: c = -(-V)^(1/(1-gamma)), not -(-V/lambda)^(1/(1-gamma))."),
 "v03_wealth_check_allows_zero_final_wealth.py": mutant("v03", [(
  "if any(wealth_cents + x <= 0 for x in prizes):",
  "if any(wealth_cents + x < 0 for x in prizes):")],
  "CRRA wealth check is off by one: final wealth of exactly zero cents is accepted instead of raising ValueError."),
 "v04_crra_returns_float_cents.py": mutant("v04", [(
  "return _half_up(_crra_change(prizes, probs, gamma, wealth_cents))",
  "return float(_half_up(_crra_change(prizes, probs, gamma, wealth_cents)))")],
  "CRRA certainty equivalent returned as a float number of cents rather than an int."),
 "v05_logit_scale_per_dollar.py": mutant("v05", [(
  "CENTS_PER_UNIT = 10_000.0  # the logit uses differences in units of $100: z = kappa * dCE / 10000",
  "CENTS_PER_UNIT = 100.0  # the logit uses differences in units of $1 (student error)")],
  "Logit scale read as dollars instead of hundreds of dollars: z = kappa * dCE / 100 with dCE in cents."),
}

ALT = {
 "alt1_bisection_prospect_inverse.py": alt("alt1", [(
  "    total = sum(float(p) * _value(x, gamma, lam) for x, p in zip(prizes, probs, strict=True))\n    if total >= 0.0:\n        return math.pow(total, 1.0 / (1.0 - gamma))\n    return -math.pow(-total / lam, 1.0 / (1.0 - gamma))",
  "    total = sum(float(p) * _value(x, gamma, lam) for x, p in zip(prizes, probs, strict=True))\n    lo, hi = -1.0e12, 1.0e12\n    for _ in range(300):\n        mid = (lo + hi) / 2.0\n        if _value(mid, gamma, lam) < total:\n            lo = mid\n        else:\n            hi = mid\n    return (lo + hi) / 2.0")]),
 "alt2_compass_search_optimiser.py": alt("alt2", [(
  "def _maximise(parsed: list[Parsed]) -> list[float]:\n    def f(t: list[float]) -> float:\n        return _objective(t, parsed)\n",
  "def _maximise(parsed: list[Parsed]) -> list[float]:\n    import itertools\n\n    def f(t: list[float]) -> float:\n        return _objective(t, parsed)\n\n    best_t = [0.0, 0.0, 0.0]\n    best_v = -math.inf\n    for gamma in (0.05, 0.25, 0.45, 0.65, 0.85):\n        for lam in (1.0, 2.0, 4.0):\n        	for kappa in (0.5, 2.0, 5.0):\n                s = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]\n                if f(s) > best_v:\n                    best_v, best_t = f(s), s\n    t, v, step = list(best_t), best_v, 0.5\n    dirs = [list(d) for d in itertools.product((-1.0, 0.0, 1.0), repeat=3) if any(d)]\n    while step > 1e-10:\n        cand = [[x + step * d for x, d in zip(t, dv, strict=True)] for dv in dirs]\n        bv, bt = max(((f(c), c) for c in cand), key=lambda p: p[0])\n        if bv > v:\n            v, t = bv, bt\n        else:\n            step /= 2.0\n    return t\n\n    def _unused() -> None:\n        pass\n")]),
 "alt3_decimal_half_up.py": alt("alt3", [(
  "def _half_up(y: float) -> int:\n    \"\"\"The nearest whole cent with an exact half going up (toward plus infinity): floor(y + 1/2).\"\"\"\n    return math.floor(y + 0.5)",
  "def _half_up(y: float) -> int:\n    from decimal import ROUND_FLOOR, Decimal\n\n    return int((Decimal(repr(y)) + Decimal('0.5')).to_integral_value(rounding=ROUND_FLOOR))")]),
}

for d, table in (("/tmp/e3d-v/d/mut", MUT), ("/tmp/e3d-v/d/alt", ALT)):
    p = pathlib.Path(d); p.mkdir(parents=True, exist_ok=True)
    for name, src in table.items():
        (p / name).write_text(src, encoding="utf-8")
        print("wrote", p / name)
