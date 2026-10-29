import html, re, sys
root = sys.argv[1]
for lid in ["L01", "L02", "L03", "L04"]:
    page = open(f"{root}/course/modules/M/M6/{lid}.html").read()
    m = re.search(r'<code class="language-python" data-run>(.*?)</code>', page, re.S)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    twin_path = f"{root}/tests/labs/M6/lab-M6-{lid}-1.py"
    twin = open(twin_path).read()
    code = html.unescape(m.group(1))
    print(lid, "code==twin:", code.rstrip("\n") == twin.rstrip("\n"), "len", len(code), len(twin), "expected-blocks:", len(re.findall(r'class="expected"', page)))
    if exp:
        print(lid, "expected-block bytes", len(html.unescape(exp.group(1))))
