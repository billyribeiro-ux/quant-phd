import html, re, sys, difflib
root = sys.argv[1]
for L, twin in (("L07", "lab-E5-L07-1"), ("L08", "lab-E5-L08-1")):
    page = open(f"{root}/course/modules/E/E5/{L}.html", encoding="utf-8").read()
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1))
    twin_src = open(f"{root}/tests/labs/E5/{twin}.py", encoding="utf-8").read()
    d = list(difflib.unified_diff(twin_src.splitlines(True), code.splitlines(True), "twin", "page"))
    print(L, "diff lines:", len(d), "repr-end twin:", repr(twin_src[-30:]), "page:", repr(code[-30:]))
    print("".join(d[:60]))
