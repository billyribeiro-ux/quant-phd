"""Word counts of the two exemplar bodies (five sections, headings excluded; appendix excluded). A word is a run of
characters between spaces (project.html brief, Length). Usage: word_counts_r16.py <checkout root>."""
import html
import re
import sys

root = sys.argv[1]
page = open(f"{root}/course/modules/SC/SC1/project.html", encoding="utf-8").read()
for ex in ("exemplar-a", "exemplar-b"):
    body = re.search(rf'<article class="exemplar" id="{ex}".*?</article>', page, re.S).group(0)
    body = re.sub(r'<aside class="annotation".*?</aside>', " ", body, flags=re.S)
    body = re.sub(r'<p class="exemplar-verdict".*?</p>', " ", body, flags=re.S)
    passages = re.findall(r'<div class="memo-text">(.*?)</div>', body, re.S)
    counts = {}
    for p in passages:
        heading = re.search(r"<h5>(.*?)</h5>", p, re.S)
        name = html.unescape(re.sub(r"<[^>]+>", "", heading.group(1))).strip() if heading else "(no heading)"
        text = re.sub(r"<h5>.*?</h5>", " ", p, flags=re.S)
        text = html.unescape(re.sub(r"<[^>]+>", " ", text))
        counts[name] = len(text.split())
    body_names = [k for k in counts if not k.startswith("Appendix") and k != "(no heading)"]
    body_total = sum(counts[k] for k in body_names)
    appendix_total = sum(v for k, v in counts.items() if k not in body_names)
    print(f"{ex}: body sections {body_names} -> {body_total} words; other passages -> {appendix_total} words")
    for k, v in counts.items():
        print(f"    {k!r}: {v}")
