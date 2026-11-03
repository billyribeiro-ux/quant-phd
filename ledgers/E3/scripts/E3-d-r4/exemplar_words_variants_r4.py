"""Round-4 verifier (E3-d): exemplar word-count variants for project.html (page says A = 103, B = 554)."""
import html
import re
import sys

src = open(sys.argv[1] if len(sys.argv) > 1 else "course/modules/E/E3/project.html", encoding="utf-8").read()


def memo(aid: str) -> str:
    start = src.index(f'<article class="exemplar" id="{aid}"')
    end = src.index("</article>", start)
    return "\n".join(re.findall(r'<div class="memo-text">(.*?)</div>\s*<aside', src[start:end], flags=re.S))


def variants(raw: str) -> dict[str, int]:
    no_tags_empty = html.unescape(re.sub(r"<[^>]+>", "", raw))
    no_tags_space = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    return {
        "tags->'' split() any whitespace": len(no_tags_empty.split()),
        "tags->' ' split() any whitespace": len(no_tags_space.split()),
        "tags->'' split(' ') literal spaces, drop empties": len([w for w in no_tags_empty.split(" ") if w]),
        "tags->' ' split(' ') literal spaces, drop empties": len([w for w in no_tags_space.split(" ") if w]),
        "tags->'' split(' ') keep empties": len(no_tags_empty.split(" ")),
    }


for aid in ("exemplar-a", "exemplar-b"):
    raw = memo(aid)
    for name, n in variants(raw).items():
        print(aid, "|", name, "|", n)
    body = re.sub(r"<h5>.*?</h5>", "", raw, flags=re.S)
    print(aid, "| headings removed, tags->' ' split() |", len(html.unescape(re.sub(r"<[^>]+>", " ", body)).split()))
