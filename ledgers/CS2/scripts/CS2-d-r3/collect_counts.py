"""Collect-only test count of the CS2 suite on the reference, for every seed given. Usage: python -I collect_counts.py <repo_root> <seeds 0-49>
Uses the grader's own workspace() (copies suite, instance.py and reference.py as streamstats.py)."""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, workspace  # noqa: E402

u = unit("CS2")
cfg = panel(u)
ref = u.directory / "grader" / "reference.py"
counts: dict[int, int] = {}
for seed in parse_seeds(sys.argv[2]):
    work = workspace(u, ref, cfg)
    try:
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        res = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", cfg["suite"]],
                             cwd=work, capture_output=True, text=True, env=env, check=False)
        m = re.search(r"(\d+) tests? collected", res.stdout + res.stderr)
        counts[seed] = int(m.group(1)) if m else -1
        if res.returncode != 0:
            print("collect error", seed, res.stdout[-300:], res.stderr[-300:])
    finally:
        shutil.rmtree(work, ignore_errors=True)
print("distinct counts:", sorted(set(counts.values())), "seeds:", len(counts))
