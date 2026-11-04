"""Re-run the patched round-5 alternative A against the M2 grader on seeds 0-49 (verifier round 5)."""

import os
import pathlib
import shutil
import subprocess

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD5-M2-e")
GRADER = ROOT / "course/modules/M/M2/grader"
PY = str(ROOT / ".venv/bin/python")
ALT = ROOT / "ledgers/M2/scripts/M2-e-r5/alts_r5/alt_r5_a_decimal_rounding_fsum.py"
d = pathlib.Path("/tmp/m2e_r5/alts_work/r5_alt_a_patched")
shutil.rmtree(d, ignore_errors=True)
d.mkdir(parents=True)
shutil.copy(GRADER / "test_project.py", d)
shutil.copy(GRADER / "instance.py", d)
shutil.copy(GRADER / "reference.py", d / "reference_core.py")
shutil.copy(ALT, d / "sensitivity_engine.py")
fails = []
for seed in range(50):
    env = dict(os.environ, QF_SEED=str(seed))
    r = subprocess.run(
        [PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
        cwd=d, env=env, capture_output=True, text=True,
    )
    if r.returncode != 0:
        fails.append((seed, [l for l in r.stdout.splitlines() if l.startswith("FAILED")][:2]))
print(f"r5_alt_a_decimal_rounding_fsum (patched precision): {50 - len(fails)}/50 seeds pass")
for f in fails[:4]:
    print("   FAIL", f)
