import re, sys, html
src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding="utf-8").read()
t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
t = re.sub(r"<style.*?</style>", "", t, flags=re.S)
t = re.sub(r"<(/?)(p|div|h[1-6]|li|tr|section|figure|figcaption|pre|details|summary)\b[^>]*>", r"\n<\1\2>", t)
t = re.sub(r"</?[a-zA-Z][a-zA-Z0-9]*\b[^>]*>", "", t)
t = html.unescape(t)
lines = [ln.strip() for ln in t.split("\n")]
out = []
for i, ln in enumerate(lines):
    if ln:
        out.append(ln)
open(dst, "w", encoding="utf-8").write("\n".join(out))
print(dst, len(out), sum(len(x) for x in out))
