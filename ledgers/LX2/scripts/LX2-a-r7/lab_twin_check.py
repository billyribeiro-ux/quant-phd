"""Check one LX2 lab on one page: the page code equals the twin, the expected block equals the twin's output.

Usage: python -I ledgers/LX2/scripts/LX2-a-r7/lab_twin_check.py <page.html> <twin.py> <lab-id>
Runs the twin as `python -I -W error <twin>` in a subprocess (cwd is the repository checkout) and reports the exit
status, stderr length and whether the printed stdout equals the page's expected block.
"""

import html
import re
import subprocess
import sys


def blocks(page_path: str, lab_id: str) -> tuple[str, str]:
    with open(page_path, encoding="utf-8") as fh:
        raw = fh.read()
    start = raw.index(f'id="{lab_id}"')
    section = raw[start : raw.index("</section>", start)]
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', section, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section, re.S)
    if not code or not expected:
        raise SystemExit(f"{lab_id}: code or expected block not found")
    return html.unescape(code.group(1)), html.unescape(expected.group(1))


def main() -> int:
    page, twin, lab_id = sys.argv[1], sys.argv[2], sys.argv[3]
    code, expected = blocks(page, lab_id)
    with open(twin, encoding="utf-8") as fh:
        twin_text = fh.read()
    page_code_equals_twin = code.rstrip("\n") == twin_text.rstrip("\n")
    proc = subprocess.run(
        [sys.executable, "-I", "-W", "error", twin], capture_output=True, text=True, timeout=60
    )
    expected_equals_output = expected.rstrip("\n") == proc.stdout.rstrip("\n")
    print(f"{lab_id}: page_code_equals_twin={page_code_equals_twin} exit={proc.returncode} "
          f"stderr_bytes={len(proc.stderr)} expected_equals_output={expected_equals_output} "
          f"stdout_lines={len(proc.stdout.splitlines())}")
    if not expected_equals_output:
        import difflib

        for line in difflib.unified_diff(
            expected.rstrip("\n").splitlines(), proc.stdout.rstrip("\n").splitlines(), "expected", "output", lineterm=""
        ):
            print(line)
    return 0 if (page_code_equals_twin and proc.returncode == 0 and expected_equals_output) else 1


if __name__ == "__main__":
    sys.exit(main())
