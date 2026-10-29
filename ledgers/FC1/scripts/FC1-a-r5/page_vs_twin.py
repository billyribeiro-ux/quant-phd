import html, re, sys
root = "/Users/billyribeiro/.fanout/wt/verifyC5-FC1-a/"
for lab, page in (("L01-1", "L01"), ("L02-1", "L02"), ("L03-1", "L03")):
    src = open(root + f"course/modules/FC/FC1/{page}.html", encoding="utf-8").read()
    twin = open(root + f"tests/labs/FC1/lab-FC1-{lab}.py", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    code = html.unescape(m.group(1))
    out = open(f"/tmp/fc1a-r5/twin-{lab}.out", encoding="utf-8").read()
    after = src[m.end():]
    m2 = re.search(r'<pre[^>]*>(.*?)</pre>', after, re.S)
    expected = html.unescape(m2.group(1)) if m2 else None
    print(lab, "code==twin:", code.strip() == twin.strip(), "| expected==output:", expected is not None and expected.strip() == out.strip(), "| expected first line:", (expected or "")[:60].replace("\n", " | "))
