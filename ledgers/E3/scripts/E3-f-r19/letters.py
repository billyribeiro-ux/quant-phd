import re, glob, sys, collections
root = "/Users/billyribeiro/dev/quant-phd"
files = sorted(glob.glob(root + "/course/modules/E/E3/*.html")) + [root + "/course/modules/E/E3/cards.json"] + sorted(glob.glob(root + "/tests/labs/E3/*.py")) + sorted(glob.glob(root + "/course/modules/E/E3/grader/*.py"))
mathre = re.compile(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", re.S)
letter_ctx = collections.defaultdict(list)
for f in files:
    txt = open(f, encoding="utf-8").read()
    for m in mathre.finditer(txt):
        seg = m.group(1) or m.group(2) or ""
        # strip macros and commands
        s = re.sub(r"\\[A-Za-z]+", " ", seg)
        for L in re.finditer(r"(?<![A-Za-z])([A-Za-z])(?![A-Za-z])", s):
            letter_ctx[L.group(1)].append((f.split("quant-phd/")[1], txt[:m.start()].count("\n")+1))
for L in sorted(letter_ctx, key=lambda c: (c.lower(), c)):
    c = collections.Counter(x[0] for x in letter_ctx[L])
    print(L, len(letter_ctx[L]), dict(c))
