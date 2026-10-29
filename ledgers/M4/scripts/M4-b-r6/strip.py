import re, sys, html
src = open(sys.argv[1], encoding="utf-8").read()
src = re.sub(r"(?s)<script.*?</script>", "", src)
src = re.sub(r"(?s)<style.*?</style>", "", src)
src = re.sub(r"(?i)<(br|/p|/li|/h[1-6]|/div|/tr|/pre|/section)[^>]*>", "\n", src)
txt = html.unescape(re.sub(r"<\/?[a-zA-Z!][^>]*>", "", src))
out = [l.rstrip() for l in txt.split("\n") if l.strip()]
print("\n".join(out))
