"""Word count of the Exemplar A memo body (six paragraphs under the brief headings) in project.html. Run with python -I from the checkout root."""
import html, re
src = open("course/modules/E/E5/project.html", encoding="utf-8").read()
start = src.index('id="exemplar-a"')
end = src.index('id="exemplar-b"')
block = src[start:end]
paras = re.findall(r"<p(?: [^>]*)?>(.*?)</p>", block, re.S)
body = []
for p in paras:
    t = html.unescape(re.sub(r"<[^>]+>", "", p)).strip()
    if not t or t.startswith(("Official scoring", "Meets ", "Misses ")):
        continue
    body.append(t)
heads = re.findall(r"<h5>(.*?)</h5>", block)
words = sum(len(t.split()) for t in body)
print("memo paragraphs", len(body), "body words", words, "headings", len(heads), "heading words", sum(len(h.split()) for h in heads), "total", words + sum(len(h.split()) for h in heads))
print("limit 600 (project.html spec Constraints)")
