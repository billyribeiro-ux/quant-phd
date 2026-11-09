import html, re, subprocess, sys, os
ROOT = "/Users/billyribeiro/.fanout/wt/verifyS5-M3-b"
PY = os.path.join(ROOT, ".venv/bin/python")
for lab in ["L04", "L05", "L06"]:
    page = open(f"{ROOT}/course/modules/M/M3/{lab}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1))
    twin_path = f"{ROOT}/tests/labs/M3/lab-M3-{lab}-1.py"
    twin = open(twin_path, encoding="utf-8").read()
    print(f"{lab}: page code == twin: {code.rstrip(chr(10)) == twin.rstrip(chr(10))}; code bytes page={len(code)} twin={len(twin)}")
    r = subprocess.run([PY, "-I", "-W", "error", twin_path], capture_output=True, text=True, cwd="/tmp")
    print(f"{lab}: exit={r.returncode} stderr_bytes={len(r.stderr)}")
    print(f"{lab}: expected == output: {expected.strip() == r.stdout.strip()}")
    if expected.strip() != r.stdout.strip():
        print("EXPECTED:\n" + expected); print("OUTPUT:\n" + r.stdout)
    print("---- OUTPUT ----"); print(r.stdout)
