"""Compare each E5 lab page's embedded code and expected output with its twin and with a fresh run.

Run from the checkout root: python -I -W error ledgers/E5/scripts/E5-b-r2/cmp_r2.py
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path.cwd()
pages = {"L04": "course/modules/E/E5/L04.html", "L05": "course/modules/E/E5/L05.html", "L06": "course/modules/E/E5/L06.html"}
for name, rel in pages.items():
    text = (root / rel).read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    code_src = html.unescape(code.group(1))
    exp_src = html.unescape(exp.group(1))
    twin = (root / f"tests/labs/E5/lab-E5-{name}-1.py").read_text(encoding="utf-8")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/E5/lab-E5-{name}-1.py")],
                         capture_output=True, text=True, cwd=root)
    print(name, "code_equals_twin", code_src.strip() == twin.strip(), "exit", run.returncode, "stderr_empty", run.stderr == "")
    print(name, "expected_equals_run", exp_src.strip() == run.stdout.strip(), "lines", len(run.stdout.splitlines()))
    if exp_src.strip() != run.stdout.strip():
        import difflib
        print("\n".join(difflib.unified_diff(exp_src.strip().splitlines(), run.stdout.strip().splitlines(), lineterm="")))
