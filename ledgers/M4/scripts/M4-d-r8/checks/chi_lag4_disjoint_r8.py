"""Chi-square lag test on a disjoint lag-four pair sharing (round 8, slice d).

Draws 8m+4 reuse the chi-square variable of draw 8m (pairs (0,4), (8,12), ...; no chains). Each seed 0-49 runs the
grader's test_student_t_draws_do_not_share_chi_square, and the full suite is run on seed 0.
Usage: python -I ledgers/M4/scripts/M4-d-r8/checks/chi_lag4_disjoint_r8.py
"""

import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import chi_lag_r8 as base  # noqa: E402

if __name__ == "__main__":
    path = base.variant("lag4_disjoint_pairs", "d % 8 == 4", "chi_by_draw[d - 4]")
    jobs = [(path, "lag4_disjoint", s, "test_student_t_draws_do_not_share_chi_square") for s in range(50)]
    with ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(base.run, jobs))
    fails = [s for _, s, ok, _ in res if not ok]
    print(f"lag4_disjoint_pairs: chi-square lag test fails on {len(fails)} of 50 seeds: {fails[:10]}")
    full = base.run((path, "lag4_disjoint_full", 0, None))
    print("lag4_disjoint_pairs full suite seed 0 passes:", full[2], "failing tests:", full[3])
