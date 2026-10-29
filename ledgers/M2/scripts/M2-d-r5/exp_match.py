import html, re, sys
for p in ["19","20","21","22","23","24"]:
    src = open(f"/tmp/verifyB5-M2-d/course/modules/M/M2/L{p}.html", encoding="utf-8").read()
    m = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    out = open(f"/tmp/M2-v/d-r5/L{p}.out", encoding="utf-8").read()
    ok = [html.unescape(re.sub(r"<[^>]+>", "", x)).strip() == out.strip() for x in m]
    print(p, len(m), ok)
