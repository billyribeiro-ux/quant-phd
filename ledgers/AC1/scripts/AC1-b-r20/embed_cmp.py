import html, re, sys
for L in ("L04", "L05", "L06"):
    page = open(f"/tmp/verify20-AC1-b/course/modules/AC/AC1/{L}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin = open(f"/tmp/verify20-AC1-b/tests/labs/AC1/lab-AC1-{L}-1.py", encoding="utf-8").read()
    print(L, "embedded==twin", code.strip() == twin.strip(), len(code), len(twin))
