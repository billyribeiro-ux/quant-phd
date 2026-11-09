import html, re, sys
page = open(sys.argv[1], encoding="utf-8").read()
twin = open(sys.argv[2], encoding="utf-8").read()
m = re.search(r'<section class="[^"]*" id="%s".*?<pre><code class="language-python" data-run>(.*?)</code></pre>' % sys.argv[3], page, re.S)
code = html.unescape(m.group(1))
print("page code == twin:", code.strip() == twin.strip(), len(code), len(twin))
e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page[m.end():], re.S)
print("expected block present:", bool(e))
