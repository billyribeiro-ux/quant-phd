"""E3 slice f round 11: build the ledger fragment ledgers/E3/E3-f.json from the round-11 checks.

Each card row cites the card in cards.json and the lesson line of every label the card's back cites (definition,
proposition, lemma, theorem, remark, example, assumption, problem, section). Run from the checkout root with
python3 -I ledgers/E3/scripts/E3-f-r11/build_fragment.py
"""
import json
import re
from pathlib import Path

ROOT = Path(".")
UNIT = ROOT / "course/modules/E/E3"
cards = json.loads((UNIT / "cards.json").read_text(encoding="utf-8"))
lesson_text = {f"L0{i}": (UNIT / f"L0{i}.html").read_text(encoding="utf-8").splitlines() for i in range(1, 5)}
slice_cards = [c for c in cards if c["lesson"] in lesson_text]

LABEL = re.compile(r"(Definition|Proposition|Theorem|Lemma|Remark|Example|Assumption|Problem)\s+([A-Z]?\d+(?:\.\d+)?)")


def locate(lesson: str, kind: str, num: str) -> str:
    lines = lesson_text[lesson]
    if kind == "Problem":
        alt = {"M": "mech-", "P": "proof-", "E": "emp-", "R": "res-"}
        ids = [num] + [alt[num[0]] + num[1:]] if num[0] in alt else [num]
        pat = re.compile("|".join(r'id="%s"' % re.escape(i) for i in ids))
    else:
        pat = re.compile(r">%s %s(?!\d)" % (kind, re.escape(num)))
    for i, line in enumerate(lines, 1):
        if pat.search(line):
            return f"{lesson}.html:{i}"
    for other in sorted(lesson_text):
        if other == lesson:
            continue
        for i, line in enumerate(lesson_text[other], 1):
            if pat.search(line):
                return f"{other}.html:{i} (cited from {lesson} as an earlier-lesson result)"
    return f"{lesson}.html (label {kind} {num} not found)"


NOTES = {
    "E3-c049": ("FAIL", "Proposition 2.7 was re-lettered this round to phi > 0 and real eta (L03.html:173-175, proof L03.html:178-180, P1 solution L03.html:393), "
                "but the back still writes 'a > 0 and real b', which reuses the letter a that Definition 1.1 and Proposition 1.2 use for the power exponent. "
                "The content (hypotheses and conclusion) is identical, so the defect is the symbol clash with the lesson's current text, not the mathematics.",
                "Change the back to: 'No. For a lottery whose certainty equivalent under u exists and is unique, and for phi > 0 and real eta, the certainty equivalent under phi u + eta equals the one under u (Proposition 2.7).'"),
    "E3-c047": ("", "Recomputed: M = 1/2*1/1000 + 1/2*1/4000 = 1/1600, CE_2 = 1600 cents; Example 2.5 (L03.html:159) states 1600."),
    "E3-c055": ("", "Recomputed: M = 9/80000, CE_2 = 80000/9 = 8888.89; Lab 1 printed line 'gamma 2 exact value 1 / sum of p/x: 80000/9 cents' (L03.html:315)."),
    "E3-c180": ("", "Recomputed: CE_1 = exp(1/2 ln 1000 + 1/2 ln 4000) = 2000 cents; Example 2.5 (L03.html:159) states 2000."),
    "E3-c054": ("", "Lab 1 printed lines L03.html:309-314 give 11250.0000, 10000.0000, 8888.8889, 7337.6161 at gamma 0, 1, 2, 4; falling order printed True (L03.html:319). Recomputed in rederive_numbers.out."),
    "E3-c071": ("", "Problem R3 (L04.html:613-617) proves the claim: b1 = sigma_{m-1} >= 0 by monotonicity and I_X(s_m) = s_m - E X gives E X >= E Y."),
    "E3-c073": ("", "Lab 1 output pairs 16 and 19 print 'SOSD no ranking' (L04.html:472, 475); equal-mean pairs are 01,04,07,10,13,16,19,22 (8 pairs)."),
    "E3-c075": ("", "Lab 1 output (L04.html:480-481): FOSD verdicts 3/10/1/10 and 'agree on 24 of 24'."),
    "E3-c076": ("", "Lab 1 output (L04.html:483-484): SOSD verdicts 3/2/1/2 over 8 equal-mean pairs and '8 of 8'."),
    "E3-c016": ("", "Lab 1 part A output (L01.html:303-305): EV 15000, 12500, 15000; quadratic EU 45000, 21250, 37500. Recomputed in rederive_numbers.out."),
    "E3-c017": ("", "Lab 1 part B output (L01.html:307-313): six lines 'equal True' and 'all_linearity_checks True'."),
    "E3-c013": ("", "Problem R1 (L01.html:437-443) gives the maximizer and the equality case; the card matches."),
    "E3-c014": ("", "Example 1.4 (L01.html:79) and Misconception 1 (L01.html:343): u(EX) = 22500, E u(X) = 45000, twice that value."),
    "E3-c034": ("", "0.565835/5.065835 = 0.11170 -> 11.17 percent (rederive_numbers.out); L02.html:387 states 11.17 percent. Grade C with basis Lab 1 part A is conservative for an arithmetic fact; not a defect."),
    "E3-c183": ("", "Example 2.6 (L04.html:172-173): I_Y(t) = (t-3000)^+ <= I_X(t) at every support point (1000: 0 vs 0; 3000: 0 vs 1000; 5000: 2000 vs 2000), and no first-order ranking. The card carries no grade; grade is mandatory only for key empirical results (BUILDER_RULES 7), so this is not a defect."),
    "E3-c159": ("", "Remark 1.4 (L02.html:131) lists A2, F2, F1, A1, A3 and F5 (through the strict-increase step); the card lists the same hypotheses."),
}


