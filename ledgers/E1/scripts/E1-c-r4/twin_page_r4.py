"""Compare each E1 lab on pages L07-L09 with its twin: code equality and expected-block equality.

Run from the repository root: python -I ledgers/E1/scripts/E1-c-r4/twin_page_r4.py
Reads course/modules/E/E1/Lnn.html and tests/labs/E1/lab-E1-Lnn-1.py; runs each twin alone in a fresh temp dir
under python -I -W error with an empty environment, and compares its stdout with the expected block.
"""

from __future__ import annotations

import html
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PY = str(ROOT / ".venv" / "bin" / "python")


def section(text: str, lab_id: str) -> str:
    start = text.index(f'id="{lab_id}"')
    end = text.index("</section>", start)
    return text[start:end]


def main() -> int:
    ok = True
    for page in ("L07", "L08", "L09"):
        lab_id = f"lab-E1-{page}-1"
        src = (ROOT / "course/modules/E/E1" / f"{page}.html").read_text(encoding="utf-8")
        sec = section(src, lab_id)
        code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S)
        exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S)
        assert code_m and exp_m, page
        page_code = html.unescape(code_m.group(1))
        page_expected = html.unescape(exp_m.group(1))
        twin_path = ROOT / "tests/labs/E1" / f"lab-E1-{page}-1.py"
        twin_code = twin_path.read_text(encoding="utf-8")
        code_equal = page_code.strip() == twin_code.strip()
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "twin.py").write_text(twin_code, encoding="utf-8")
            res = subprocess.run(
                [PY, "-I", "-W", "error", "twin.py"],
                cwd=d,
                env={},
                capture_output=True,
                text=True,
                check=False,
            )
        stdout_equal = res.stdout.strip() == page_expected.strip()
        print(
            f"{page}: code_equals_twin={code_equal} expected_equals_output={stdout_equal} "
            f"twin_exit={res.returncode} twin_stderr_bytes={len(res.stderr.encode())} "
            f"twin_stdout_lines={len(res.stdout.splitlines())} page_expected_lines={len(page_expected.splitlines())}"
        )
        ok = ok and code_equal and stdout_equal and res.returncode == 0 and not res.stderr
    print("ALL_OK" if ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
