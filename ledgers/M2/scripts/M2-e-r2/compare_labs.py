"""Compare each project lab's page code block and expected block with its twin and with its observed output.

Usage: python3 -I compare_labs.py <checkout>   (run the twins first; outputs are read from /tmp/m2e_r2/*.twin.out)
"""
import html
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
page = (root / "course/modules/M/M2/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    sec = re.search(rf'<section class="lab[^"]*" id="lab-M2-project-{n}".*?</section>', page, re.S).group(0)
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin = (root / f"tests/labs/M2/lab-M2-project-{n}.py").read_text(encoding="utf-8")
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M2/lab-M2-project-{n}.py")],
                         capture_output=True, text=True).stdout
    if n == 2:
        page_lines = code.splitlines()
        twin_lines = twin.splitlines()
        diff = [(i + 1, a, b) for i, (a, b) in enumerate(zip(page_lines, twin_lines)) if a != b]
        print(f"lab {n}: page lines {len(page_lines)}, twin lines {len(twin_lines)}, differing lines:")
        for i, a, b in diff:
            print(f"   line {i}: page={a!r}  twin={b!r}")
    else:
        print(f"lab {n}: page code == twin: {code == twin}")
    print(f"lab {n}: expected block == observed twin output: {expected.strip() == out.strip()}")
    if expected.strip() != out.strip():
        print("   expected:", repr(expected[:200]))
        print("   observed:", repr(out[:200]))
