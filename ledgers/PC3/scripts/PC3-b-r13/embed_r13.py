import html, re, subprocess, sys, pathlib
root = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE13-PC3-b")
py = root / ".venv/bin/python"
for lid, page in (("L04", "L04"), ("L05", "L05"), ("L06", "L06")):
    text = (root / f"course/modules/PC/PC3/{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    twin = (root / f"tests/labs/PC3/lab-PC3-{lid}-1.py").read_text(encoding="utf-8")
    print(lid, "page code == twin:", code == twin, len(code), len(twin))
    if code != twin:
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True)))[:40]))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1))
    out = subprocess.run([str(py), "-I", "-W", "error", str(root / f"tests/labs/PC3/lab-PC3-{lid}-1.py")],
                         capture_output=True, text=True, cwd="/tmp")
    print(lid, "twin exit", out.returncode, "stderr bytes", len(out.stderr), "stdout == expected:", out.stdout.rstrip("\n") == expected.rstrip("\n"))
    if out.stdout.rstrip("\n") != expected.rstrip("\n"):
        import difflib
        print("".join(difflib.unified_diff(expected.splitlines(True), out.stdout.splitlines(True))))
    open(f"/Users/billyribeiro/.fanout/scratch-PC3-b-r13/stdout_{lid}.txt","w").write(out.stdout)
