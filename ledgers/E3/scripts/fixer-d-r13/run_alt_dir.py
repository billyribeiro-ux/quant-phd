"""Run one alternative directory (its elicit.py) through the current test_project.py on a seed list; print PASS/FAIL."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/Users/billyribeiro/dev/quant-phd")
GRADER = ROOT / "course/modules/E/E3/grader"
alt_dir = Path(sys.argv[1])
seeds = [int(x) for x in sys.argv[2].split(",")]
failed = []
for seed in seeds:
    work = Path(tempfile.mkdtemp(prefix="altdir-"))
    try:
        for f in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / f, work / f)
        shutil.copy(alt_dir / "elicit.py", work / "elicit.py")
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                           cwd=work, capture_output=True, text=True, check=False,
                           env={"PATH": "/usr/bin:/bin", "QF_SEED": str(seed), "PYTHONHASHSEED": "0"})
        if r.returncode != 0:
            failed.append(seed)
            names = [ln.split("::")[1].split(" ")[0] for ln in r.stdout.splitlines() if ln.startswith("FAILED ")]
            print(f"  seed {seed}: {names}", flush=True)
    finally:
        shutil.rmtree(work, ignore_errors=True)
print(f"{alt_dir.name}: {'PASS' if not failed else 'FAIL'} ({len(seeds) - len(failed)}/{len(seeds)} seeds; failing {failed})", flush=True)
