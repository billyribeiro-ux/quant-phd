"""Print short text windows around a regex match in a lesson page (tags stripped). Usage: ctx.py FILE REGEX [WIDTH] [MAX]"""
import html, re, sys
f, pat = sys.argv[1], sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 else 250
mx = int(sys.argv[4]) if len(sys.argv) > 4 else 3
raw = open(f, encoding="utf-8").read()
raw = re.sub(r"(?s)<script.*?</script>", " ", raw)
raw = re.sub(r"<[^>]+>", " ", raw)
t = re.sub(r"\s+", " ", html.unescape(raw))
for i, m in enumerate(re.finditer(pat, t)):
    if i >= mx:
        break
    print("...", t[max(0, m.start() - w): m.end() + w], "...\n")
