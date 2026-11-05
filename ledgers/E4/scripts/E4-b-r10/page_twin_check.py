"""Compare each E4 L04-L06 lab block with its twin: page code vs twin source, expected block vs twin stdout.

Run from the checkout root: python -I ledgers/E4/scripts/E4-b-r10/page_twin_check.py
The twin is run as `python -I -W error <twin>` with cwd set to its own directory (no network).
"""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
PY = sys.executable
ok_all = True
for page in ("L04", "L05", "L06"):
    text = (ROOT / f"course/modules/E/E4/{page}.html").read_text(encoding="utf-8")
    sections = re.findall(r'<section class="lab([^"]*)" id="([^"]+)".*?</section>', text, re.S)
    for cls, lab_id in sections:
        block = re.search(rf'<section class="lab[^"]*" id="{lab_id}".*?</section>', text, re.S).group(0)
        code = re.search(r'<code class="language-python" data-run>(.*?)</code>', block, re.S)
        exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', block, re.S)
        twin = ROOT / f"tests/labs/E4/{lab_id}.py"
        twin_src = twin.read_text(encoding="utf-8")
        page_code = html.unescape(code.group(1))
        code_eq = page_code == twin_src
        code_eq_nl = page_code.rstrip("\n") == twin_src.rstrip("\n")
        run = subprocess.run(
            [PY, "-I", "-W", "error", str(twin)], cwd=str(twin.parent), capture_output=True, text=True, timeout=60
        )
        expected = html.unescape(exp.group(1))
        out = run.stdout
        exp_eq = expected == out
        exp_eq_nl = expected.rstrip("\n") == out.rstrip("\n")
        ok = code_eq_nl and exp_eq_nl and run.returncode == 0 and run.stderr == ""
        ok_all &= ok
        print(
            f"{page} {lab_id} class={cls.strip() or '-'} exit={run.returncode} stderr_bytes={len(run.stderr)} "
            f"code_equal_strict={code_eq} code_equal_modulo_trailing_newline={code_eq_nl} "
            f"expected_equal_strict={exp_eq} expected_equal_modulo_trailing_newline={exp_eq_nl} "
            f"lines_out={out.count(chr(10))} lines_expected={expected.count(chr(10))} PASS={ok}"
        )
        if not exp_eq_nl:
            import difflib

            for line in difflib.unified_diff(
                out.rstrip("\n").splitlines(), expected.rstrip("\n").splitlines(), "twin_stdout", "page_expected", lineterm=""
            ):
                print("   ", line)
    print(f"{page} data-check snippets: {len(re.findall(r'data-check=', text))}")
print("ALL_PASS" if ok_all else "SOME_FAIL")
