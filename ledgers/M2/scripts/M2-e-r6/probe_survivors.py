"""Show that the two surviving round-6 mutants are killed by strengthened probe tests (not applied to the grader).
Run: python probe_survivors.py <repo_root>. Prints one line per (file, probe) with pass/fail."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1])
GRADER = ROOT / "course/modules/M/M2/grader"
MUT = ROOT / "ledgers/M2/mutants"
PROBES = '''

def test_probe_large_step_value_is_the_quotient() -> None:
    coeffs, x0 = INST["cubic"], INST["x0"]
    f = lambda x: float(cubic(coeffs, x))
    for h in (1.0, 5.0):
        want = (f(x0 + h) - f(x0)) / h
        got = sol.fd_derivative(f, x0, h, "forward")
        require(close(got, want, 1e-9), "probe: forward quotient at a large step")


def test_probe_hessian_step_one_nonpolynomial() -> None:
    import math as _m
    f = lambda p: _m.sin(p[0]) * _m.cos(p[1])
    point, h = [0.3, 0.2], 1.0
    got = sol.hessian_fd(f, point, h)
    x, y = point
    want00 = (f([x + h, y]) - 2 * f(point) + f([x - h, y])) / (h * h)
    require(close(got[0][0], want00, 1e-9), "probe: diagonal formula at step one, non-polynomial")
'''
for name, path in (("reference", GRADER / "reference.py"),
                   ("r6_01", MUT / "r6_01_fd_step_silently_capped_at_one.py"),
                   ("r6_02", MUT / "r6_02_hessian_step_silently_capped_at_a_thousandth.py")):
    with tempfile.TemporaryDirectory() as work:
        shutil.copy(GRADER / "instance.py", work)
        Path(work, "test_project.py").write_text((GRADER / "test_project.py").read_text(encoding="utf-8") + PROBES, encoding="utf-8")
        shutil.copy(path, Path(work, "sensitivity_engine.py"))
        out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                              "test_project.py", "-k", "probe"], cwd=work, capture_output=True, text=True, env={"QF_SEED": "0", "PATH": "/usr/bin:/bin"})
        print(f"{name}: exit {out.returncode} ({out.stdout.strip().splitlines()[-1]})")
