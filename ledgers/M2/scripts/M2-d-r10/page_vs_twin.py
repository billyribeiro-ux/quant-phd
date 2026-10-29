import html, re, sys, pathlib
root = pathlib.Path(sys.argv[1])
for n in range(19, 25):
    page = (root / f"course/modules/M/M2/L{n}.html").read_text(encoding="utf-8")
    m = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin = (root / f"tests/labs/M2/lab-M2-L{n}-1.py").read_text(encoding="utf-8")
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(exp.group(1))
    print(f"L{n}: page code == twin: {code == twin} (len {len(code)} vs {len(twin)}); expected block lines {len(expected.splitlines())}")
