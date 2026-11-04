import re, sys, html
src = open(sys.argv[1], encoding="utf-8").read()
src = re.sub(r"<script.*?</script>", "", src, flags=re.S)
src = re.sub(r"<style.*?</style>", "", src, flags=re.S)
src = re.sub(r"<(br|/p|/li|/h[1-6]|/div|/tr|/pre|/section|/details|/summary|/figcaption)[^>]*>", "\n", src)
src = re.sub(r"</?[a-zA-Z][^>]*>", "", src)
src = html.unescape(src)
lines = [re.sub(r"[ \t]+", " ", l).strip() for l in src.split("\n")]
out = []
for l in lines:
    if l or (out and out[-1]):
        out.append(l)
print("\n".join(out))
