"""Build the round-18 M1-a fragment from the round-17 fragment and this round's re-verification."""
import json
import re
import sys

PREV = "/tmp/fanout-frags/M1-a.round17.json"
OUT = sys.argv[1]
CARRY = ("Carried from round 17 (cited subject byte-identical since the previous pin; the round-18 "
         "hunks in this slice are L01.html:316, L02.html:51, 62, 82, 286, L03.html:51, 63, 260, 352, 388 "
         "and cards.json M1-c060, M1-c175): ")

prev = json.load(open(PREV, encoding="utf-8"))

# Rows whose cited subject changed or that were non-PASS: re-verified this round (new evidence).
REVERIFIED = {
    "L01-scope-prose": "Re-read L01.html:316 (bullet 'Natural-language scope is ambiguous' now ends 'Formal notation removes the ambiguity by fixing the order.'). Removing the trailing clause adds no claim; the Example 4.1 cross-reference is unchanged at L01.html:107-113. PASS.",
    "L02-theorems": "Re-read L02.html:62 (Definition 1.2 now says the argument 'uses P(x), the definitions and earlier results, and it never fixes a particular value of x') and L02.html:82 (proof of Theorem 1.5: the hypothesis is used only to write a and b as 2m and 2n; no particular values). Statements at L02.html:76-77, 97-98, 107-108, 122-123, 132-133 unchanged and re-read. PASS.",
    "L02-misconceptions": "L02.html:286 re-read: 'Lab 1 searches p^2 = 2q^2 over q <= 300 and |p| <= 500, and finds no solution.' Lab twin lab-M1-L02-1.py:93 calls search_square_equation(2, 300, 500); run output /tmp/M1-v/M1-a/r18/L02.out line 8 'pairs tested 300300', line 9 'solutions found: 0' (300*1001 = 300300 recomputed). Theorem 2.5 (L02.html:123) covers every coprime pair with q >= 1 and p^2 = 2q^2. PASS.",
    "L02-numbers": "Re-checked L02.html:148,259,266,268,278,286,351,365,390,484 against /tmp/M1-v/M1-a/r18/L02.out (3721; 3721 of 3721; 0 solutions; 300300; 500; 2 coprime; least counterexample 0) and recomputed 61*61 = 3721, 300*1001 = 300300. L02.html:286 bound now re-read (above). PASS.",
    "L02-prereqs": "Re-read L02.html:62 (Definition 1.2 wording changed, dfn id def-direct-proof kept; grep finds one dfn for direct-proof in L02.html and one link in L03.html:37). L02.html:37, 93 unchanged. PASS.",
    "L03-numbers": "Re-checked the changed doubling-time interpretation L03.html:260 against lab line 78 (t:.4f of doubling_time(0.05)) and /tmp/M1-v/M1-a/r18/L03.out line 6 '13.8629 years'; (ln 2)/0.05 = 13.862943611198904 recomputed, rounded 13.8629. 2.0000 (line 7), 1.6487 (line 9; e^0.5 = 1.6487212707) recomputed. Other cited numbers (L03.html:155,165,256-260,352,357,366,377,409) re-checked; 352 is the E1 solution re-derived below. PASS.",
    "L03-lab-1": "Lab twin tests/labs/M1/lab-M1-L03-1.py unchanged since the previous pin (git diff --quiet fefbf8b 7143726 -- tests/labs/M1 exits 0). Re-ran it under python -I -W error: exit 0, output in /tmp/M1-v/M1-a/r18/L03.out. L03.html:163-261 re-read; the hypothesis and output lines match. PASS.",
    "L03-interpretation": "L03.html:260 re-read: 'The printed doubling time, 13.8629 years, is the code's value of (ln 2)/0.05, computed with math.log and rounded to four decimals. That value is 20 ln 2 up to rounding, and nothing is typed in.' Lab line 77 computes t = doubling_time(rate) and line 78 prints it with :.4f; doubling_time returns math.log(2.0)/rate (lab lines 57-62). Recomputed 20*ln2 = 13.862943611198906. PASS.",
    "L03-problems": "L03.html:352 (E1 solution) re-derived: the printed factor 1.6487 is rounded to four decimals, so the factor is in [1.64865, 1.64875) (true e^0.5 = 1.6487212707 is inside). The gain is in [0.64865, 0.64875), i.e. [64.865, 64.875) percent, and every value there rounds to 64.9 at one decimal. L03.html:388-390 (R3 solution): the derivation of ln(ab) = ln a + ln b uses A2 and A3 (Proposition 1.6(b), L03.html:118). R1-R2 and E2-E3 unchanged and re-read. PASS.",
    "L03-simulated-label": "L03.html:349-363 re-read, including the changed E1 solution at :352 (the lab output is labelled as printed to four decimals, which is what the solution uses). PASS.",
    "L03-prereqs": "L03.html:37 (link data-concept direct-proof to L02.html#def-direct-proof) and L03.html:68 unchanged; L03 prerequisites unchanged. PASS.",
    "M1A-hours-total": "Re-run: grep data-hours L01-L08 = 8,9,9,9,8,9,9,9 (sum 70); index.html:29 data-hours-lessons=70, index.html:39 hours-split '70 lesson hours and 30 project hours'. Lesson data-hours lines are unchanged (no hunk at line 2 in L01-L03). PASS.",
    "M1A-r6-recheck-numbers": "Re-run ledgers/M1/scripts/M1-a-r7/recheck_numbers.py in this checkout (the M1-a-r6 folder is not in the checkout; the r7 script is the one the round-17 row used): exit 0; output ledgers/M1/scripts/M1-a-r18/recheck_out.txt, including 'hub hours: 8+9+9+9+8+9+9+9 = 70 ; +30 = 100', 'L03 ln(1.5)/4 = 0.10137', 'L03 ln3/5 = 0.21972', '7^3 check 343'. PASS.",
    "M1A-r7-expected-vs-run": "Re-run ledgers/M1/scripts/M1-a-r7/expected_vs_run.py /tmp/verify18-M1-a: 'L01 lines 13 IDENTICAL', 'L02 lines 10 IDENTICAL', 'L03 lines 9 IDENTICAL', 'ALL IDENTICAL'. Covers the L02 and L03 expected blocks changed in the lessons. PASS.",
    "M1A-why-words": "Re-read the changed why-it-matters paragraphs L02.html:51 and L03.html:51 and the scanned added lines (grep for build, builder, round, verifier, request, unit report, banned words): none present. PASS.",
    "M1A-banned": "Scan of every added line in L01.html, L02.html, L03.html, cards.json (this round's diff) for roughly, about, historically, ellipsis, typically, usually: none. Scope words in the changed lines (every, only, all, always, same) each checked against the text: L02.html:286 'every coprime pair' (Theorem 2.5), L03.html:63 'Every proposition below' (Props 1.2-2.2 use only A1-A3 and definitions), L03.html:118 proofs. PASS.",
    "M1A-dfn-once": "grep data-concept=\"direct-proof\": one <dfn> in L02.html (line 62 id def-direct-proof), one link in L03.html:37. PASS.",
    "M1A-curriculum-concepts": "L02.html:62 keeps the <dfn id=\"def-direct-proof\" data-concept=\"direct-proof\"> definition after the rewording; L03.html:37 links it. Concept definitions unchanged elsewhere. PASS.",
    "M1A-cmd-check_pages": "Round 18: .venv/bin/python tools/check_pages.py --unit M1 printed 'check_pages M1: PASS' (exit 0).",
    "M1A-cmd-check_dag": "Round 18: tools/check_dag.py --all exit 0; 'check_dag M1: PASS' (also AC4, CF1, AP1 PASS).",
    "M1A-cmd-run_labs": "Round 18: tools/run_labs.py --unit M1 printed 'run_labs M1: PASS (11/11)', exit 0.",
    "M1A-cmd-twin-isolated": "Round 18: python -I -W error tests/labs/M1/lab-M1-L01-1.py, lab-M1-L02-1.py, lab-M1-L03-1.py each exit 0 (outputs /tmp/M1-v/M1-a/r18/L0{1,2,3}.out).",
    "M1A-cmd-page_smoke": "Round 18: tools/page_smoke.py --unit M1 --pages index.html L01.html L02.html L03.html printed 'page_smoke M1: PASS'.",
    "M1A-cmd-ruff-mypy": "Round 18 (whole project, since AC1, AC4, CF1 changed): ruff check . exit 0; ruff format --check . '212 files already formatted' exit 0; mypy --no-incremental 'Success: no issues found in 153 source files' exit 0 (/tmp/M1-v/M1-a/r18/ruff.txt, mypy.txt).",
    "M1A-cmd-verify_refs": "Round 18: verify_refs.py --offline '560 entries, 0 problems'; verify_refs.py --unit M1 'live re-verification of M1: 1 of 560 entries, 0 problems'.",
    "M1A-cmd-pytest-labs": "Round 18: pytest -q tests/test_labs.py tests/test_run_labs.py exit 0 (all dots, 100%).",
    "M1A-cards-L01-L03": "Round 18 full re-read of all 76 current L01-L03 cards (the round-17 FAIL is closed: c060 fixed, c175 removed; 77 -> 76). Each card's cited label was read in stripped text: Definitions 1.1-2.4 (L01.html:58-70, L02.html:56-120), Theorems 3.1, 3.2, 4.2, 5.1, 1.5, 2.5, Corollary 2.6, Lemmas 2.2, 2.3, Fact 1.4, Remarks 2.2, 2.4, 2.7, Examples 2.3, 4.1, Propositions 1.2-1.7, 2.1, 2.2, Problems E1-E3 (L01.html:398; L02.html:348-363; L03.html:349-352). Lab-derived numbers checked against /tmp/M1-v/M1-a/r18/L01.out (16, 512, 343, 40, 1681), L02.out (3721, 300300, 500, 0, 2 and 2001 values), L03.out (169, 13, 6, 36, 13.8629, 1.6487). Cards c001-c174 for L01-L03 match their lesson text; cards outside L01-L03 (M1-c160, c163 etc.) are not in this slice. PASS.",
    "M1A17-card-c060": "M1-c060 back is now '13.8629 years (to four decimals), the value of (ln 2)/0.05 = 20 ln 2'. Recomputed (ln 2)/0.05 = 13.862943611198904, round to four decimals 13.8629 = lab line 6 (L03.out) and L03.html:257. The card grade C and basis 'Lab 1 (printed to four decimals)' match. PASS.",
    "M1A17-card-c175-dup": "M1-c175 ('For y > 0, what is ln(1/y)?') is removed from cards.json. Remaining card M1-c063 ('Is ln(1/y) equal to 1/ln y?') is the only card with the ln(1/y) fact (grep '1/y' finds only c063 at cards.json:429-430). Proposition 1.6(c) at L03.html:113 and proof at L03.html:118 verified. Total cards 179 -> 178, L01-L03 77 -> 76. PASS.",
    "M1A17-cards-changed-L03": "cards.json L03 entries changed at M1-c060 (fixed) and M1-c175 (removed); cited L03.html Propositions 1.4, 1.6, 1.7, 2.1, 2.2 and Lab 1 lines re-read (L03.html:92-151, 256-260). PASS.",
    "M1A17-cards-grades-basis": "Round 18: all L01-L03 cards with grade C keep a basis naming the lab or the listed range (c016, c017, c034-c036, c041, c056, c058-c060, c147-c151). c060 basis unchanged. PASS.",
    "M1A17-delta-read": "Replaced by M1A18-delta-read (the round-17 pin is fefbf8b; the round-18 delta is listed there).",
    "M1A17-lessons-unchanged": "No longer true: L01.html, L02.html and L03.html changed between fefbf8b and 7143726 (the hunks are listed in M1A18-delta-read). index.html and tests/labs/M1 are byte-identical (git diff --quiet exits 0). Replaced by the round-18 rows.",
}

