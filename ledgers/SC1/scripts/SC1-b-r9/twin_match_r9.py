"""Round-8 twin check for SC1 L04-L06: page code equals the twin; expected block equals twin stdout;
twin runs under python -I -W error; no unexpanded @@LAB/@@OUT markers; twin sha256 values.

Usage (from the checkout root): python3 -I ledgers/SC1/scripts/SC1-b-r9/twin_match_r9.py
"""
import hashlib
import html
import re
import subprocess
import sys
import time

PAIRS = {
    "L04": "tests/labs/SC1/lab-SC1-L04-1.py",
    "L05": "tests/labs/SC1/lab-SC1-L05-1.py",
    "L06": "tests/labs/SC1/lab-SC1-L06-1.py",
}
ok = True
for page, twin in PAIRS.items():
    src = open(f"course/modules/SC/SC1/{page}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    code = html.unescape(m.group(1))
    twin_src = open(twin, encoding="utf-8").read()
    same_code = code.rstrip("\n") == twin_src.rstrip("\n")  # embed strips the final newline only
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    expected = html.unescape(exp.group(1))
    t0 = time.time()
    run = subprocess.run([sys.executable, "-I", "-W", "error", twin], capture_output=True, text=True)
    dt = time.time() - t0
    out_ok = run.stdout == expected + ("" if expected.endswith("\n") else "\n") or run.stdout.rstrip("\n") == expected.rstrip("\n")
    markers = re.findall(r"@@(LAB|OUT):", src)
    sha = hashlib.sha256(twin_src.encode()).hexdigest()
    print(f"{page}: page code == twin: {same_code}; expected == stdout: {out_ok}; exit={run.returncode}; "
          f"stderr_bytes={len(run.stderr)}; markers_left={len(markers)}; runtime={dt:.2f}s; twin_sha256={sha[:16]}")
    ok = ok and same_code and out_ok and run.returncode == 0 and not markers
print("ALL PASS" if ok else "MISMATCH")
