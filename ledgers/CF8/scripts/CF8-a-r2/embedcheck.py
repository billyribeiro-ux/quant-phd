import html, re, sys
for page, twin in [("course/modules/CF/CF8/L01.html", "tests/labs/CF8/lab-CF8-L01-1.py"), ("course/modules/CF/CF8/L02.html", "tests/labs/CF8/lab-CF8-L02-1.py")]:
    src = open(page, encoding="utf-8").read()
    m = re.search(r'<code class="language-python" data-run>(.*?)</code>', src, re.S)
    code = html.unescape(m.group(1))
    tw = open(twin, encoding="utf-8").read()
    print(page, "embedded==twin:", code.strip() == tw.strip(), len(code), len(tw))
