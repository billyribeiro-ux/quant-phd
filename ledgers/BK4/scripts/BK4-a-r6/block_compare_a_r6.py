"""Round-6 BK4 slice a: each lab block on L01-L03 equals its twin (code, rstrip per line) and each expected block
equals the output of python3 -I -W error on the twin. Also checks the twin ends with an unconditional main() call.
Usage: python3 -I block_compare_a_r6.py <checkout root>
"""
import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
for page, lab in (("L01", "lab-BK4-L01-1"), ("L02", "lab-BK4-L02-1"), ("L03", "lab-BK4-L03-1")):
    src = (root / f"course/modules/BK/BK4/{page}.html").read_text(encoding="utf-8")
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    code = html.unescape(re.sub(r"</?[a-zA-Z][^>]*>", "", code_m.group(1)))
    expected = html.unescape(re.sub(r"</?[a-zA-Z][^>]*>", "", exp_m.group(1)))
    twin_path = root / f"tests/labs/BK4/{lab}.py"
    twin = twin_path.read_text(encoding="utf-8")
    rs = lambda t: [ln.rstrip() for ln in t.strip("\n").split("\n")]
    code_eq = rs(code) == rs(twin)
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp")
    out_eq = rs(expected) == rs(run.stdout)
    main_last = rs(twin)[-1] == "main()" and "__name__" not in twin
    print(page, lab, "code==twin:", code_eq, "expected==output:", out_eq, "exit:", run.returncode,
          "stderr bytes:", len(run.stderr), "unconditional main last line:", main_last,
          "expected lines:", len(rs(expected)), "output lines:", len(rs(run.stdout)))
    if not out_eq:
        for d in difflib.unified_diff(rs(expected), rs(run.stdout), lineterm=""):
            print("   ", d)
    if not code_eq:
        for d in difflib.unified_diff(rs(code), rs(twin), lineterm=""):
            print("   ", d)
