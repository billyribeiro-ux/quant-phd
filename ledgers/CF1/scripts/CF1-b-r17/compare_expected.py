import re, html, sys
root = sys.argv[1]
pairs = [("course/modules/CF/CF1/L03.html", "/tmp/cf1-v/CF1-b-r17/l03.out"),
         ("course/modules/CF/CF1/L04.html", "/tmp/cf1-v/CF1-b-r17/l04.out")]
for page, out in pairs:
    s = open(root + "/" + page, encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', s, re.S)
    exp = html.unescape(m.group(1)).strip().splitlines()
    got = open(out, encoding="utf-8").read().strip().splitlines()
    print(page, "expected", len(exp), "got", len(got), "IDENTICAL" if exp == got else "DIFF")
    for a, b in zip(exp, got):
        if a != b:
            print("  exp:", a, "| got:", b)
