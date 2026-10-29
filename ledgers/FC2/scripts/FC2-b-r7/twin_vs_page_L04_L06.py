"""FC2-a round 4: page code and page expected block versus the lab twins.

For each lesson page L01..L03: extract the <code data-run> block and the <pre class="expected"> block,
HTML-unescape them, compare the page code with the twin (modulo one trailing newline), run the twin under
`python -I -W error`, and compare its stdout with the expected block (modulo trailing whitespace).
Usage: python -I -W error twin_vs_page.py <repo_root>
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
ok = True
for lesson, twin_id in [("L04", "lab-FC2-L04-1"), ("L05", "lab-FC2-L05-1"), ("L06", "lab-FC2-L06-1")]:
    page = (root / "course/modules/FC/FC2" / f"{lesson}.html").read_text(encoding="utf-8")
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    twin_path = root / "tests/labs/FC2" / f"{twin_id}.py"
    twin = twin_path.read_text(encoding="utf-8")
    same_code = code.rstrip("\n") == twin.rstrip("\n")
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp"
    )
    same_out = run.stdout.rstrip() == expected.rstrip()
    print(f"{lesson}: page code == twin: {same_code}; twin exit {run.returncode} stderr_len {len(run.stderr)}; "
          f"stdout == expected block: {same_out}; twin lines {twin.count(chr(10))}")
    if not (same_code and run.returncode == 0 and same_out):
        ok = False
        print("DIFF stdout:\n" + run.stdout)
        print("EXPECTED:\n" + expected)
        print("STDERR:\n" + run.stderr)
print("twin_vs_page PASS" if ok else "twin_vs_page FAIL")
