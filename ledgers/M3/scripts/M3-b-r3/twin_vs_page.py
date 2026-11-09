"""Round-3 slice b: page code == twin, expected block == twin output, twins run alone under python -I -W error.

Run from the checkout root. Prints one block per lab with the comparison result and the twin's exact output.
"""
import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(".")
PY = str(ROOT / ".venv/bin/python")
ok_all = True
for page in ("L04", "L05", "L06"):
    src = (ROOT / f"course/modules/M/M3/{page}.html").read_text(encoding="utf-8")
    labs = re.findall(r'<section class="lab" id="(lab-M3-[^"]+)"', src)
    for lab_id in labs:
        sec = src[src.index(f'id="{lab_id}"'):]
        sec = sec[: sec.index("</section>")]
        code = re.search(r'<code class="language-python" data-run>(.*?)</code>', sec, re.S).group(1)
        code = html.unescape(code)
        expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
        twin_name = lab_id.replace("lab-M3-", "lab-M3-") + ".py"
        twin = ROOT / f"tests/labs/M3/{twin_name}"
        twin_text = twin.read_text(encoding="utf-8")
        same_code = code.strip("\n") == twin_text.strip("\n")
        run = subprocess.run([PY, "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd=ROOT)
        out = run.stdout
        same_out = expected.strip("\n") == out.strip("\n")
        ok_all &= same_code and same_out and run.returncode == 0 and not run.stderr
        print(f"== {page} {lab_id} twin={twin} page_code_equals_twin={same_code} expected_equals_output={same_out} "
              f"exit={run.returncode} stderr_bytes={len(run.stderr)}")
        if not same_code:
            print("".join(difflib.unified_diff(twin_text.splitlines(True), code.splitlines(True), "twin", "page")))
        if not same_out:
            print("".join(difflib.unified_diff(expected.splitlines(True), out.splitlines(True), "expected", "output")))
        print("OUTPUT:")
        print(out, end="")
print("ALL_OK" if ok_all else "MISMATCH")
sys.exit(0 if ok_all else 1)
