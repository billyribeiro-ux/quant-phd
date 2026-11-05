"""Round-11 E4 slice b: lab twins run alone under python -I -W error; page code equals twin; expected equals stdout.

Run from the checkout root: python -I -W error is applied to each twin, from its own directory copy.
Usage: python -I ledgers/E4/scripts/E4-b-r11/twin_page_check_r11.py
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE11-E4-b")
OUT = ROOT / "ledgers/E4/scripts/E4-b-r11/outputs"
PAGES = {"L04": "course/modules/E/E4/L04.html", "L05": "course/modules/E/E4/L05.html", "L06": "course/modules/E/E4/L06.html"}
PY = str(ROOT / ".venv/bin/python")

lines_out: list[str] = []


def block(text: str, pattern: str) -> str:
    m = re.search(pattern, text, re.S)
    if not m:
        raise SystemExit(f"pattern not found: {pattern}")
    return m.group(1)


for page, rel in PAGES.items():
    text = (ROOT / rel).read_text(encoding="utf-8")
    lab_id = f"lab-E4-{page}-1"
    section = block(text, rf'(<section class="lab" id="{lab_id}".*?</section>)')
    code_raw = block(section, r'<code class="language-python" data-run>(.*?)</code></pre>')
    expected_raw = block(section, r'<pre class="expected"[^>]*>(.*?)</pre>')
    page_code = html.unescape(code_raw)
    page_expected = html.unescape(expected_raw)
    twin_path = ROOT / f"tests/labs/E4/{lab_id}.py"
    twin = twin_path.read_text(encoding="utf-8")
    code_ok_strict = page_code == twin
    code_ok_mod = page_code.rstrip("\n") == twin.rstrip("\n")
    with tempfile.TemporaryDirectory() as td:
        # run the twin alone, from its own scratch directory, with -I -W error
        copy = Path(td) / f"{lab_id}.py"
        copy.write_text(twin, encoding="utf-8")
        proc = subprocess.run([PY, "-I", "-W", "error", str(copy)], capture_output=True, text=True, cwd=td, timeout=120)
    stdout = proc.stdout
    stderr = proc.stderr
    exp_ok_strict = page_expected == stdout
    exp_ok_mod = page_expected.rstrip("\n") == stdout.rstrip("\n")
    lines_out.append(f"{page} twin={twin_path.relative_to(ROOT)} exit={proc.returncode} stderr_bytes={len(stderr.encode())}")
    lines_out.append(f"{page} stdout_lines={stdout.count(chr(10))} page_expected_lines={page_expected.count(chr(10))}")
    lines_out.append(f"{page} code_equal_strict={code_ok_strict} code_equal_modulo_trailing_newline={code_ok_mod}")
    lines_out.append(f"{page} expected_equal_strict={exp_ok_strict} expected_equal_modulo_trailing_newline={exp_ok_mod}")
    lines_out.append(f"{page} twin_trailing_newline={twin.endswith(chr(10))} page_code_trailing_newline={page_code.endswith(chr(10))}")
    (OUT / f"twin_{page}_stdout.txt").write_text(stdout, encoding="utf-8")
    (OUT / f"twin_{page}_stderr.txt").write_text(stderr, encoding="utf-8")
    if not code_ok_mod:
        import difflib

        lines_out.extend(difflib.unified_diff(twin.splitlines(), page_code.splitlines(), "twin", "page", lineterm=""))
    if not exp_ok_mod:
        import difflib

        lines_out.extend(difflib.unified_diff(stdout.splitlines(), page_expected.splitlines(), "stdout", "page", lineterm=""))
    lines_out.append("")

(OUT / "twin_page_check_r11.txt").write_text("\n".join(lines_out) + "\n", encoding="utf-8")
print("\n".join(lines_out))
sys.exit(0)
