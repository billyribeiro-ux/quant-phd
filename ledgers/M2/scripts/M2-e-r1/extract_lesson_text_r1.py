"""Plain text of each M2 lesson page (scripts and styles removed, tags stripped, entities decoded) into /tmp/m2e_r1_text."""
import html
import pathlib
import re

root = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyF21-M2-e")
out = pathlib.Path("/tmp/m2e_r1_text")
out.mkdir(parents=True, exist_ok=True)
for i in range(1, 25):
    raw = (root / f"course/modules/M/M2/L{i:02d}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<style.*?</style>", " ", raw, flags=re.S)
    raw = re.sub(r"<(p|li|tr|h[1-6]|div|section|pre|dt|dd|blockquote)[^>]*>", "\n", raw)
    raw = re.sub(r"<br\s*/?>", "\n", raw)
    text = html.unescape(re.sub(r"<[^>]+>", "", raw))
    (out / f"L{i:02d}.txt").write_text(text, encoding="utf-8")
print("lesson text written for L01-L24")
