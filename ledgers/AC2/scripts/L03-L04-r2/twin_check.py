"""Round-2 check: each page's data-run code equals its twin; its expected block equals the twin's stdout."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
pairs = {
    "L03": "lab-AC2-L03-1",
    "L04": "lab-AC2-L04-1",
}
for page, lab in pairs.items():
    text = (root / f"course/modules/AC/AC2/{page}.html").read_text(encoding="utf-8")
    code = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', text, re.S).group(1)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1)
    code = html.unescape(code)
    expected = html.unescape(expected).strip()
    twin = (root / f"tests/labs/AC2/{lab}.py").read_text(encoding="utf-8")
    print(page, "code == twin (modulo final newline):", code.rstrip("\n") == twin.rstrip("\n"))
    out = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(root / f"tests/labs/AC2/{lab}.py")],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    print(page, "twin stdout == expected block:", out == expected, "lines:", len(out.splitlines()))
