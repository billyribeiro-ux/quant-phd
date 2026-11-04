"""Check that each E4 slice page's embedded lab code equals its twin, and its expected block equals the twin's stdout.

Run from the checkout root with the repository venv, with the working directory set to a scratch dir outside the tree:
    python -I -W error <this script> <checkout-root>
Reads only; runs each twin as `python -I -W error <twin>` in a temporary directory with no network.
"""

from __future__ import annotations

import html
import pathlib
import re
import subprocess
import sys
import tempfile

root = pathlib.Path(sys.argv[1])
pages = {
    "L01": root / "course/modules/E/E4/L01.html",
    "L02": root / "course/modules/E/E4/L02.html",
    "L03": root / "course/modules/E/E4/L03.html",
}
for lesson, page in pages.items():
    text = page.read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    twin = root / f"tests/labs/E4/lab-E4-{lesson}-1.py"
    twin_text = twin.read_text(encoding="utf-8")
    print(f"{lesson} embedded code == twin: {code.rstrip() == twin_text.rstrip()}  ({len(code)} vs {len(twin_text)} chars)")
    exp = re.search(r'<pre class="expected" data-tolerance="0">(.*?)</pre>', text, re.S)
    expected = html.unescape(exp.group(1))
    with tempfile.TemporaryDirectory() as d:
        out = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(twin)], cwd=d, capture_output=True, text=True, timeout=120
        )
    print(f"{lesson} twin exit {out.returncode}; stderr empty: {out.stderr == ''}")
    print(f"{lesson} expected block == twin stdout: {expected.rstrip() == out.stdout.rstrip()}")
    if expected.rstrip() != out.stdout.rstrip():
        print("---- diff ----")
        for a, b in zip(expected.splitlines(), out.stdout.splitlines()):
            if a != b:
                print("expected:", a)
                print("actual:  ", b)
