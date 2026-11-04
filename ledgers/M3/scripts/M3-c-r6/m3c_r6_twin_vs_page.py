"""Round-6 verifier check (slice c): each lab twin runs alone and matches its page.

For L07, L08, L09: run tests/labs/M3/lab-M3-Lnn-1.py with python -I -W error from an empty temporary
directory; require exit 0 and empty stderr; compare stdout with the page's <pre class="expected"> block;
compare the page's <code data-run> text with the twin file (both rstripped of the trailing newline).
Run from the checkout root: .venv/bin/python ledgers/M3/scripts/M3-c-r6/m3c_r6_twin_vs_page.py
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
    "L07": ("course/modules/M/M3/L07.html", "tests/labs/M3/lab-M3-L07-1.py"),
    "L08": ("course/modules/M/M3/L08.html", "tests/labs/M3/lab-M3-L08-1.py"),
    "L09": ("course/modules/M/M3/L09.html", "tests/labs/M3/lab-M3-L09-1.py"),
}


def page_parts(page_text: str, lesson: str) -> tuple[str, str]:
    section_re = re.compile(
        rf'<section class="lab" id="lab-M3-{lesson}-1"[^>]*>(.*?)</section>',
        re.S,
    )
    matches = section_re.findall(page_text)
    if len(matches) != 1:
        raise SystemExit(f"{lesson}: expected one lab section, found {len(matches)}")
    body = matches[0]
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    if code_m is None or exp_m is None:
        raise SystemExit(f"{lesson}: code or expected block missing")
    return html.unescape(code_m.group(1)), html.unescape(exp_m.group(1))


def main() -> int:
    ok = True
    for lesson, (page_rel, twin_rel) in PAGES.items():
        page_text = (ROOT / page_rel).read_text(encoding="utf-8")
        twin_text = (ROOT / twin_rel).read_text(encoding="utf-8")
        code, expected = page_parts(page_text, lesson)
        code_equal = code.rstrip() == twin_text.rstrip()
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, "-I", "-W", "error", str(ROOT / twin_rel)],
                cwd=tmp,
                capture_output=True,
                text=True,
                timeout=120,
            )
        stdout_equal = proc.stdout.rstrip() == expected.rstrip()
        stderr_empty = proc.stderr == ""
        print(
            f"{lesson}: twin exit={proc.returncode} stderr_bytes={len(proc.stderr)} "
            f"page_code_equals_twin={code_equal} expected_equals_stdout={stdout_equal} "
            f"stdout_lines={len(proc.stdout.splitlines())}"
        )
        if proc.returncode != 0 or not stderr_empty or not code_equal or not stdout_equal:
            ok = False
            print(proc.stdout)
            print(proc.stderr)
    print("TWIN_VS_PAGE:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
