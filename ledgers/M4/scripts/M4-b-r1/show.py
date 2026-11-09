import re, sys, html
path, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
lines = open(path, encoding="utf-8").read().split("\n")
for i in range(a, b + 1):
    t = html.unescape(re.sub(r"<[^>]*>", "", lines[i - 1])).strip()
    if t:
        print(f"{i}: {t}")
