import html, re, sys
page = open(sys.argv[1], encoding="utf-8").read()
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
expected = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("code blocks", len(blocks), "expected blocks", len(expected))
for i, (b, e) in enumerate(zip(blocks, expected), 1):
    code = html.unescape(b)
    open(f"/tmp/sc1d17_page_{i}.py", "w", encoding="utf-8").write(code)
    open(f"/tmp/sc1d17_exp_{i}.txt", "w", encoding="utf-8").write(html.unescape(e))
    print("block", i, "lines", code.count("\n"))
