"""Verifier r8: run each M4 lab twin alone under python -I -W error; compare page code to twin and expected block to stdout."""
import html
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(sys.argv[1]).resolve()
ok = True
for lid in ["L01", "L02", "L03", "L04"]:
    page = (root / f"course/modules/M/M4/{lid}.html").read_text(encoding="utf-8")
    twin_path = root / f"tests/labs/M4/lab-M4-{lid}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    codes = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    expects = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(codes[0]) if codes else None
    exp = html.unescape(expects[0]) if expects else None
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp"
    )
    code_eq = code is not None and code.strip() == twin.strip()
    exp_eq = exp is not None and exp.strip() == run.stdout.strip()
    print(f"{lid}: codes_on_page={len(codes)} expects_on_page={len(expects)} exit={run.returncode} "
          f"stdout_lines={len(run.stdout.splitlines())} stderr_len={len(run.stderr)} "
          f"code_equals_twin={code_eq} expected_equals_stdout={exp_eq}")
    if run.returncode or run.stderr or not code_eq or not exp_eq or len(codes) != 1:
        ok = False
        print(run.stderr[:2000])
    if lid == "L03":
        print(run.stdout)
print("ALL OK" if ok else "MISMATCH")
