import re, sys, html
src = open(sys.argv[1], encoding="utf-8").read()
src = re.sub(r"<(script|style)\b.*?</\1>", "", src, flags=re.S)
src = re.sub(r"<!--.*?-->", "", src, flags=re.S)
src = re.sub(r"</(p|li|h[1-6]|div|section|pre|tr|dt|dd|blockquote|figcaption|td|th)>|<br\s*/?>", "\n", src)
txt = re.sub(r"<[^>]+>", "", src)
txt = html.unescape(txt)
lines = [re.sub(r"[ \t]+", " ", l).strip() for l in txt.split("\n")]
lines = [l for l in lines if l]
print("\n".join(lines))
