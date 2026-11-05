"""Compare each project lab's page code and expected block with its twin and with a fresh run of the twin."""
import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
PAGE = ROOT / "course/modules/LX/LX2/project.html"
text = PAGE.read_text(encoding="utf-8")
codes = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
expecteds = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
print("code blocks:", len(codes), "expected blocks:", len(expecteds))
for i, (code, exp) in enumerate(zip(codes, expecteds), start=1):
    code_s = html.unescape(code).rstrip("\n") + "\n"
    exp_s = html.unescape(exp)
    twin_path = ROOT / f"tests/labs/LX2/lab-LX2-project-{i}.py"
    twin = twin_path.read_text(encoding="utf-8")
    diff = [l for l in difflib.unified_diff(twin.splitlines(), code_s.splitlines(), lineterm="", n=0)
            if not l.startswith(("---", "+++", "@@"))]
    print(f"--- lab {i}: page code vs twin differing lines: {len(diff)}")
    for l in diff:
        print("   ", l)
    proc = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True,
                          cwd="/tmp", timeout=60)
    print(f"    twin exit={proc.returncode} stderr_bytes={len(proc.stderr)}")
    out_tokens = proc.stdout.split()
    exp_tokens = exp_s.split()
    print(f"    stdout tokens={len(out_tokens)} expected tokens={len(exp_tokens)} exact-token-equal={out_tokens == exp_tokens}")
    if out_tokens != exp_tokens:
        for l in difflib.unified_diff(exp_s.splitlines(), proc.stdout.splitlines(), "expected", "twin", lineterm="", n=0):
            print("    ", l)
