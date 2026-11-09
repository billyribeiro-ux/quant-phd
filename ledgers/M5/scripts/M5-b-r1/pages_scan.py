"""M5 slice b (L05-L07) page scan: raw '<' in HTML/math, banned strings, registry macros, term use, scope words."""
import re, sys, collections
base = sys.argv[1]
TAGS = set("a abbr article aside audio b blockquote body br button canvas caption cite code col colgroup data dd del details dfn div dl dt em fieldset figcaption figure footer form h1 h2 h3 h4 h5 h6 head header hr html i iframe img input ins kbd label legend li link main mark menu meta nav noscript object ol optgroup option output p param pre progress q s samp script section select small source span strong style sub summary sup svg table tbody td template textarea tfoot th thead time title tr track u ul var video wbr path g rect circle line polyline polygon text desc defs marker use clipPath".split())
REG = {"R", "N", "E", "Prob", "Var", "Cov", "Corr", "indic", "Normal", "iid", "dto", "pto", "argmax", "argmin", "tr", "diag", "SR", "hSR", "PSR", "DSR", "PBO", "FWER", "FDR", "FDP", "se", "emgamma"}
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well known", "obviously", "clearly", "it can be shown", "roughly", "historically", "builder", "verifier", "ledger"]
SCOPE = r"\b(only|all|always|every|any|same|drives|exactly|never)\b"
for L in ("L05", "L06", "L07"):
    src = open(f"{base}/course/modules/M/M5/{L}.html", encoding="utf-8").read()
    bad = []
    for m in re.finditer(r"<(/?)([A-Za-z][A-Za-z0-9-]*)", src):
        if m.group(2).lower() not in TAGS:
            bad.append((src.count("\n", 0, m.start()) + 1, m.group(0)))
    for m in re.finditer(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", src, re.S):
        if re.search(r"<[A-Za-z/]", m.group(0)):
            bad.append(("math", src.count("\n", 0, m.start()) + 1))
    print(L, "raw-angle-bracket hits:", bad)
    macros = collections.Counter(re.findall(r"\\([A-Za-z]+)", src))
    print(L, "macros not in registry and not KaTeX builtin:", sorted(k for k in macros if k in REG))
    hits = [(b, L) for b in BANNED for _ in re.finditer(re.escape(b), src, re.I)]
    print(L, "banned-string hits:", collections.Counter(b for b, _ in hits))
    lines = src.split("\n")
    for i, line in enumerate(lines, 1):
        if re.search(r"sup norm", line, re.I):
            print(L, "sup norm at line", i, line.strip()[:110])
    print(L, "scope-word count:", len(re.findall(SCOPE, re.sub(r"<[^>]+>", " ", src), re.I)))
