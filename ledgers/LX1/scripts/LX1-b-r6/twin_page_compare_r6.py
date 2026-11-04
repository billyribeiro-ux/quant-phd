import re, sys, html
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE6-LX1-b"
for page, twin in (("L03", "lab-LX1-L03-1"), ("L04", "lab-LX1-L04-1")):
    src = open(f"{ROOT}/course/modules/LX/LX1/{page}.html", encoding="utf-8").read()
    m = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    code = html.unescape(m.group(1))
    twin_src = open(f"{ROOT}/tests/labs/LX1/{twin}.py", encoding="utf-8").read()
    print(page, "page code equals twin (rstrip):", code.rstrip() == twin_src.rstrip(), "len", len(code), len(twin_src))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    exp = html.unescape(e.group(1)).rstrip("\n").split("\n")
    out = open(f"{ROOT}/ledgers/LX1/scripts/LX1-b-r6/twin_{page}.out", encoding="utf-8").read().rstrip("\n").split("\n")
    print(page, "expected block lines", len(exp), "twin output lines", len(out), "equal:", exp == out)
    if exp != out:
        for i, (a, b) in enumerate(zip(exp, out)):
            if a != b:
                print("DIFF", i, repr(a), repr(b))
