import html, re, sys
src = open(sys.argv[1], encoding="utf-8").read()
src = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", "", src)
src = re.sub(r"(?i)</(p|li|div|h[1-6]|tr|pre|details|summary|dt|dd|section)>", "\n", src)
src = re.sub(r"(?i)<br\s*/?>", "\n", src)
src = re.sub(r"<[^>]+>", "", src)
out = html.unescape(src)
lines = [ln.rstrip() for ln in out.splitlines()]
print("\n".join(l for l in lines if l.strip()))
