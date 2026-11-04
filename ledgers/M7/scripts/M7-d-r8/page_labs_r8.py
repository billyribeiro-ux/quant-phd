"""Round 8 (M7-d): compare each project.html lab block with its twin, run the twin alone under python -I -W error,
and compare the output with the page's expected block. Usage: python -I page_labs_r8.py <repo-root>"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/M/M7/project.html").read_text(encoding="utf-8")
twins = {"lab-M7-project-1": "lab-M7-project-1.py", "lab-M7-project-2": "lab-M7-project-2.py",
         "lab-M7-project-3": "lab-M7-project-3.py"}
ok = True
for lab_id, twin_name in twins.items():
    sec = re.search(rf'<section[^>]*id="{lab_id}"[^>]*>(.*?)</section>', page, re.S)
    body = sec.group(1)
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1)).strip()
    twin = (root / "tests/labs/M7" / twin_name).read_text(encoding="utf-8")
    same = code.strip() == twin.strip()
    run = subprocess.run([str(root / ".venv/bin/python"), "-I", "-W", "error", "-c", twin], capture_output=True, text=True, cwd="/tmp")
    out = run.stdout.strip()
    match = out == expected
    print(f"{lab_id}: page code == twin: {same}; twin exit {run.returncode} under -I -W error; output == expected block: {match}")
    if not (same and run.returncode == 0 and match):
        ok = False
        print("  stderr:", run.stderr[-400:])
        print("  diff-first-line output:", out[:200], "| expected:", expected[:200])
print("ALL OK" if ok else "MISMATCH")
