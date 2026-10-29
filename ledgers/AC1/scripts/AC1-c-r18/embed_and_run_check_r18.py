import html, re, sys

page, out = sys.argv[1], sys.argv[2]
t = open(page, encoding="utf-8").read()
m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', t, re.S)
exp = html.unescape(m.group(1))
got = open(out, encoding="utf-8").read()
print("expected==run:", exp.strip() == got.strip(), len(exp), len(got))
# embedded lab code == twin
code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', t, re.S)
src = html.unescape(code.group(1))
tw = open(sys.argv[3], encoding="utf-8").read()
print("embedded code==twin:", src.strip() == tw.strip())
