"""Round-4 verifier (E3-d): page lab code vs its twin, and the expected block vs the twin's output.

Runs each twin under python -I -W error (stdout captured), then compares: (a) page code with the twin, line by line,
after HTML unescaping; (b) the page's expected block with the twin's stdout (modulo a final newline).
"""
import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
page = (ROOT / "course/modules/E/E3/project.html").read_text(encoding="utf-8")
sections = {m.group(1): m.group(0) for m in re.finditer(r'<section class="lab[^"]*" id="(lab-E3-project-\d)".*?</section>', page, flags=re.S)}
for lab_id in ("lab-E3-project-1", "lab-E3-project-2", "lab-E3-project-3"):
    sec = sections[lab_id]
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, flags=re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, flags=re.S).group(1))
    twin_path = ROOT / f"tests/labs/E3/{lab_id}.py"
    twin = twin_path.read_text(encoding="utf-8")
    diff = [d for d in difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm="", n=0)]
    print(f"== {lab_id}: page code == twin: {code.rstrip() == twin.rstrip()}; differing lines (unified, n=0):")
    for d in diff:
        print("   ", d)
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, check=False)
    print(f"   twin exit {run.returncode}; stderr: {run.stderr.strip()!r}")
    same = run.stdout.rstrip("\n") == expected.rstrip("\n")
    print(f"   expected block == twin stdout (ignoring trailing newline): {same}")
    if not same:
        for d in difflib.unified_diff(expected.splitlines(), run.stdout.splitlines(), "expected", "stdout", lineterm="", n=0):
            print("   ", d)
