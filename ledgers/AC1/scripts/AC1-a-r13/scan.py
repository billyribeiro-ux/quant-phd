import re, json, html, sys
root = sys.argv[1]
files = ["course/modules/AC/AC1/index.html","course/modules/AC/AC1/L01.html","course/modules/AC/AC1/L02.html","course/modules/AC/AC1/L03.html","course/modules/AC/AC1/cards.json"]
pat = re.compile(r"roughly|about \d|historically|typically|generally|usually|as much as|drives|offsets|builder|verifier|round \d|REQUEST|unit report|\.\.\.|…|clearly|obviously|simply|half of|most |often|it is well known", re.I)
for f in files:
    txt = open(root + f, encoding="utf-8").read()
    t = html.unescape(re.sub(r"<[^>]+>", " ", txt)) if f.endswith(".html") else txt
    hits = [(m.group(0), t[max(0,m.start()-60):m.end()+40].replace("\n"," ")) for m in pat.finditer(t)]
    print(f, len(hits))
    for h in hits: print("   ", h[0], "|", h[1][:140])
spans = []
for f in files[:4]:
    txt = open(root + f, encoding="utf-8").read()
    for m in re.finditer(r"\\\((.*?)\\\)", txt, re.S):
        spans += re.findall(r"\\[A-Za-z]+", m.group(1))
print("macros", sorted(set(spans)))
