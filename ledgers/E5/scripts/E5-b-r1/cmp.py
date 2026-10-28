import html, re, sys
page, twin, out = sys.argv[1], sys.argv[2], sys.argv[3]
t = open(page, encoding="utf-8").read()
code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', t, re.S).group(1)
code = html.unescape(code)
exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', t, re.S).group(1)
exp = html.unescape(exp)
tw = open(twin, encoding="utf-8").read()
o = open(out, encoding="utf-8").read()
print("code_equals_twin", code.strip() == tw.strip(), len(code), len(tw))
print("expected_equals_run", exp.strip() == o.strip())
if exp.strip() != o.strip():
    import difflib
    print("\n".join(difflib.unified_diff(exp.strip().splitlines(), o.strip().splitlines(), lineterm="")))
