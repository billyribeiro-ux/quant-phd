"""Word count of each exemplar memo body with the headings excluded (C5 band 300 to 600 words)."""
import html, pathlib, re, sys
s = (pathlib.Path(sys.argv[1]) / "course/modules/AC/AC4/project.html").read_text(encoding="utf-8")
for m in re.finditer(r'<div class="memo-text">(.*?)</div>\s*<aside', s, flags=re.S):
    body = m.group(1)
    heads = re.findall(r"<h5>(.*?)</h5>", body)
    text = re.sub(r"<h5>.*?</h5>", " ", body, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    print("headings", heads, "body words", len(text.split()))
