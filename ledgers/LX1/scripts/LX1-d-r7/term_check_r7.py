"""Round-7 check: is the term 'monetary base' defined (a <dfn>) anywhere in the course, and where is it used?

Usage: python3 -I term_check_r7.py <checkout>
Scans course/ (HTML, JSON, JS) case-insensitively. Prints every occurrence with file and line, and the count of <dfn> hits.
"""
import os, re, sys

base = sys.argv[1]
pat = re.compile(r"monetary\s+base", re.I)
dfn = re.compile(r"<dfn[^>]*>\s*monetary\s+base", re.I)
hits, dfns = [], []
for root, _, files in os.walk(os.path.join(base, "course")):
    for f in files:
        if not f.endswith((".html", ".json", ".js", ".md")):
            continue
        p = os.path.join(root, f)
        for n, line in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
            if pat.search(line):
                rel = os.path.relpath(p, base)
                hits.append(f"{rel}:{n}")
                if dfn.search(line):
                    dfns.append(f"{rel}:{n}")
print("occurrences of 'monetary base' under course/:", len(hits))
for h in hits:
    print("  ", h)
print("<dfn> definitions of 'monetary base':", dfns)
