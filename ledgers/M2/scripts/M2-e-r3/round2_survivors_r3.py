"""Round-3: re-create the round-2 surviving-mutant classes in a scratch directory and show the suite kills each one."""

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
GRADER = ROOT / "course/modules/M/M2/grader"
PY = str(ROOT / ".venv/bin/python")
work = pathlib.Path("/tmp/m2e_r3/kill_r3")
work.mkdir(parents=True, exist_ok=True)
ref = (GRADER / "reference.py").read_text(encoding="utf-8")
(work / "test_project.py").write_text((GRADER / "test_project.py").read_text(encoding="utf-8"), encoding="utf-8")
(work / "instance.py").write_text((GRADER / "instance.py").read_text(encoding="utf-8"), encoding="utf-8")
variants = {
    "v2_01 numerical dprice_dy": ref.replace('"dprice_dy": first,', '"dprice_dy": (sum(c * (1 / (1 + rate + 1e-5)) ** t for t, c in flows) - sum(c * (1 / (1 + rate - 1e-5)) ** t for t, c in flows)) / 2e-5,'),
    "v2_02 numerical d2price_dy2": ref.replace('"d2price_dy2": second,', '"d2price_dy2": (sum(c * (1 / (1 + rate + 1e-5)) ** t for t, c in flows) - 2 * price + sum(c * (1 / (1 + rate - 1e-5)) ** t for t, c in flows)) / 1e-10,'),
    "v2_03 forward step floored at 1e-8": ref.replace("    step = _positive_step(h)\n    if scheme == \"forward\":", "    step = max(_positive_step(h), 1e-8)\n    if scheme == \"forward\":"),
}
for name, src in variants.items():
    assert src != ref, name
    (work / "sensitivity_engine.py").write_text(src, encoding="utf-8")
    r = subprocess.run([PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                       cwd=work, env={"QF_SEED": "0", "PATH": "/usr/bin:/bin"}, capture_output=True, text=True)
    failed = [l.split("::")[1].split(" ")[0] for l in r.stdout.splitlines() if l.startswith("FAILED")]
    print(f"{name}: rc={r.returncode} failed={len(failed)} e.g. {failed[:2]}")
(work / "sensitivity_engine.py").write_text(ref, encoding="utf-8")
r = subprocess.run([PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                   cwd=work, env={"QF_SEED": "0", "PATH": "/usr/bin:/bin"}, capture_output=True, text=True)
print(f"reference: rc={r.returncode} {r.stdout.strip().splitlines()[-1]}")
