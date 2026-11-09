import re, json, pathlib, html
D = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyS6-FC1-b")
F = D / "course/modules/FC/FC1"
nt = json.load(open(D / "notation/notation.json", encoding="utf-8"))
registered = [s["symbol"] for s in nt["symbols"]]
print("registered symbols:", registered)
for f in ["L04.html", "L05.html"]:
    t = (F / f).read_text(encoding="utf-8")
    exprs = [a or b for a, b in re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", t, re.S)]
    hits = {}
    for sym in ["\\Phi", "\\gamma_3", "\\gamma_4", "R^\\ast", "R^{e\\ast}", "R_f", "\\mathbb{Q}", "T"]:
        n = sum(1 for e in exprs if re.search(re.escape(sym) + (r"(?![A-Za-z])" if sym == "T" else ""), e))
        hits[sym] = n
    print(f, "math expressions", len(exprs), "registered-symbol hits", hits)
    plain = re.sub(r"<[^>]+>", " ", t)
    words = ["we ", " round ", "verif", "builder", "draft", "placeholder", "TODO", "lorem"]
    print(f, "process-word hits", {w: len(re.findall(re.escape(w), plain, re.I)) for w in words})
c = (F / "cards.json").read_text(encoding="utf-8").lower()
print("cards.json process-word hits", {w: c.count(w) for w in ["we ", " round ", "verif", "builder", "draft", "placeholder", "todo"]})
