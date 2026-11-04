import html, re, sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
src = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", "", src)
src = re.sub(r"(?i)<br\s*/?>", "\n", src)
src = re.sub(r"(?i)</(p|li|h[1-6]|div|pre|tr|summary|dt|dd|section|figcaption)>", "\n", src)
src = re.sub(r"(?s)</?[A-Za-z][^<>]*>", "", src)
src = re.sub(r"(?s)<!--.*?-->", "", src)
src = html.unescape(src)
out = [l.strip() for l in src.splitlines() if l.strip()]
print("\n".join(out))
