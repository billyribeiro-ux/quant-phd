import re, sys, html
for f in sys.argv[1:]:
    s = open(f, encoding="utf-8").read()
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', s, re.S)
    t = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
    print(f.split("/")[-1], "why-it-matters words:", len(t.split()))
    # banned phrases
    body = html.unescape(re.sub(r"<[^>]+>", " ", s))
    for w in ["roughly", "about 6%", "historically", "TODO", "TBD", "lorem", "for brevity", "beyond the scope", "left as an exercise", "it is important to note", "well known", "obviously", "clearly", "experts agree", "studies show", "most ", "only ", "always", "every ", "all ", "any ", "same ", "drives", "offsets", "raises", "as much as", "build", "builder", "round ", "verifier", "...", "…"]:
        n = body.lower().count(w.lower())
        if n: print("   ", repr(w), n)
