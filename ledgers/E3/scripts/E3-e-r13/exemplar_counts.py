"""E3-e round 12: exemplar memo word counts in course/modules/E/E3/project.html (run with python -I)."""
import html
import re
import sys

s = open(f"{sys.argv[1]}/course/modules/E/E3/project.html", encoding="utf-8").read()
for ex in ["exemplar-a", "exemplar-b"]:
    i = s.index(f'id="{ex}"')
    j = s.index("</article>", i)
    passages = re.findall(r'<div class="memo-text">(.*?)</div>\s*<aside', s[i:j], re.S)
    total = sum(len(html.unescape(re.sub(r"<[^>]+>", " ", p)).split()) for p in passages)
    body = sum(
        len(html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<h5>.*?</h5>", "", p, flags=re.S))).split())
        for p in passages
    )
    print(ex, "passages", len(passages), "words incl. headings", total, "body only", body)
