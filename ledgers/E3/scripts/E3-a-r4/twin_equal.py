import html, re, sys
# Compare each page's data-run code block with its lab twin byte-for-byte.
pairs = [("L01", "lab-E3-L01-1"), ("L02", "lab-E3-L02-1"), ("L03", "lab-E3-L03-1")]
for page, lab in pairs:
    src = open(f"course/modules/E/E3/{page}.html", encoding="utf-8").read()
    m = re.search(r'<code class="language-python" data-run>(.*?)</code>', src, re.S)
    code = html.unescape(m.group(1))
    twin = open(f"tests/labs/E3/{lab}.py", encoding="utf-8").read()
    print(page, "page-code == twin:", code.rstrip("\n") == twin.rstrip("\n"), len(code), len(twin))
    if code.rstrip("\n") != twin.rstrip("\n"):
        import difflib
        print("".join(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page"))[:3000])
