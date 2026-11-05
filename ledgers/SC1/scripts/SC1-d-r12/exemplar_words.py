"""Word counts of the five report sections of each exemplar (body, headings excluded), per the brief's word rule."""
import html
import re
import sys
from pathlib import Path

page = Path(sys.argv[1], "course/modules/SC/SC1/project.html").read_text(encoding="utf-8")
for ex in ("exemplar-a", "exemplar-b"):
    start = page.index(f'id="{ex}"')
    end = page.index("</article>", start)
    block = re.sub(r'<aside class="annotation".*?</aside>', "", page[start:end], flags=re.S)
    block = re.sub(r'<p class="exemplar-verdict".*?</p>', "", block, flags=re.S)
    sections = re.split(r'<h5>(.*?)</h5>', block)
    print(ex, "headings:", [html.unescape(h) for h in sections[1::2]])
    total = 0
    for title, body in zip(sections[1::2], sections[2::2]):
        text = html.unescape(re.sub(r"<[^>]+>", " ", body))
        n = len(text.split())
        if title.startswith("Appendix"):
            print(f"  {title}: {n} words (appendix, no limit)")
        else:
            print(f"  {title}: {n} words")
            total += n
    print(f"  body total (five sections, excluding appendix): {total} words")
