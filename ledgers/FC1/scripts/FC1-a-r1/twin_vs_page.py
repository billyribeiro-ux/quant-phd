import re, html, sys, subprocess
page, twin = sys.argv[1], sys.argv[2]
s = open(page, encoding="utf-8").read()
code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', s, re.S).group(1)
exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', s, re.S).group(1)
code = html.unescape(code); exp = html.unescape(exp)
t = open(twin, encoding="utf-8").read()
print("code==twin:", code.strip() == t.strip(), len(code), len(t))
if code.strip() != t.strip():
    import difflib
    print("\n".join(list(difflib.unified_diff(t.strip().splitlines(), code.strip().splitlines(), lineterm=""))[:40]))
out = subprocess.run([sys.executable, "-I", "-W", "error", twin], capture_output=True, text=True).stdout
print("expected==run:", out.strip() == exp.strip())
if out.strip() != exp.strip():
    import difflib
    print("\n".join(list(difflib.unified_diff(exp.strip().splitlines(), out.strip().splitlines(), lineterm=""))[:40]))
