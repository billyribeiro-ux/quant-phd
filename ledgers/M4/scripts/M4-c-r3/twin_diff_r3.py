import html, re, sys, pathlib, difflib
root = pathlib.Path(sys.argv[1])
for page, twin in (("L08", "lab-M4-L08-1"), ("L09", "lab-M4-L09-1"), ("L10", "lab-M4-L10-1")):
    text = (root / f"course/modules/M/M4/{page}.html").read_text(encoding="utf-8")
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S).group(1))
    twin_src = (root / f"tests/labs/M4/{twin}.py").read_text(encoding="utf-8")
    d = list(difflib.unified_diff(code.splitlines(True), twin_src.splitlines(True), "page", "twin"))
    print(page, "lines_equal_ignoring_final_newline:", code.rstrip("\n") == twin_src.rstrip("\n"), "diff_lines", len(d))
    print("".join(d)[:500])
