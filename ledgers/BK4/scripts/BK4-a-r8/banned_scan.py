"""Scan visible prose of the BK4 slice pages for banned strings, filler, process words and ellipses."""
import re
import sys

PAGES = ["course/modules/BK/BK4/index.html", "course/modules/BK/BK4/L01.html",
         "course/modules/BK/BK4/L02.html", "course/modules/BK/BK4/L03.html"]
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "it can be shown", "round", "fixer", "verifier", "builder", "erratum",
          "revision", "previous version", "we changed", "updated", "placeholder", "coming soon", "not yet written"]
PROCESS = re.compile(r"\b(builder|fixer|verifier|verification|round \d|revision|reviewer|ledger|pin|batch)\b", re.I)
hits = 0
for p in PAGES:
    raw = open(p, encoding="utf-8").read()
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<pre><code.*?</code></pre>", " ", raw, flags=re.S)
    raw = re.sub(r"<pre class=\"expected\".*?</pre>", " ", raw, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", raw)
    text = text.replace("&amp;", "&").replace("&nbsp;", " ")
    for lineno, line in enumerate(text.split("\n"), 1):
        low = line.lower()
        for b in BANNED:
            if re.search(r"\b" + re.escape(b.lower()) + r"\b", low):
                print(f"{p}: banned/filler '{b}': ...{line.strip()[:140]}")
                hits += 1
        for m in PROCESS.finditer(line):
            print(f"{p}: process word '{m.group(0)}': ...{line.strip()[:140]}")
            hits += 1
        for m in re.finditer(r"\.\.\.|…", line):
            print(f"{p}: ellipsis: ...{line.strip()[:140]}")
            hits += 1
print("hits", hits)
