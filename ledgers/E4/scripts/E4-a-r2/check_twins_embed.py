"""For each E4 slice lesson: page code block equals its twin byte for byte; the expected block equals the twin's stdout
when run alone with python -I -W error and a cleared environment. Prints one line per lab."""
import html
import os
import re
import subprocess
import sys

BASE = "/Users/billyribeiro/.fanout/wt/verifyE2-E4-a"
PY = os.path.join(BASE, ".venv/bin/python")
LABS = {"L01": "lab-E4-L01-1", "L02": "lab-E4-L02-1", "L03": "lab-E4-L03-1"}
ok_all = True
for page, lab in LABS.items():
    html_text = open(os.path.join(BASE, "course/modules/E/E4", page + ".html"), encoding="utf-8").read()
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', html_text, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', html_text, re.S)
    code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    twin_path = os.path.join(BASE, "tests/labs/E4", lab + ".py")
    twin = open(twin_path, encoding="utf-8").read()
    env = {"PATH": "/usr/bin:/bin"}
    run = subprocess.run([PY, "-I", "-W", "error", twin_path], capture_output=True, text=True, env=env, cwd="/tmp")
    code_eq = code.rstrip("\n") == twin.rstrip("\n")
    out_eq = expected.rstrip("\n") == run.stdout.rstrip("\n")
    ok_all = ok_all and code_eq and out_eq and run.returncode == 0
    print(f"{page} {lab}: page_code_equals_twin={code_eq} expected_equals_stdout={out_eq} exit={run.returncode} stderr_bytes={len(run.stderr)}")
    if not out_eq:
        print("--- expected\n" + expected + "\n--- stdout\n" + run.stdout)
print("ALL_OK" if ok_all else "MISMATCH")
sys.exit(0 if ok_all else 1)
