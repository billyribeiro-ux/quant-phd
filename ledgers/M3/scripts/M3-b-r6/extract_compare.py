import html, re, sys
for n in ("04", "05", "06"):
    page = open(f"course/modules/M/M3/L{n}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    embedded = html.unescape(m.group(1))
    twin = open(f"tests/labs/M3/lab-M3-L{n}-1.py", encoding="utf-8").read()
    print(n, "embedded==twin:", embedded == twin, len(embedded), len(twin))
    if embedded != twin:
        import difflib
        for line in difflib.unified_diff(twin.splitlines(), embedded.splitlines(), "twin", "page", lineterm=""):
            print(line)
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)
    print(n, "expected block:", repr(html.unescape(e)[:80]))
