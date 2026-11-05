"""Round-10: run each alternative correct implementation through the BK4 suite on seeds 0-49 (local pytest flags).

Usage: python run_alts_r10.py <repo_root>   (uses tools/run_graders.py helpers from the same checkout)
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "tools"))
import run_graders as rg  # noqa: E402
from coursekit import unit  # noqa: E402

u = unit("BK4")
cfg = rg.panel(u)
alts = sorted((root / "ledgers/BK4/alternatives").glob("*.py"))
total_fail = 0
for alt in alts:
    work = rg.workspace(u, alt, cfg)
    passed = 0
    first_fail = None
    try:
        for seed in range(50):
            ok, output, _ = rg.run_suite(work, cfg["suite"], seed)
            if ok:
                passed += 1
            elif first_fail is None:
                first_fail = (seed, output[-400:])
    finally:
        import shutil
        shutil.rmtree(work, ignore_errors=True)
    total_fail += 50 - passed
    print(f"{alt.name}: {passed}/50 seeds pass")
    if first_fail:
        print(f"  first failure seed {first_fail[0]}: {first_fail[1]}")
print("ALTERNATIVES PASS" if total_fail == 0 else f"ALTERNATIVES FAIL ({total_fail} seed failures)")
