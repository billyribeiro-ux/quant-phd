import html, re, sys, difflib
root = sys.argv[1]
page = open(f"{root}/course/modules/PC/PC3/project.html", encoding="utf-8").read()
blocks = re.findall(r'<section class="lab[^"]*" id="(lab-PC3-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
for lab_id, code, expected in blocks:
    code = html.unescape(code)
    expected = html.unescape(expected)
    n = lab_id.rsplit("-", 1)[1]
    twin = open(f"{root}/tests/labs/PC3/lab-PC3-project-{n}.py", encoding="utf-8").read()
    print(lab_id, "page_code_len", len(code), "twin_len", len(twin), "identical" if code == twin else "DIFFERENT")
    if code != twin:
        for line in difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm="", n=0):
            print("   ", line)
    open(f"/tmp/pc3c-r8/expected_{n}.txt", "w", encoding="utf-8").write(expected)
    open(f"/tmp/pc3c-r8/page_code_{n}.py", "w", encoding="utf-8").write(code)
print("labs found:", [b[0] for b in blocks])
