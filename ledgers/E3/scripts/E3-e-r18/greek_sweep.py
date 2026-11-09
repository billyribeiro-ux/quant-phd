import html, re, sys, pathlib, collections
root = pathlib.Path(sys.argv[1]) / "course/modules/E/E3"
names = ["alpha","beta","gamma","delta","lambda","psi","theta","omega","eta","nu","mu","sigma","pi","zeta","varsigma","upsilon","kappa","chi","xi","Gamma","Delta","Lambda","Sigma","Pi","Psi","Theta","Omega","nu"]
math_re = re.compile(r"\\\((.+?)\\\)|\\\[(.+?)\\\]", re.S)
where = collections.defaultdict(set)
for f in ["index.html"] + [f"L0{i}.html" for i in range(1, 9)]:
    text = (root / f).read_text(encoding="utf-8")
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", text, flags=re.S)
    for m in math_re.finditer(body):
        seg = html.unescape(next(g for g in m.groups() if g is not None))
        for n in names:
            if re.search(r"\\" + n + r"(?![A-Za-z])", seg):
                where[n].add(f)
for n in names:
    if where[n]:
        print(n, sorted(where[n]))
