import json, re, html, glob
W = "/Users/billyribeiro/.fanout/wt/verifyS9-FC1-b"
M = W + "/course/modules/FC/FC1/"
cards = json.load(open(M + "cards.json"))
def text(p):
    raw = open(p, encoding="utf-8").read()
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return html.unescape(raw)
lessons = {L: text(M + L + ".html") for L in ["L01", "L02", "L03", "L04", "L05"]}
twin = {L: open(W + f"/ledgers/FC1/scripts/FC1-b-r9/out/twin_{L}.stdout", encoding="utf-8").read() for L in ["L01","L02","L03","L04","L05"]}
banned = ["TODO", "TBD", "lorem", "for brevity", "beyond the scope", "it is important to note", "obviously", "clearly", "it can be shown", "roughly", "historically", "...", "…"]
process = ["builder", "verifier", "round", "agent", "orchestrat", "fixer", "pass ", "ledger", "delta"]
print("cards", len(cards))
miss = []
for c in cards:
    s = c["front"] + " " + c["back"]
    toks = set(re.findall(r"\d[\d,]*(?:\.\d+)?", s))
    for t in sorted(toks):
        core = t.rstrip(",")
        L = c["lesson"]
        if core in lessons[L] or core in twin[L] or any(core in lessons[x] for x in lessons) or any(core in twin[x] for x in twin):
            continue
        miss.append((c["id"], c["lesson"], core))
    low = s.lower()
    for b in banned:
        if b.lower() in low: print("BANNED", c["id"], b)
    for p in process:
        if p in low: print("PROCESS?", c["id"], p, "|", s[:140])
print("numeric tokens not found in any lesson text or any twin stdout:")
for m in miss: print("  ", m)
