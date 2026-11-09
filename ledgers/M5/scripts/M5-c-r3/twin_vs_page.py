"""Round-3 check: the lab code on each slice page equals its twin, and the expected block equals the twin's stdout.

Run from the checkout root with the checkout's interpreter: .venv/bin/python -I <this file>.
Reads only files in the checkout. Prints one line per lab and exits 1 on any mismatch.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = {
    "L08": "lab-M5-L08-1",
    "L09": "lab-M5-L09-1",
    "L10": "lab-M5-L10-1",
}
bad = 0
for page, lab in PAGES.items():
    text = (ROOT / "course/modules/M/M5" / f"{page}.html").read_text(encoding="utf-8")
    section = re.search(r'<section class="lab" id="%s".*?</section>' % lab, text, re.S)
    if section is None:
        print(f"{page}: lab section not found")
        bad += 1
        continue
    body = section.group(0)
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', body, re.S).group(1)
    code = html.unescape(code)
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1))
    twin = (ROOT / "tests/labs/M5" / f"{lab}.py").read_text(encoding="utf-8")
    same_code = code.strip() == twin.strip()
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(ROOT / "tests/labs/M5" / f"{lab}.py")],
        capture_output=True,
        text=True,
        cwd=str(ROOT / "tests/labs/M5"),
    )
    out = run.stdout
    same_expected = expected.strip() == out.strip()
    print(
        f"{page} code_equals_twin={same_code} expected_equals_stdout={same_expected} "
        f"exit={run.returncode} stderr_bytes={len(run.stderr)}"
    )
    if not (same_code and same_expected and run.returncode == 0 and not run.stderr):
        bad += 1
        if not same_code:
            import difflib

            for line in list(difflib.unified_diff(twin.strip().splitlines(), code.strip().splitlines(), lineterm=""))[:40]:
                print("  " + line)
        if not same_expected:
            import difflib

            for line in list(difflib.unified_diff(expected.strip().splitlines(), out.strip().splitlines(), lineterm=""))[:40]:
                print("  " + line)
print("RESULT", "PASS" if bad == 0 else f"FAIL ({bad})")
sys.exit(1 if bad else 0)
