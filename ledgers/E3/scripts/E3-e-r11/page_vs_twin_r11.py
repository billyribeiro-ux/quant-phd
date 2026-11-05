import re, sys, html
page = open(sys.argv[1], encoding="utf-8").read()
for lab in ("lab-E3-project-1", "lab-E3-project-2", "lab-E3-project-3"):
    m = re.search(r'<section class="lab[^"]*" id="%s".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>' % lab, page, re.S)
    code = html.unescape(m.group(1)).rstrip("\n") + "\n"
    exp = html.unescape(m.group(2)).rstrip("\n")
    twin = open("tests/labs/E3/%s.py" % lab, encoding="utf-8").read().rstrip("\n") + "\n"
    print(lab, "page code == twin:", code == twin, "| len page", len(code), "len twin", len(twin))
    if code != twin:
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page"))[:40]))
    print(lab, "expected block lines:", len(exp.splitlines()))
