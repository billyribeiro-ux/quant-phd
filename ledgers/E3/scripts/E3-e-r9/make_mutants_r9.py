"""Writes the three round-9 verifier mutants as complete solution modules, each a one-edit variant of reference.py."""

import pathlib

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD9-E3-e")
REF = (ROOT / "course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/E3/mutants"


def make(stem: str, first_line: str, old: str, new: str) -> None:
    assert REF.count(old) == 1, (stem, REF.count(old))
    body = REF.replace(old, new, 1)
    parts = body.split('"""', 2)
    body = '"""' + first_line + "\n\n" + parts[1] + '"""' + parts[2]
    (OUT / f"{stem}.py").write_text(body, encoding="utf-8")
    print("wrote", stem)


make(
    "r9e_01_lambda_hat_clamped_at_ten",
    "Reported lambda_hat is clamped at 10 by hand, so a participant with a larger loss weight gets a wrong estimate.",
    "    lam = math.exp(a)\n    kappa = math.exp(b)\n    return {",
    "    lam = min(math.exp(a), 10.0)\n    kappa = math.exp(b)\n    return {",
)

make(
    "r9e_02_single_start_no_grid_search",
    "Maximiser starts from the single point gamma 0.5, lambda 1, kappa 1 and never tries the grid of starts.",
    "    for gamma in (0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95):\n"
    "        for lam in (1.0, 1.5, 2.0, 3.0, 4.0, 6.0):\n"
    "            for kappa in (0.5, 1.0, 2.0, 3.0, 5.0, 8.0):\n"
    "                t = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]\n"
    "                v = f(t)\n"
    "                if best is None or v > best[0]:\n"
    "                    best = (v, t)",
    "    t = [0.0, 0.0, 0.0]\n    best = (f(t), t)",
)

make(
    "r9e_03_prospect_ce_returned_in_dollars",
    "Prospect certainty equivalent is divided by 100 before the cent rounding, so it is returned in dollars.",
    "    return _half_up(_prospect_ce(prizes, probs, gamma, lam))",
    "    return _half_up(_prospect_ce(prizes, probs, gamma, lam) / 100.0)",
)
