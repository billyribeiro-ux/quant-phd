import html, re, sys, pathlib
src = pathlib.Path(sys.argv[1]); dst = pathlib.Path(sys.argv[2])
t = src.read_text(encoding="utf-8")
t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
t = re.sub(r"<[^>]+>", " ", t)
t = html.unescape(t)
t = re.sub(r"[ \t]+", " ", t)
t = re.sub(r"\n\s*\n+", "\n", t)
dst.write_text(t, encoding="utf-8")
