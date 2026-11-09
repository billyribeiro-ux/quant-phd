import html, re, sys, pathlib
root = pathlib.Path(sys.argv[1])
page = (root / "course/modules/M/M5/project.html").read_text(encoding="utf-8")
labs = re.findall(r'<section class="lab[^"]*" id="(lab-M5-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected" data-tolerance="([^"]+)">(.*?)</pre>', page, re.S)
for lab_id, code, tol, expected in labs:
    code = html.unescape(code)
    expected = html.unescape(expected)
    n = lab_id[-1]
    twin = (root / f"tests/labs/M5/lab-M5-project-{n}.py").read_text(encoding="utf-8")
    print(lab_id, "tol", tol, "page_code_vs_twin_equal", code == twin, "len", len(code), len(twin))
    if code != twin:
        import difflib
        for l in difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""):
            print("  ", l)
    open(f"/tmp/m5d5/expected_{n}.txt", "w").write(expected)
    open(f"/tmp/m5d5/page_code_{n}.py", "w").write(code)
