"""LX2-c r12: page code and expected blocks of the three project labs vs their twins, and vs the twin's real output.

Reads course/modules/LX/LX2/project.html (repo-relative), extracts each <pre><code data-run> block and the following
<pre class="expected"> block, unescapes HTML entities, and compares with tests/labs/LX2/lab-LX2-project-N.py
(code) and with the stdout of running that twin under python -I -W error (expected).
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/LX/LX2/project.html").read_text(encoding="utf-8")
code_blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
expected_blocks = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("code blocks:", len(code_blocks), "expected blocks:", len(expected_blocks))
for n in (1, 2, 3):
    twin = (root / f"tests/labs/LX2/lab-LX2-project-{n}.py").read_text(encoding="utf-8")
    page_code = html.unescape(code_blocks[n - 1])
    same_code = page_code.rstrip("\n") == twin.rstrip("\n")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/LX2/lab-LX2-project-{n}.py")],
                         capture_output=True, text=True)
    out = run.stdout.rstrip("\n")
    exp = html.unescape(expected_blocks[n - 1]).rstrip("\n")
    print(f"lab {n}: page code == twin: {same_code}; twin exit={run.returncode}; stderr={run.stderr!r}; "
          f"expected block == twin stdout: {exp == out}")
    if page_code.rstrip("\n") != twin.rstrip("\n"):
        import difflib
        print("\n".join(difflib.unified_diff(twin.splitlines(), page_code.splitlines(), lineterm="")))
    if exp != out:
        import difflib
        print("\n".join(difflib.unified_diff(out.splitlines(), exp.splitlines(), lineterm="")))
