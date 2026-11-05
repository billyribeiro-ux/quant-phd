"""Compare each E4 slice page's data-run code and expected block with its lab twin and the twin's real stdout."""

import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
PAIRS = [("L01", "lab-E4-L01-1"), ("L02", "lab-E4-L02-1"), ("L03", "lab-E4-L03-1")]
ok_all = True
for page, lab in PAIRS:
    text = (ROOT / "course/modules/E/E4" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    twin_path = ROOT / "tests/labs/E4" / f"{lab}.py"
    twin = twin_path.read_text(encoding="utf-8")
    code_eq = code.rstrip("\n") == twin.rstrip("\n")
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1))
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)],
        capture_output=True,
        text=True,
        cwd="/tmp",
        timeout=60,
    )
    out_eq = expected.rstrip("\n") == run.stdout.rstrip("\n")
    print(f"{page} code_equals_twin={code_eq} expected_equals_stdout={out_eq} exit={run.returncode} stderr_bytes={len(run.stderr)}")
    ok_all = ok_all and code_eq and out_eq and run.returncode == 0 and run.stderr == ""
    print("data-run placeholders:", re.findall(r"@@(?:LAB|OUT):[^@]*@@", text))
print("ALL_OK" if ok_all else "MISMATCH")
