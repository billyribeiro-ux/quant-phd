"""Round-11 check: each project lab twin runs alone under python -I -W error; the page code equals the twin; the page's expected block equals the twin's output."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
page = (ROOT / "course/modules/E/E3/project.html").read_text(encoding="utf-8")
labs = re.findall(r'<section class="lab[^"]*" id="(lab-E3-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
ok = True
for lab_id, code_html, expected_html in labs:
    n = lab_id[-1]
    code = html.unescape(code_html)
    expected = html.unescape(expected_html)
    twin_path = ROOT / f"tests/labs/E3/lab-E3-project-{n}.py"
    twin = twin_path.read_text(encoding="utf-8")
    same_code = code.rstrip("\n") == twin.rstrip("\n")
    proc = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp")
    out = proc.stdout
    same_expected = expected.strip() == out.strip()
    print(f"{lab_id}: twin rc={proc.returncode} stderr_bytes={len(proc.stderr)} page_code_equals_twin={same_code} expected_equals_output={same_expected}")
    if not (same_code and same_expected and proc.returncode == 0 and not proc.stderr):
        ok = False
        if not same_code:
            import difflib
            print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page"))[:60]))
        if not same_expected:
            print("EXPECTED:\n" + expected + "\nOUTPUT:\n" + out)
print("labs_check:", "PASS" if ok and len(labs) == 3 else "FAIL", len(labs))
