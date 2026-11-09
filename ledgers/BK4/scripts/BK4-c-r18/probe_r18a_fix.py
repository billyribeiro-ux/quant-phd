"""Round 18 (BK4 slice c): probe that a candidate full-cover test kills r18a and the reference still passes.
Copies the grader into a scratch directory, appends the candidate test, and runs it. Usage: python -I probe_r18a_fix.py <checkout-root>"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(sys.argv[1])
G = ROOT / "course/modules/BK/BK4/grader"
PY = str(ROOT / ".venv/bin/python")
CANDIDATE = '''

def test_full_target_margin_is_the_largest_loss_in_any_order() -> None:
    """Probe for the fix (not part of the submitted suite): a full target takes the largest loss, wherever it sits."""
    __tracebackhide__ = True
    assert sol.margin_for_cover([30, 50, 10, 20], 10_000) == 50, "full cover needs every scenario, so the margin is the largest loss"
'''
for label, impl in (("r18a", ROOT / "ledgers/BK4/mutants/r18a_full_cover_margin_is_last_loss_given.py"), ("reference", G / "reference.py")):
    W = pathlib.Path(tempfile.mkdtemp(prefix="bk4c_r18_probe_"))
    try:
        shutil.copy(G / "instance.py", W / "instance.py")
        shutil.copy(G / "test_project.py", W / "test_project.py")
        with open(W / "test_project.py", "a", encoding="utf-8") as fh:
            fh.write(CANDIDATE)
        shutil.copy(impl, W / "clearing_house.py")
        r = subprocess.run([PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                           cwd=W, env={"QF_SEED": "0", "PATH": "/usr/bin:/bin"}, capture_output=True, text=True, check=False)
        print(label, "exit", r.returncode, "|", r.stdout.strip().splitlines()[-1])
    finally:
        shutil.rmtree(W, ignore_errors=True)
