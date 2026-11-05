"""Compare each project lab's page code with its twin (page code unescaped; blanks allowed for lab 2)."""
import html
import re
import sys

PAGE = "course/modules/LX/LX2/project.html"
src = open(PAGE, encoding="utf-8").read()
blocks = re.findall(r'<section class="lab[^"]*" id="(lab-LX2-project-\d)"[^>]*>.*?<pre><code[^>]*data-run>(.*?)</code></pre>', src, flags=re.S)
for lab_id, raw in blocks:
    code = html.unescape(raw)
    n = lab_id[-1]
    twin = open(f"tests/labs/LX2/lab-LX2-project-{n}.py", encoding="utf-8").read()
    if code.rstrip("\n") == twin.rstrip("\n"):
        print(lab_id, "page == twin (byte-identical, trailing newlines aside)")
        continue
    pl = code.rstrip("\n").split("\n")
    tl = twin.rstrip("\n").split("\n")
    print(lab_id, "differs: page lines", len(pl), "twin lines", len(tl))
    for i, (a, b) in enumerate(zip(pl, tl), 1):
        if a != b:
            print(f"  line {i}: page={a!r}\n           twin={b!r}")
    if len(pl) != len(tl):
        print("  length differs")
