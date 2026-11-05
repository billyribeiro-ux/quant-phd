"""For each E4 L04-L06 page: the embedded code block equals its twin, and the expected-output block equals the
stdout of the twin run as `python -I -W error <twin>`. Usage (repo root): .venv/bin/python <this file>."""

import difflib
import html
import re
import subprocess
import sys

ROOT = "."
ok = True
for lesson, twin in (("L04", "lab-E4-L04-1"), ("L05", "lab-E4-L05-1"), ("L06", "lab-E4-L06-1")):
    page = open(f"{ROOT}/course/modules/E/E4/{lesson}.html", encoding="utf-8").read()
    blocks = [html.unescape(re.sub(r"<[^>]+>", "", b)) for b in re.findall(r"<pre[^>]*>(.*?)</pre>", page, flags=re.S)]
    code = next(b for b in blocks if "E4 " + lesson[0] + lesson[1:] in b[:400] or '"""E4 ' + lesson in b[:400])
    twin_src = open(f"{ROOT}/tests/labs/E4/{twin}.py", encoding="utf-8").read()
    code_eq = code.strip() == twin_src.strip()
    out = subprocess.run(
        [f"{ROOT}/.venv/bin/python", "-I", "-W", "error", f"{ROOT}/tests/labs/E4/{twin}.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    # the expected-output block is the pre block that starts with the first printed line of the run
    first = out.stdout.splitlines()[0].strip()
    exp = next(b for b in blocks if b.strip().startswith(first))
    exp_eq = exp.strip() == out.stdout.strip()
    print(f"{lesson}: code_equals_twin={code_eq} expected_equals_output={exp_eq} exit={out.returncode} stderr_bytes={len(out.stderr)}")
    if not (code_eq and exp_eq and out.returncode == 0 and not out.stderr):
        ok = False
        for line in difflib.unified_diff(out.stdout.splitlines(), exp.strip().splitlines(), "run", "page", lineterm=""):
            print(line)
sys.exit(0 if ok else 1)
