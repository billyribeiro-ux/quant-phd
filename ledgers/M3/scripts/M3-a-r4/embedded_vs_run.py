"""Compare each L01-L03 page's embedded lab code and expected output with the twin and a fresh run.

Usage: python -I embedded_vs_run.py <checkout-root>
"""
import difflib
import html
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(sys.argv[1]).resolve()
py = str(root / ".venv/bin/python")
for lab in ("L01", "L02", "L03"):
    text = (root / "course/modules/M/M3" / f"{lab}.html").read_text(encoding="utf-8")
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    twin = (root / f"tests/labs/M3/lab-M3-{lab}-1.py").read_text(encoding="utf-8")
    run = subprocess.run([py, "-I", "-W", "error", str(root / f"tests/labs/M3/lab-M3-{lab}-1.py")],
                         capture_output=True, text=True, cwd="/tmp")
    print(lab, "code==twin:", code.strip() == twin.strip(), "| expected==run:", expected.strip() == run.stdout.strip(),
          "| run exit", run.returncode, "| stderr bytes", len(run.stderr), "| lines", len(run.stdout.splitlines()))
    if expected.strip() != run.stdout.strip():
        print("\n".join(difflib.unified_diff(expected.strip().splitlines(), run.stdout.strip().splitlines(), lineterm="")))
