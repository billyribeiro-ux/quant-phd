"""Print every line of the E4 slice pages that contains one of the given patterns (plain substring, case-insensitive)."""
import re
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE2-E4-a/course/modules/E/E4/"
PAGES = ["index.html", "L01.html", "L02.html", "L03.html"]
TWINS = [
    "/Users/billyribeiro/.fanout/wt/verifyE2-E4-a/tests/labs/E4/lab-E4-L01-1.py",
    "/Users/billyribeiro/.fanout/wt/verifyE2-E4-a/tests/labs/E4/lab-E4-L02-1.py",
    "/Users/billyribeiro/.fanout/wt/verifyE2-E4-a/tests/labs/E4/lab-E4-L03-1.py",
]
patterns = sys.argv[1:]
files = [ROOT + p for p in PAGES] + TWINS
for path in files:
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            low = line.lower()
            for pat in patterns:
                if pat.lower() in low:
                    short = path.split("verifyE2-E4-a/")[1]
                    print(f"{short}:{n}: [{pat}] {line.rstrip()[:260]}")
                    break
