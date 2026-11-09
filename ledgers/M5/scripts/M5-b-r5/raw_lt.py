"""Lists raw '<' followed by a digit or backslash in text (not a tag start) on the three slice pages."""
import re
base = "/Users/billyribeiro/.fanout/wt/verifyS5-M5-b/course/modules/M/M5/"
total = 0
for f in ["L05.html", "L06.html", "L07.html"]:
    lines = open(base + f, encoding="utf-8").read().splitlines()
    occ = []
    for i, l in enumerate(lines, 1):
        n = len(re.findall(r"<(?=[0-9\\])", l))
        if n:
            occ.append((i, n))
    total += sum(n for _, n in occ)
    print(f, "lines", [i for i, _ in occ], "occurrences", sum(n for _, n in occ))
print("total occurrences", total)
