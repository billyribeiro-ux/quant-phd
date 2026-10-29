"""Compare each CS2 L05-L08 page lab code block with its twin, and the printed expected block with the twin output.

Usage: python -I this.py <checkout-root>
"""
import html
import pathlib
import re
import subprocess
import sys
import tempfile

root = pathlib.Path(sys.argv[1])
for page in ["L05", "L06", "L07", "L08"]:
    text = (root / f"course/modules/CS/CS2/{page}.html").read_text(encoding="utf-8")
    blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    twin = (root / f"tests/labs/CS2/lab-CS2-{page}-1.py").read_text(encoding="utf-8")
    code = html.unescape(blocks[0])
    print(page, "blocks", len(blocks), "page==twin", code.rstrip("\n") == twin.rstrip("\n"), "sha256-ish len", len(code), len(twin))
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/CS2/lab-CS2-{page}-1.py")],
                           cwd=d, capture_output=True, text=True)
        print(page, "exit", r.returncode, "stderr bytes", len(r.stderr.encode()))
        out = r.stdout
    print(out)