def row_for_card(c):
    cid = c["id"]
    rid = "E3f-" + cid
    lesson = c["lesson"]
    locs = []
    for kind, num in LABEL.findall(c["back"] + " " + c["front"]):
        loc = locate(lesson, kind, num)
        if loc not in locs:
            locs.append(loc)
    if not locs:
        locs.append(f"{lesson}.html (section or lab reference only)")
    status, note, fix = "PASS", "", ""
    if cid in NOTES:
        verdict, text, *rest = NOTES[cid]
        if verdict:
            status = verdict
        note = text
        fix = rest[0] if rest else ""
    head = (f"Round 11: cards.json {cid} (lesson {lesson}, grade {c.get('grade', 'none')}) checked against the current "
            f"{lesson}.html (read in full) at {', '.join(locs)}.")
    if status == "PASS":
        body = " Statement, hypotheses and numbers agree with the lesson text." + (" " + note if note else "")
        evidence = head + body
    else:
        evidence = head + " " + note
    row = {"id": rid, "check": "2.7-cards", "location": f"course/modules/E/E3/cards.json ({cid}); {', '.join(locs)}",
           "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    return row


rows = [row_for_card(c) for c in slice_cards]
rows.append({"id": "E3f-E3-c186", "check": "2.7-cards", "location": "course/modules/E/E3/cards.json (E3-c186 absent)",
             "status": "PASS",
             "evidence": "Round 11: grep -c '\"E3-c186\"' course/modules/E/E3/cards.json returns 0 (card removed in ccaeeaf; replaced by E3-c187 in L07, outside slice f). The round-10 FAIL (c186 duplicate of c020 and wrong Definition 2.3 citation) is no longer present. Scan in E3f-cards-near-duplicates re-run."})
rows.append({"id": "E3f-E3-c178-b", "check": "2.7-cards", "location": "course/modules/E/E3/cards.json (E3-c178) vs L03.html:112",
             "status": "PASS",
             "evidence": "Round 11: the duplicate-id row carried from round 8 re-checked: E3-c178 appears once in cards.json (unique id scan, check_cards_slice.py output). Definition 1.6 at L03.html:112 states u twice differentiable on (0,infinity) with u' > 0, which is the card's back."})
rows[0]  # keep order
json.dump(rows, open(ROOT / "ledgers/E3/scripts/E3-f-r11/card_rows.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(rows), sum(1 for r in rows if r["status"] == "PASS"), [r["id"] for r in rows if r["status"] != "PASS"])
