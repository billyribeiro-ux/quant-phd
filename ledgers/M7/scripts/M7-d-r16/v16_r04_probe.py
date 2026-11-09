"""Probe equivalence mutant r04 (budget gap left out of the primal residual) on page-valid starts (round-16 verifier).

Reports the reference's and r04's primal residual, and the certified difference, for the named budget-gap cases and
for the sweep case idx 459 of seed 17. Run from the repository root with -I.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import v16_probe as P  # noqa: E402
import v16_sweep as S  # noqa: E402

R04 = P.load(P.EQUIV / "r04_budget_left_out_of_primal_residual.py", "eq_r04_probe")


def report(title: str, case: dict) -> None:
    ok_start = S.valid_start(case)
    ref = P.REF.allocate(json.loads(json.dumps(case)))
    mut = R04.allocate(json.loads(json.dumps(case)))
    rec = P.recomputed(case, ref)
    print(f"[{title}] start_valid_exact={ok_start} ref_primal={ref['certificate']['primal_residual']} "
          f"r04_primal={mut['certificate']['primal_residual']} recomputed_primal={float(rec['primal'])} "
          f"budget_gap={float(rec['budget_gap'])} ref_weights_sum_minus_1={float(rec['budget_gap'])}")
    print(f"[{title}] |r04 primal - recomputed primal| = {abs(mut['certificate']['primal_residual'] - float(rec['primal'])):.3g} (agreement tolerance 1e-9)")


def main() -> None:
    base = P.case_of
    report("B1 start sum 1+1e-9, asset 0 1e-9 below lower bound", base(mu=[0.0, 0.0], lower=[0.5, -1.0], w0=[0.5 - 1e-9, 0.5 + 2e-9], turnover_limit=2.0))
    report("B2 start sum 1-1e-9, asset 0 1e-9 above upper bound", base(mu=[0.0, 0.0], upper=[0.5, 2.0], w0=[0.5 + 1e-9, 0.5 - 2e-9], turnover_limit=2.0))
    import random
    rng = random.Random(17)
    for idx in range(460):
        case = S.gen(rng)
        if idx == 459:
            report("seed17 sweep idx 459", case)


if __name__ == "__main__":
    main()
