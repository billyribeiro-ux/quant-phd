"""Classify the page-valid sweep cases on which the reference's own certificate exceeds 1e-8 (round-16 verifier).

For each case: which certificate field is above 1e-8, whether the start snap was taken or refused (and why), and the
row of the working set that carries the largest complementary product. Run from the repository root with -I.
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


def snap_status(case: dict) -> str:
    problem = P.REF._parse(case)
    snapped = P.REF._snapped_start(problem)
    if [float(x) for x in snapped] == [float(x) for x in problem.w0]:
        moved = sum((abs(a - b) for a, b in zip(snapped, problem.w0, strict=True)), F(0))
        return "start returned unchanged (" + ("no breach" if moved == 0 else "snap refused: turnover guard or unrepairable sector") + ")"
    return "snapped start used"


def main() -> None:
    count, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    rows = []
    for idx in range(count):
        case = S.gen(rng)
        if not S.valid_start(case):
            continue
        try:
            out = P.REF.allocate(json.loads(json.dumps(case)))
        except Exception:
            continue
        rec = P.recomputed(case, out)
        bad = {k: float(v) for k, v in rec.items() if k != "budget_gap" and float(v) > 1e-8}
        if not bad:
            continue
        rows.append({"idx": idx, "bad_fields": bad, "snap": snap_status(case), "tau": case["turnover_limit"],
                     "lower_minus_w0": [round(case["lower"][i] - case["w0"][i], 12) for i in range(len(case["w0"]))],
                     "cap_minus_sector_sum": [round(case["sector_caps"][k] - sum(case["w0"][i] for i in range(len(case["w0"])) if case["sector"][i] == k), 12) for k in range(len(case["sector_caps"]))],
                     "mu": case["mu"], "gamma": case["gamma"]})
    print(json.dumps({"count": count, "seed": seed, "page_valid_cert_fail": len(rows), "rows": rows}, indent=1))


if __name__ == "__main__":
    main()
