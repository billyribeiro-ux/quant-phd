exec(open("ledgers/E3/scripts/E3-f-r18/write_fragment.py", encoding="utf-8").read())
import re as _re
cards = {c["id"]: c for c in json.load(open("course/modules/E/E3/cards.json", encoding="utf-8"))}
changed_old_new = {"E3-c005","E3-c007","E3-c008","E3-c017","E3-c036","E3-c037","E3-c177"}
handled = {r["id"] for r in rows}
# per-card rows for the 91 L01-L04 cards
for rid in sorted(old):
    m = _re.fullmatch(r"E3f-E3-c(\d{3})", rid)
    if not m:
        continue
    cid = f"E3-c{m.group(1)}"
    card = cards[cid]
    lesson = card["lesson"]
    if lesson == "L02":
        carry(rid, f"course/modules/E/E3/L02.html and the cards.json entry {cid}")
    else:
        extra = ""
        if cid in changed_old_new:
            extra = " CHANGED in this delta: text now uses " + ("Xi" if cid in ("E3-c005","E3-c007","E3-c008","E3-c017") else "iota" if cid in ("E3-c036","E3-c037") else "a rewritten section-4 reference")
        redo(rid, f"Round 18 full read of {cid} ({lesson}) against course/modules/E/E3/{lesson}.html at the pin 4540351d: front/back claims and cited labels checked (cards_xref.py) and numbers present (cards_numbers.py); the lesson hunks in this delta were read.{extra}")
# card rows for the 16 changed cards in L05-L08
L58 = {
 "E3-c078": ("L05", "Definition 1.1 (line 64-66): V0 with Omega := 1 - 1/psi; assumptions A1-A4 (lines 55-60) give 0<beta<1, psi>0, psi!=1, gamma!=1, positive consumption. Ruling 33 rename a -> Omega; card matches."),
 "E3-c080": ("L05", "Theorem 1.3 (lines 76-79) under A1-A4: (a) V0 = [(1-beta)c0^Omega + beta CE1^Omega]^(1/Omega); (b) strictly increasing in CE1 for fixed c0, beta, gamma, psi. Card matches."),
 "E3-c100": ("L06", "Definition 1.3 (line 68-69): PV := sum p_i v(x_i), p_i > 0 summing to 1; line 301 says probability weighting is absent and comes in L07. Card matches the renamed PV."),
 "E3-c104": ("L06", "Proposition 2.1 (lines 97-99): alpha = delta = 1, lambda* = pg/((1-p) l), PV(lambda) = pg - (1-p) lambda l strictly decreasing, PV(1) = EV, PV(lambda*) = 0. Card matches."),
 "E3-c105": ("L06", "Proposition 2.2 (lines 107-108): PV = p g^alpha - (1-p) lambda l^delta; zero at lambda* = p g^alpha/((1-p) l^delta), positive below, negative above. Card matches."),
 "E3-c107": ("L06", "Remark 2.4 (lines 122-123): CE under v defined by v(c) = PV; v continuous, strictly increasing, v(0)=0, so sign of CE equals sign of PV. Card matches."),
 "E3-c116": ("L06", "Lab 1 expected block (L06 lines 272-274): 'alpha = delta = 0.5: threshold lam* = 1.2910' and 'PV at lam = 2 with alpha = delta = 0.5: -8.6835'; sqrt(5/3) = 1.29099. Card matches the renamed PV."),
 "E3-c143": ("L08", "Proposition 2.4 (lines 117-122): worst prior for the bet on red is P_0 (no red balls) under A1-A3; the card keeps the red part, a faithful restriction. Card matches."),
 "E3-c145": ("L08", "Definition 3.1 (lines 141-142): Omega = 1 - 1/psi with psi>0, psi!=1. Card matches the renamed exponent."),
}
for cid, (lesson, ev) in L58.items():
    add(f"E3f-r18-changed-card-{cid}", f"card text changed in this delta and cited lesson changed (renamed symbols)", f"course/modules/E/E3/cards.json ({cid}); course/modules/E/E3/{lesson}.html", "PASS",
        f"Round 18 full read of {cid} against {lesson}.html at 4540351d. " + ev + " Cited label found by cards_xref.py (out/cards_xref.out).")
# L05-L08 sample and unsampled rows: subject lesson changed by renames only
for rid in ["E3f-r14-cards-sample-L05","E3f-r14-cards-sample-L06","E3f-r14-cards-sample-L07","E3f-r14-cards-sample-L08","E3f-r14-cards-unsampled","E3f-r15-cards-changed-L05-L08"]:
    prev = old[rid]
    add(rid, prev["check"], prev["location"], "PASS",
        "Round 18 re-verification of the subject: the L05-L08 pages changed only by word-level renames (a -> Omega in L05 and L08, W -> PV in L06) and the footer sentence (ledgers/E3/scripts/E3-f-r18/worddiff.py output, reviewed for each of L05, L06, L07, L08). A grep of cards.json for a, W, PV, Omega and omega over L05-L08 cards found no card that quotes a renamed symbol except the cards listed in E3f-r18-changed-card-*; the rest read English 'a' or the L07 weighting omega, which is unchanged. The card text is byte-identical to the previous pin (cards_delta.py). Round-15 evidence retained: " + prev["evidence"][:500])
# leftover ids check
missing = [r for r in old if r not in handled and r not in {x["id"] for x in rows}]
print("round15 ids not yet handled:", missing)
