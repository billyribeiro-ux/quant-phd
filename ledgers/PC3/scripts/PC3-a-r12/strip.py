import html, re, sys
path = sys.argv[1]
for n, line in enumerate(open(path, encoding="utf-8"), 1):
    t = re.sub(r"<[^>]+>", "", line)
    t = html.unescape(t).strip()
    if t:
        print(f"{n}: {t}")
