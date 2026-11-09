"""Round 2: every numeric token in the 37 L07/L08 cards appears in its lesson's visible text; process-word and scope-word scan."""
import html
import json
import re

ROOT = "/Users/billyribeiro/.fanout/wt/verifyS2-FC2-c"
cards = json.load(open(f"{ROOT}/course/modules/FC/FC2/cards.json", encoding="utf-8"))
texts = {}
for page in ("L07", "L08"):
    src = open(f"{ROOT}/course/modules/FC/FC2/{page}.html", encoding="utf-8").read()
    src = re.sub(r"<script.*?</script>|<style.*?</style>", " ", src, flags=re.S)
    src = re.sub(r"<[^>]+>", " ", src)
    texts[page] = html.unescape(re.sub(r"\s+", " ", src))
sel = [c for c in cards if c["lesson"] in ("L07", "L08")]
print("cards", len(sel), "unique ids", len({c["id"] for c in sel}))
ids = [c["id"] for c in cards]
print("all-card id duplicates:", len(ids) - len(set(ids)))
missing = []
for c in sel:
    body = c["front"] + " " + c["back"]
    nums = set(re.findall(r"\d+(?:\.\d+)?", body))
    for n in nums:
        if n in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "16", "100"):
            # small integers can match trivially; check them anyway as whole tokens
            pass
        if not re.search(r"(?<![\d.])" + re.escape(n) + r"(?![\d])", texts[c["lesson"]]):
            missing.append((c["id"], n))
print("numeric tokens not in lesson text:", missing)
banned = re.compile(r"\b(verifier|verified by|builder|ledger|round \d|fragment|TODO|TBD|lorem|placeholder|draft|fixed in|previous round)\b", re.I)
for p in ("L07", "L08"):
    print(p, "process words:", banned.findall(texts[p]))
for p in ("L07", "L08"):
    t = texts[p]
    print(p, "vega occurrences:", len(re.findall(r"\bvega\b", t)), " bisection:", len(re.findall(r"bisection", t, re.I)))
