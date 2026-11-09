import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyF21-M4-a")
PY = str(ROOT / ".venv/bin/python")
for lid in ["L01", "L02", "L03", "L04"]:
    page = (ROOT / f"course/modules/M/M4/{lid}.html").read_text(encoding="utf-8")
    twin_path = ROOT / f"tests/labs/M4/lab-M4-{lid}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    m = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    same_code = code.rstrip("\n") == twin.rstrip("\n")
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(exp.group(1)) if exp else None
    run = subprocess.run([PY, "-I", "-W", "error", str(twin_path)], cwd="/tmp", capture_output=True, text=True)
    out = run.stdout
    print(lid, "exit", run.returncode, "stderr_len", len(run.stderr), "page_code_eq_twin", same_code,
          "expected_eq_stdout", expected is not None and expected.rstrip("\n") == out.rstrip("\n"))
    if run.stderr:
        print(run.stderr)
    if not (same_code and expected is not None and expected.rstrip("\n") == out.rstrip("\n")):
        print("DIFF page_code_len", len(code), "twin_len", len(twin))
        print("--- expected\n" + (expected or "<none>") + "\n--- stdout\n" + out)
    if lid == "L02":
        print("--- L02 stdout ---")
        print(out)
