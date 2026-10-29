import html, re, sys
page = open(sys.argv[1], encoding="utf-8").read()
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
exp = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("run blocks", len(blocks), "expected blocks", len(exp))
for i, b in enumerate(blocks, 1):
    code = html.unescape(b)
    twin = open(f"tests/labs/M5/lab-M5-project-{i}.py", encoding="utf-8").read()
    if code.strip() == twin.strip():
        print(f"block {i}: code identical to twin")
    else:
        import difflib
        d = list(difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm=""))
        print(f"block {i}: differs, {len(d)} diff lines")
        print("\n".join(d[:20]))
for i, e in enumerate(exp, 1):
    print(f"expected {i}:", repr(html.unescape(e)[:60]))
