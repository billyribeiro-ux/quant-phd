import re, html, sys
page = open("course/modules/E/E3/project.html", encoding="utf-8").read()
for n, lab in ((1, "lab-E3-project-1"), (2, "lab-E3-project-2"), (3, "lab-E3-project-3")):
    m = re.search(r'<section class="lab[^"]*" id="%s".*?<pre><code[^>]*data-run>(.*?)</code></pre>' % lab, page, re.S)
    code = html.unescape(m.group(1))
    twin = open("tests/labs/E3/%s.py" % lab, encoding="utf-8").read()
    print(lab, "page code chars", len(code), "twin chars", len(twin), "identical:", code == twin,
          "identical after rstrip:", code.rstrip() == twin.rstrip())
    if code.rstrip() != twin.rstrip():
        import difflib
        for line in list(difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""))[:40]:
            print("   ", line)
