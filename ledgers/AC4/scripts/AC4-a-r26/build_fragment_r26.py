"""Round 26: build the AC4-a fragment from the round-25 fragment (carry and re-verify rules) plus this round's rows."""
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
prev = json.loads(Path("/tmp/fanout-frags/AC4-a.round25.json").read_text(encoding="utf-8"))
CARRY = ("Carried from round 25 (cited lines of index.html, L01.html, L02.html and tests/labs/AC4/*.py "
         "byte-identical since the previous pin b49a857; cards.json changed only in AC4-c026): ")
REVER_PREFIX = "Re-run or re-read in round 26 (pin f9f3fed): "
CMD = {
    "AC4-a-cmd-check-pages", "AC4-a-cmd-check-dag", "AC4-a-r19-cmd-check-projects", "AC4-a-cmd-run-labs",
    "AC4-a-cmd-twins-isolated", "AC4-a-cmd-twin-output-equals-page", "AC4-a-cmd-page-smoke",
    "AC4-a-cmd-pytest-labs-lint", "AC4-a-cmd-verify-refs", "AC4-a-r18-cmd-build-site-check",
    "AC4-a-r25-cmd-twin-stdout-equals-embedded", "AC4-a-banned-phrases",
}
CARDS = {
    "AC4-a-cards-L02-changed", "AC4-a-cards-r17-changed-subjects", "AC4-a-r18-cards-c008-c018-c125",
    "AC4-a-r23-card-c020", "AC4-a-r23-card-c135", "AC4-a-r25-card-c135", "AC4-a-r25-cards-reread",
    "AC4-a-r18-L02-key-results-source-c125",
}
MUT = {
    "AC4-a-r18-mutants-labs", "AC4-a-r21-new-mutants", "AC4-a-r23-mutants-committed", "AC4-a-r23-mutants-new",
    "AC4-a-r24-mutants-committed", "AC4-a-r24-mutants-new", "AC4-a-r25-mutants-new", "AC4-a-r25-mutants-suite",
}
NUM = {"AC4-a-num-L01-examples", "AC4-a-num-L01-lab", "AC4-a-num-L01-R3-recomputed", "AC4-a-r25-L01-E2-residual",
       "AC4-a-L01-R3-range-sentence", "AC4-a-L01-R3-unquantified", "AC4-a-r21-indep-recompute",
       "AC4-a-L02-lab-numbers", "AC4-a-L02-problems", "AC4-a-L02-sensitivity-proofs", "AC4-a-L02-quiz"}
CARD_FIXED = {"AC4-a-cards-L01-L02": "PASS", "AC4-a-r25-card-c026": "PASS"}
for r in prev["rows"]:
    rid = r["id"]
    r.pop("fix", None)
    if rid in CARD_FIXED:
        r["status"] = CARD_FIXED[rid]
        r["evidence"] = ("Re-read round 26: all 39 L01 and L02 cards (cards.json) checked against the current lesson "
                         "text; AC4-c026 now reads 'In the single-segment model ... (Proposition 3.3, single-segment "
                         "model)' and matches L02.html:107-110. No other card differs from its lesson. Round-25 "
                         "evidence: " + r["evidence"])
        if rid == "AC4-a-cards-L01-L02":
            r["location"] = "course/modules/AC/AC4/cards.json (39 L01 and L02 cards)"
    elif rid == "AC4-a-L01-quiz":
        r["status"] = "FAIL"
        r["evidence"] = ("FAIL round 26: L01.html:459 quiz explanation for item 7 says 'Other months carry residuals "
                         "(Remark 3.3)'. A month off the endpoints can lie exactly on the line; witness "
                         "(400,1200),(700,2100),(1000,3000) gives F=0, v=3, residual 0 at 700 hours. Row "
                         "AC4-a-r26-L01-q7-explanation. Other quiz items re-checked and correct.")
        r["fix"] = ("Change L01.html:459 'Other months carry residuals' to 'Other months may carry residuals' "
                    "(Remark 3.3 says only that a residual is free to be positive or negative).")
    elif rid in CMD:
        r["evidence"] = REVER_PREFIX + r["evidence"]
    elif rid in CARDS or rid in MUT or rid in NUM:
        r["evidence"] = REVER_PREFIX + r["evidence"]
    else:
        r["evidence"] = CARRY + r["evidence"]
    if r["status"] != "PASS" and "fix" not in r:
        r["fix"] = "See the row evidence."
