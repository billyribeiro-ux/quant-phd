import html, re, sys
# usage: embed_check.py <page.html> <out.txt>
page = open(sys.argv[1], encoding="utf-8").read()
out = open(sys.argv[2], encoding="utf-8").read()
m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
expected = html.unescape(m.group(1))
print("expected_equals_output", expected.strip() == out.strip())
code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
code = html.unescape(code_m.group(1))
twin = open(sys.argv[3], encoding="utf-8").read()
print("code_equals_twin", code.strip() == twin.strip())
