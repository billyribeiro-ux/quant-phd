"""Round-11: run alt6_candidate_scan.py through the BK4 suite on seeds 0-49 (same helpers as run_alts_r11.py).

Usage: python -I run_alt6_r11.py <repo_root>
"""

import shutil
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "tools"))
import run_graders as rg  # noqa: E402
from coursekit import unit  # noqa: E402

u = unit("BK4")
cfg = rg.panel(u)
alt = root / "ledgers/BK4/scripts/BK4-c-r11/alt6_candidate_scan.py"
work = rg.workspace(u, alt, cfg)
passed, first_fail = 0, None
try:
    for seed in range(50):
        ok, output, _ = rg.run_suite(work, cfg["suite"], seed)
        if ok:
            passed += 1
        elif first_fail is None:
            first_fail = (seed, output[-400:])
finally:
    shutil.rmtree(work, ignore_errors=True)
print(f"{alt.name}: {passed}/50 seeds pass")
if first_fail:
    print(f"  first failure seed {first_fail[0]}: {first_fail[1]}")
print("ALT6 PASS" if passed == 50 else "ALT6 FAIL")
