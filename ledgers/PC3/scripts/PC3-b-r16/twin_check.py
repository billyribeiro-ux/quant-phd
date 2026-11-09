"""PC3-b round 16: for L04-L06, (1) the page's data-run code equals the twin file byte for byte (after HTML
unescaping); (2) the twin runs alone under python -I -W error and exits 0; (3) the stdout equals the page's
pre.expected block (after HTML unescaping, trailing whitespace stripped per line).

Usage: python -I ledgers/PC3/scripts/PC3-b-r16/twin_check.py <repo-root> <python-exe>
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
py = sys.argv[2]
for page, lab in (("L04", "lab-PC3-L04-1"), ("L05", "lab-PC3-L05-1"), ("L06", "lab-PC3-L06-1")):
    s = (root / "course/modules/PC/PC3" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<section class="lab" id="' + lab + r'".*?<pre><code class="language-python" data-run>(.*?)</code></pre>', s, flags=re.S)
    code = html.unescape(m.group(1))
    twin = (root / "tests/labs/PC3" / f"{lab}.py").read_text(encoding="utf-8")
    same = code == twin
    print(f"{page} page code == twin {lab}.py: {same} (page {len(code)} bytes, twin {len(twin)} bytes)")
    if not same:
        import difflib
        for line in list(difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm=""))[:40]:
            print("   ", line)
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', s[m.end():], flags=re.S)
    expected = html.unescape(e.group(1))
    r = subprocess.run([py, "-I", "-W", "error", str(root / "tests/labs/PC3" / f"{lab}.py")], capture_output=True, text=True, cwd="/tmp")
    print(f"{lab}: exit={r.returncode} stderr_bytes={len(r.stderr)}")
    out_lines = [x.rstrip() for x in r.stdout.rstrip("\n").split("\n")]
    exp_lines = [x.rstrip() for x in expected.rstrip("\n").split("\n")]
    eq = out_lines == exp_lines
    print(f"{lab}: stdout == expected block: {eq} (out {len(out_lines)} lines, expected {len(exp_lines)} lines)")
    if not eq:
        import difflib
        for line in list(difflib.unified_diff(exp_lines, out_lines, lineterm=""))[:40]:
            print("   ", line)
