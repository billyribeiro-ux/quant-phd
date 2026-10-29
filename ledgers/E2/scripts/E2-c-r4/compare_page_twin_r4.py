"""Compare each lab's page code block and expected block with its twin and its live stdout."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
for lesson in ["L07", "L08", "L09"]:
    page = (ROOT / f"course/modules/E/E2/{lesson}.html").read_text(encoding="utf-8")
    twin_path = ROOT / f"tests/labs/E2/lab-E2-{lesson}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    code = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    exp = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code_text = html.unescape(code[0]) if code else None
    exp_text = html.unescape(exp[0]) if exp else None
    out = subprocess.run(
        [str(ROOT / ".venv/bin/python"), "-I", "-W", "error", str(twin_path)],
        capture_output=True, text=True, cwd="/tmp",
    ).stdout
    print(lesson, "n_code_blocks", len(code), "n_expected", len(exp))
    print("  code == twin (modulo trailing newline):", code_text is not None and code_text.rstrip("\n") == twin.rstrip("\n"))
    print("  expected == stdout (modulo trailing newline):", exp_text is not None and exp_text.rstrip("\n") == out.rstrip("\n"))
    print("  expected lines:", len((exp_text or "").splitlines()), "stdout lines:", len(out.splitlines()))
