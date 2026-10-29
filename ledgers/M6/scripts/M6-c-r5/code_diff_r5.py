import html, re, sys, pathlib, difflib
root = pathlib.Path(sys.argv[1])
for L in ["L09", "L10", "L11", "L12"]:
    page = (root / f"course/modules/M/M6/{L}.html").read_text()
    twin = (root / f"tests/labs/M6/lab-M6-{L}-1.py").read_text()
    code = html.unescape(re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)[0])
    d = list(difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm="", n=0))
    print(L, "difflines", len(d), "twin_trailing_nl", twin.endswith("\n"), "code_trailing_nl", code.endswith("\n"))
    print("\n".join(d[:12]))
