# Round 8: every <a class="concept"> in L08-L10 must resolve to exactly one <dfn data-concept> in the course.
import glob, re, collections
root = "/Users/billyribeiro/.fanout/wt/verifyB8-M4-c/course/modules/"
dfn = collections.defaultdict(list)
for p in glob.glob(root + "*/*/*.html") + glob.glob(root + "*/*/*/*.html"):
    s = open(p, encoding="utf-8").read()
    for m in re.finditer(r'<dfn id="def-([^"]+)" data-concept="([^"]+)"', s):
        dfn[m.group(2)].append(p)
for L in ("L08", "L09", "L10"):
    s = open(root + f"M/M4/{L}.html", encoding="utf-8").read()
    links = set(re.findall(r'<a class="concept" data-concept="([^"]+)"', s))
    bad = [c for c in links if len(dfn.get(c, [])) != 1]
    print(L, "links", len(links), "unresolved_or_ambiguous", bad)
