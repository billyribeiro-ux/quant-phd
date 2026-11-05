"""Round-11: word counts of the two exemplar memo texts (project.html), tags removed, runs of non-space characters."""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
page = (ROOT / "course/modules/E/E3/project.html").read_text(encoding="utf-8")


def words(fragment: str) -> int:
    text = re.sub(r"<[^>]+>", " ", fragment)
    return len(html.unescape(text).split())


for label in ("exemplar-a", "exemplar-b"):
    article = re.search(rf'<article class="exemplar" id="{label}".*?</article>', page, re.S).group(0)
    memo_divs = re.findall(r'<div class="memo-text">(.*?)</div>', article, re.S)
    memo = sum(words(d) for d in memo_divs)
    annotations = sum(words(a) for a in re.findall(r'<aside class="annotation".*?</aside>', article, re.S))
    verdict = sum(words(v) for v in re.findall(r'<p class="exemplar-verdict"[^>]*>(.*?)</p>', article, re.S))
    print(f"{label}: memo-text divs={memo} (n={len(memo_divs)}) memo+annotations={memo + annotations} memo+verdict={memo + verdict} whole-article={words(article)}")
claim = re.search(r"the memo text of Exemplar A is (\d+) words and that of Exemplar B is (\d+) words", page)
print("claim:", claim.groups() if claim else None)
