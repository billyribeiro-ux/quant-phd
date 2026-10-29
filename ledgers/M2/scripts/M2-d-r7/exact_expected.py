import sys, re, html
page, out = sys.argv[1], sys.argv[2]
src = open(page, encoding="utf-8").read()
m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
exp = html.unescape(m.group(1)).rstrip("\n").splitlines()
got = open(out, encoding="utf-8").read().rstrip("\n").splitlines()
print(page.split("/")[-1], "expected lines", len(exp), "output lines", len(got), "EXACT" if exp == got else "DIFF")
for i, (a, b) in enumerate(zip(exp, got)):
    if a != b:
        print(" line", i + 1, "\n  page:", a, "\n  twin:", b)
