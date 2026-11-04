import re, html, sys, pathlib
root = pathlib.Path(sys.argv[1])
for lesson in ["L03", "L04"]:
    page = (root / f"course/modules/LX/LX2/{lesson}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin = (root / f"tests/labs/LX2/lab-LX2-{lesson}-1.py").read_text(encoding="utf-8")
    same = code.rstrip("\n") == twin.rstrip("\n")
    print(lesson, "page code == twin (ignoring trailing newlines):", same, "| page bytes", len(code), "twin bytes", len(twin))
    if not same:
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True)))[:60]))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    exp = html.unescape(e.group(1))
    out = (root / f"{sys.argv[2]}/twin_{lesson}.out").read_text(encoding="utf-8")
    print(lesson, "expected == output (ignoring trailing newline):", exp.rstrip("\n") == out.rstrip("\n"))
    if exp.rstrip("\n") != out.rstrip("\n"):
        print(list(difflib.unified_diff(exp.splitlines(), out.splitlines(), lineterm=""))[:40])
    print(lesson, "expected block lines:", len(exp.splitlines()), "output lines:", len(out.splitlines()))
