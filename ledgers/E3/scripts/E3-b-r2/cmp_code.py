import sys, re, html
page, twin = sys.argv[1], sys.argv[2]
src = open(page, encoding='utf-8').read()
m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
code = html.unescape(re.sub(r'<[^>]+>', '', m.group(1)))
t = open(twin, encoding='utf-8').read()
print("code identical to twin:", code.strip() == t.strip(), len(code), len(t))
