"""Round-6 verifier (slice d): run ledgers/M4/equivalent/m17 through the grader suite on seeds 0..49 (claimed conforming)."""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, run_suite, workspace  # noqa: E402

u = unit("M4")
cfg = panel(u)
src = ROOT / "ledgers" / "M4" / "equivalent" / "m17_student_t_second_seed.py"
failed = []
for seed in range(50):
    work = workspace(u, src, cfg)
    try:
        ok, output, _ = run_suite(work, cfg["suite"], seed)
        if not ok:
            failed.append((seed, re.findall(r"FAILED \S+::(\S+)", output)[:2]))
    finally:
        shutil.rmtree(work, ignore_errors=True)
print("m17 seeds failing:", len(failed), failed[:5])
print("m17 seeds passing:", 50 - len(failed), "of 50")
