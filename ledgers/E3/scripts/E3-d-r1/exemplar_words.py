"""Word counts of the two exemplar memos on project.html (headings included), and the prize/pair facts they quote."""
import html, re
src = open("course/modules/E/E3/project.html", encoding="utf-8").read()
for label in ("exemplar-a", "exemplar-b"):
    art = src[src.index(f'id="{label}"'):]
    art = art[:art.index("</article>")]
    memos = re.findall(r'<div class="memo-text">(.*?)</div>', art, re.S)
    total = 0
    for m in memos:
        text = html.unescape(re.sub(r"<[^>]+>", " ", m))
        n = len(text.split())
        total += n
        print(label, "memo block words", n)
    print(label, "TOTAL words (headings included, tags stripped)", total)
