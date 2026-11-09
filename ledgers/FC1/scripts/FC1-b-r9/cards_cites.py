import json, re, html
W = "/Users/billyribeiro/.fanout/wt/verifyS9-FC1-b"
M = W + "/course/modules/FC/FC1/"
cards = json.load(open(M + "cards.json"))
def text(p):
    raw = open(p, encoding="utf-8").read()
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return html.unescape(re.sub(r"\s+", " ", raw))
L = {x: text(M + x + ".html") for x in ["L01","L02","L03","L04","L05"]}
kinds = r"(Definition|Proposition|Remark|Example|Problem|Assumption|Section|Lemma|Theorem|Corollary|misconception|Assumption [A-Z]\d|Assumption \d\.\d)"
notfound = []
n = 0
for c in cards:
    s = c["back"]
    for grp in re.findall(r"\(([^()]*)\)", s):
        for item in re.split(r";", grp):
            item = item.strip()
            m = re.fullmatch(r"((?:Assumption|Definition|Proposition|Remark|Example|Problem|Section|misconception|Lab|Assumption)\s?[A-Za-z]?\d?\.?\d*)(.*)", item)
            if not m: continue
            key = m.group(1).strip()
            n += 1
            # locate in the card's own lesson first, then all FC1 lessons
            if key in L[c["lesson"]] or any(key in L[x] for x in L):
                continue
            notfound.append((c["id"], c["lesson"], key, item))
print("citations checked", n)
for x in notfound: print("NOT FOUND", x)
