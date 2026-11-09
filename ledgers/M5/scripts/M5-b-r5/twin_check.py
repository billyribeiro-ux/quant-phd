"""Round-5 twin check for M5-b: page code == twin, expected == stdout of twin run alone under -I -W error."""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyS5-M5-b")
PY = str(ROOT / ".venv/bin/python")
PAGES = {
    "L05": ("course/modules/M/M5/L05.html", "tests/labs/M5/lab-M5-L05-1.py", "lab-M5-L05-1"),
    "L06": ("course/modules/M/M5/L06.html", "tests/labs/M5/lab-M5-L06-1.py", "lab-M5-L06-1"),
    "L07": ("course/modules/M/M5/L07.html", "tests/labs/M5/lab-M5-L07-1.py", "lab-M5-L07-1"),
}
rc_all = 0
for key, (page, twin, lab) in PAGES.items():
    text = (ROOT / page).read_text(encoding="utf-8")
    m = re.search(r'<section class="lab" id="%s".*?<code class="language-python" data-run>(.*?)</code></pre>' % lab, text, re.S)
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text[m.end():], re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(e.group(1))
    twin_src = (ROOT / twin).read_text(encoding="utf-8")
    same_code = code.rstrip("\n") == twin_src.rstrip("\n")
    with tempfile.TemporaryDirectory() as d:
        run = subprocess.run([PY, "-I", "-W", "error", str(ROOT / twin)], cwd=d, capture_output=True, text=True)
    same_expected = expected.rstrip("\n") == run.stdout.rstrip("\n")
    print(f"{key} twin={twin} rc={run.returncode} stderr_len={len(run.stderr)} page_code==twin(rstrip)={same_code} "
          f"expected==stdout={same_expected} code_lines={code.count(chr(10))} twin_lines={twin_src.count(chr(10))} "
          f"stdout_lines={run.stdout.count(chr(10))}")
    if not same_code:
        import difflib
        print("".join(list(difflib.unified_diff(twin_src.splitlines(True), code.splitlines(True), "twin", "page"))[:60]))
    if not same_expected:
        import difflib
        print("".join(list(difflib.unified_diff(run.stdout.splitlines(True), expected.splitlines(True), "stdout", "expected"))[:60]))
    rc_all |= run.returncode | (0 if same_code and same_expected else 1)
    if key == "L05":
        print("STDOUT L05 (for reading):")
        print(run.stdout)
    if key == "L06":
        print("STDOUT L06:")
        print(run.stdout)
    if key == "L07":
        print("STDOUT L07:")
        print(run.stdout)
sys.exit(rc_all)
