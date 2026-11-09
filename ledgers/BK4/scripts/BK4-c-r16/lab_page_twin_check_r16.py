"""Round-16 check of each project-page lab block against its twin (slice c).

Run from the checkout root with the checkout's .venv python in isolated mode. For each lab: the page code equals the
twin after HTML unescape and stripping the final newline; for the completion lab (lab 2) the page code with the two
blanks replaced by the twin's expressions equals the twin; the twin runs alone under -I -W error with exit 0 and no
stderr; the twin's stdout equals the page's expected block.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
page = (ROOT / "course/modules/BK/BK4/project.html").read_text(encoding="utf-8")
blocks = re.findall(
    r'<section class="lab[^"]*" id="(lab-BK4-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>',
    page,
    flags=re.S,
)
print("labs found on page:", [b[0] for b in blocks])
for lab_id, code_html, expected_html in blocks:
    code = html.unescape(code_html).rstrip("\n")
    expected = html.unescape(expected_html)
    n = lab_id[-1]
    twin_path = ROOT / f"tests/labs/BK4/lab-BK4-project-{n}.py"
    twin = twin_path.read_text(encoding="utf-8").rstrip("\n")
    print(f"{lab_id}: page code == twin (trailing newline ignored): {code == twin}")
    if "___" in code:
        filled = code.replace("{m: ___ for m in survivors}", "{m: residual * FUND[m] // pool for m in survivors}")
        filled = filled.replace("index = ___", "index = -((-target * count) // 10_000)")
        print(f"{lab_id}: blanks present: {code.count('___')}; page code with the twin's expressions == twin: {filled == twin}")
    result = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, check=False)
    print(f"{lab_id}: twin exit {result.returncode}, stderr {len(result.stderr)} chars")
    same_out = result.stdout.rstrip("\n") == expected.rstrip("\n")
    print(f"{lab_id}: twin stdout == page expected block: {same_out}")
