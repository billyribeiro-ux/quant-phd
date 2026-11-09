"""LX1-c round 20: page code blocks vs lab twins, expected blocks vs twin stdout, twin run under python -I -W error."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
codes = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
expected = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("code blocks", len(codes), "expected blocks", len(expected))
for i, (code, exp) in enumerate(zip(codes, expected), start=1):
    code_txt = html.unescape(code)
    twin = root / f"tests/labs/LX1/lab-LX1-project-{i}.py"
    twin_txt = twin.read_text(encoding="utf-8")
    same = code_txt.strip() == twin_txt.strip()
    diffs = sum(1 for a, b in zip(code_txt.splitlines(), twin_txt.splitlines()) if a != b) + abs(
        len(code_txt.splitlines()) - len(twin_txt.splitlines()))
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd=str(root / "course/assets/data/market/..").resolve() if False else str(root))
    stdout = run.stdout
    exp_txt = html.unescape(exp).rstrip("\n")
    print(f"lab {i}: page==twin {same} line-diffs {diffs}; twin rc {run.returncode}; stderr bytes {len(run.stderr)}; "
          f"stdout==expected {stdout.rstrip(chr(10)) == exp_txt}")
    if stdout.rstrip("\n") != exp_txt:
        print("  STDOUT:\n" + stdout)
        print("  EXPECTED:\n" + exp_txt)
