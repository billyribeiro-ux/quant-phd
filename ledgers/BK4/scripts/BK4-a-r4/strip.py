import html, re, sys
tag = re.compile(r"<(?=[A-Za-z/!])[^>]*>")
for n, line in enumerate(open(sys.argv[1], encoding="utf-8"), 1):
    t = html.unescape(tag.sub("", line)).strip()
    if t:
        print(f"{n}: {t}")
