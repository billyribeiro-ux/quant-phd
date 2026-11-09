"""Round-4 check: page lab code equals its twin; page expected block equals the twin's stdout (run alone, python -I -W error)."""
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PY = str(ROOT / ".venv" / "bin" / "python")
ok_all = True
for lesson in ("L04", "L05", "L06"):
    page = (ROOT / f"course/modules/E/E1/{lesson}.html").read_text(encoding="utf-8")
    twin_path = ROOT / f"tests/labs/E1/lab-E1-{lesson}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    m_code = re.search(r'<section class="lab" id="lab-E1-%s-1".*?<pre><code[^>]*>(.*?)</code></pre>' % lesson, page, re.S)
    m_exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(m_code.group(1))
    expected = html.unescape(m_exp.group(1))
    code_eq = code.rstrip("\n") == twin.rstrip("\n")
    tmp = Path(tempfile.mkdtemp(prefix=f"twin_{lesson}_"))
    shutil.copy(twin_path, tmp / "twin.py")
    r = subprocess.run([PY, "-I", "-W", "error", "twin.py"], cwd=tmp, capture_output=True, text=True, timeout=120)
    exp_eq = expected.strip() == r.stdout.strip()
    print(f"{lesson}: rc={r.returncode} stderr_bytes={len(r.stderr)} page_code_equals_twin={code_eq} expected_equals_stdout={exp_eq} stdout_lines={len(r.stdout.splitlines())}")
    if not (code_eq and exp_eq and r.returncode == 0 and not r.stderr):
        ok_all = False
        if not exp_eq:
            import difflib
            print("\n".join(difflib.unified_diff(expected.strip().splitlines(), r.stdout.strip().splitlines(), "page", "twin", lineterm="")))
        if not code_eq:
            import difflib
            print("\n".join(list(difflib.unified_diff(code.rstrip().splitlines(), twin.rstrip().splitlines(), "page", "twin", lineterm=""))[:40]))
    shutil.rmtree(tmp)
print("ALL OK" if ok_all else "MISMATCH")
sys.exit(0 if ok_all else 1)
