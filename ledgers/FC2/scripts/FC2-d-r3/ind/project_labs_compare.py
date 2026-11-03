"""Compare each project lab's page code with its twin, and each expected block with the twin's own output.

Usage: project_labs_compare.py <checkout>. Writes nothing; prints a line per lab and every differing line.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/FC/FC2/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    sec = re.search(rf'<section class="lab[^"]*" id="lab-FC2-project-{n}".*?</section>', page, re.S).group(0)
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin = (root / f"tests/labs/FC2/lab-FC2-project-{n}.py").read_text(encoding="utf-8")
    code_lines = code.rstrip("\n").split("\n")
    twin_lines = twin.rstrip("\n").split("\n")
    diffs = [(i + 1, a, b) for i, (a, b) in enumerate(zip(code_lines, twin_lines)) if a != b]
    print(f"lab {n}: page code lines {len(code_lines)}, twin lines {len(twin_lines)}, differing lines {len(diffs)}")
    for ln, a, b in diffs:
        print(f"   line {ln}: page={a!r} twin={b!r}")
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/FC2/lab-FC2-project-{n}.py")],
                         capture_output=True, text=True)
    print(f"   twin rc={out.returncode}; expected block == twin output: {expected.strip() == out.stdout.strip()}")
    if expected.strip() != out.stdout.strip():
        print("   expected:", expected.strip()[:300])
        print("   output:", out.stdout.strip()[:300])
