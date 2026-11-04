import html, re, subprocess, sys, pathlib
root = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-E3-d")
page = (root / "course/modules/E/E3/project.html").read_text(encoding="utf-8")
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("code+expected blocks:", len(blocks))
for i, (code, exp) in enumerate(blocks, 1):
    code = html.unescape(code)
    exp = html.unescape(exp)
    twin = root / f"tests/labs/E3/lab-E3-project-{i}.py"
    twin_src = twin.read_text(encoding="utf-8")
    print(f"lab {i}: page code == twin: {code == twin_src} (page {len(code)} chars, twin {len(twin_src)} chars)")
    if code != twin_src:
        import difflib
        print("".join(list(difflib.unified_diff(twin_src.splitlines(True), code.splitlines(True), "twin", "page"))[:40]))
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True)
    print(f"lab {i}: twin rc={r.returncode} stderr_bytes={len(r.stderr)}")
    out = r.stdout.rstrip("\n")
    print(f"lab {i}: expected == output: {out == exp.rstrip(chr(10))}")
    if out != exp.rstrip("\n"):
        print("OUTPUT:\n" + out); print("EXPECTED:\n" + exp)
    print("OUTPUT lab", i, ":\n" + out)
