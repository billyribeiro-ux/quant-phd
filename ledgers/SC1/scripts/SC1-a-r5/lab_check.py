import html, re, subprocess, sys, time, pathlib, os, tempfile
root = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE5-SC1-a")
pages = {"L01": "course/modules/SC/SC1/L01.html", "L02": "course/modules/SC/SC1/L02.html", "L03": "course/modules/SC/SC1/L03.html"}
twins = {"L01": "tests/labs/SC1/lab-SC1-L01-1.py", "L02": "tests/labs/SC1/lab-SC1-L02-1.py", "L03": "tests/labs/SC1/lab-SC1-L03-1.py"}
for k in pages:
    text = (root / pages[k]).read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    twin = (root / twins[k]).read_text(encoding="utf-8")
    same = code.rstrip("\n") == twin.rstrip("\n")
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1))
    tol = re.search(r'<pre class="expected" data-tolerance="([^"]+)"', text).group(1)
    with tempfile.TemporaryDirectory() as d:
        t0 = time.time()
        r = subprocess.run([sys.executable, "-I", "-W", "error", str(root / twins[k])], cwd=d, capture_output=True, text=True, timeout=120)
        dt = time.time() - t0
    out = r.stdout
    print(f"== {k}: code==twin {same}; exit {r.returncode}; stderr bytes {len(r.stderr)}; time {dt:.2f}s; tol {tol}")
    print(out, end="")
    exp_lines = expected.rstrip("\n").split("\n")
    out_lines = out.rstrip("\n").split("\n")
    print(f"  expected lines {len(exp_lines)} output lines {len(out_lines)}; exact text equal: {expected.rstrip()==out.rstrip()}")
    for a, b in zip(exp_lines, out_lines):
        if a != b:
            print("   DIFF exp:", a, "| out:", b)
    open(root / f"ledgers/SC1/scripts/SC1-a-r5/out/{k}.stdout", "w").write(out)
    open(root / f"ledgers/SC1/scripts/SC1-a-r5/out/{k}.expected", "w").write(expected)
