import html, re, sys, pathlib
src = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
for f in sorted(src.glob("L*.html")):
    t = f.read_text(encoding="utf-8")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<(br|/p|/li|/h\d|/tr|/pre|/div)[^>]*>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    lines = [re.sub(r"[ \t]+", " ", l).strip() for l in t.split("\n")]
    (out / (f.stem + ".txt")).write_text("\n".join(l for l in lines if l), encoding="utf-8")
