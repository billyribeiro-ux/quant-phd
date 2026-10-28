import html, re, sys, pathlib
root = pathlib.Path(sys.argv[1])
for unit in ("L03", "L04"):
    page = (root / f"course/modules/AC/AC4/{unit}.html").read_text(encoding="utf-8")
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)).rstrip("\n")
    out = (pathlib.Path(sys.argv[2]) / f"twin_{unit}.out").read_text(encoding="utf-8").rstrip("\n")
    print(unit, "expected lines", exp.count("\n") + 1, "twin lines", out.count("\n") + 1, "IDENTICAL" if exp == out else "DIFFERENT")
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1))
    twin = (root / f"tests/labs/AC4/lab-AC4-{unit}-1.py").read_text(encoding="utf-8")
    print(unit, "embedded code == twin file:", code.rstrip("\n") == twin.rstrip("\n"), len(code), len(twin))
