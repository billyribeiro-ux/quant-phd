"""Verifier script (SC1 slice c, round 9): page lab code and expected blocks against the twins.

Usage: python -I -W error ledgers/SC1/scripts/SC1-c-r9/lab_equivalence.py <repo_root>

For L07 and L08: extracts the data-run code block and the pre.expected block from the page,
html-unescapes them, compares the code with the twin file byte for byte, runs the twin in a
fresh temporary directory under python -I -W error, and compares its stdout with the expected block.
"""

from __future__ import annotations

import html
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    ok = True
    for page in ("L07", "L08"):
        text = (root / "course/modules/SC/SC1" / f"{page}.html").read_text(encoding="utf-8")
        twin_name = f"lab-SC1-{page}-1.py"
        twin = (root / "tests/labs/SC1" / twin_name).read_text(encoding="utf-8")
        code_match = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
        expected_match = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
        if code_match is None or expected_match is None:
            print(f"{page}: block not found")
            ok = False
            continue
        page_code = html.unescape(code_match.group(1))
        expected = html.unescape(expected_match.group(1))
        code_equal = page_code.rstrip("\n") == twin.rstrip("\n")
        print(f"{page}: page code equals twin {twin_name}: {code_equal} (page {len(page_code)} chars, twin {len(twin)})")
        with tempfile.TemporaryDirectory() as scratch:
            target = Path(scratch) / twin_name
            target.write_text(twin, encoding="utf-8")
            env = {"PATH": os.environ.get("PATH", ""), "LANG": "C.UTF-8"}
            proc = subprocess.run(
                [sys.executable, "-I", "-W", "error", str(target)],
                cwd=scratch,
                capture_output=True,
                text=True,
                env=env,
                timeout=120,
                check=False,
            )
        stdout_equal = proc.stdout.rstrip("\n") == expected.rstrip("\n")
        print(f"{page}: twin exit code {proc.returncode}, stderr bytes {len(proc.stderr.encode())}")
        print(f"{page}: expected block equals twin stdout: {stdout_equal}")
        if not stdout_equal:
            print("---- expected ----")
            print(expected)
            print("---- stdout ----")
            print(proc.stdout)
        ok = ok and code_equal and stdout_equal and proc.returncode == 0 and not proc.stderr
    print(f"lab_equivalence SC1-c: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
