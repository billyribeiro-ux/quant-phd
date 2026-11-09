"""Round 1 verifier: the page's embedded lab code and expected block equal the twin and its output (L07, L08).

Run from the checkout root: .venv/bin/python -I ledgers/FC2/scripts/FC2-c-r1/v1_twin_equal.py
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGE = ROOT / "course" / "modules" / "FC" / "FC2"
TWIN = ROOT / "tests" / "labs" / "FC2"


def main() -> int:
    status = 0
    for name in ("L07", "L08"):
        raw = (PAGE / f"{name}.html").read_text(encoding="utf-8")
        lab_id = f"lab-FC2-{name}-1"
        section = re.search(rf'<section class="lab" id="{lab_id}".*?</section>', raw, flags=re.S)
        assert section, lab_id
        code = re.search(r'<code class="language-python" data-run>(.*?)</code>', section.group(0), flags=re.S)
        expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section.group(0), flags=re.S)
        assert code and expected
        page_code = html.unescape(code.group(1))
        twin_code = (TWIN / f"{lab_id}.py").read_text(encoding="utf-8")
        same_code = page_code.rstrip("\n") == twin_code.rstrip("\n")
        out = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(TWIN / f"{lab_id}.py")],
            capture_output=True,
            text=True,
            check=False,
        )
        page_expected = html.unescape(expected.group(1)).rstrip("\n")
        same_out = page_expected == out.stdout.rstrip("\n")
        print(
            f"{lab_id}: code_equal={same_code} twin_exit={out.returncode} stderr_bytes={len(out.stderr)} "
            f"expected_equal_output={same_out} lines={len(out.stdout.splitlines())}"
        )
        if not (same_code and out.returncode == 0 and not out.stderr and same_out):
            status = 1
    return status


if __name__ == "__main__":
    raise SystemExit(main())
