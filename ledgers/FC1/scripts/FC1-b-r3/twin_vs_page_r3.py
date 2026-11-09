"""Verifier script (FC1-b round 3): page code == twin, twin runs alone under python -I -W error, expected == stdout."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PAGES = {"L04": "lab-FC1-L04-1", "L05": "lab-FC1-L05-1"}
ok = True
for page, lab in PAGES.items():
    text = (ROOT / f"course/modules/FC/FC1/{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    twin = (ROOT / f"tests/labs/FC1/{lab}.py").read_text(encoding="utf-8")
    same = code.rstrip("\n") == twin.rstrip("\n")
    markers = text.count("@@LAB") + text.count("@@OUT")
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1))
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/FC1/{lab}.py")],
        capture_output=True, text=True, cwd="/tmp", timeout=60,
    )
    exp_ok = expected.strip("\n") == run.stdout.strip("\n")
    print(f"{page}: page_code_bytes={len(code)} twin_bytes={len(twin)} identical={same} markers={markers} "
          f"rc={run.returncode} stderr_bytes={len(run.stderr)} expected_equals_stdout={exp_ok} stdout_lines={run.stdout.count(chr(10))}")
    ok = ok and same and markers == 0 and run.returncode == 0 and not run.stderr and exp_ok
print("ALL OK" if ok else "FAIL")
