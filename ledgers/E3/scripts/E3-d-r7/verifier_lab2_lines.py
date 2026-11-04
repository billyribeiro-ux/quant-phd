import re, html, difflib
src = open("/Users/billyribeiro/.fanout/wt/verifyD7-E3-d/course/modules/E/E3/project.html", encoding="utf-8").read()
body = re.search(r'<section class="lab completion" id="lab-E3-project-2"[^>]*>(.*?)</section>', src, re.S).group(1)
code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', body, re.S).group(1))
twin = open("/Users/billyribeiro/.fanout/wt/verifyD7-E3-d/tests/labs/E3/lab-E3-project-2.py", encoding="utf-8").read()
pl, tl = code.rstrip("\n").split("\n"), twin.rstrip("\n").split("\n")
print(len(pl), len(tl))
for i, (a, b) in enumerate(zip(pl, tl), 1):
    if a != b and "___" not in a:
        print("MISMATCH line", i, repr(a), repr(b))
for i, a in enumerate(pl, 1):
    if "___" in a: print("blank line", i, repr(a))
for i, b in enumerate(tl, 1):
    if "return" in b: print("twin return line", i, repr(b))
