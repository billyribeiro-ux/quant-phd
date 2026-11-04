"""Round-2 BK4-a scan: banned strings (BUILDER_RULES 1.3-1.4), process words, and ASCII ellipses in visible text."""

import html
import re

D = "course/modules/BK/BK4/"
banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "it can be shown"]
process = r"\b(build|builder|builders|round|verifier|verify|verified|REQUESTS?|unit report|fixer|planner|architect|ledger|Builder)\b"
hits = 0
for page in ["index.html", "L01.html", "L02.html", "L03.html"]:
    raw = open(D + page, encoding="utf-8").read()
    txt = re.sub(r"<script.*?</script>|<style.*?</style>", "", raw, flags=re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", txt))
    for b in banned:
        for m in re.finditer(re.escape(b), txt, re.I):
            hits += 1
            print(page, "BANNED", b, txt[max(0, m.start() - 60):m.end() + 40])
    for m in re.finditer(process, txt, re.I):
        hits += 1
        print(page, "PROCESS", m.group(0), txt[max(0, m.start() - 60):m.end() + 40])
    for m in re.finditer(r"\.\.\.", txt):
        hits += 1
        print(page, "ELLIPSIS", txt[max(0, m.start() - 40):m.end() + 20])
print("hits", hits)
