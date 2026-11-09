"""Round-15 verifier: does anything exercise the lab's two-pass / statistics.stdev agreement raise?

Usage: python -I agreement_r16.py <checkout_root> <lab.py>...
The wrapper makes statistics.stdev return the true value plus 1e-6 (a disagreement of 1e-4 percent per month,
far above the 1e-9 tolerance the page states), then runs the lab with runpy under python -I -W error on the
real snapshot. The twin must raise the agreement ValueError; a candidate that still prints the expected block
with rc 0 has no agreement check.
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(sys.argv[1]).resolve()
WRAPPER = """
import runpy, statistics, sys
_orig = statistics.stdev
statistics.stdev = lambda xs: _orig(xs) + 1e-6
runpy.run_path(sys.argv[1], run_name="__main__")
"""
for arg in sys.argv[2:]:
    lab = pathlib.Path(arg).resolve()
    with tempfile.TemporaryDirectory(prefix="lx1c_r16_agree_") as tmp:
        tmp_path = pathlib.Path(tmp)
        (tmp_path / "data").mkdir()
        shutil.copy(ROOT / "course/assets/data/market/fx_monthly.csv", tmp_path / "data" / "fx_monthly.csv")
        wrap = tmp_path / "wrap.py"
        wrap.write_text(WRAPPER, encoding="utf-8")
        p = subprocess.run([sys.executable, "-I", "-W", "error", str(wrap), str(lab)], cwd=tmp,
                           capture_output=True, text=True, timeout=120)
    last = p.stderr.strip().splitlines()[-1] if p.stderr.strip() else ""
    print(f"{lab.name}: rc={p.returncode} stdout_lines={len(p.stdout.splitlines())} last_stderr={last[:120]!r}")
