"""Verifier check (E4 slice a, round 1): embedded lab code equals its twin; expected block equals a fresh run.

Run from the checkout root with: .venv/bin/python -I ledgers/E4/scripts/E4-a-r1/check_embeds.py
"""

import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
PAGES = {"L01": "lab-E4-L01-1", "L02": "lab-E4-L02-1", "L03": "lab-E4-L03-1"}
ok = True
for page, lab in PAGES.items():
    html_text = (ROOT / "course/modules/E/E4" / f"{page}.html").read_text(encoding="utf-8")
    section = re.search(r'<section class="lab" id="%s".*?</section>' % lab, html_text, re.S)
    if section is None:
        print(f"{page}: lab section {lab} NOT FOUND")
        ok = False
        continue
    body = section.group(0)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    twin = (ROOT / "tests/labs/E4" / f"{lab}.py").read_text(encoding="utf-8")
    embedded = html.unescape(code.group(1))
    same_code = embedded.rstrip("\n") == twin.rstrip("\n")
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(ROOT / "tests/labs/E4" / f"{lab}.py")],
        capture_output=True,
        text=True,
        check=False,
        env={"PATH": "/usr/bin:/bin"},
    )
    shown = html.unescape(expected.group(1)).rstrip("\n")
    same_out = shown == run.stdout.rstrip("\n") and run.returncode == 0
    print(f"{page} {lab}: code_equals_twin={same_code} expected_equals_run={same_out} exit={run.returncode}")
    ok = ok and same_code and same_out
print("ALL_EMBEDS_MATCH" if ok else "MISMATCH")
