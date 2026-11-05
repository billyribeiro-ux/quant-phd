"""Round-9 check: each M4 project lab's page code equals its twin, the twin runs under python -I -W error,
and the page's expected block equals the twin's stdout (Lab 2 is the completion page: its blanks are excluded).
Usage: python -I ledgers/M4/scripts/M4-d-r9/checks/labs_project_r9.py   (run from the checkout root)
"""
import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path.cwd()
PAGE = ROOT / "course/modules/M/M4/project.html"
text = PAGE.read_text(encoding="utf-8")
for n in (1, 2, 3):
    lab_id = f"lab-M4-project-{n}"
    start = text.index(f'id="{lab_id}"')
    end = text.index("</section>", start)
    section = text[start:end]
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', section, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section, re.S).group(1))
    twin_path = ROOT / f"tests/labs/M4/{lab_id}.py"
    twin = twin_path.read_text(encoding="utf-8")
    same = code.strip("\n") == twin.strip("\n")
    print(f"{lab_id}: page code == twin: {same} (page {len(code)} chars, twin {len(twin)} chars)")
    if not same:
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page"))[:40]))
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, check=False)
    print(f"{lab_id}: twin exit {run.returncode}, stderr {run.stderr.strip()[:200]!r}")
    print(f"{lab_id}: expected block == twin stdout: {expected.strip() == run.stdout.strip()}")
    if expected.strip() != run.stdout.strip():
        print("EXPECTED:\n" + expected + "\nSTDOUT:\n" + run.stdout)
    print(run.stdout.rstrip())
