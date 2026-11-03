"""Compare each slice-c lab section (page <code> and expected block) with its twin and the twin's stdout.

Usage: python3 -I check_embed_r2.py <repo_root> <stdout_dir>
Reads course/modules/M/M3/L07..L09.html and tests/labs/M3/lab-M3-L0n-1.py; stdout_dir holds twin_L0n.out
written by running each twin alone under python -I -W error.
"""

import html
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
out_dir = pathlib.Path(sys.argv[2])
ok = True
for n in ("07", "08", "09"):
    page = (root / f"course/modules/M/M3/L{n}.html").read_text(encoding="utf-8")
    m = re.search(r'<section class="lab" id="lab-M3-L%s-1".*?</section>' % n, page, re.S)
    assert m, n
    sec = m.group(0)
    code_m = re.search(r"<code[^>]*>(.*?)</code>", sec, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S)
    code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    twin = (root / f"tests/labs/M3/lab-M3-L{n}-1.py").read_text(encoding="utf-8")
    stdout = (out_dir / f"twin_L{n}.out").read_text(encoding="utf-8")
    code_eq = code.rstrip("\n") == twin.rstrip("\n")
    exp_eq = expected.strip() == stdout.strip()
    markers = "@@" in sec
    print(f"L{n}: code==twin {code_eq}; expected==twin stdout {exp_eq}; markers left {markers}; "
          f"code lines {code.count(chr(10))}, expected lines {expected.strip().count(chr(10)) + 1}")
    if not (code_eq and exp_eq and not markers):
        ok = False
        if not code_eq:
            import difflib
            print("".join(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page")))
        if not exp_eq:
            import difflib
            print("".join(difflib.unified_diff(stdout.splitlines(True), expected.splitlines(True), "stdout", "page")))
print("PASS" if ok else "FAIL")
