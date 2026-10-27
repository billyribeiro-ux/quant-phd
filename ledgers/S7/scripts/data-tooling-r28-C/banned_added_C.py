"""Round-28 part C: banned phrases (BUILDER_RULES 1.3-1.4) in the lines ADDED since 5e5da87 in the S7 pages and the
data-tooling sources named by r25-banned-phrases. Also reports the ellipsis count in all S7 pages (not a changed line).
Run: python -I banned_added_C.py <checkout>"""
import re
import subprocess
import sys

CK = sys.argv[1]
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "roughly half", "…"]
paths = ["course/modules/S/S7", "project.html", "tools/data_sources.yaml"]
diff = subprocess.run(["git", "-C", CK, "diff", "-U0", "5e5da87", "c9beb92", "--"] + paths, capture_output=True, text=True, check=True).stdout
added = [l[1:] for l in diff.split("\n") if l.startswith("+") and not l.startswith("+++")]
print("added lines in the S7 pages and data_sources.yaml since 5e5da87:", len(added))
hits = []
for line in added:
    for b in BANNED:
        if b.lower() in line.lower():
            hits.append((b, line[:120]))
print("banned hits in added lines:", hits)
ell = 0
for n in range(1, 9):
    text = open(f"{CK}/course/modules/S/S7/L{n:02d}.html", encoding="utf-8").read()
    ell += len(re.findall(r"\.\.\.|…", text))
print("ellipsis tokens in L01-L08 html (all lines, unchanged since release unless listed above):", ell)
