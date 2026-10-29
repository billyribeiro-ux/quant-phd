import re, html, sys
base = "/Users/billyribeiro/.fanout/wt/verifyB15-CS2-d/"
page = open(base + "course/modules/CS/CS2/project.html", encoding="utf-8").read()
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
exp = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("code blocks", len(blocks), "expected blocks", len(exp))
for i, b in enumerate(blocks, 1):
    code = html.unescape(b)
    twin = open(base + f"tests/labs/CS2/lab-CS2-project-{i}.py", encoding="utf-8").read()
    print("lab", i, "page==twin:", code.rstrip("\n") == twin.rstrip("\n"), "lines", len(code.splitlines()), len(twin.splitlines()))
    if code.rstrip("\n") != twin.rstrip("\n"):
        import difflib
        for l in list(difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm=""))[:30]:
            print("   ", l)
for i, e in enumerate(exp, 1):
    print("expected", i, repr(html.unescape(e)[:60]))
