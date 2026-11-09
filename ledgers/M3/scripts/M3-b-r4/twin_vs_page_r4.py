"""Compare each lab page code block with its twin, run each twin alone under python -I -W error, and compare output with the expected block."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PY = str(ROOT / ".venv/bin/python")
for page in ["L04", "L05", "L06"]:
    src = (ROOT / f"course/modules/M/M3/{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, flags=re.S)
    code_page = html.unescape(m.group(1))
    twin_name = f"lab-M3-{page}-1.py"
    twin_text = (ROOT / "tests/labs/M3" / twin_name).read_text(encoding="utf-8")
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, flags=re.S).group(1)
    exp = html.unescape(exp)
    r = subprocess.run([PY, "-I", "-W", "error", str(ROOT / "tests/labs/M3" / twin_name)], capture_output=True, text=True, cwd="/tmp")
    out = r.stdout
    print(f"{page}: page_code_equals_twin={code_page == twin_text} exit={r.returncode} stderr_bytes={len(r.stderr.encode())}")
    print(f"{page}: expected_equals_output={exp.strip() == out.strip()}")
    if exp.strip() != out.strip():
        print("EXPECTED:\n" + exp + "\nOUTPUT:\n" + out)
    print(f"{page}: output lines:")
    print(out)
