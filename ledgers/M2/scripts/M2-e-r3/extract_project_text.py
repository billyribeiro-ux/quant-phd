import re, html, sys
src = open(sys.argv[1], encoding="utf-8").read()
s = re.sub(r"<script.*?</script>", "", src, flags=re.S)
s = re.sub(r"<style.*?</style>", "", s, flags=re.S)
s = re.sub(r"<(br|/p|/li|/dd|/dt|/h[1-6]|/tr|/pre|/div|/section)[^>]*>", "\n", s)
s = re.sub(r"<[^>]+>", "", s)
s = html.unescape(s)
print("\n".join(l.rstrip() for l in s.split("\n") if l.strip()))
