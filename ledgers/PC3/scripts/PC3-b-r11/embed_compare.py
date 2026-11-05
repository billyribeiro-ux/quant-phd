"""Compare each lab on L04-L06 with its twin (PC3-b round 10). Standard library only.

For each lab section: (1) the page's code block, unescaped, equals the twin file exactly; (2) the page's expected block,
unescaped, equals the stdout of running the twin under python -I -W error. Run from the checkout root.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
PAGES = {"L04": "lab-PC3-L04-1", "L05": "lab-PC3-L05-1", "L06": "lab-PC3-L06-1"}


def block(text: str, pattern: str) -> str:
    m = re.search(pattern, text, flags=re.S)
    if not m:
        raise SystemExit(f"pattern not found: {pattern}")
    return html.unescape(m.group(1))


def main() -> int:
    status = 0
    for page, twin in PAGES.items():
        src = (ROOT / f"course/modules/PC/PC3/{page}.html").read_text(encoding="utf-8")
        code = block(src, r'<code class="language-python" data-run>(.*?)</code></pre>')
        expected = block(src, r'<pre class="expected"[^>]*>(.*?)</pre>')
        twin_text = (ROOT / f"tests/labs/PC3/{twin}.py").read_text(encoding="utf-8")
        # The embedded block omits the twin file's final newline (embed_labs convention); compare the rest exactly.
        same_code = code.rstrip("\n") == twin_text.rstrip("\n")
        run = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/PC3/{twin}.py")],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        stdout = run.stdout
        same_expected = expected.rstrip("\n") == stdout.rstrip("\n")
        print(f"{page} {twin}: code==twin {same_code} (page {len(code)} chars, twin {len(twin_text)} chars); "
              f"expected==stdout {same_expected} (expected {expected.count(chr(10)) + 1} lines, stdout "
              f"{stdout.count(chr(10))} lines); exit {run.returncode}; stderr bytes {len(run.stderr)}")
        if not (same_code and same_expected and run.returncode == 0 and not run.stderr):
            status = 1
            if not same_expected:
                for i, (a, b) in enumerate(zip(expected.splitlines(), stdout.splitlines()), 1):
                    if a != b:
                        print(f"  first diff line {i}: page={a!r} stdout={b!r}")
                        break
    return status


if __name__ == "__main__":
    raise SystemExit(main())
