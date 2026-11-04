"""Print the complete pytest output (browser flags) for one candidate and one seed (verifier BK4-c, round 2).

Usage: .venv/bin/python ledgers/BK4/scripts/BK4-c-r2/full_output.py <seed> <candidate.py>
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))

from coursekit import unit  # noqa: E402
from run_graders import panel, run_suite, workspace  # noqa: E402

u = unit("BK4")
cfg = panel(u)
seed, cand = int(sys.argv[1]), Path(sys.argv[2]).resolve()
work = workspace(u, cand, cfg)
try:
    import subprocess
    import sys as _s

    res = subprocess.run(
        [_s.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", cfg["suite"]],
        cwd=work, capture_output=True, text=True, env={"QF_SEED": str(seed), "PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0"},
        check=False,
    )
    print(res.stdout)
    print(res.stderr)
finally:
    shutil.rmtree(work, ignore_errors=True)
