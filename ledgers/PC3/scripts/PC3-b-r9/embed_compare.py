"""Compare each PC3 L04-L06 lab in the page with its twin and with the twin's own stdout (verifier round 8).

Run as: .venv/bin/python -I ledgers/PC3/scripts/PC3-b-r8/embed_compare.py
It reads the pages and twins, runs each twin as python -I -W error from a scratch directory, and prints:
  page code == twin, expected == twin stdout, the twin's rc and stderr size.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PY = str(ROOT / ".venv" / "bin" / "python")
PAGES = {"L04": "lab-PC3-L04-1", "L05": "lab-PC3-L05-1", "L06": "lab-PC3-L06-1"}


def page_lab(page: str, lab_id: str) -> tuple[str, str]:
    text = (ROOT / "course" / "modules" / "PC" / "PC3" / f"{page}.html").read_text(encoding="utf-8")
    sec = re.search(rf'<section class="lab" id="lab-PC3-{page}-1".*?</section>', text, re.S)
    assert sec, f"no lab section in {page}"
    body = sec.group(0)
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', body, re.S)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    assert code and exp, f"missing code or expected block in {page}"
    return html.unescape(code.group(1)), html.unescape(exp.group(1))


def main() -> int:
    rc_all = 0
    for page, lab_id in PAGES.items():
        twin_path = ROOT / "tests" / "labs" / "PC3" / f"{lab_id}.py"
        twin = twin_path.read_text(encoding="utf-8")
        code, expected = page_lab(page, lab_id)
        with tempfile.TemporaryDirectory() as scratch:
            proc = subprocess.run(
                [PY, "-I", "-W", "error", str(twin_path)],
                cwd=scratch,
                capture_output=True,
                text=True,
                timeout=60,
            )
        stdout = proc.stdout
        code_eq = code.strip("\n") == twin.strip("\n")
        exp_eq = expected.strip("\n") == stdout.strip("\n")
        print(
            f"{page}: twin rc={proc.returncode} stderr_bytes={len(proc.stderr.encode())} "
            f"page code == twin: {code_eq} (code {len(code)} chars, twin {len(twin)} chars); "
            f"expected == twin stdout: {exp_eq} (expected {len(expected.splitlines())} lines, stdout {len(stdout.splitlines())} lines)"
        )
        if not code_eq:
            rc_all = 1
        if not exp_eq:
            rc_all = 1
        if proc.returncode != 0 or proc.stderr:
            rc_all = 1
    return rc_all


if __name__ == "__main__":
    sys.exit(main())
