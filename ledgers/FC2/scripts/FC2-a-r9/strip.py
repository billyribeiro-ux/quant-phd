import re, sys, html
src, dst = sys.argv[1], sys.argv[2]
out = []
for i, line in enumerate(open(src, encoding='utf-8'), 1):
    t = re.sub(r"</?[a-zA-Z!][^>]*>", "", line)
    t = html.unescape(t).rstrip()
    out.append(f"{i:4d}| {t}")
open(dst, 'w', encoding='utf-8').write("\n".join(out) + "\n")
