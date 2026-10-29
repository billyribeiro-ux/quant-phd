import html, re
for n in ("04", "05", "06"):
    page = open(f"course/modules/M/M3/L{n}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    embedded = html.unescape(m.group(1))
    twin = open(f"tests/labs/M3/lab-M3-L{n}-1.py", encoding="utf-8").read()
    print(n, "equal after stripping trailing newline:", embedded == twin.rstrip("\n"), repr(twin[-6:]))
