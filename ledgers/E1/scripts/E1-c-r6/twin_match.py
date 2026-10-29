import html, re, sys, pathlib
root = pathlib.Path(sys.argv[1])
for n in ("07", "08", "09"):
    page = (root / f"course/modules/E/E1/L{n}.html").read_text(encoding="utf-8")
    twin = (root / f"tests/labs/E1/lab-E1-L{n}-1.py").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(exp.group(1)) if exp else None
    print(f"L{n}: code blocks={len(re.findall('data-run', page))}, code==twin: {code.strip() == twin.strip()}, "
          f"twin bytes={len(twin)}, page code bytes={len(code)}, expected present={expected is not None}")
    if code.strip() != twin.strip():
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), 'twin', 'page'))[:60]))
    out = pathlib.Path(f"/tmp/e1c-r6-L{n}.out").read_text(encoding="utf-8")
    print(f"L{n}: expected==twin output: {expected is not None and expected.strip() == out.strip()}")
    if expected is not None and expected.strip() != out.strip():
        import difflib
        print("".join(list(difflib.unified_diff(out.splitlines(True), expected.splitlines(True), 'output', 'expected'))[:60]))
