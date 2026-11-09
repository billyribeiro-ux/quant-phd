"""Round 3, slice d: run each candidate solution through the M5 suite on seeds 0-49 (same flags as the browser).

Usage: python3 -I alt_seeds_r3.py <checkout-root>. Each candidate is copied into a fresh scratch workspace
outside the repository; the suite and instance come from course/modules/M/M5/grader.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
py = root / ".venv" / "bin" / "python"
grader = root / "course" / "modules" / "M" / "M5" / "grader"
alts = root / "ledgers" / "M5" / "alternatives"
cands = {
    "reference": grader / "reference.py",
    "alt1_functional": alts / "alt1_functional_reduce_and_tuples.py",
    "alt2_class": alts / "alt2_class_with_precomputed_feasible_tables.py",
    "alt3_comprehension": alts / "alt3_comprehension_with_feasible_index_lists.py",
    "alt4_bisect": alts / "alt4_bisect_for_feasible_successors.py",
    "alt5_reverse_order": alts / "alt5_reverse_order_synchronous_sweep.py",
    "not_accepted_alt1_inplace": alts / "not_accepted" / "alt1_gauss_seidel_in_place.py",
    "not_accepted_alt2_residual": alts / "not_accepted" / "alt2_residual_stop.py",
}
for name, src in cands.items():
    passed = []
    failed = []
    for seed in range(50):
        work = Path(tempfile.mkdtemp(prefix=f"m5r3_{name}_"))
        shutil.copy(grader / "test_project.py", work / "test_project.py")
        shutil.copy(grader / "instance.py", work / "instance.py")
        shutil.copy(src, work / "contraction_solver.py")
        r = subprocess.run(
            [str(py), "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work, capture_output=True, text=True, check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            timeout=600,
        )
        (passed if r.returncode == 0 else failed).append(seed)
        shutil.rmtree(work, ignore_errors=True)
    print(f"{name}: {len(passed)}/50 seeds PASS; failing seeds: {failed[:10]}{' ...' if len(failed) > 10 else ''}")
