import html, re, sys, pathlib
page = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
for lab in ("lab-E3-project-1", "lab-E3-project-2", "lab-E3-project-3"):
    m = re.search(r'<section class="lab[^"]*" id="%s".*?<pre><code[^>]*data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>' % lab, page, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin = pathlib.Path("tests/labs/E3/%s.py" % lab).read_text(encoding="utf-8")
    print(lab, "page code == twin:", code.strip() == twin.strip(), "len", len(code), len(twin))
    pathlib.Path("%s/page_%s.py" % (sys.argv[2], lab)).write_text(code, encoding="utf-8")
    pathlib.Path("%s/expected_%s.txt" % (sys.argv[2], lab)).write_text(expected, encoding="utf-8")
