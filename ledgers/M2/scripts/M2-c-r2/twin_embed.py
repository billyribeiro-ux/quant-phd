import html, re, sys, pathlib
root = pathlib.Path(sys.argv[1])
for n in range(13, 19):
    page = (root / f"course/modules/M/M2/L{n}.html").read_text(encoding="utf8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    embedded = html.unescape(m.group(1))
    twin = (root / f"tests/labs/M2/lab-M2-L{n}-1.py").read_text(encoding="utf8")
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    print(f"L{n} twin==embedded: {embedded.strip() == twin.strip()}  expected-block-lines: {len(html.unescape(exp.group(1)).splitlines())}")
