import html, re
root = "/tmp/verify7-AC4-c"
for page, twin in [("course/modules/AC/AC4/L05.html", "tests/labs/AC4/lab-AC4-L05-1.py"), ("course/modules/AC/AC4/L06.html", "tests/labs/AC4/lab-AC4-L06-1.py")]:
    t = open(f"{root}/{page}", encoding="utf-8").read()
    m = re.search(r'<code class="language-python" data-run>(.*?)</code>', t, re.S)
    code = html.unescape(m.group(1))
    tw = open(f"{root}/{twin}", encoding="utf-8").read()
    print(page, "embedded == twin:", code.rstrip("\n") == tw.rstrip("\n"), len(code), len(tw))
