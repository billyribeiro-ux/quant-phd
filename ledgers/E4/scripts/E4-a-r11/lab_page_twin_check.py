"""E4 slice a, round 11: page lab blocks equal their twins, expected blocks equal twin output.

Run from the checkout root with the venv interpreter:
    .venv/bin/python ledgers/E4/scripts/E4-a-r11/lab_page_twin_check.py
Reads course/modules/E/E4/L01.html..L03.html and tests/labs/E4/lab-E4-L0n-1.py, runs each twin under
python -I -W error, and compares: (1) the data-run code text (HTML-unescaped) with the twin source,
(2) the pre.expected text with the twin's stdout. Also checks the hypothesis paragraph precedes the expected
block and that an interpretation paragraph follows it.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PY = ROOT / ".venv" / "bin" / "python"
FAILS: list[str] = []


def check(cond: bool, msg: str) -> None:
    status = "PASS" if cond else "FAIL"
    print(f"{status}: {msg}")
    if not cond:
        FAILS.append(msg)


for lesson in ("L01", "L02", "L03"):
    page = (ROOT / "course/modules/E/E4" / f"{lesson}.html").read_text(encoding="utf-8")
    lab_id = f"lab-E4-{lesson}-1"
    m = re.search(r'<section class="lab" id="' + lab_id + r'"(.*?)</section>', page, re.S)
    check(m is not None, f"{lesson}: section {lab_id} present")
    if m is None:
        continue
    body = m.group(1)
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    check(code_m is not None and exp_m is not None, f"{lesson}: data-run code and pre.expected blocks present")
    if code_m is None or exp_m is None:
        continue
    page_code = html.unescape(code_m.group(1))
    page_expected = html.unescape(exp_m.group(1))
    twin_path = ROOT / "tests/labs/E4" / f"{lab_id}.py"
    twin_src = twin_path.read_text(encoding="utf-8")
    check(
        page_code.rstrip("\n") == twin_src.rstrip("\n"),
        f"{lesson}: page code equals twin {twin_path.name} (only the trailing newline differs, as the embedder strips it)",
    )
    run = subprocess.run(
        [str(PY), "-I", "-W", "error", str(twin_path)],
        capture_output=True,
        text=True,
        cwd="/tmp/e4-v/a-r11",
        check=False,
    )
    check(run.returncode == 0, f"{lesson}: twin exits 0 under python -I -W error (rc={run.returncode})")
    check(run.stderr.strip() == "", f"{lesson}: twin prints nothing to stderr")
    check(page_expected.rstrip("\n") == run.stdout.rstrip("\n"), f"{lesson}: pre.expected equals twin stdout")
    hyp = body.find('class="hypothesis"')
    check(0 <= hyp < code_m.start(), f"{lesson}: hypothesis paragraph precedes the code block")
    interp = body.find('class="interpretation"')
    check(interp > exp_m.end() - 1, f"{lesson}: interpretation paragraph follows the expected block")
    check("data-files" not in body, f"{lesson}: no data-files attribute on the lab")
    check("random" not in twin_src.lower() or "No random draws" in page.split(lab_id)[1][:3000],
          f"{lesson}: twin random use is stated or absent")

print("FAILS:", len(FAILS))
sys.exit(1 if FAILS else 0)
