"""Input tests for the lab-3 docstring claims (LX1-c round 1). Usage: python3 -I input_tests_lab3.py <checkout>

Claims tested (tests/labs/LX1/lab-LX1-project-3.py docstring, shown on project.html): a blank GBP cell raises
ValueError; a month that does not follow the previous one raises; no row is skipped or filled.
The blank-skipping mutant (ledgers/LX1/mutants/lx1c_m10_lab3_blank_cell_skipped.py) is told apart by a blank in the
LAST row: the original raises on the blank; the mutant drops the row, leaves no month gap, and exits 0.
"""
import shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
SNAP = ROOT / "course/assets/data/market/fx_monthly.csv"
ORIG = ROOT / "tests/labs/LX1/lab-LX1-project-3.py"
MUT = ROOT / "ledgers/LX1/mutants/lx1c_m10_lab3_blank_cell_skipped.py"
lines = SNAP.read_text(encoding="utf-8").splitlines(keepends=True)
header, body = lines[0], lines[1:]

def case(label: str, content: str) -> None:
    d = Path(tempfile.mkdtemp(prefix="lx1c-in-"))
    (d / "data").mkdir()
    (d / "data" / "fx_monthly.csv").write_text(content, encoding="utf-8")
    for name, script in (("original", ORIG), ("blank-skipping mutant", MUT)):
        r = subprocess.run([sys.executable, "-I", "-W", "error", str(script)], cwd=d, capture_output=True, text=True, timeout=60)
        last = (r.stderr.strip().splitlines() or ["<no stderr>"])[-1]
        print(f"{label}: {name} rc={r.returncode} stdout_lines={len(r.stdout.splitlines())} last_stderr={last[:140]}")
    shutil.rmtree(d)

# 1. blank GBP cell in the middle (GBP is the 7th field)
b = list(body); cells = b[300].rstrip("\n").split(","); cells[6] = ""; b[300] = ",".join(cells) + "\n"
case("blank_gbp_middle", header + "".join(b))
# 2. blank GBP cell in the last row
b = list(body); cells = b[-1].rstrip("\n").split(","); cells[6] = ""; b[-1] = ",".join(cells) + "\n"
case("blank_gbp_last_row", header + "".join(b))
# 3. a missing month in the middle
case("missing_month", header + "".join(body[:200] + body[201:]))
# 4. the untouched snapshot (control)
case("control_untouched", header + "".join(body))
