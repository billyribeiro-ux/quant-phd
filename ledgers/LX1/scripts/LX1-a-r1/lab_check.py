"""LX1-a r1: compare each page lab's code and expected block with its twin and with the twin's real output.

Run from the checkout root: python -I -W error ledgers/LX1/scripts/LX1-a-r1/lab_check.py
"""
import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(".")
PAGES = {"L01": "course/modules/LX/LX1/L01.html", "L02": "course/modules/LX/LX1/L02.html"}
for page, path in PAGES.items():
    text = pathlib.Path(path).read_text(encoding="utf-8")
    for m in re.finditer(r'<section class="lab" id="([^"]+)"[^>]*>(.*?)</section>', text, re.S):
        lab_id, body = m.group(1), m.group(2)
        code = re.search(r"<code[^>]*data-run[^>]*>(.*?)</code>", body, re.S).group(1)
        expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1)
        code = html.unescape(code)
        expected = html.unescape(expected)
        twin = ROOT / "tests/labs/LX1" / f"{lab_id}.py"
        twin_src = twin.read_text(encoding="utf-8")
        print(f"[{lab_id}] twin={twin} page_code_equals_twin={code.rstrip() == twin_src.rstrip()} "
              f"code_len={len(code)} twin_len={len(twin_src)}")
        if code.rstrip() != twin_src.rstrip():
            import difflib
            for line in list(difflib.unified_diff(twin_src.splitlines(), code.splitlines(), "twin", "page", lineterm=""))[:40]:
                print("   ", line)
        out = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True)
        print(f"[{lab_id}] twin exit={out.returncode} stderr_len={len(out.stderr)}")
        print(f"[{lab_id}] expected_equals_output={expected.strip() == out.stdout.strip()}")
        if expected.strip() != out.stdout.strip():
            import difflib
            for line in list(difflib.unified_diff(expected.strip().splitlines(), out.stdout.strip().splitlines(), "expected", "output", lineterm=""))[:40]:
                print("   ", line)
