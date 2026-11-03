import re, glob, json, collections
reg = json.load(open("notation/notation.json"))
regm = {k for k, _ in reg["macros"]} if isinstance(reg["macros"], list) and isinstance(reg["macros"][0], list) else set()
if not regm:
    regm = {m[0] if isinstance(m, list) else m for m in reg["macros"]}
# macros may be dict-like tuples; normalize
try:
    regm = {k for k, v in reg["macros"]}
except Exception:
    pass
files = sorted(glob.glob("course/modules/E/E3/*.html")) + ["tests/labs/E3/lab-E3-project-1.py", "tests/labs/E3/lab-E3-project-3.py"]
cnt = collections.Counter()
where = collections.defaultdict(set)
for f in files:
    s = open(f, encoding="utf-8").read()
    # TeX spans only
    for span in re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", s, re.S):
        t = span[0] or span[1]
        for mac in re.findall(r"\\([A-Za-z]+)", t):
            cnt["\\" + mac] += 1
            where["\\" + mac].add(f.split("/")[-1])
print("registry macros:", sorted(regm))
print("direct \\mathbb occurrences:")
for f in files:
    s = open(f, encoding="utf-8").read()
    for m in re.finditer(r"\\mathbb", s):
        print("  ", f, s[:m.start()].count("\n") + 1, s[m.start()-30:m.start()+20].replace("\n", " "))
print("macro census (TeX spans):")
for k, v in sorted(cnt.items()):
    print("  ", k, v, "REG" if k[1:] in regm else "not-registered", sorted(where[k])[:6])
