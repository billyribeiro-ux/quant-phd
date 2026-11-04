"""Compare each slice lab twin with the code block and expected block on its page.

Run from the checkout root: .venv/bin/python ledgers/M2/scripts/M2-d2-r8/twin_vs_page.py
For each page in L22, L23, L24: extracts the <pre><code class="language-python" data-run> block
(HTML-unescaped) and the <pre class="expected"> block, runs the twin under `python -I -W error` in an
empty scratch directory, and reports (a) page code == twin, (b) exact stdout == expected, (c) exit code, stderr.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = ["L22", "L23", "L24"]
PY = str(ROOT / ".venv" / "bin" / "python")


def blocks(page_html: str) -> tuple[str, str]:
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page_html, re.S)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page_html, re.S)
    if code is None or exp is None:
        raise SystemExit("missing code or expected block")
    return html.unescape(code.group(1)), html.unescape(exp.group(1))


def main() -> int:
    ok = True
    for pg in PAGES:
        page = (ROOT / "course/modules/M/M2" / f"{pg}.html").read_text(encoding="utf-8")
        code, expected = blocks(page)
        twin_path = ROOT / "tests/labs/M2" / f"lab-M2-{pg}-1.py"
        twin = twin_path.read_text(encoding="utf-8")
        same_code = code.rstrip("\n") == twin.rstrip("\n")
        with tempfile.TemporaryDirectory() as scratch:
            proc = subprocess.run(
                [PY, "-I", "-W", "error", str(twin_path)],
                cwd=scratch,
                capture_output=True,
                text=True,
                timeout=120,
            )
        out = proc.stdout
        same_out = out.rstrip("\n") == expected.rstrip("\n")
        print(f"== {pg}: twin={twin_path.relative_to(ROOT)} lines={twin.count(chr(10))} bytes={len(twin)}")
        print(f"   page code == twin (modulo trailing newline): {same_code}")
        print(f"   exit={proc.returncode} stderr_len={len(proc.stderr)}")
        print(f"   exact stdout == expected block: {same_out}")
        print("   live stdout:")
        for line in out.splitlines():
            print("     | " + line)
        if not (same_code and same_out and proc.returncode == 0 and proc.stderr == ""):
            ok = False
            print("   MISMATCH")
            if not same_out:
                import difflib

                for d in difflib.unified_diff(
                    expected.rstrip("\n").splitlines(), out.rstrip("\n").splitlines(), "expected", "live", lineterm=""
                ):
                    print("     " + d)
    print("ALL OK" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
