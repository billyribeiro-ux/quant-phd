"""Compare each project lab's page code and expected block with its twin and run the twin alone (python -I -W error)."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE13-PC3-c")
page = (ROOT / "course/modules/PC/PC3/project.html").read_text(encoding="utf-8")
blocks = re.findall(r'<section class="lab[^"]*" id="(lab-PC3-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("labs found on page:", [b[0] for b in blocks])
for lab_id, code_html, expected_html in blocks:
    code = html.unescape(code_html)
    expected = html.unescape(re.sub(r"<[^>]+>", "", expected_html))
    n = lab_id[-1]
    twin = ROOT / f"tests/labs/PC3/lab-PC3-project-{n}.py"
    twin_src = twin.read_text(encoding="utf-8")
    lines_page = code.split("\n")
    lines_twin = twin_src.rstrip("\n").split("\n")
    print(f"== {lab_id}: page code lines {len(lines_page)}, twin lines {len(lines_twin)}")
    if len(lines_page) == len(lines_twin):
        diffs = [(i + 1, a, b) for i, (a, b) in enumerate(zip(lines_page, lines_twin)) if a != b]
    else:
        diffs = [("LENGTH", len(lines_page), len(lines_twin))]
    print("  page vs twin differing lines:", diffs if len(diffs) < 10 else len(diffs))
    for d in diffs:
        print("   ", d)
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd="/tmp", timeout=120)
    print("  twin exit", run.returncode, "stderr bytes", len(run.stderr))
    print("  expected == stdout:", expected.strip() == run.stdout.strip())
    if expected.strip() != run.stdout.strip():
        import difflib
        print("\n".join(difflib.unified_diff(expected.strip().split("\n"), run.stdout.strip().split("\n"), lineterm="")))
