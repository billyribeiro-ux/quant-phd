"""Count words of each exemplar's memo-text (the report body) and its Summary, per the brief's rule: a word is a run of characters between spaces."""
import re, html, pathlib, sys
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB11-M4-d")
page = (ROOT / "course/modules/M/M4/project.html").read_text(encoding="utf-8")
def article(name):
    m = re.search(rf'<article class="exemplar" id="{name}".*?</article>', page, re.S)
    return m.group(0)
def memo_texts(art):
    out = []
    for m in re.finditer(r'<div class="memo-text">(.*?)</div>', art, re.S):
        body = m.group(1)
        heading = re.search(r'<h5>(.*?)</h5>', body, re.S)
        text = re.sub(r'<h5>.*?</h5>', '', body, flags=re.S)
        text = html.unescape(re.sub(r'<[^>]+>', ' ', text))
        out.append((html.unescape(re.sub(r'<[^>]+>', '', heading.group(1))) if heading else '', text))
    return out
def words(s):
    return len([w for w in s.split() if w])
for name in ("exemplar-a", "exemplar-b"):
    art = article(name)
    passages = memo_texts(art)
    total = 0
    for h, t in passages:
        n = words(t)
        total += n
        print(f"{name} | {h!r}: {n} words")
    print(f"{name} | body total (all memo-text passages): {total} words")
    if passages:
        print(f"{name} | Summary words: {words(passages[0][1])}")
