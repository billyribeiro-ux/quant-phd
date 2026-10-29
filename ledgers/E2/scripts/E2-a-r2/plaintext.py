import re, sys, html
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
s = re.sub(r"<script.*?</script>", "", s, flags=re.S)
s = re.sub(r"<style.*?</style>", "", s, flags=re.S)
s = re.sub(r"<(?=[a-zA-Z/!])[^>]*>", "", s)
s = html.unescape(s)
lines = [l.strip() for l in s.split("\n")]
out = [l for l in lines if l]
open(dst, "w", encoding="utf-8").write("\n".join(f"{i+1}\t{l}" for i, l in enumerate(out)) + "\n")
print(dst, len(out))
