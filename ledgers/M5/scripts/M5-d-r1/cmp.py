import html, re, sys
page = open("course/modules/M/M5/project.html", encoding="utf-8").read()
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("blocks", len(blocks))
for i, (code, exp) in enumerate(blocks, 1):
    code = html.unescape(code)
    exp = html.unescape(exp)
    twin = open(f"tests/labs/M5/lab-M5-project-{i}.py", encoding="utf-8").read()
    print(i, "code==twin:", code.rstrip() == twin.rstrip(), "len", len(code), len(twin))
    if code.rstrip() != twin.rstrip():
        import difflib
        print("\n".join(list(difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm=""))[:40]))
    out = open(f"/tmp/M5-v/d/lab{i}.out", encoding="utf-8").read()
    print(i, "expected==output:", exp.strip() == out.strip())
    if exp.strip() != out.strip():
        import difflib
        print("\n".join(difflib.unified_diff(out.strip().splitlines(), exp.strip().splitlines(), lineterm="")))
