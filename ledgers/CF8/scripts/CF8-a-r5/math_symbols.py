import re, sys, collections
root = sys.argv[1]
files = ["course/modules/CF/CF8/index.html", "course/modules/CF/CF8/L01.html", "course/modules/CF/CF8/L02.html"]
for f in files:
    txt = open(f"{root}/{f}", encoding="utf-8").read()
    segs = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", txt, re.S)
    syms = collections.Counter()
    for a, b in segs:
        s = a or b
        s2 = re.sub(r"\\[A-Za-z]+", " ", s)
        for tok in re.findall(r"(?<![A-Za-z])[A-Za-z](?:_\{?\w+\}?)?|\\mathrm\{[A-Za-z]+\}", s2):
            syms[tok] += 1
        for tok in re.findall(r"\\mathrm\{(\w+)\}", s):
            syms["mathrm:" + tok] += 1
    print(f, dict(syms))
