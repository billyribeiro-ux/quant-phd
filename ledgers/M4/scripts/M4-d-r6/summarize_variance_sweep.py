"""Summarize sweep_variance_0-1999.jsonl: per nu, max matched relative error, and counts of unmatched failures at tol 0.30."""

import json
import sys
from pathlib import Path

rows = [json.loads(line) for line in Path(sys.argv[1]).read_text().splitlines()]
TOL = 0.30
for nu in range(3, 9):
    sel = [r for r in rows if r["nu"] == nu]
    if not sel:
        print(f"nu={nu}: no seeds")
        continue
    worst = max(sel, key=lambda r: r["rel_matched"])
    fails_u = sum(1 for r in sel if r["rel_unmatched"] > TOL)
    fails_m = sum(1 for r in sel if r["rel_matched"] > TOL)
    print(
        f"nu={nu}: seeds={len(sel)} max_matched_rel={worst['rel_matched']:.4f} at seed {worst['seed']} "
        f"matched_fail_at_0.30={fails_m} unmatched_fail_at_0.30={fails_u}"
    )
s1093 = [r for r in rows if r["seed"] == 1093][0]
print("seed 1093:", s1093)
print("total seeds:", len(rows))
