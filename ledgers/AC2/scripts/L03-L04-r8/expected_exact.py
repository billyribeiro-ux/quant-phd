import html, re, sys
root = sys.argv[1]
for n in ("03", "04"):
    page = open(f"{root}/course/modules/AC/AC2/L{n}.html", encoding="utf-8").read()
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)).strip()
    out = open(f"/tmp/ac2-v/L03-L04/r8/twin_L{n}.txt", encoding="utf-8").read().strip()
    print("L" + n, "expected == twin stdout:", exp == out, "lines", len(exp.splitlines()), len(out.splitlines()))
