import html, re, sys
root = "/tmp/verifyB4-M7-c/"
for lab, page in [("L07", "L07"), ("L08", "L08")]:
    src = open(f"{root}tests/labs/M7/lab-M7-{lab}-1.py", encoding="utf-8").read()
    out = open(f"/tmp/M7-v/c4/twin_{lab}.out", encoding="utf-8").read()
    h = open(f"{root}course/modules/M/M7/{page}.html", encoding="utf-8").read()
    codes = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', h, re.S)
    exps = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', h, re.S)
    print(lab, "code blocks", len(codes), "expected blocks", len(exps))
    for c in codes:
        print(" code==twin:", html.unescape(c) == src, " len", len(html.unescape(c)), len(src))
    for e in exps:
        print(" expected==actual:", html.unescape(e).rstrip("\n") == out.rstrip("\n"))
        print(" expected sample:", repr(html.unescape(e)[:120]))
