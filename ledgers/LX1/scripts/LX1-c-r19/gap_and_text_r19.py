"""LX1-c round 19: distinguishing inputs for the Lab 3 Check paragraph (run as python -I -W error).

Usage: python -I gap_and_text_r19.py <checkout_root>. Builds three scratch snapshots from the committed CSV:
(a) one month dropped (1985-03), (b) a non-decimal GBP cell ('n/a' at 1985-03), (c) an exact duplicate
of a month (1985-03 repeated). The twin must raise ValueError on each, as the page's Check paragraph states.
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

root = pathlib.Path(sys.argv[1]).resolve()
twin = root / "tests/labs/LX1/lab-LX1-project-3.py"
snap = (root / "course/assets/data/market/fx_monthly.csv").read_text(encoding="utf-8").splitlines()
line = next(i for i, l in enumerate(snap) if l.startswith("1985-03,"))
variants = {
    "dropped_month": snap[:line] + snap[line + 1:],
    "non_decimal_cell": snap[:line] + [",".join(c if i != 6 else "n/a" for i, c in enumerate(snap[line].split(","))) ] + snap[line + 1:],
    "repeated_month": snap[:line] + [snap[line]] + snap[line:],
}
for name, lines in variants.items():
    with tempfile.TemporaryDirectory() as tmp:
        (pathlib.Path(tmp) / "data").mkdir()
        (pathlib.Path(tmp) / "data" / "fx_monthly.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
        p = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], cwd=tmp, capture_output=True, text=True)
    last = p.stderr.strip().splitlines()[-1] if p.stderr.strip() else ""
    print(f"{name}: rc={p.returncode} stdout_lines={len(p.stdout.splitlines())} last_stderr={last}")
