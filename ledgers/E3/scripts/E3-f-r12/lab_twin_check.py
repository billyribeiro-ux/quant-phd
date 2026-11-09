"""Verifier check (E3 slice f, round 12): page lab code equals the twin; expected block equals twin output."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
for n in (1, 2, 3, 4):
    page = (ROOT / f"course/modules/E/E3/L0{n}.html").read_text(encoding="utf-8")
    twin_path = ROOT / f"tests/labs/E3/lab-E3-L0{n}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1)
    code = html.unescape(code)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)
    expected = html.unescape(expected)
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd=ROOT)
    out = run.stdout
    code_eq = code.strip() == twin.strip()
    exp_eq = expected.strip() == out.strip()
    print(f"L0{n}: page_code_equals_twin={code_eq} (page {len(code)} chars, twin {len(twin)} chars); "
          f"expected_equals_output={exp_eq}; exit={run.returncode}; stderr_bytes={len(run.stderr)}")
    if not code_eq:
        import difflib
        print("\n".join(list(difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm=""))[:40]))
    if not exp_eq:
        import difflib
        print("\n".join(list(difflib.unified_diff(out.splitlines(), expected.splitlines(), lineterm=""))[:40]))
