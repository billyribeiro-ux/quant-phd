"""Verifier round 1 (M4-d): for each M4 lab section, (a) the page code block equals the lab twin file byte for byte
after HTML unescape, (b) the expected block equals the twin's stdout under python -I -W error."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(".")
PY = sys.argv[1]
M4 = ROOT / "course/modules/M/M4"
twins = ROOT / "tests/labs/M4"
bad = []
for page in sorted(M4.glob("L*.html")) + [M4 / "project.html"]:
    raw = page.read_text(encoding="utf-8")
    for sec in re.finditer(r'<section class="lab[^"]*" id="([^"]+)"[^>]*>(.*?)</section>', raw, re.S):
        lab_id, body = sec.group(1), sec.group(2)
        code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S)
        exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
        if not code or not exp:
            bad.append((page.name, lab_id, "missing code or expected block"))
            continue
        code_txt = html.unescape(code.group(1))
        twin = twins / f"{lab_id.replace('lab-', 'lab-')}.py"
        if not twin.exists():
            bad.append((page.name, lab_id, "no twin file"))
            continue
        twin_txt = twin.read_text(encoding="utf-8")
        same_code = code_txt.rstrip() == twin_txt.rstrip()
        r = subprocess.run([PY, "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd=ROOT, timeout=600)
        out = r.stdout
        exp_txt = html.unescape(exp.group(1))
        same_exp = exp_txt.rstrip("\n") == out.rstrip("\n")
        print(f"{page.name:12s} {lab_id:24s} code==twin {same_code}  expected==stdout {same_exp}  exit {r.returncode}  stderr {len(r.stderr)}")
        if not (same_code and same_exp and r.returncode == 0):
            bad.append((page.name, lab_id, same_code, same_exp, r.returncode))
print("mismatches:", bad)
