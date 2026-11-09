"""Compare each slice lab page's embedded code and expected block with its twin and the twin's real output.

Usage: python -I lab_embed_check.py <checkout_root>
Prints one line per lab: code_equal, expected_equal, and the sha256 of the twin's stdout.
"""

import hashlib
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
py = root / ".venv" / "bin" / "python"
ok = True
for n in range(13, 19):
    page = (root / f"course/modules/M/M2/L{n}.html").read_text(encoding="utf-8")
    twin_path = root / f"tests/labs/M2/lab-M2-L{n}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    m_code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    m_exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(m_code.group(1)) if m_code else None
    expected = html.unescape(m_exp.group(1)) if m_exp else None
    out = subprocess.run([str(py), "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp")
    code_eq = code is not None and code.strip() == twin.strip()
    exp_eq = expected is not None and expected.strip() == out.stdout.strip()
    ok = ok and code_eq and exp_eq and out.returncode == 0 and not out.stderr
    print(
        f"L{n}: code_equal={code_eq} expected_equal={exp_eq} run_exit={out.returncode} "
        f"stderr_bytes={len(out.stderr)} stdout_sha256={hashlib.sha256(out.stdout.encode()).hexdigest()[:16]} "
        f"code_blocks={len(re.findall(r'data-run', page))} expected_blocks={len(re.findall(r'class=\"expected\"', page))}"
    )
print("ALL_OK" if ok else "MISMATCH")
