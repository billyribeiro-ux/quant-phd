"""Compare each M3 L01-L03 page lab code block with its twin, and the expected block with a fresh run of the twin."""
import html
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
ok = True
for lid in ["L01", "L02", "L03"]:
    page = (root / f"course/modules/M/M3/{lid}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin = (root / f"tests/labs/M3/lab-M3-{lid}-1.py").read_text(encoding="utf-8")
    same = code.rstrip("\n") == twin.rstrip("\n")
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(exp.group(1)).rstrip("\n")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M3/lab-M3-{lid}-1.py")],
                         capture_output=True, text=True, cwd="/tmp")
    out = run.stdout.rstrip("\n")
    eq = out == expected
    print(f"{lid}: page code == twin: {same}; expected == fresh output: {eq}; exit={run.returncode}; stderr={run.stderr.strip()!r}")
    if not (same and eq and run.returncode == 0):
        ok = False
        if not eq:
            print("EXPECTED:\n" + expected + "\nOUTPUT:\n" + out)
print("ALL OK" if ok else "MISMATCH")
