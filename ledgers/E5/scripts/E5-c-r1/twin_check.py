import html, re, sys
page, twin, out = sys.argv[1], sys.argv[2], sys.argv[3]
src = open(page, encoding="utf-8").read()
m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
code = html.unescape(m.group(1))
tw = open(twin, encoding="utf-8").read()
print("page code == twin (trailing newlines aside):", code.rstrip("\n") == tw.rstrip("\n"))
e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
expected = html.unescape(e.group(1))
observed = open(out, encoding="utf-8").read()
print("expected == observed (trailing newlines aside):", expected.rstrip("\n") == observed.rstrip("\n"))
