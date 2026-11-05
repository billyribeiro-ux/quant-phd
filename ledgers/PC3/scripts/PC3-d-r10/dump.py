import html, json, re, sys
root = sys.argv[1]
base = root + "/course/modules/PC/PC3/"
out = sys.argv[2]
for n in range(1, 7):
    name = f"L0{n}.html"
    with open(base + name, encoding="utf-8") as f:
        lines = f.read().split("\n")
    with open(f"{out}/{name}.txt", "w", encoding="utf-8") as g:
        for i, line in enumerate(lines, 1):
            t = re.sub(r"<script.*?</script>", "", line, flags=re.S)
            t = re.sub(r"<[^>]+>", "", t)
            t = html.unescape(t).strip()
            if t:
                g.write(f"{i}|{t}\n")
cards = json.load(open(base + "cards.json", encoding="utf-8"))
with open(f"{out}/cards.txt", "w", encoding="utf-8") as g:
    for c in cards:
        g.write(f"{c['id']} | {c['lesson']} | grade={c.get('grade')} | cite={c.get('cite')} | basis={c.get('basis')}\n  F: {c['front']}\n  B: {c['back']}\n")
print(len(cards))
