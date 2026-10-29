import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
for page, twin in [("L04", "lab-FC1-L04-1.py"), ("L05", "lab-FC1-L05-1.py")]:
    text = (root / "course/modules/FC/FC1" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    tw = (root / "tests/labs/FC1" / twin).read_text(encoding="utf-8")
    print(page, "page code == twin:", code == tw, "len", len(code), len(tw))
    if code != tw:
        import difflib
        print("\n".join(list(difflib.unified_diff(tw.splitlines(), code.splitlines(), lineterm=""))[:40]))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1))
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / "tests/labs/FC1" / twin)], capture_output=True, text=True)
    print(page, "twin exit", out.returncode, "stderr", out.stderr[:200])
    print(page, "expected == output:", expected.strip() == out.stdout.strip())
    if expected.strip() != out.stdout.strip():
        print("\n".join(difflib.unified_diff(expected.strip().splitlines(), out.stdout.strip().splitlines(), lineterm="")))
