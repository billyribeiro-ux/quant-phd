"""Round-13: page code equals lab twin; expected block equals the twin's stdout (run under python -I -W error)."""
import html
import re
import subprocess
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE13-E4-b"
PY = f"{ROOT}/.venv/bin/python"
for lesson in ("L04", "L05", "L06"):
    page = open(f"{ROOT}/course/modules/E/E4/{lesson}.html", encoding="utf-8").read()
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    twin_path = f"{ROOT}/tests/labs/E4/lab-E4-{lesson}-1.py"
    twin = open(twin_path, encoding="utf-8").read()
    print(f"{lesson}: page code lines {code.count(chr(10))+1} twin lines {twin.count(chr(10))+1} identical={code == twin}")
    if code != twin:
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page"))[:60]))
    run = subprocess.run([PY, "-I", "-W", "error", twin_path], capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"}, cwd="/tmp")
    print(f"{lesson}: twin exit={run.returncode} stderr_bytes={len(run.stderr)}")
    out = run.stdout
    print(f"{lesson}: expected block == stdout: {expected.strip() == out.strip()}  (expected lines {expected.strip().count(chr(10))+1}, stdout lines {out.strip().count(chr(10))+1})")
    if expected.strip() != out.strip():
        print(difflib_out := "\n".join(__import__('difflib').unified_diff(expected.strip().splitlines(), out.strip().splitlines(), 'expected', 'stdout', lineterm='')))
