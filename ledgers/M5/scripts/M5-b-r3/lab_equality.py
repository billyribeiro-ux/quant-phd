"""Compare each slice page's lab code block and expected block with its twin and with the twin's stdout.

Run from the checkout root: python3 -I ledgers/M5/scripts/M5-b-r3/lab_equality.py
"""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
for lesson in ("L05", "L06", "L07"):
    page = (ROOT / f"course/modules/M/M5/{lesson}.html").read_text(encoding="utf-8")
    lab_id = f"lab-M5-{lesson}-1"
    m = re.search(rf'<section class="lab" id="{lab_id}".*?</section>', page, re.S)
    assert m, lab_id
    section = m.group(0)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', section, re.S).group(1)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section, re.S).group(1)
    code_txt = html.unescape(code)
    expected_txt = html.unescape(expected)
    twin = (ROOT / f"tests/labs/M5/{lab_id}.py").read_text(encoding="utf-8")
    code_eq = code_txt.rstrip("\n") == twin.rstrip("\n")
    with tempfile.TemporaryDirectory(prefix="m5b-r3-eq-") as d:
        (Path(d) / f"{lab_id}.py").write_text(twin, encoding="utf-8")
        out = subprocess.run([sys.executable, "-I", "-W", "error", f"{lab_id}.py"], cwd=d, capture_output=True, text=True)
    stdout_eq = out.stdout.rstrip("\n") == expected_txt.rstrip("\n")
    print(f"{lesson}: rc={out.returncode} stderr_bytes={len(out.stderr)} page_code_equals_twin={code_eq} "
          f"expected_equals_stdout={stdout_eq} lines_expected={len(expected_txt.splitlines())}")
    if not stdout_eq:
        import difflib
        print("\n".join(difflib.unified_diff(expected_txt.splitlines(), out.stdout.splitlines(), lineterm="")))
