import json, re, html
W = "/Users/billyribeiro/.fanout/wt/verifyS9-FC1-b"
M = W + "/course/modules/FC/FC1/"
cards = json.load(open(M + "cards.json"))
def text(p):
    raw = open(p, encoding="utf-8").read()
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return html.unescape(raw)
T = {L: text(M + L + ".html") for L in ["L04", "L05"]}
TW = {L: open(f"{W}/ledgers/FC1/scripts/FC1-b-r9/out/twin_{L}.stdout", encoding="utf-8").read() for L in ["L04", "L05"]}
for L in ["L04", "L05"]:
    n = 0; miss = []
    for c in cards:
        if c["lesson"] != L: continue
        n += 1
        s = c["front"] + " " + c["back"]
        for t in sorted(set(re.findall(r"\d[\d,]*(?:\.\d+)?", s))):
            core = t.rstrip(",")
            if core not in T[L] and core not in TW[L]:
                miss.append((c["id"], core))
    print(L, "cards", n, "numbers missing from own lesson and twin output:", miss)
