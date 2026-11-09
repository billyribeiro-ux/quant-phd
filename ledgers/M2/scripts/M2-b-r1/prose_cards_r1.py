# Round-1: banned strings (BUILDER_RULES 1.3-1.4) and process words (verifier rules item 12) over the changed and added cards.
import json, re
S = "ledgers/M2/scripts/M2-b-r1/"
cards = json.load(open(S + "cards_head_95f3f8cb.json", encoding="utf-8"))
ids = ["M2-c087", "M2-c161", "M2-c169", "M2-c176", "M2-c417", "M2-c421", "M2-c422", "M2-c423", "M2-c425", "M2-c428", "M2-c429"]
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise", "obviously", "clearly", "it can be shown", "...", "…", "studies show", "it is well known"]
PROCESS = [r"\bround\b", r"\bverifier", r"\bledger", r"\bfixed\b", r"\bfix\b", r"\bfixer", r"\bcorrected\b", r"\bpreviously\b", r"\bearlier\b", r"\bdelta\b", r"\bversion\b", r"\bnow\b", r"\bruling", r"\bchanged\b", r"\bwe changed\b"]
hits = 0
for c in cards:
    if c["id"] not in ids:
        continue
    s = " ".join([c["front"], c["back"], c.get("basis", "")])
    for b in BANNED:
        if b.lower() in s.lower():
            print(c["id"], "banned", b); hits += 1
    for p in PROCESS:
        for m in re.finditer(p, s, re.I):
            print(c["id"], "process", p, repr(s[max(0, m.start()-40): m.end()+30])); hits += 1
print("changed/added cards scanned", len([c for c in cards if c["id"] in ids]), "hits", hits)
