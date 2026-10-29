import re, sys, html
page, twin, out = sys.argv[1], sys.argv[2], sys.argv[3]
src = open(page, encoding="utf-8").read()
m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
code = html.unescape(m.group(1))
tw = open(twin, encoding="utf-8").read()
print("page code == twin:", code.strip() == tw.strip(), len(code), len(tw))
e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
exp = html.unescape(e.group(1)).strip().splitlines()
got = open(out, encoding="utf-8").read().strip().splitlines()
print("expected == output:", exp == got, len(exp), len(got))
for a, b in zip(exp, got):
    if a != b: print("DIFF exp:", a, "| got:", b)
