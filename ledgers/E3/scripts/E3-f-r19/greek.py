import glob, re, sys
root = "/Users/billyribeiro/dev/quant-phd"
files = sorted(glob.glob(root + "/course/modules/E/E3/*.html")) + [root + "/course/modules/E/E3/cards.json"] + sorted(glob.glob(root + "/tests/labs/E3/*.py")) + sorted(glob.glob(root + "/course/modules/E/E3/grader/*.py")) + sorted(glob.glob(root + "/course/modules/E/E3/*.js"))
cands = ["sigma","Sigma","varsigma","rho","Rho","epsilon","varphi","Delta","Theta","Lambda","Pi","Psi","varpi","vartheta","varrho","Upsilon","Gamma","Phi","zeta","chi","eta","tau","xi","iota"]
for c in cands:
    pat = re.compile(r"\\" + c + r"(?![A-Za-z])")
    hits = []
    for f in files:
        txt = open(f, encoding="utf-8").read()
        n = len(pat.findall(txt))
        if n: hits.append((f.split("E3/")[-1], n))
    print(c, hits)
# plain word sigma in text / python identifiers
for f in files:
    txt = open(f, encoding="utf-8").read()
    for w in ["sigma","Sigma","zeta","varsigma"]:
        if re.search(r"\b"+w+r"\b", txt): print("word", w, f.split("E3/")[-1])
