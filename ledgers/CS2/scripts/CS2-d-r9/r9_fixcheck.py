"""Round-9: check the proposed grader fixes in scratch copies (the repo test file is not edited).
Runs a given test file with instance.py and a candidate streamstats.py for seeds in a range."""
import os, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
PY = ROOT / ".venv/bin/python"
test_file, candidate, seeds = Path(sys.argv[1]), Path(sys.argv[2]), range(int(sys.argv[3]), int(sys.argv[4]) + 1)
bad = []
for seed in seeds:
    w = Path(tempfile.mkdtemp(prefix="cs2fix_"))
    try:
        shutil.copy(ROOT / "course/modules/CS/CS2/grader/instance.py", w / "instance.py")
        shutil.copy(test_file, w / "test_project.py")
        shutil.copy(candidate, w / "streamstats.py")
        p = subprocess.run([str(PY), "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                           cwd=w, env=dict(os.environ, QF_SEED=str(seed)), capture_output=True, text=True, timeout=300)
        if p.returncode != 0:
            bad.append((seed, [l for l in p.stdout.splitlines() if l.startswith("FAILED")][:2]))
    finally:
        shutil.rmtree(w, ignore_errors=True)
print(f"{test_file.name} vs {candidate.name} seeds {seeds.start}-{seeds.stop-1}: failing seeds {len(bad)}; first {bad[:2]}")