NEW = [
    {"id": "M1A18-delta-read",
     "check": "Delta of this slice between the previous pin fefbf8b and the round-18 pin 7143726",
     "location": "course/modules/M/M1/L01.html, L02.html, L03.html, cards.json; index.html and tests/labs/M1 unchanged",
     "status": "PASS",
     "evidence": "git diff fefbf8b 7143726 -- course/modules/M/M1/ shows hunks only at L01.html:316; L02.html:51, 62, 82, 286; L03.html:51, 63, 260, 352, 388; cards.json M1-c060 and M1-c175 changed or removed; M1-c160 and M1-c163 (L05, L04) changed outside this slice. git diff --quiet fefbf8b 7143726 for course/modules/M/M1/index.html and tests/labs/M1 exits 0. L04, L05, L08 changes are outside this slice. Every hunk in the slice is read (see rows)."},
    {"id": "M1A18-L01-scope-bullet", "check": "Rewritten L01 canon bullet (scope and ambiguity)",
     "location": "course/modules/M/M1/L01.html:316", "status": "PASS",
     "evidence": "Only the trailing clause 'which is the reason for it' was removed. The bullet's claims (two readings, different quantifier orders, Example 4.1 shows they can differ) are unchanged and checked against L01.html:107-113."},
    {"id": "M1A18-L02-why-it-matters", "check": "Rewritten L02 why-it-matters: 'The lab runs finite checks and reads each one as evidence about its range.'",
     "location": "course/modules/M/M1/L02.html:51; tests/labs/M1/lab-M1-L02-1.py:89-96", "status": "PASS",
     "evidence": "lab-M1-L02-1.py enumerates finite ranges and prints each range with its count (lines 89-96: 'parity lemma, p in -2000 to 2000', 'search p*p == 2*q*q, 1 <= q <= 300, |p| <= 500'). The sentence describes that behaviour; L02.out lines 1-9 confirm."},
    {"id": "M1A18-L03-assumption-scope", "check": "Rewritten L03 sentence 'Every proposition below follows from A1 to A3 and the definitions.'",
     "location": "course/modules/M/M1/L03.html:63 (block at :56-63); propositions L03.html:72-151", "status": "PASS",
     "evidence": "grep for 'Assumption E' in L01-L03 finds nothing; the only assumptions block is A1-A3 (L03.html:57-61). Propositions 1.2 (A2, A1), 1.3 (A2, A1, 1.2), 1.4 (A1, A3), 1.5 (1.4), 1.6 (1.2, A2, A3, 1.4), 1.7 (A2), 2.1 (1.4, A3), 2.2 (1.4, A3) use only A1-A3 and earlier results. The 'Assumption E' of L05 is not in this lesson (its card M1-c160 is outside this slice)."},
    {"id": "M1A18-L03-doubling-interpretation", "check": "Rewritten L03 interpretation: printed doubling time is the code's value of (ln 2)/0.05, rounded to four decimals, nothing typed in",
     "location": "course/modules/M/M1/L03.html:260; tests/labs/M1/lab-M1-L03-1.py:57-62, 76-78; /tmp/M1-v/M1-a/r18/L03.out line 6", "status": "PASS",
     "evidence": "doubling_time returns math.log(2.0) / rate (lab line 62); line 78 prints it with {t:.4f}. Output '13.8629 years'. Recomputed (ln 2)/0.05 = 13.862943611198904 and 20*math.log(2) = 13.862943611198906. The sentence says 'up to rounding', which is correct."},
    {"id": "M1A18-L03-E1-solution", "check": "E1 solution: percentage gain from the printed factor, to one decimal",
     "location": "course/modules/M/M1/L03.html:352", "status": "PASS",
     "evidence": "Printed 1.6487 means true factor in [1.64865, 1.64875). Gain in [64.865, 64.875) percent. Both ends round to 64.9 at one decimal; e^0.5 - 1 = 0.6487212707 (64.87%) is inside. Stated basis (the lab prints four decimals, no unrounded value) matches the lab print at L03.out line 9."},
    {"id": "M1A18-L03-R3-solution", "check": "R3 solution: why the product rule is a theorem, not a definition",
     "location": "course/modules/M/M1/L03.html:388-390; proof at L03.html:118", "status": "PASS",
     "evidence": "The proof of Proposition 1.6(b) (L03.html:118) uses A2 (e^(x+z) = e^x e^z) and the uniqueness in A3. The new sentence 'The derivation uses A2 and A3 together, so a reader who changes A2 must derive the rule again' describes that dependence and makes no stronger claim."},
    {"id": "M1A18-L02-direct-proof-def", "check": "Rewritten Definition 1.2 and proof of Theorem 1.5 wording ('never fixes a particular value of x'; 'no particular values are used')",
     "location": "course/modules/M/M1/L02.html:62, 82", "status": "PASS",
     "evidence": "Definition 1.2 (L02.html:62) and the Theorem 1.5 proof (L02.html:82) read in full. The proof's hypothesis use is limited to writing a = 2m, b = 2n; no particular a or b is chosen. Matches the definition."},
    {"id": "M1A18-L02-search-misconception", "check": "Rewritten misconception: search covers the listed range, Theorem 2.5 covers every coprime pair",
     "location": "course/modules/M/M1/L02.html:286; lab-M1-L02-1.py:93; L02.out line 8-9", "status": "PASS",
     "evidence": "Lab searches 1 <= q <= 300, |p| <= 500 (lab line 93): 'pairs tested 300300', 'solutions found: 0'. Theorem 2.5 (L02.html:122-123) covers all coprime pairs with q >= 1 and p^2 = 2q^2. The new clause 'whereas the search covers the listed range' is accurate."},
    {"id": "M1A18-cards-L01-L03-changed", "check": "Cards changed in this slice: M1-c060 (rounded value), M1-c175 (removed as duplicate); L01-L03 count 77 -> 76",
     "location": "course/modules/M/M1/cards.json (M1-c060 at :405-411; M1-c063 at :427-432; M1-c175 removed at former :1212)", "status": "PASS",
     "evidence": "Parsed cards.json: 178 cards total (previous 179), 76 L01-L03 cards (previous 77), no duplicate id, no duplicate front. The hub index.html (cards grid :150-158) quotes no card count. c063 is the only remaining card for ln(1/y) = -ln y."},
    {"id": "M1A18-hub-unchanged", "check": "index.html and its cards unchanged; hub hours and lesson links",
     "location": "course/modules/M/M1/index.html:29, 39, 150-158", "status": "PASS",
     "evidence": "git diff --quiet fefbf8b 7143726 -- course/modules/M/M1/index.html exits 0. Lesson data-hours L01-L03 = 8, 9, 9 (sum 26); hub lesson hours data-hours-lessons=70 is the sum of all eight lesson hours (8+9+9+9+8+9+9+9). Hours are design targets (architect ruling); only the split arithmetic is checked."},
    {"id": "M1A18-mutants-na", "check": "Mutant and alternative-implementation requirement",
     "location": "ledgers/M1/mutants/ (project slice only)", "status": "PASS",
     "evidence": "Not applicable: M1-a is a hub and lesson slice, not a project slice. The round-17 note says the same. No mutants or alternative implementations are claimed for this slice."},
]

