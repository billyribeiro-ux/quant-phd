"""Round 6 (M7-d): run the three project lab twins alone under python -I -W error and compare each output with the
page's expected block; compare each page code block with its twin (unescaped, trailing newlines aside)."""

import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD6-M7-d")
PY = str(ROOT / ".venv" / "bin" / "python")
page = (ROOT / "course/modules/M/M7/project.html").read_text(encoding="utf-8")
sections = re.findall(r'<section class="lab[^"]*" id="(lab-M7-project-\d)".*?</section>', page, flags=re.S)
ok = True
for lab_id in ["lab-M7-project-1", "lab-M7-project-2", "lab-M7-project-3"]:
    m = re.search(r'<section class="lab[^"]*" id="%s".*?</section>' % lab_id, page, flags=re.S)
    block = m.group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', block, flags=re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', block, flags=re.S).group(1))
    twin = (ROOT / "tests/labs/M7" / f"{lab_id}.py").read_text(encoding="utf-8")
    same_code = code.rstrip("\n") == twin.rstrip("\n")
    twin_path = ROOT / "tests/labs/M7" / f"{lab_id}.py"
    proc = subprocess.run([PY, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp")
    out_ok = proc.stdout.rstrip("\n") == expected.rstrip("\n")
    print(f"{lab_id}: page code == twin: {same_code}; twin rc={proc.returncode} stderr={proc.stderr.strip()!r}; "
          f"output == expected block: {out_ok}")
    if not (same_code and out_ok and proc.returncode == 0 and not proc.stderr):
        ok = False
        print(proc.stdout)
print("ALL OK" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
