"""Round-3 lab check for FC2 project labs: twin runs alone under -I -W error, page code == twin, expected == output."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PAGE = ROOT / "course/modules/FC/FC2/project.html"
text = PAGE.read_text(encoding="utf-8")
PY = str(ROOT / ".venv/bin/python")
for n in (1, 2, 3):
    lab_id = f"lab-FC2-project-{n}"
    sec = re.search(rf'<section class="lab[^"]*" id="{lab_id}".*?</section>', text, re.S).group(0)
    code = html.unescape(re.search(r'<code class="language-python"[^>]*>(.*?)</code>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin = (ROOT / f"tests/labs/FC2/{lab_id}.py").read_text(encoding="utf-8")
    print(f"{lab_id}: page code == twin: {code == twin} (len page {len(code)}, twin {len(twin)})")
    if n != 2:
        same = code.replace("\n", "") == twin.replace("\n", "")
    if n == 2:
        lines_p = code.splitlines(); lines_t = twin.splitlines()
        print("  page lines:", len(lines_p), "twin lines:", len(lines_t), "page blanks:", sum("___" in l for l in lines_p))
    out = subprocess.run([PY, "-I", "-W", "error", str(ROOT / f"tests/labs/FC2/{lab_id}.py")],
                         capture_output=True, text=True, cwd="/tmp")
    print(f"  twin exit {out.returncode}; stderr: {out.stderr.strip()[:200]!r}")
    print(f"  expected == stdout: {out.stdout.rstrip() == expected.rstrip()}")
    if out.stdout.rstrip() != expected.rstrip():
        print("  DIFF:\n" + "\n".join(__import__('difflib').unified_diff(expected.splitlines(), out.stdout.splitlines(), lineterm='')))
