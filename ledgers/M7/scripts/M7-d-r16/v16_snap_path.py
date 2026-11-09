"""Name the branch of reference._snapped_start that each page-valid certificate-failing sweep case takes (round 16).

Branches (reference.py:197-220): 'room' = a sector breach that the bounds cannot absorb (returns w0); 'guard' = the snapped
start moves further than tau (returns w0); 'snapped' = the snapped start is used. Run from the repository root with -I.
"""

from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import v16_probe as P  # noqa: E402
import v16_sweep as S  # noqa: E402

F = Fraction


def branch(case: dict) -> str:
    problem = P.REF._parse(case)
    n = problem.n
    x = [min(max(problem.w0[i], problem.lower[i]), problem.upper[i]) for i in range(n)]
    for k, cap in enumerate(problem.caps):
        members = [i for i in range(n) if problem.sector[i] == k]
        excess = sum((x[i] for i in members), F(0)) - cap
        if excess <= 0:
            continue
        room = sum((x[i] - problem.lower[i] for i in members), F(0))
        if room < excess:
            return "room (sector breach not absorbable; returns w0)"
        for i in members:
            x[i] -= excess * (x[i] - problem.lower[i]) / room
    moved = sum((abs(x[i] - problem.w0[i]) for i in range(n)), F(0))
    if moved > problem.tau:
        return "guard (snapped move exceeds tau; returns w0)"
    return "snapped"


def main() -> None:
    count, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    tally: dict[str, int] = {}
    for idx in range(count):
        case = S.gen(rng)
        if not S.valid_start(case):
            continue
        try:
            out = P.REF.allocate(json.loads(json.dumps(case)))
        except Exception:
            continue
        rec = P.recomputed(case, out)
        if max(float(rec[k]) for k in ("primal", "stationarity", "dual", "complementary")) > 1e-8:
            b = branch(case)
            tally[b] = tally.get(b, 0) + 1
            print("CASE", idx, b, "tau", case["turnover_limit"], "gamma", case["gamma"], "mu", case["mu"])
    print("TALLY", json.dumps(tally))


if __name__ == "__main__":
    main()
