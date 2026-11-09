"""Check each lab section of the given pages: page code equals the twin, expected block equals the twin's output.

Usage: python3 -I ledgers/M5/scripts/M5-a-r1/check_labs.py <checkout-root> <page-html>...
Each twin runs under `.venv/bin/python -I -W error` in an empty temporary directory.
"""

from __future__ import annotations

import difflib
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SECTION = re.compile(r'<section class="lab"[^>]*id="([^"]+)"[^>]*>(.*?)</section>', re.S)
CODE = re.compile(r'<code class="language-python" data-run>(.*?)</code>', re.S)
EXPECTED = re.compile(r'<pre class="expected"[^>]*>(.*?)</pre>', re.S)


def check_page(root: Path, page: str) -> None:
    text = (root / page).read_text(encoding="utf-8")
    for section in SECTION.finditer(text):
        lab_id, body = section.group(1), section.group(2)
        code_m = CODE.search(body)
        exp_m = EXPECTED.search(body)
        code = html.unescape(code_m.group(1)).rstrip("\n") if code_m else ""
        expected = html.unescape(exp_m.group(1)).rstrip("\n") if exp_m else ""
        twin_path = root / "tests" / "labs" / "M5" / f"{lab_id}.py"
        twin = twin_path.read_text(encoding="utf-8").rstrip("\n") if twin_path.exists() else ""
        python = root / ".venv" / "bin" / "python"
        with tempfile.TemporaryDirectory() as work:
            run = subprocess.run(
                [str(python), "-I", "-W", "error", str(twin_path)],
                cwd=work,
                capture_output=True,
                text=True,
                check=False,
            )
        output = run.stdout.rstrip("\n")
        print(
            f"{page} {lab_id}: twin_exists={twin_path.exists()} code_equals_twin={code == twin} "
            f"exit={run.returncode} stderr_bytes={len(run.stderr)} expected_equals_output={expected == output} "
            f"expected_len={len(expected)} output_len={len(output)}"
        )
        if code != twin:
            print("  CODE DIFF:", *list(difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm=""))[:20])
        if expected != output:
            print(
                "  EXPECTED DIFF:",
                *list(difflib.unified_diff(expected.splitlines(), output.splitlines(), lineterm=""))[:20],
            )
        if run.returncode != 0 or run.stderr:
            print("  STDERR:", run.stderr[-400:])


def main() -> None:
    root = Path(sys.argv[1])
    for page in sys.argv[2:]:
        check_page(root, page)


if __name__ == "__main__":
    main()
