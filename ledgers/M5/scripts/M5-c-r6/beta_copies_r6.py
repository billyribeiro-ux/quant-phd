"""Round-6: run copies of the L08 twin with BETA changed (not the page), to re-check the iteration counts in card M5-c139 and the page's E1 figures."""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
src = (ROOT / "tests/labs/M5/lab-M5-L08-1.py").read_text(encoding="utf-8")
print("BETA line in twin:", [l for l in src.splitlines() if re.match(r"^BETA\b", l)])
for b in ("0.5", "0.9", "0.95"):
    code = re.sub(r"^BETA(\s*[:=][^\n]*)=?.*$", lambda m: f"BETA{m.group(1).split('=')[0]}= {b}", src, count=1, flags=re.M)
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "copy.py"
        p.write_text(code, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", "-W", "error", str(p)], capture_output=True, text=True, cwd=d)
    m = re.search(r"part A: iterations until the successive gap is at most 1e-12 = (\d+)", r.stdout)
    print(f"BETA={b}: exit={r.returncode} stderr_bytes={len(r.stderr)} iterations={m.group(1) if m else None}")
