import html, re, sys
# usage: twin_check.py <page> <twin> <output-file>
page = open(sys.argv[1], encoding="utf-8").read()
twin = open(sys.argv[2], encoding="utf-8").read()
out = open(sys.argv[3], encoding="utf-8").read()
code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1)
exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)
code = html.unescape(code)
exp = html.unescape(exp)
print("code==twin (modulo final newline):", code.rstrip("\n") == twin.rstrip("\n"))
print("expected==output (modulo final newline):", exp.rstrip("\n") == out.rstrip("\n"))
