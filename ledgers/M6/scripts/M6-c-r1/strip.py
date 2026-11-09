import sys, re, html
path = sys.argv[1]
for i, line in enumerate(open(path, encoding="utf-8"), 1):
    t = re.sub(r"</?[a-zA-Z!][^>]*>", "", line)
    t = html.unescape(t).strip()
    if t:
        print(f"{i}: {t}")
