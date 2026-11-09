"""Attribution and registry-citation scan of the six slice pages (M2 slice c, round 4).

Run: .venv/bin/python -I <this file> <checkout root>. Prints every citation-related hit and the
concept links, and counts data-cite and data-locator markup per page.
"""
import re
import sys

root = sys.argv[1] + "/course/modules/M/M2/"
for p in ["L13", "L14", "L15", "L16", "L17", "L18"]:
    s = open(root + p + ".html", encoding="utf-8").read()
    refs = [(s.count("\n", 0, m.start()) + 1, s[max(0, m.start() - 40): m.end() + 40].replace("\n", " "))
            for m in re.finditer(r"data-cite|spivak|hubbard|velleman|Spivak|Hubbard|Velleman|References|data-locator|doi|isbn", s, re.I)]
    print(p, "citation-related hits:", len(refs))
    for ln, txt in refs:
        print("   ", ln, txt[:110])
    print("   concept links:", sorted(set(re.findall(r'data-concept="([^"]+)"', s))))
    print("   data-cite count:", len(re.findall("data-cite", s)), " data-locator count:", len(re.findall("data-locator", s)))
