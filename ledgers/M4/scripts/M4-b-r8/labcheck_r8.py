import html, re, subprocess, sys, pathlib
root = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB8-M4-b")
for L in ["L05", "L06", "L07"]:
    page = (root / f"course/modules/M/M4/{L}.html").read_text()
    twin = (root / f"tests/labs/M4/lab-M4-{L}-1.py").read_text()
    codes = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    exps = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code_ok = [html.unescape(c) == twin for c in codes]
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M4/lab-M4-{L}-1.py")], capture_output=True, text=True, cwd="/tmp")
    exp_ok = [html.unescape(e).rstrip("\n") == r.stdout.rstrip("\n") for e in exps]
    print(L, "codes", len(codes), code_ok, "expected", len(exps), exp_ok, "exit", r.returncode, "stderr_bytes", len(r.stderr.encode()))
    open(root / f"ledgers/M4/scripts/M4-b-r8/logs/twin_{L}.out", "w").write(r.stdout)
