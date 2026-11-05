"""Re-run the twenty prior-round alternatives that earlier rounds recorded as correct (seeds 0-49) against the round-13
suite, which gained two closed-form tests. The step-major and Box-Muller alternatives are intentionally wrong draws and
are not part of this set."""

import shutil
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402

S = root / "ledgers/SC1/scripts"
names = [
    S / "SC1-d-r4/alternatives/alt1_normaldist_tail.py",
    S / "SC1-d-r4/alternatives/alt2_simpson_only_tail.py",
    S / "SC1-d-r4/alternatives/alt3_srw_dp.py",
    S / "SC1-d-r4/alternatives/alt5_cumsum_index_subsample.py",
    S / "SC1-d-r4/alternatives/alt6_pascal_row_terminal.py",
    S / "SC1-d-r4/alternatives/alt8_one_minus_erf.py",
    S / "SC1-d-r4/alternatives/alt9_se_closed_form.py",
    S / "SC1-d-r8/alternatives/alt_r8_a_normaldist_tail.py",
    S / "SC1-d-r8/alternatives/alt_r8_b_quadrature_tail.py",
    S / "SC1-d-r8/alternatives/alt_r8_c_dp_srw.py",
    S / "SC1-d-r8/alternatives/alt_r8_d_streaming.py",
    S / "SC1-d-r9/alternatives/alt_r9_a_normal_cdf_and_dp.py",
    S / "SC1-d-r9/alternatives/alt_r9_b_erf_and_pascal.py",
    S / "SC1-d-r9/alternatives/alt_r9_c_closed_form_and_running_max.py",
    S / "SC1-d-r9/alternatives/alt_r9_d_list_comprehension_and_cached_grid.py",
    S / "SC1-d-r9/alternatives/alt_r9_e_iterative_tail_and_one_pass.py",
    S / "SC1-d-r10/alternatives/alt_r10_a_normaldist_tail.py",
    S / "SC1-d-r10/alternatives/alt_r10_b_quadrature_tail.py",
    S / "SC1-d-r10/alternatives/alt_r10_c_dp_walk_counts.py",
    S / "SC1-d-r10/alternatives/alt_r10_e_index_subsample.py",
]
u = unit("SC1")
cfg = panel(u)
for f in names:
    if not f.exists():
        print(f"MISSING {f}")
        continue
    work = workspace(u, f, cfg)
    failures = []
    try:
        for seed in parse_seeds("0-49"):
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                failures.append((seed, output.strip().splitlines()[-1] if output.strip() else ""))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"{f.parent.parent.name}/{f.name}: {'PASS' if not failures else 'FAIL'} on 0-49 ({50 - len(failures)}/50)")
    for seed, last in failures[:3]:
        print(f"    seed {seed}: {last}")
