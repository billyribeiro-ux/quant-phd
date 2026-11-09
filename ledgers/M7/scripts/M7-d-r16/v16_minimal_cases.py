"""Minimal page-valid inputs that the round-16 reference answers outside the 1e-8 certificate tolerance, and the
decimal-reading validity of the budget-gap input used against mutant r04 (round-16 verifier).

Decimal reading: each value is Fraction(repr(value)), as reference.py:46 reads it. Run from the repository root with -I.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import v16_probe as P  # noqa: E402
import v16_invalid_answered as I  # noqa: E402

R04 = P.load(P.EQUIV / "r04_budget_left_out_of_primal_residual.py", "eq_r04_minimal")
TOL = Fraction(1, 10**9)


def show(title: str, case: dict) -> None:
    print(f"[{title}] decimal-reading valid start: {I.decimal_start_ok(case)}")
    out = P.REF.allocate(json.loads(json.dumps(case)))
    ok, info = P.check(case, out)
    print(f"[{title}] reference weights={out['weights']} multipliers.lower={out['multipliers']['lower']} "
          f"certificate={out['certificate']}")
    print(f"[{title}] independent recomputation: feasibility max={info['feas']:.3g} (tolerance 1e-8), agreement={info['agree']:.3g} (1e-9), certified={ok}")
    mut = R04.allocate(json.loads(json.dumps(case)))
    rec = P.recomputed(case, out)
    print(f"[{title}] r04 primal={mut['certificate']['primal_residual']} vs recomputed primal={float(rec['primal']):.3g}; "
          f"|difference|={abs(mut['certificate']['primal_residual'] - float(rec['primal'])):.3g} (agreement tolerance 1e-9)")


def main() -> None:
    # G: tau = 0 (valid), lower bound of asset 0 is 5e-10 above its starting weight (inside the 1e-9 tolerance), mu=[-1000,0]
    G = P.case_of(mu=[-1000.0, 0.0], lower=[0.5000000005, -1.0], w0=[0.5, 0.5], turnover_limit=0.0)
    show("G tau=0, lower bound 5e-10 above start", G)
    # H: same with tau = 5e-10 (the snap is allowed; a control)
    H = P.case_of(mu=[-1000.0, 0.0], lower=[0.5000000005, -1.0], w0=[0.5, 0.5], turnover_limit=5e-10)
    show("H control tau=5e-10", H)
    # B1: start sums to 1+1e-9, asset 0 is 1e-9 below its lower bound (decimal values exact)
    B1 = P.case_of(mu=[0.0, 0.0], lower=[0.5, -1.0], w0=[0.499999999, 0.500000002], turnover_limit=2.0)
    show("B1 budget gap via snap, decimal values", B1)


if __name__ == "__main__":
    main()
