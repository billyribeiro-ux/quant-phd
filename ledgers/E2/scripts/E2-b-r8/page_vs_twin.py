import html, re, sys, pathlib
root = pathlib.Path(sys.argv[1])
for L in ("04", "05", "06"):
    page = (root / f"course/modules/E/E2/L{L}.html").read_text(encoding="utf-8")
    twin = (root / f"tests/labs/E2/lab-E2-L{L}-1.py").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1)
    code = html.unescape(code)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)
    exp = html.unescape(exp)
    out = (root / f"ledgers/E2/scripts/E2-b-r8/twin-L{L}.out").read_text(encoding="utf-8")
    print(f"L{L} code==twin:", code.rstrip("\n") == twin.rstrip("\n"), "| expected==twin output:", exp.rstrip("\n") == out.rstrip("\n"), "| len", len(code), len(twin))
