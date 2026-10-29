import pathlib, re, shutil, subprocess, sys, tempfile, os
R = pathlib.Path(sys.argv[1])
G = R / "course/modules/M/M3/grader"
ref = (G / "reference.py").read_text()
# (name, old, new): single-line edits of the mutant's real change, applied to the CURRENT reference
edits = {
  "r11d_m02_stop_on_step_only": ("        if gap <= tol and step <= tol:", "        if step <= tol:"),
  "r6d_m04_stop_on_gap_only": ("        if gap <= tol and step <= tol:", "        if gap <= tol:"),
  "r9d_m02_return_last_psd_iterate": ("    return x\n", "    return y\n"),
  "r12d_m01_weights_accept_nan": ("    if not all(float(v) > 0.0 for v in vols):", "    if any(float(v) <= 0.0 for v in vols):"),
}
py = sys.executable
for name, (old, new) in edits.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    mut = ref.replace(old, new)
    fails = []
    for seed in range(50):
        w = pathlib.Path(tempfile.mkdtemp(prefix="pm-"))
        for n in ["test_project.py", "instance.py"]:
            shutil.copy(G / n, w / n)
        (w / "covariance_doctor.py").write_text(mut)
        env = dict(os.environ, QF_SEED=str(seed))
        r = subprocess.run([py, "-m", "pytest", "--assert=plain", "-W", "error", "-q", "-p", "no:cacheprovider", "-x", "test_project.py"], cwd=w, capture_output=True, text=True, env=env)
        if r.returncode != 0:
            fails.append((seed, [l for l in r.stdout.splitlines() if l.startswith("FAILED")][:1]))
        shutil.rmtree(w)
    print(name, "killed on", len(fails), "of 50 seeds; first:", fails[0] if fails else "SURVIVED on all 50 seeds")
