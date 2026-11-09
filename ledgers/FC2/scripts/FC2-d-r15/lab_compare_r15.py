"""Compare each FC2 project lab's page code and expected block with its twin and with the twin's own output."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/FC/FC2/project.html").read_text(encoding="utf-8")
ok = True
for n in (1, 2, 3):
    m = re.search(rf'<section class="lab[^"]*" id="lab-FC2-project-{n}".*?</section>', page, re.S)
    sec = m.group(0)
    code = html.unescape(re.search(r'<code class="language-python"[^>]*>(.*?)</code>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin = (root / f"tests/labs/FC2/lab-FC2-project-{n}.py").read_text(encoding="utf-8")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/FC2/lab-FC2-project-{n}.py")],
                         capture_output=True, text=True)
    out = run.stdout
    same_code = code.strip() == twin.strip()
    same_expected = expected.strip() == out.strip()
    print(f"lab {n}: twin exit={run.returncode} page_code_equals_twin={same_code} expected_equals_output={same_expected}")
    if not (same_code and same_expected and run.returncode == 0):
        ok = False
        if not same_code:
            import difflib
            print("".join(list(difflib.unified_diff(twin.strip().splitlines(True), code.strip().splitlines(True), n=0))[:20]))
        if not same_expected:
            import difflib
            print("".join(list(difflib.unified_diff(out.strip().splitlines(True), expected.strip().splitlines(True), n=0))[:20]))
print("LAB_COMPARE", "PASS" if ok else "FAIL")
