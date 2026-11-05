"""Compare each slice-c lab twin with its page: code equality, expected block equals the twin's output.

Run from the checkout root: .venv/bin/python -I ledgers/M3/scripts/M3-c-r9/twin_vs_page.py
Each twin runs alone under python -I -W error in a fresh temporary directory.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
PAGES = {
    "L07": ("course/modules/M/M3/L07.html", "lab-M3-L07-1"),
    "L08": ("course/modules/M/M3/L08.html", "lab-M3-L08-1"),
    "L09": ("course/modules/M/M3/L09.html", "lab-M3-L09-1"),
}


def section(text: str, lab_id: str) -> str:
    start = text.index(f'id="{lab_id}"')
    end = text.index("</section>", start)
    return text[start:end]


def main() -> int:
    ok = True
    for page, (path, lab_id) in PAGES.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        sec = section(text, lab_id)
        code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S)
        exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S)
        assert code_m and exp_m, page
        code = html.unescape(code_m.group(1))
        expected = html.unescape(exp_m.group(1))
        twin = (ROOT / "tests/labs/M3" / f"{lab_id}.py").read_text(encoding="utf-8")
        code_eq = code.rstrip() == twin.rstrip()
        with tempfile.TemporaryDirectory() as scratch:
            run = subprocess.run(
                [sys.executable, "-I", "-W", "error", str(ROOT / "tests/labs/M3" / f"{lab_id}.py")],
                cwd=scratch,
                capture_output=True,
                text=True,
                timeout=60,
            )
        out_eq = run.stdout.rstrip() == expected.rstrip()
        print(f"{page} twin exit={run.returncode} stderr_bytes={len(run.stderr.encode())}")
        print(f"{page} page code == twin: {code_eq}")
        print(f"{page} expected == output: {out_eq}")
        if not out_eq:
            print("--- expected ---")
            print(expected)
            print("--- output ---")
            print(run.stdout)
        ok = ok and run.returncode == 0 and not run.stderr and code_eq and out_eq
    print("ALL OK" if ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
