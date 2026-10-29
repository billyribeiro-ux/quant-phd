"""Round-7 coverage: every named statement (Definition/Proposition/Theorem/Lemma/Corollary heading in the lesson text,
written as 'Kind n.m (' ) is cited by at least one card of its lesson; key-results rows are listed for manual review."""
import json, re, html
ROOT = "/Users/billyribeiro/.fanout/wt/verifyC7-E3-d/"
S = ROOT + "ledgers/E3/scripts/E3-d-r7/"
cards = json.load(open(ROOT + "course/modules/E/E3/cards.json", encoding="utf-8"))
tot_missing = 0
for L in ["L01","L02","L03","L04","L05","L06","L07","L08"]:
    t = open(S + "lessons/" + L + ".txt", encoding="utf-8").read()
    named = sorted(set(re.findall(r"((?:Definition|Proposition|Theorem|Lemma|Corollary) \d+\.\d+)\s*\(", t)))
    cards_text = " ".join(c["front"] + " " + c["back"] for c in cards if c["lesson"] == L)
    missing = [n for n in named if n not in cards_text]
    tot_missing += len(missing)
    print(L, "named statements", len(named), "not cited by a card of the lesson:", missing)
print("total not cited:", tot_missing)
