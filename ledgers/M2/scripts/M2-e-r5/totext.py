import html, re, sys, pathlib
src = pathlib.Path("/tmp/verifyB5-M2-e/course/modules/M/M2")
out = pathlib.Path("/tmp/M2-v/M2-e-r5/text")
for p in sorted(src.glob("L*.html")):
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"(?is)<script.*?</script>", "", s)
    s = re.sub(r"(?is)<style.*?</style>", "", s)
    s = re.sub(r"(?i)<br\s*/?>", "\n", s)
    s = re.sub(r"(?i)</(p|li|h[1-6]|div|tr|section|pre|dt|dd|ol|ul|table|article|aside|blockquote)>", "\n", s)
    s = re.sub(r"(?i)<(h[1-6])[^>]*>", "\n## ", s)
    s = re.sub(r"(?s)</?[a-zA-Z][a-zA-Z0-9]*(?:\s[^<>]*)?/?>", "", s)
    s = html.unescape(s)
    lines = [ln.strip() for ln in s.split("\n")]
    lines = [ln for ln in lines if ln]
    (out / (p.stem + ".txt")).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(p.stem, len(lines), sum(len(l) for l in lines))
