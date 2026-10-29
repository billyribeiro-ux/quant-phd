import html, re, sys
page, twin = sys.argv[1], sys.argv[2]
src = open(page, encoding="utf-8").read()
m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
exp = html.unescape(m.group(1)).strip("\n")
out = open(twin, encoding="utf-8").read().rstrip("\n")
print(page, "expected lines", len(exp.splitlines()), "twin lines", len(out.splitlines()), "identical" if exp == out else "DIFFERENT")
