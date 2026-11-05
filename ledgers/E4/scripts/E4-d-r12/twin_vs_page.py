"""Compare each project lab's page code block with its twin; print the differing lines and the expected block vs twin output."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
page = (ROOT / "course/modules/E/E4/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    sec = re.search(rf'<section class="lab[^"]*" id="lab-E4-project-{n}".*?</section>', page, re.S).group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', sec, re.S).group(1))
    twin = (ROOT / f"tests/labs/E4/lab-E4-project-{n}.py").read_text(encoding="utf-8")
    code_lines = code.rstrip("\n").split("\n")
    twin_lines = twin.rstrip("\n").split("\n")
    print(f"lab {n}: page lines {len(code_lines)}, twin lines {len(twin_lines)}, equal={code_lines == twin_lines}")
    for i, (a, b) in enumerate(zip(code_lines, twin_lines), 1):
        if a != b:
            print(f"  line {i} page: {a!r}\n  line {i} twin: {b!r}")
    if len(code_lines) != len(twin_lines):
        print("  length differs")
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1)).rstrip("\n")
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/E4/lab-E4-project-{n}.py")],
                         capture_output=True, text=True, check=True).stdout.rstrip("\n")
    print(f"  expected block equals twin stdout: {exp == out}")
