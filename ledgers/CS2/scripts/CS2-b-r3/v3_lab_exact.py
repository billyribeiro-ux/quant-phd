"""Check each CS2 slice lab: page code == twin, twin alone under -I -W error, expected block == stdout.

Usage: python -I -W error v3_lab_exact.py <checkout-root>
Each twin runs in its own empty temporary directory (no data/ files: the slice declares none).
Prints one line per lab and ALL_OK at the end when every check holds.
"""

import html
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

LABS = ["L05", "L06", "L07", "L08"]


def section(text: str, lab_id: str) -> tuple[str, str]:
    start = text.index(f'id="{lab_id}"')
    end = text.index("</section>", start)
    body = text[start:end]
    code_match = re.search(r"<code[^>]*>(.*?)</code>", body, re.S)
    expected_match = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    if code_match is None or expected_match is None:
        raise SystemExit(f"{lab_id}: code or expected block not found")
    code = html.unescape(code_match.group(1))
    expected = html.unescape(expected_match.group(1))
    return code, expected


def main() -> None:
    root = Path(sys.argv[1])
    ok_all = True
    for page in LABS:
        page_path = root / "course" / "modules" / "CS" / "CS2" / f"{page}.html"
        text = page_path.read_text(encoding="utf-8")
        lab_id = f"lab-CS2-{page}-1"
        code, expected = section(text, lab_id)
        twin_path = root / "tests" / "labs" / "CS2" / f"{lab_id}.py"
        twin = twin_path.read_text(encoding="utf-8")
        code_equal = code.rstrip("\n") == twin.rstrip("\n")
        with tempfile.TemporaryDirectory() as scratch:
            env = {"PATH": os.environ.get("PATH", ""), "PYTHONDONTWRITEBYTECODE": "1"}
            proc = subprocess.run(
                [sys.executable, "-I", "-W", "error", str(twin_path)],
                cwd=scratch,
                capture_output=True,
                text=True,
                env=env,
                timeout=60,
            )
            written = sorted(os.listdir(scratch))
        stdout_equal = proc.stdout.rstrip("\n") == expected.rstrip("\n")
        ok = code_equal and proc.returncode == 0 and proc.stderr == "" and stdout_equal and written == []
        ok_all = ok_all and ok
        print(
            f"{page}: page_code_equals_twin={code_equal} exit={proc.returncode} stderr_empty={proc.stderr == ''} "
            f"expected_equals_stdout={stdout_equal} files_written={written} stdout_lines={len(proc.stdout.splitlines())}"
        )
    print("ALL_OK" if ok_all else "FAILED")


main()
