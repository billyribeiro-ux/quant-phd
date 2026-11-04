"""Run each alternative correct engine against the M2 grader test suite on seeds 0-49 (verifier round 5)."""

import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD5-M2-e")
GRADER = ROOT / "course/modules/M/M2/grader"
PY = str(ROOT / ".venv/bin/python")
WORK = pathlib.Path("/tmp/m2e_r5/alts_work")
CASES = {
    "reference": GRADER / "reference.py",
    "r3_alt1_richardson_central": ROOT / "ledgers/M2/scripts/M2-e-r3/alts/alt1_richardson_central.py",
    "r3_alt2_complex_step": ROOT / "ledgers/M2/scripts/M2-e-r3/alts/alt2_complex_step.py",
    "r3_alt3_reverse_mode": ROOT / "ledgers/M2/scripts/M2-e-r3/alts/alt3_reverse_mode.py",
    "r3_alt4_exact_rational": ROOT / "ledgers/M2/scripts/M2-e-r3/alts/alt4_exact_rational.py",
    "r3_alt5_numpy": ROOT / "ledgers/M2/scripts/M2-e-r3/alts/alt5_numpy.py",
    "r5_alt_a_decimal_rounding_fsum": ROOT / "ledgers/M2/scripts/M2-e-r5/alts_r5/alt_r5_a_decimal_rounding_fsum.py",
    "r5_alt_b_iterative_discounting": ROOT / "ledgers/M2/scripts/M2-e-r5/alts_r5/alt_r5_b_iterative_discounting.py",
}
shutil.rmtree(WORK, ignore_errors=True)
for name, path in CASES.items():
    d = WORK / name
    d.mkdir(parents=True)
    shutil.copy(GRADER / "test_project.py", d)
    shutil.copy(GRADER / "instance.py", d)
    shutil.copy(GRADER / "reference.py", d / "reference_core.py")
    shutil.copy(path, d / "sensitivity_engine.py")
    fails = []
    for seed in range(50):
        env = dict(os.environ, QF_SEED=str(seed))
        r = subprocess.run(
            [PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=d, env=env, capture_output=True, text=True,
        )
        if r.returncode != 0:
            last = [line for line in r.stdout.splitlines() if line.startswith("FAILED")]
            fails.append((seed, last[:2] if last else r.stdout[-200:]))
    print(f"{name}: {50 - len(fails)}/50 seeds pass")
    for f in fails[:4]:
        print("   FAIL", f)
    sys.stdout.flush()
