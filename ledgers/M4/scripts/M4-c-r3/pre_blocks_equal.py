import re, html, sys
# usage: pre_blocks_equal.py <page.html> <twin.py> <twin_output.txt>
page = open(sys.argv[1], encoding="utf-8").read()
twin = open(sys.argv[2], encoding="utf-8").read()
out = open(sys.argv[3], encoding="utf-8").read()
code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1)
exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)
code = html.unescape(code); exp = html.unescape(exp)
print("code_equal_twin:", code.strip() == twin.strip(), "| expected_equal_output:", exp.strip() == out.strip())
