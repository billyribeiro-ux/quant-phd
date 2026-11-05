"""Round-10 slice-d check: page code of each M4 project lab equals its twin, and each expected block equals the twin's output."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD10-M4-d")
PAGE = ROOT / "course/modules/M/M4/project.html"
text = PAGE.read_text(encoding="utf-8")
blocks = re.findall(r'<section class="lab[^"]*" id="(lab-M4-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
for lab_id, code, expected in blocks:
    code = html.unescape(code)
    twin = (ROOT / f"tests/labs/M4/lab-M4-{lab_id.split('-', 2)[2]}.py" if False else ROOT / "tests/labs/M4" / f"{lab_id.replace('lab-', 'lab-')}.py")
    twin_text = twin.read_text(encoding="utf-8")
    same = code.strip() == twin_text.strip()
    diff_lines = []
    if not same:
        import difflib
        diff_lines = [l for l in difflib.unified_diff(twin_text.strip().splitlines(), code.strip().splitlines(), lineterm="", n=0)]
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd="/tmp")
    out = run.stdout.rstrip("\n")
    exp = html.unescape(expected).rstrip("\n")
    print(f"== {lab_id}: page code == twin: {same}; twin exit {run.returncode}; stderr bytes {len(run.stderr)}; expected == output: {exp == out}")
    for l in diff_lines:
        print("   ", l)
    if exp != out:
        print("--- expected\n" + exp + "\n--- output\n" + out)
