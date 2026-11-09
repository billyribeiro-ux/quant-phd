"""Count the words of each exemplar's five body sections, headings excluded, by the brief's rule (a word is a run of
characters between spaces). Whitespace runs (including newlines from the source) are normalised to one space first.
The appendix passage (the one whose heading or first line is the Assumptions/Proofs block, after the Limitations
passage) is excluded. Round 15, SC1-d."""
import html
import re
import sys
from pathlib import Path

page = Path(sys.argv[1], "course/modules/SC/SC1/project.html").read_text(encoding="utf-8")


def passages(exemplar_id):
    art = re.search(r'<article class="exemplar" id="%s".*?</article>' % exemplar_id, page, re.S).group(0)
    out = []
    for p in re.findall(r'<div class="passage">(.*?)</div>\s*</div>|<div class="passage">(.*?)</div>\s*(?=<aside|</article)', art, re.S):
        pass
    for block in re.split(r'<div class="passage">', art)[1:]:
        memo = re.search(r'<div class="memo-text">(.*?)</div>\s*(?:<aside|$)', block, re.S)
        if not memo:
            memo = re.search(r'<div class="memo-text">(.*)', block, re.S)
        inner = memo.group(1)
        head = re.search(r"<h5>(.*?)</h5>", inner, re.S)
        title = html.unescape(re.sub(r"<[^>]+>", "", head.group(1))) if head else "(no heading)"
        body = re.sub(r"<h5>.*?</h5>", " ", inner, flags=re.S)
        text = html.unescape(re.sub(r"<[^>]+>", " ", body))
        text = re.sub(r"\s+", " ", text).strip()
        out.append((title, text))
    return out


for ex, nsec in (("exemplar-a", 5), ("exemplar-b", 5)):
    ps = passages(ex)
    for title, text in ps:
        print(f"{ex} | {title} | words={len(text.split(' '))}")
    body = [t for ti, t in ps if ti in ("Summary", "Setup and conventions", "The checks", "Discretization", "Limitations")]
    print(f"{ex} five-section body words={sum(len(t.split(' ')) for t in body)} sections={len(body)}")
