import html, re, subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
for page in ["L04", "L05", "L06"]:
    src = (root / f"course/modules/E/E2/{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    code = html.unescape(m.group(1))
    twin = (root / f"tests/labs/E2/lab-E2-{page}-1.py").read_text(encoding="utf-8")
    print(page, "page code == twin:", code == twin, "len", len(code), len(twin))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    expected = html.unescape(e.group(1))
    out = subprocess.run([sys.executable, "-I", "-W", "error", "-c", twin], capture_output=True, text=True, cwd="/tmp")
    print(page, "exit", out.returncode, "stderr", repr(out.stderr[:200]))
    print(page, "expected == output:", expected.strip() == out.stdout.strip(), "lines", len(out.stdout.splitlines()))
