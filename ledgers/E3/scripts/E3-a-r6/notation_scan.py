import html, json, re, sys
root = sys.argv[1]
reg = json.load(open(f"{root}/notation/notation.json"))
regsyms = []
for s in reg["symbols"]:
    for part in s["symbol"].split(","):
        regsyms.append((part.strip(), s["module"], s["meaning"][:70]))
macros = reg["macros"]
for L in ["index", "L01", "L02", "L03"]:
    src = open(f"{root}/course/modules/E/E3/{L}.html", encoding="utf-8").read()
    maths = re.findall(r"\\\((.*?)\\\)", src, re.S) + re.findall(r"\\\[(.*?)\\\]", src, re.S)
    maths = [html.unescape(m) for m in maths]
    toks = set()
    for m in maths:
        for t in re.findall(r"\\[A-Za-z]+|[A-Za-z](?:_\{?[A-Za-z0-9]+\}?)?(?:\^\{?[\\A-Za-z0-9]+\}?)?", m):
            toks.add(t)
    hits = []
    for sym, mod, mean in regsyms:
        core = sym.replace("\\", "").replace("{", "").replace("}", "")
        for t in toks:
            tc = t.replace("\\", "").replace("{", "").replace("}", "")
            if sym == t or (len(core) <= 3 and tc == core) or (sym.startswith("\\") and t == sym):
                hits.append((t, sym, mod))
    print(L, "math segments", len(maths), "distinct tokens", len(toks))
    print("  registry hits:", sorted(set(hits)))
    print("  single-letter tokens:", sorted(t for t in toks if len(t) == 1 and t.isalpha()))
    print("  greek/other:", sorted(t for t in toks if t.startswith("\\")))
