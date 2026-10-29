import html, re, sys
for n in ("07", "08", "09"):
    page = open(f"course/modules/M/M3/L{n}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin = open(f"tests/labs/M3/lab-M3-L{n}-1.py", encoding="utf-8").read()
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    print(n, "page==twin:", code == twin, "len", len(code), len(twin))
    if code != twin:
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True)))[:20]))
