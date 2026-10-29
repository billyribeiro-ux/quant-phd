import html, re, sys, pathlib
root = pathlib.Path(sys.argv[1])
for page in ["L04", "L05", "L06"]:
    src = (root / f"course/modules/E/E2/{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    code = html.unescape(m.group(1))
    twin = (root / f"tests/labs/E2/lab-E2-{page}-1.py").read_text(encoding="utf-8")
    print(page, "identical modulo trailing newlines:", code.rstrip("\n") == twin.rstrip("\n"), "| page ends with newline:", code.endswith("\n"), "twin ends with newline:", twin.endswith("\n"))
    print(page, "unified-diff lines:", sum(1 for a, b in zip(code.splitlines(), twin.splitlines()) if a != b), "line count", len(code.splitlines()), len(twin.splitlines()))
