import re, html, json
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE6-LX1-b"
reg = json.load(open(f"{ROOT}/notation/notation.json"))
macros = list(reg["macros"].keys())
forbid = [r"\\Phi", r"\\gamma_3", r"\\gamma_4", r"R\^\\ast", r"R\^\{e\\ast\}", r"R_f", r"\\mathbb\{Q\}", r"\bT\b"]
for page in ("L03", "L04"):
    src = open(f"{ROOT}/course/modules/LX/LX1/{page}.html", encoding="utf-8").read()
    src = html.unescape(src)
    segs = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", src, re.S)
    maths = [a or b for a, b in segs]
    print(page, "math segments", len(maths))
    for s in maths:
        for pat in forbid:
            if re.search(pat, s):
                print("  REGISTERED SYMBOL", pat, "in:", s[:100])
        for mac in macros:
            if re.search(re.escape(mac) + r"(?![a-zA-Z])", s):
                print("  REGISTERED MACRO", mac, "in:", s[:100])
    # symbols used
    syms = set()
    for s in maths:
        for tok in re.findall(r"(?<!\\)\b([A-Za-z])(?:_\{?[a-z0-9]+\}?)?", s):
            syms.add(tok)
    print("  single-letter math symbols used:", sorted(syms))
    # prose notation check for T
    print("  bare 'T' inside math:", [s[:60] for s in maths if re.search(r"(^|[^A-Za-z\\])T([^A-Za-z]|$)", s)])
    # banned phrases and process words
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", src, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", body)
    for w in ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
              "you can add more", "it is important to note", "studies show", "experts agree", "well known", "obviously",
              "clearly", "it can be shown", "plans/", "tools/", "open item", "D-1", "B1", "B2", "B3", "N1", "N2", "N3", "N4",
              "builder", "fixer", "verifier", "ledger", "architect", " round ", "REQUEST", "registry", "reference list"]:
        hits = [m.start() for m in re.finditer(re.escape(w), text, re.I if w.islower() else 0)]
        if hits:
            print(f"  word {w!r}: {len(hits)}")
    print("  ellipsis outside math:", len(re.findall(r"\.\.\.|…", text)))
