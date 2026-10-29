import html, re, sys, difflib
root = sys.argv[1]
out = {"L01": "/tmp/r5-L01.out", "L02": "/tmp/r5-L02.out", "L03": "/tmp/r5-L03.out"}
for lid in ("L01", "L02", "L03"):
    page = open(f"{root}/course/modules/E/E5/{lid}.html", encoding="utf-8").read()
    twin = open(f"{root}/tests/labs/E5/lab-E5-{lid}-1.py", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    exp = html.unescape(re.sub(r"<[^>]+>", "", e.group(1)))
    ran = open(out[lid], encoding="utf-8").read()
    print(lid, "code==twin", code.strip() == twin.strip(), "expected==output", exp.strip() == ran.strip(),
          "explines", len(exp.strip().splitlines()), "outlines", len(ran.strip().splitlines()))
    if exp.strip() != ran.strip():
        print("\n".join(difflib.unified_diff(ran.strip().splitlines(), exp.strip().splitlines(), lineterm="")))
