import re, sys, html
f, pat = sys.argv[1], sys.argv[2]
t = open(f, encoding="utf-8").read()
for m in re.finditer(r'<span class="block-title[^"]*"[^>]*>(.*?)</span>', t, re.S):
    title = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
    if re.search(pat, title):
        seg = t[m.end(): m.end() + 1400]
        seg = html.unescape(re.sub(r"<[^>]+>", " ", seg))
        seg = re.sub(r"\s+", " ", seg)
        print("##", title, "::", seg[:900], "\n")
