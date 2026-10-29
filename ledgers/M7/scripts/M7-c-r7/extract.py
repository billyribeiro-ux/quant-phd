import html, re, sys
page, out_py, out_exp = sys.argv[1], sys.argv[2], sys.argv[3]
src = open(page, encoding="utf-8").read()
m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
code = html.unescape(m.group(1))
open(out_py, "w", encoding="utf-8").write(code)
e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
open(out_exp, "w", encoding="utf-8").write(html.unescape(e.group(1)))
