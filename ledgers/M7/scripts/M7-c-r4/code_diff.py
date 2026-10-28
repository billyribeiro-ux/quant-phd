import html, re, difflib
root = "/tmp/verifyB4-M7-c/"
for lab in ["L07", "L08"]:
    src = open(f"{root}tests/labs/M7/lab-M7-{lab}-1.py", encoding="utf-8").read()
    h = open(f"{root}course/modules/M/M7/{lab}.html", encoding="utf-8").read()
    code = html.unescape(re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', h, re.S)[0])
    print(lab, "repr tail src", repr(src[-30:]), "code tail", repr(code[-30:]))
    for l in difflib.unified_diff(src.splitlines(True), code.splitlines(True), "twin", "page", n=0):
        print(repr(l))
