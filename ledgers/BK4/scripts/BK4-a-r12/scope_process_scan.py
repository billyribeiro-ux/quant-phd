"""Round 12 banned-phrase, process-word and scope-word scan for BK4 slice a (index, L01-L03, twins).
Word-boundary matching. Usage: python3 -I scope_process_scan.py <checkout_root>"""

import html
import os
import re
import sys

root = sys.argv[1]
base = os.path.join(root, "course/modules/BK/BK4")
files = [os.path.join(base, f) for f in ["index.html", "L01.html", "L02.html", "L03.html"]]
files += [os.path.join(root, "tests/labs/BK4", f"lab-BK4-L0{n}-1.py") for n in "123"]
banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly"]
process = ["builder", "verifier", "fixer", "ruling", "architect", "REQUEST", "unit report", "round", "plans/"]
hits = 0
for f in files:
    s = open(f, encoding="utf-8").read()
    for w in banned + process:
        for m in re.finditer(r"(?<![A-Za-z])" + re.escape(w) + r"(?![A-Za-z])", s, re.I):
            hits += 1
            print("HIT", os.path.basename(f), repr(w), s[max(0, m.start() - 30):m.end() + 20].replace("\n", " "))
    if f.endswith(".html"):
        t = re.sub(r"<script.*?</script>|<pre.*?</pre>|<code.*?</code>", "", s, flags=re.S)
        t = html.unescape(re.sub(r"<[^>]+>", " ", t))
        for m in re.finditer(r"\.\.\.", t):
            hits += 1
            print("ELLIPSIS", os.path.basename(f), t[max(0, m.start() - 30):m.end() + 10].replace("\n", " "))
print("banned and process-word hits (word boundary):", hits)
scope = ["only", "all", "every", "always", "never", "same", "exactly", "any"]
counts = {w: 0 for w in scope}
for f in files:
    s = open(f, encoding="utf-8").read().lower()
    for w in scope:
        counts[w] += len(re.findall(r"(?<![a-z])" + w + r"(?![a-z])", s))
print("scope word occurrences (index, L01-L03, twins, raw source):", counts)
