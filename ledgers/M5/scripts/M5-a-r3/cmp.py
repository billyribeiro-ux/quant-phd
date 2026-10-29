import re, html, sys
page_path, twin_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
page = open(page_path, encoding="utf-8").read()
code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1)
code = html.unescape(code)
exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)
exp = html.unescape(exp)
twin = open(twin_path, encoding="utf-8").read()
print("code==twin:", code.strip() == twin.strip())
got = open(out_path, encoding="utf-8").read()
print("output==expected:", got.strip() == exp.strip())
