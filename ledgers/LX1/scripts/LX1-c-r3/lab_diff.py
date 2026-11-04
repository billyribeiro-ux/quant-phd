import difflib, html, re, sys
ROOT = sys.argv[1]
text = open(ROOT + "/course/modules/LX/LX1/project.html", encoding="utf-8").read()
for lab in ["lab-LX1-project-1", "lab-LX1-project-2", "lab-LX1-project-3"]:
    body = re.search(r'<section class="lab[^"]*" id="%s".*?</section>' % lab, text, re.S).group(0)
    code = html.unescape(re.search(r"<pre><code[^>]*data-run>(.*?)</code></pre>", body, re.S).group(1))
    twin = open(ROOT + "/tests/labs/LX1/%s.py" % lab, encoding="utf-8").read()
    print(lab, "page==twin+newline:", code == twin.rstrip("\n"), "twin ends newline:", twin.endswith("\n"))
    tl, pl = twin.splitlines(), code.splitlines()
    sm = difflib.SequenceMatcher(None, tl, pl, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            print("  ", tag, [l for l in tl[i1:i2]], "->", [l for l in pl[j1:j2]])
