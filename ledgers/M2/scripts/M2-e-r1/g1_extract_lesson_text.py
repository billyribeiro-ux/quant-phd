import html, pathlib, re
root = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyG1-M2-e/course/modules/M/M2")
out = pathlib.Path("/tmp/m2e_r1b/text")
for i in range(1, 25):
    raw = (root / f"L{i:02d}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<(?=[\s\d\\(=])", "&lt;", raw)
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<style.*?</style>", " ", raw, flags=re.S)
    raw = re.sub(r"<(p|li|tr|h[1-6]|div|section|pre|dt|dd|blockquote)[^>]*>", "\n", raw)
    raw = re.sub(r"<br\s*/?>", "\n", raw)
    text = html.unescape(re.sub(r"<[^>]+>", "", raw))
    (out / f"L{i:02d}.txt").write_text(text, encoding="utf-8")
print("ok")