rows = prev["rows"]
NEW = [
    {"id": "AC4-a-r26-delta-scan", "check": "delta b49a857..f9f3fed for the AC4-a slice (every hunk read)",
     "location": "git diff --stat b49a857 f9f3fed; git diff b49a857 f9f3fed -- course/modules/AC/AC4 tests/labs/AC4",
     "status": "PASS",
     "evidence": "Only course/modules/AC/AC4/cards.json changed in the slice (AC4-c026 front and back, 4 lines: the single-segment qualifier added), plus three new mutant files under ledgers/AC4/mutants/AC4-a-r25/. index.html, L01.html, L02.html and tests/labs/AC4 are byte-identical to the previous pin. Every changed hunk was read; the cards re-read covers the full L01 and L02 deck."},
    {"id": "AC4-a-r26-card-c026", "check": "card AC4-c026 against Proposition 3.3 and the lab-free claim",
     "location": "course/modules/AC/AC4/cards.json AC4-c026; L02.html:107-110 (Proposition 3.3, single-segment model); L02.html:435",
     "status": "PASS",
     "evidence": "Front 'In the single-segment model, how far does the break-even volume move when fixed cost rises by delta F, with the margin unchanged?' and back 'It rises by exactly delta F/m units. The derivative of Q* with respect to F is 1/m (Proposition 3.3, single-segment model).' match Proposition 3.3 (L02.html:108) and the key-results row at L02.html:435. The scope is restricted as Proposition 3.3 requires; no step-cost use is implied."},
    {"id": "AC4-a-r26-L01-q7-explanation", "check": "L01 quiz item 7 explanation: scope of 'other months carry residuals'",
     "location": "course/modules/AC/AC4/L01.html:459 (explanation of item L01q7); compare L01.html:134 and Remark 3.3 at L01.html:129",
     "status": "FAIL",
     "evidence": "The explanation says 'Other months carry residuals (Remark 3.3)'. Remark 3.3 says only that the residual of any other month 'is free to be positive or negative'. L01.html:134 correctly predicts a nonzero residual only 'unless its cost happens to lie exactly on the line'. Independent witness (python -I, run in this round): costs (400 h, 1200), (700 h, 2100), (1000 h, 3000) give high-low v = 3, F = 0 and residual 0 at 700 hours, so the universal claim is false for some histories. The lab output (10 of 12 nonzero) supports it only for the seeded history.",
     "fix": "Replace 'Other months carry residuals (Remark 3.3)' in L01.html:459 with 'Other months may carry residuals (Remark 3.3)'."},
    {"id": "AC4-a-r26-scope-words", "check": "scope words (only, exactly, every, any, always, all, must, raises) in L01, L02 and the cards",
     "location": "L01.html:71,103,129,134,242,259,260,271,279,283,362,373,473; L02.html:76,81,98,108,122,130,134,267,291,294,311,362,394,405,417,434,435,496",
     "status": "PASS",
     "evidence": "Grep output read line by line. Each scope word has a stated computation or proof behind it: 'zero only at Q*' (L02:76, strictly increasing line); 'exactly when m divides F' (L02:81, integer F and m); 'exactly' in Prop 3.2 and 3.3 (proved); L02:311 'exactly when ... at or above the segment's zero' (Prop 4.1 proof); L01:134 'unless its cost happens to lie exactly on the line' (qualified); L01:279 'chosen by two observations only' (Prop 3.2). The only overreach found is L01:459, row AC4-a-r26-L01-q7-explanation."},
    {"id": "AC4-a-r26-cards-dup-scan", "check": "full duplicate scan of the 39 L01 and L02 cards and of the 140-card deck",
     "location": "course/modules/AC/AC4/cards.json",
     "status": "PASS",
     "evidence": "python -I scan in this round: 140 cards in the deck, no duplicate id, front or back; 19 L01 cards and 20 L02 cards (39 in all). Every card read against its lesson (AC4-c001..c030, c118..c120, c125, c127, c128, c130, c132, c135)."},
    {"id": "AC4-a-r26-indep-recompute", "check": "independent recomputation of every L01 and L02 number (own code, python -I)",
     "location": "ledgers/AC4/scripts/AC4-a-r26/indep_recompute_r26.py",
     "status": "PASS",
     "evidence": "Regenerated the seeded history: v-hat 4198.96 cents (41.99 USD), F-hat 1846389.18 cents (18,463.89 USD); largest |residual| 51,473.46 cents; 10 nonzero residuals; zero residuals at months 6 and 11; the noise identities for v-hat and F-hat hold exactly. R3 brute force over 1,201 whole hours: max error 3,990 at 1, 401, 801 h; 99.75% of 4,000. L02: margin 1350; BE 88.89; OI(88)=-12.00, OI(89)=1.50, OI(2001)=-1186.50, OI(2088)=-12.00, OI(2089)=1.50; loss runs [0,88] and [2001,2088]; upper BE 2088.89; MoS 411.11 (16.44%); DOL 6.08; +10,000 cents moves BE 7.41 units; R2 derivative -6.58 per USD and exact change -6.13; M1 Q*=1500, R*=120000; M2 1429; Example 2.4 3000 and 150000; Example 4.1 v 20, F 10000."},
    {"id": "AC4-a-r26-twin-equals-embedded", "check": "twin stdout (python -I -W error) equals the page's expected block",
     "location": "ledgers/AC4/scripts/AC4-a-r26/twin_equals_embedded_r26.py; out/twin_equals_embedded.out",
     "status": "PASS",
     "evidence": "L01: rc 0, stdout equals embedded block (20 lines). L02: rc 0, stdout equals embedded block (13 lines)."},
    {"id": "AC4-a-r26-mutants-new", "check": "three NEW student-error lab-twin mutants (round 26)",
     "location": "ledgers/AC4/mutants/AC4-a-r26/L02_v01_step_from_2000_inclusive.py, L02_v02_first_whole_by_floor.py, L01_v03_high_tie_takes_latest.py",
     "status": "PASS",
     "evidence": "v01 (step applies from 2000 inclusive) KILLED: stdout differs and the loss runs change. v02 (first whole unit by floor, 88) KILLED: stdout differs. v03 (high-activity tie takes the latest month) SURVIVED with identical stdout: the seeded hours have no tie for the maximum (1161 is unique), so the twin cannot see the tie rule. Out of scope under the architect ruling: no lesson sentence says the lab checks the tie rule (Definition 3.1 states the rule; card AC4-c132 cites the definition)."},
    {"id": "AC4-a-r26-mutants-suite", "check": "every committed AC4-a lab-twin mutant re-run (r18..r26, 39 files)",
     "location": "ledgers/AC4/scripts/AC4-a-r26/run_mutants_r26.py; out/mutants_r26.out",
     "status": "PASS",
     "evidence": "python -I -W error run of every file under ledgers/AC4/mutants/AC4-a-r*/ against the unmutated twin stdout: 34 KILLED, 5 SURVIVED with identical stdout and rc 0 (AC4-a-r21/L01_p01, AC4-a-r21/L02_p03, AC4-a-r21/L02_p04, AC4-a-r22/L01_q01, AC4-a-r26/L01_v03). Each survivor is out of scope: the seeded data has no tie, no zero operating income, or a month exactly at zero residual, and no lesson sentence claims the lab checks those properties."},
]
rows.extend(NEW)
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
for old in prev["rows"]:
    assert old["id"] in ids, old["id"]
