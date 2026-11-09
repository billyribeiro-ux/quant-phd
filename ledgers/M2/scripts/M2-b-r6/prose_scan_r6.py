# Round-6 prose scan: banned strings (BUILDER_RULES 1.3-1.4, 3.5) and process words (verifier rules item 12)
# over the whole of L07-L12 page text and over the slice cards; plus the added lines of the delta.
import re, json, subprocess, html, sys
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "it can be shown", "...", "…"]
PROCESS = [r"\bround\b", r"\bverifier", r"\bledger", r"\bfixed\b", r"\bfix\b", r"\brubric", r"\bbuilder", r"\bauditor",
           r"\bthe fix\b", r"\bcorrected\b", r"\bpreviously\b", r"\bearlier version", r"\bstrict sweep", r"\bdelta\b",
           r"\bwe changed\b", r"\bnow reads\b", r"\bversion\b"]
slices = ["L07", "L08", "L09", "L10", "L11", "L12"]
hits = []
for n in slices:
    txt = open(f"course/modules/M/M2/{n}.html", encoding="utf-8").read()
    plain = html.unescape(re.sub(r"<[^>]+>", " ", txt))
    for b in BANNED:
        for m in re.finditer(re.escape(b), plain, re.I):
            hits.append((n, "banned", b, plain[max(0,m.start()-60):m.end()+40].replace("\n", " ")))
    for p in PROCESS:
        for m in re.finditer(p, plain, re.I):
            hits.append((n, "process", p, plain[max(0,m.start()-60):m.end()+40].replace("\n", " ")))
cards = json.load(open("course/modules/M/M2/cards.json", encoding="utf-8"))
slice_cards = [c for c in cards if c["lesson"] in slices]
for c in slice_cards:
    s = " ".join([c["front"], c["back"], c.get("basis", "")])
    for b in BANNED:
        if b.lower() in s.lower():
            hits.append((c["id"], "banned", b, s[:120]))
    for p in PROCESS:
        for m in re.finditer(p, s, re.I):
            hits.append((c["id"], "process", p, s[max(0,m.start()-60):m.end()+40]))
print("slice pages L07-L12 and", len(slice_cards), "slice cards scanned")
for h in hits:
    print(h)
print("total hits", len(hits))
