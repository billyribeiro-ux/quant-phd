import os
import shutil
import subprocess
import sys

sys.path.insert(0, "/tmp/verify16-CF1-d/tools")
from coursekit import unit  # noqa: E402
from run_graders import panel, workspace  # noqa: E402

u = unit("CF1")
cfg = panel(u)
seed = os.environ.get("S", "0")
for name, src in [("reference", u.directory / "grader/reference.py"), ("starter", u.directory / "grader/starter.py")]:
    work = workspace(u, src, cfg)
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", cfg["suite"]],
        cwd=work,
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin", "QF_SEED": seed, "PYTHONHASHSEED": "0"},
        check=False,
    )
    print("seed", seed, name, r.stdout.strip().splitlines()[-1])
    shutil.rmtree(work, ignore_errors=True)
