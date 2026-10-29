import html, re, sys
# usage: embed_compare.py <page.html> <twin.py> <actual_output.txt>
page = open(sys.argv[1], encoding="utf-8").read()
twin = open(sys.argv[2], encoding="utf-8").read()
actual = open(sys.argv[3], encoding="utf-8").read()
codes = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
expecteds = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("code blocks", len(codes), "expected blocks", len(expecteds))
code = html.unescape(codes[0])
print("code == twin:", code.strip() == twin.strip())
exp = html.unescape(expecteds[0])
print("expected == actual run:", exp.strip() == actual.strip())
if exp.strip() != actual.strip():
    import difflib
    print("\n".join(difflib.unified_diff(actual.strip().splitlines(), exp.strip().splitlines(), lineterm="")))
