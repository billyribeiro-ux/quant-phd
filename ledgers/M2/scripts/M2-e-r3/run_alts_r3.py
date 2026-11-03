import os, shutil, subprocess, sys, pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD3-M2-e")
GRADER = ROOT / "course/modules/M/M2/grader"
ALTS = ROOT / "ledgers/M2/scripts/M2-e-r3/alts"
PY = str(ROOT / ".venv/bin/python")
work_root = pathlib.Path("/tmp/m2e_r3/alts_work")
shutil.rmtree(work_root, ignore_errors=True)
cases = {"reference": GRADER / "reference.py"}
for name in ["alt1_richardson_central", "alt2_complex_step", "alt3_reverse_mode", "alt4_exact_rational", "alt5_numpy"]:
    cases[name] = ALTS / f"{name}.py"
seeds = range(0, 50)
for name, path in cases.items():
    d = work_root / name
    d.mkdir(parents=True)
    shutil.copy(GRADER / "test_project.py", d)
    shutil.copy(GRADER / "instance.py", d)
    shutil.copy(GRADER / "reference.py", d / "reference_core.py")
    shutil.copy(path, d / "sensitivity_engine.py")
    fails = []
    for s in seeds:
        env = dict(os.environ, QF_SEED=str(s))
        r = subprocess.run([PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                           cwd=d, env=env, capture_output=True, text=True)
        if r.returncode != 0:
            last = [l for l in r.stdout.splitlines() if l.startswith("FAILED")]
            fails.append((s, last[:3] if last else r.stdout[-300:]))
    print(f"{name}: {len(seeds)-len(fails)}/{len(seeds)} seeds pass")
    for f in fails[:5]:
        print("   FAIL", f)