statuses = [r["status"] for r in rows]
verdict = "PASS" if all(s == "PASS" for s in statuses) else "FAIL"
out = {
    "unit": "AC4", "slice": "AC4-a", "round": 26,
    "verifier": "independent verifier (Haiku), round 26",
    "pin": "f9f3fed", "base": "b49a857",
    "checkout": "/tmp/verify26-AC4-a", "scratch": "/tmp/AC4-v/AC4-a-r26",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": [
        {"id": "AC4-a-r18..r26 committed lab-twin mutants (39 files)",
         "description": "committed lab-twin mutants of L01 and L02 (ledgers/AC4/mutants/AC4-a-r18..r26)",
         "killed_by": "34 KILLED; 5 SURVIVED with identical stdout and rc=0, recorded as out of scope (out/mutants_r26.out)"},
        {"id": "AC4-a-r26/L02_v01_step_from_2000_inclusive",
         "description": "NEW student-error: step applied from 2000 units inclusive",
         "killed_by": "KILLED (loss run 2000 to 2088 printed)"},
        {"id": "AC4-a-r26/L02_v02_first_whole_by_floor",
         "description": "NEW student-error: first whole break-even taken by rounding down (88 instead of 89)",
         "killed_by": "KILLED (stdout differs)"},
        {"id": "AC4-a-r26/L01_v03_high_tie_takes_latest",
         "description": "NEW student-error: tie on highest activity resolved to the latest month",
         "killed_by": "SURVIVED (no tie in the seeded history); out of scope"},
    ],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta b49a857..f9f3fed for AC4-a: cards.json AC4-c026 only (the card now carries the single-segment qualifier). The three r25 lab mutants are committed files. index.html, L01.html, L02.html and tests/labs/AC4 are unchanged, so the carried rows keep their round-25 subjects.",
        "New FAIL: L01.html:459 (quiz item 7 explanation) states 'Other months carry residuals' as a general claim; Remark 3.3 supports only 'free to be positive or negative'. Witness in row AC4-a-r26-L01-q7-explanation. This was recorded as an observation in round 25 and is now a row.",
        "Card AC4-c026 and the cards row AC4-a-cards-L01-L02 now PASS: all 39 L01 and L02 cards were re-read against the lesson text.",
        "Carry rule: a round-25 PASS is carried only when its cited lines are byte-identical; command rows, the banned-phrase grep, cards, mutants and number rows are re-run or re-read this round.",
        "Not checked: L03 to L08 and their cards; project.html and the grader (other slices); hub hours were carried from round 25 because index.html is byte-identical; live access to external sources was not needed (registry checks run live and offline).",
    ],
    "summary": "",
}
n_fail = sum(1 for s in statuses if s != "PASS")
out["summary"] = (f"Slice AC4-a round 26 (pin f9f3fed, base b49a857): {len(rows)} rows, {n_fail} FAIL. "
                  "All command rows re-run and pass. Card AC4-c026 now states the single-segment scope (PASS), and all "
                  "39 L01/L02 cards re-read (PASS). One new FAIL: L01.html:459 quiz item 7 explanation says 'Other months "
                  "carry residuals', which a witness shows false in general (row AC4-a-r26-L01-q7-explanation). "
                  "Mutants: 34 of 39 killed; 5 survivors out of scope; 3 new mutants, 2 killed.")
dest = ROOT / "ledgers/AC4/AC4-a.json"
dest.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", dest, "rows", len(rows), "verdict", verdict)
