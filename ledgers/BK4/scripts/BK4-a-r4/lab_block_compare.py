import re, sys, html
page, twin, out = sys.argv[1], sys.argv[2], sys.argv[3]
t = open(page, encoding="utf-8").read()
blocks = re.findall(r"<pre([^>]*)>(.*?)</pre>", t, re.S)
print("pre blocks:", len(blocks))
for attrs, body in blocks:
    txt = html.unescape(re.sub(r"<[^>]+>", "", body))
    print("  attrs:", attrs.strip()[:90], "| lines:", txt.count("\n"), "| first:", txt.strip()[:60].replace("\n", " / "))
code = open(twin, encoding="utf-8").read()
output = open(out, encoding="utf-8").read()
def norm(s): return [l.rstrip() for l in s.strip().splitlines()]
best = None
for attrs, body in blocks:
    txt = html.unescape(re.sub(r"<[^>]+>", "", body))
    if norm(txt) == norm(code):
        print("CODE block equals twin:", attrs.strip()[:60])
        best = "code"
    if norm(txt) == norm(output):
        print("OUTPUT block equals twin run output:", attrs.strip()[:60])
