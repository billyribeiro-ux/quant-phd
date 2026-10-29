import re, html, sys
page, out = sys.argv[1], sys.argv[2]
s = open(page, encoding="utf-8").read()
m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', s, re.S)
exp = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
got = open(out, encoding="utf-8").read()
print("expected==twin:", exp.strip() == got.strip(), len(exp.strip().splitlines()), len(got.strip().splitlines()))
