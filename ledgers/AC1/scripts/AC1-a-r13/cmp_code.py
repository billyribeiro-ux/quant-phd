import html, re
root = "/tmp/verify13-AC1-a/"
for lid in ["L01", "L02", "L03"]:
    src = open(root + f"course/modules/AC/AC1/{lid}.html", encoding="utf-8").read()
    m = re.search(r'<code class="language-python" data-run>(.*?)</code>', src, re.S)
    code = html.unescape(m.group(1))
    twin = open(root + f"tests/labs/AC1/lab-AC1-{lid}-1.py", encoding="utf-8").read()
    print(lid, "data-run == twin:", code.strip() == twin.strip(), len(code), len(twin))
