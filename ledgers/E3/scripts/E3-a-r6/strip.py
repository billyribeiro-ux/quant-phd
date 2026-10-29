import html, re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
s = re.sub(r"<script.*?</script>", "", s, flags=re.S)
s = re.sub(r"<style.*?</style>", "", s, flags=re.S)
s = re.sub(r"<(?:/?(?:p|div|section|h[1-6]|li|tr|pre|table|ul|ol|blockquote|figure|figcaption|header|footer|nav|details|summary|dt|dd))\b[^>]*>", "\n", s)
s = re.sub(r"</?[a-zA-Z][^>]*>", "", s)
s = html.unescape(s)
lines = [l.rstrip() for l in s.splitlines()]
out = []
for l in lines:
    if l.strip() == "" and (not out or out[-1] == ""):
        continue
    out.append(l)
open(dst, "w", encoding="utf-8").write("\n".join(out) + "\n")
print(dst, len(out))