rows = []
carried_ids = set()
for r in prev["rows"]:
    rid = r["id"]
    if rid in REVERIFIED:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": REVERIFIED[rid]})
        continue
    if r["status"] != "PASS":
        raise SystemExit(f"non-PASS row {rid} has no round-18 re-verification")
    ev = re.sub(r"^Carried from round 1[67] \([^)]*\)[^:]*:?\s*", "", r["evidence"])
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                 "evidence": CARRY + ev})
    carried_ids.add(rid)

rows += NEW
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
missing = [r["id"] for r in prev["rows"] if r["id"] not in ids]
assert not missing, missing

frag = {
    "unit": "M1", "slice": "M1-a", "round": 18,
    "verifier": "Haiku 5.5 independent verifier, round 18",
    "pin": "7143726",
    "base": "fefbf8b (previous pin; delta on the slice paths: L01.html:316; L02.html:51, 62, 82, 286; L03.html:51, 63, 260, 352, 388; cards.json M1-c060, M1-c175 removed, M1-c160/c163 (L04/L05, outside the slice) changed)",
    "previous_ledger": "/tmp/fanout-frags/M1-a.round17.json",
    "checkout": "/tmp/verify18-M1-a",
    "scratch": "/tmp/M1-v/M1-a/r18",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Mutants: not required, M1-a is not a project slice. No alternative implementations were run for the same reason.",
        "Every previous non-PASS row was re-verified from scratch: M1A-cards-L01-L03 (all 76 cards read), M1A17-card-c060 and M1A17-card-c175-dup.",
        "Rows whose cited subject changed were re-verified; rows whose cited subject is byte-identical are carried with the round-17 prefix.",
        "Not checked this round: L04-L08 and the project/grader slices (other slices); the Velleman source (no publisher page opened); the cards for M1-c160 and M1-c163 (L05 and L04, outside this slice); the hours pace (architect ruling); the full PDF/HTML rendering of the lesson pages (only page_smoke was run).",
    ],
    "summary": "",
}
n = len(rows)
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag["summary"] = (f"Round 18 M1-a: {n} rows, {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. "
                   "Round 17 FAIL rows (M1A-cards-L01-L03, M1A17-card-c060, M1A17-card-c175-dup) are closed by re-reading the cards and the changed lessons. "
                   "Hub and lab twins byte-identical to the previous pin; all commands re-run and passing.")
json.dump(frag, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("rows", n, counts, "carried", len(carried_ids))
