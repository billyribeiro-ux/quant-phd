import html, re, sys, pathlib
root = pathlib.Path(sys.argv[1])
for L in ("07", "08", "09"):
    page = (root / f"course/modules/M/M3/L{L}.html").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1)
    code = html.unescape(code)
    twin = (root / f"tests/labs/M3/lab-M3-L{L}-1.py").read_text(encoding="utf-8")
    print(f"L{L} page-code == twin (ignoring trailing newline): {code.rstrip(chr(10)) == twin.rstrip(chr(10))}; page len {len(code)} twin len {len(twin)}")
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)
    exp = html.unescape(exp).rstrip("\n")
    out = (root / f"{sys.argv[2]}/lab-L{L}.out").read_text(encoding="utf-8").rstrip("\n")
    print(f"L{L} expected == output: {exp == out}")
    if exp != out:
        for a, b in zip(exp.splitlines(), out.splitlines()):
            if a != b: print("  DIFF", repr(a), repr(b))
