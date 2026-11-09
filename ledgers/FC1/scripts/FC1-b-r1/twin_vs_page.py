import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
ok = True
for lid, page in [("L04", "course/modules/FC/FC1/L04.html"), ("L05", "course/modules/FC/FC1/L05.html")]:
    text = (root / page).read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    twin = (root / f"tests/labs/FC1/lab-FC1-{lid}-1.py").read_text(encoding="utf-8")
    same = code.strip("\n") == twin.strip("\n")
    print(lid, "page code == twin (stripped):", same, "len", len(code), len(twin))
    if not same:
        ok = False
        import difflib
        for line in list(difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""))[:40]:
            print(line)
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1))
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/FC1/lab-FC1-{lid}-1.py")], capture_output=True, text=True, cwd="/tmp")
    print(lid, "twin run rc", run.returncode, "stderr", repr(run.stderr[:200]))
    out = run.stdout
    eq = out.strip("\n") == expected.strip("\n")
    print(lid, "expected == output:", eq)
    if not eq:
        ok = False
        import difflib
        for line in list(difflib.unified_diff(expected.splitlines(), out.splitlines(), "expected", "output", lineterm=""))[:40]:
            print(line)
print("ALL OK" if ok else "MISMATCH")
