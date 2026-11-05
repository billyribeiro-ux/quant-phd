import html, re, sys, subprocess, tempfile, os
ROOT = sys.argv[1]
for L in ["L07", "L08", "L09"]:
    page = open(f"{ROOT}/course/modules/E/E4/{L}.html", encoding="utf-8").read()
    twin = open(f"{ROOT}/tests/labs/E4/lab-E4-{L}-1.py", encoding="utf-8").read()
    codes = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    exps = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    print(L, "code blocks:", len(codes), "expected blocks:", len(exps))
    for i, c in enumerate(codes):
        code = html.unescape(c)
        print(f"  block {i}: equals twin = {code.strip() == twin.strip()} ; len page={len(code)} twin={len(twin)}")
        if code.strip() != twin.strip():
            import difflib
            for line in list(difflib.unified_diff(twin.strip().splitlines(), code.strip().splitlines(), lineterm=""))[:40]:
                print("    ", line)
    # run twin and compare expected block
    d = tempfile.mkdtemp()
    out = subprocess.run([f"{ROOT}/.venv/bin/python", "-I", "-W", "error", f"{ROOT}/tests/labs/E4/lab-E4-{L}-1.py"], cwd=d, capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"})
    for i, e in enumerate(exps):
        exp = html.unescape(e).strip()
        print(f"  expected block {i} equals stdout = {exp == out.stdout.strip()} (rc={out.returncode})")
        if exp != out.stdout.strip():
            import difflib
            for line in list(difflib.unified_diff(out.stdout.strip().splitlines(), exp.splitlines(), lineterm=""))[:30]:
                print("    ", line)
    os.rmdir(d)
