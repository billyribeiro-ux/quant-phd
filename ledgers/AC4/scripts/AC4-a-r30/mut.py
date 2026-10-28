import subprocess, sys, glob, os
root = "/tmp/verify30-AC4-a"
py = f"{root}/.venv/bin/python"
base = {}
for lab in ("L01", "L02"):
    base[lab] = subprocess.run([py, "-I", "-W", "error", f"{root}/tests/labs/AC4/lab-AC4-{lab}-1.py"], capture_output=True, text=True).stdout
files = sorted(glob.glob(f"{root}/ledgers/AC4/mutants/AC4-a-r*/*.py"))
killed = surv = 0
for f in files:
    lab = "L01" if "/L01_" in f else "L02"
    r = subprocess.run([py, "-I", "-W", "error", f], capture_output=True, text=True, timeout=60)
    same = r.stdout == base[lab]
    status = "SURVIVED" if (r.returncode == 0 and same) else "KILLED"
    if status == "KILLED": killed += 1
    else: surv += 1
    print(status, r.returncode, os.path.relpath(f, root), "stdout_equal" if same else "stdout_differs")
print("total", len(files), "killed", killed, "survived", surv)
