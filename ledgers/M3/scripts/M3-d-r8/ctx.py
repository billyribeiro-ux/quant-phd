import re, html, sys
lesson, pats = sys.argv[1], sys.argv[2:]
raw = open(f"course/modules/M/M3/{lesson}.html", encoding="utf-8").read()
raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
raw = re.sub(r"<(p|li|h2|h3|h4|div|section|pre|dd|dt|tr)[ >]", r"\n<\1 ", raw)
txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
txt = re.sub(r"[ \t]+", " ", txt)
for p in pats:
    for m in re.finditer(re.escape(p), txt):
        s = txt.rfind("\n", 0, m.start()); e = txt.find("\n", m.end())
        print(f"[{lesson}:{p}] ...{' '.join(txt[s+1:e if e>0 else None].split())[:700]}")
        print()
