"""E4 slice b (L04-L06) prose checks: word counts, banned strings, dfn/concept definitions, dash-free ellipses."""
import html
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "...", "…"]
PROCESS = ["builder", "verifier", "round", "REQUEST", "unit report", "pending"]
for lesson in ["L04", "L05", "L06"]:
    text = (ROOT / f"course/modules/E/E4/{lesson}.html").read_text(encoding="utf-8")
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', text, re.S)
    body = html.unescape(re.sub(r"</?[a-zA-Z][^>]*>", "", m.group(1)))
    print(lesson, "why-it-matters words:", len(body.split()))
    for b in BANNED:
        hits = [i + 1 for i, line in enumerate(text.splitlines()) if b in line]
        if hits:
            print(lesson, "banned", repr(b), "lines", hits[:20])
    for p in PROCESS:
        hits = [i + 1 for i, line in enumerate(text.splitlines()) if p.lower() in line.lower()]
        if hits:
            print(lesson, "process-word", repr(p), "lines", hits[:20])
    dfns = re.findall(r'<dfn([^>]*)>([^<]*)</dfn>', text)
    print(lesson, "dfn count", len(dfns))
    for attrs, term in dfns:
        print("   dfn", attrs.strip(), "|", term)
    sols = re.findall(r'<details class="solution">(.*?)</details>', text, re.S)
    short = [i for i, s in enumerate(sols) if len(html.unescape(re.sub(r"</?[a-zA-Z][^>]*>", "", s)).split()) < 15]
    print(lesson, "solutions", len(sols), "under-15-words", short)
    print(lesson, "misconceptions", text.count('class="misconception"'), "quiz items", text.count('class="item"'))
    print(lesson, "claim spans", len(re.findall(r'class="claim"', text)), "data-cite", len(re.findall(r'data-cite', text)))
