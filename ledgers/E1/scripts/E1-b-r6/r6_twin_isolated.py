"""Round-6 twin check (verifier-written): each twin runs alone under python -I -W error in a fresh directory;
page code block equals the twin source; page expected block equals stdout."""
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1])
PY = ROOT / ".venv/bin/python"
TWINS = {
    "L04": ("lab-E1-L04-1.py", "L04.html"),
    "L05": ("lab-E1-L05-1.py", "L05.html"),
    "L06": ("lab-E1-L06-1.py", "L06.html"),
}
ok = True
for page, (twin_name, html_name) in TWINS.items():
    twin = ROOT / "tests/labs/E1" / twin_name
    d = Path(tempfile.mkdtemp(prefix=f"e1b6_{page}_"))
    shutil.copy(twin, d / "twin.py")
    run = subprocess.run([str(PY), "-I", "-W", "error", "twin.py"], cwd=d, capture_output=True, text=True)
    src = (ROOT / "course/modules/E/E1" / html_name).read_text(encoding="utf-8")
    code = re.search(r"<pre><code[^>]*data-run[^>]*>(.*?)</code></pre>", src, re.S)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    page_code = html.unescape(code.group(1)) if code else None
    page_exp = html.unescape(exp.group(1)) if exp else None
    twin_src = twin.read_text(encoding="utf-8")
    code_eq = page_code is not None and page_code.rstrip("\n") == twin_src.rstrip("\n")
    exp_eq = page_exp is not None and page_exp.strip("\n") == run.stdout.strip("\n")
    print(f"{page} rc={run.returncode} stderr_bytes={len(run.stderr.encode())} stdout_lines={len(run.stdout.splitlines())} "
          f"page_code_equals_twin={code_eq} expected_equals_stdout={exp_eq}")
    ok = ok and run.returncode == 0 and not run.stderr and code_eq and exp_eq
print("ALL OK" if ok else "MISMATCH")
