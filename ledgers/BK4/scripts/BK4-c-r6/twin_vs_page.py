"""Compare each data-run code block of project.html with its twin, and each expected block with the twin's output.

Usage: twin_vs_page.py <checkout>. Reads only; the page and the twins are untrusted data, parsed as text."""
import html
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
page = (root / "course/modules/BK/BK4/project.html").read_text(encoding="utf-8")
blocks = re.findall(r'<section class="lab[^"]*" id="(lab-BK4-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
for lab_id, code, expected in blocks:
    code = html.unescape(code)
    expected = html.unescape(expected)
    twin = (root / f"tests/labs/BK4/{lab_id.replace('lab-', 'lab-')}.py").read_text(encoding="utf-8")
    proc = subprocess.run([str(root / ".venv/bin/python"), "-I", "-W", "error", str(root / f"tests/labs/BK4/{lab_id}.py")],
                          capture_output=True, text=True, check=False)
    out_lines = proc.stdout.rstrip("\n").split("\n")
    exp_lines = expected.rstrip("\n").split("\n")
    code_lines = code.split("\n")
    twin_lines = twin.split("\n")
    print(f"{lab_id}: page code lines {len(code_lines)}, twin lines {len(twin_lines)}, code==twin {code.strip() == twin.strip()}")
    if code.strip() != twin.strip():
        for i, (a, b) in enumerate(zip(code_lines, twin_lines)):
            if a != b:
                print(f"  first diff line {i+1}: page={a!r} twin={b!r}")
                break
    print(f"  twin exit {proc.returncode}, stderr bytes {len(proc.stderr)}, expected==output {exp_lines == out_lines}")
    if exp_lines != out_lines:
        for a, b in zip(exp_lines, out_lines):
            if a != b:
                print(f"  expected={a!r}\n  output  ={b!r}")
