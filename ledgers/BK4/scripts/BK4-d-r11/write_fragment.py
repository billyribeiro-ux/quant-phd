"""Writes ledgers/BK4/BK4-d.json (round 11, verifier d). Evidence strings cite the scripts and outputs under scripts/BK4-d-r11/."""
import json, datetime
S = "ledgers/BK4/scripts/BK4-d-r11"
OUT = S + "/out"
rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

ALLCARDS = "course/modules/BK/BK4/cards.json"
RECHECK = f"{S}/recheck_numbers.py -> {OUT}/recheck_numbers.txt (all PASS except none; 0 FAILS)"
DUP = f"{S}/dup_and_xref.py -> {OUT}/dup_and_xref.txt"

row("cards-structure", "2.7-structure", f"{ALLCARDS} (100 cards)", "PASS",
    "Re-run on the changed file: 100 cards, 100 unique ids, all match BK4-cNNN; per lesson L01 17, L02 25, L03 24, L04 19, L05 15; grades T 51, C 14, ungraded 35 (was T 53, C 12: c043, c044 moved T to C); id gaps c042 c045 c070 c082 c085 (ids need not be sequential, FINAL-ARCHITECT-RULINGS 2); every T or C card has a basis, no ungraded card has one. Command: python3 inline check, see " + DUP)
row("cards-duplicate-scan", "2.7-duplicates", f"{ALLCARDS} (full pairwise scan, front and back)", "PASS",
    "difflib SequenceMatcher over all 4950 pairs, fronts and backs: no exact duplicate; 157 pairs above 0.6 on one side, each reviewed. Closest: c049/c050 (9900 vs 9975 target; answers 2961 vs 2992), c008/c101 (Need_A vs Debit_A in Example 2.6), c029/c102 (R1 range vs R1 equality), c030/c103 (P3 netted amount 0 vs reduction 10000 bps), c080/c100 (Proposition 2.1 vs Proposition 2.4 are distinct theorems). Output: " + DUP)
row("cards-coverage", "2.7-coverage", "L01-L05 Definitions, Propositions, Examples, Remarks, Problems, key-results rows, Misconceptions vs " + ALLCARDS, "PASS",
    "Every Definition (L01 1.1, 1.2, 2.1; L02 1.1, 1.2, 2.1, Assumption 1.3; L03 1.1, 2.1; L04 1.1, 1.2, 2.1, 3.1; L05 1.1, 1.2, 2.1) has a card; every Proposition used as a key result has a card (L01 2.2-2.4; L02 2.2(a)-(d), 2.3; L03 1.2, 1.3, 2.3, Cor 2.4; L04 2.2, 2.4-2.7; L05 2.1, 2.2, 2.4-2.6); all 16 misconceptions (L01 three, L02 three, L03 four, L04 three, L05 three) have a card; all Examples used in key rows (L01 2.6, Remark 2.7; L02 2.4; L03 1.5, 1.6, 2.5; L04 Remark 2.8; L05 2.7, 2.8) have a card. Remark 2.5 (L02), Remark 2.6 (L03), Remark 3.2 (L04) carry no card and are not key results.")
row("cards-numbers", "2.7-numbers", ALLCARDS + " numbers vs lesson text and lab outputs", "PASS",
    "Independent re-derivation " + RECHECK + ". Checked: L01 Bank A/B/C need, net, debit, 1533900/2841600, 0.5398; Example 2.6 need 100 and debit 50; Remark 2.7 need 50; L02 netted 5093600, gross 7596300, 3294 and 7826 bps; L03 fixtures 8, 12, 1, 1, 0, k=198, sized 2961 and 2992 regenerated from the seeded generator (brute-force agrees); L04 9/10, 11/10, 11000, 9416, 113/120, 20/19, 19/40, 6875; L05 4375/2, 2188, 169/512, 3/8, 343/512, 1875, 133984375/4, 57421875/4, 19140625. Every card number appears in its lesson text (read in full).")
row("cards-xrefs", "2.7-xrefs", ALLCARDS + " basis and front/back label references", "PASS",
    "Every label named in a basis or in a card text resolves to a label in the same lesson (" + DUP + "). The 15 'unresolved' regex hits are trailing punctuation only; each named label was located by hand in L01-L05 (Example 2.6, Remark 2.5, Assumption 1.3, Example 2.5, Remark 1.4, Definition 1.1, Definition 3.1, Proposition 2.7, Remark 4.1, Remark 2.8, Proposition 2.1, Remark 2.3). Basis strings: 'Problem R1', 'Problem P2', 'Problem P3', 'Corollary 2.4', 'Example 2.7', 'Section 4 with Proposition 2.2(c)' all exist.")
row("cards-lab-outputs", "2.7-lab-outputs", ALLCARDS + " C-graded and lab-named cards vs lab twins", "PASS",
    "Twins run alone under python3 -I -W error from /tmp, all exit 0: " + S + "/out/lab-BK4-L01-1.out ... L05-1.out. Printed values cited by cards match: c010 1533900, c011 112500, c014 +379800 and 0 (L01 Part B); c012 1533900 and 2841600 (L01 Part C); c031 5093600, c092 7596300 (L02 Parts B and D); c049 2961 and c050 2992 with cover 9900 and 10000 bps (L03 Part B); c086 4375/2 (L05 Part B); c087 133984375/4 and 57421875/4 (L05 Part D); c094 rounding to 2188 (L05). tools/run_labs.py --unit BK4: PASS (8/8).")
row("cards-grades-vs-keyresults", "2.7-grades-vs-keyresults", f"{ALLCARDS} lines 346 and 355 (BK4-c043, BK4-c044) vs course/modules/BK/BK4/L03.html line 565 (key-results row)", "PASS",
    "Card and key row now agree: both grade the fixture claim C with basis 'Lab 1, Parts A1 and A2 (fixed fixture, not seeded)' (cards.json lines 346-359; L03.html line 565). Agreement only; the grade category itself is FAIL in cards-grade-rule9. The round-10 mismatch (cards T vs key C) is closed.")
row("cards-hypotheses", "2.7-hypotheses", f"{ALLCARDS} line 649 (BK4-c083) vs course/modules/BK/BK4/L05.html Proposition 2.5 hypotheses", "PASS",
    "Round-10 FAIL closed: c083 front now reads 'Assuming the finite probability space, A1, A2, 0 < p < 1 and kappa > 0, with A3 ... and A4', matching the Proposition 2.5 hypotheses on L05.html (A1 and A2; A3 for Var_3; A4 for Var_4; 0 < p < 1; kappa > 0). Re-checked every T card's front against its proposition: L01 2.2-2.4, L02 2.2-2.3, L03 1.2-1.3, 2.3, Cor 2.4, L04 2.2, 2.4-2.7, L05 2.1-2.6 (c088 front omits 0<p<1 and kappa>0 but its back states them before the variance claim; c055 uses Remark 2.2 under Definition 1.1 and says so in its back; both accepted).")
row("cards-attribution-duffie", "attribution", "BK4-c032 (cite duffie2011central); references/references.json line 7412", "PASS",
    "Registry record title 'Does a Central Clearing Counterparty Reduce Counterparty Risk?' (Duffie, Zhu; 2011; Review of Asset Pricing Studies). Live plain-curl Crossref call https://api.crossref.org/works/10.1093/rapstu/rar001 returned the same title, container and 2011 issue date (" + OUT + "/duffie_crossref.txt). The card's back says 'the title of the paper' and states no finding, matching L02 Section 4. Registry change this round is used_by only (BK4 added to bisndbasel, LX1 to another key), which does not touch this record.")
row("cards-banned-and-process-words", "2.2-banned-and-process-words", ALLCARDS + " all fronts and backs", "PASS",
    "grep for banned and scope/process words (obvious, clearly, simply, trivial, we show, the learner, this card, as expected, surely) over the file: no hit. 'processes' in c077 is the lesson's own operational-risk definition text, not a process word. 'never changes the net debit' (c015) is the proved order-independence of Remark 2.5.")
row("cards-notation", "2.3-notation", ALLCARDS + "; notation/notation.json", "PASS",
    "Registered symbols (T, Phi, gamma_3, gamma_4, R^ast, R^e-ast, R_f, Q) do not occur as symbols in any card (grep: the only capital T hits are the grade field and the settlement label 'T+1', not a variable). Card-local symbols (S, D, C, K, G, rho, theta, ell, n, Z) are lesson-local per notation.json 'about' and are defined on their own lesson page.")
row("cards-dag", "4-dag", "course/modules/BK/BK4 cards; check_dag --unit BK4", "PASS",
    "check_dag --unit BK4: PASS (" + OUT + "/check_dag.txt). Cards name no concept outside the unit's prerequisite closure; the Duffie attribution is paper-level.")
row("cards-pages-gate", "2.7-pages", "check_pages --unit BK4 (includes check_cards); page_smoke --unit BK4 (alone)", "PASS",
    "check_pages --unit BK4: PASS (" + OUT + "/check_pages.txt). page_smoke --unit BK4 run alone: PASS for project.html, index.html, concepts.html, review.html and BK4 (" + OUT + "/page_smoke.txt).")
row("cards-c001-c010", "2.7-card-read", ALLCARDS + " BK4-c001..c010", "PASS",
    "Each card read against L01 Definitions 1.1, 1.2, 2.1, Proposition 2.2-2.4, Problem P2, Example 2.6, Remark 2.7 and Lab 1 Part B: all statements agree; numbers per cards-numbers.")
row("cards-c011-c020", "2.7-card-read", ALLCARDS + " BK4-c011..c020", "PASS",
    "c011 (112500), c012 (1533900 of 2841600, 0.5398), c013 (A2 funding), c014 (net credit, Bank A figures), c015 (Remark 2.5) read against L01 and recomputed.")
row("cards-c021-c030", "2.7-card-read", ALLCARDS + " BK4-c021..c030", "PASS",
    "L02 Definitions 2.1 (n_i, A, reduction, floor), Proposition 2.2(a)-(d), 2.3, Example 2.4 (A=50, 7826 bps), Problem R1 and P3 read against the cards; all agree.")
row("cards-c031-c040", "2.7-card-read", ALLCARDS + " BK4-c031..c040", "PASS",
    "c031 (5093600, Lab 1 Part D), c032 (Duffie question; no finding), c033-c035 misconceptions (Proposition 2.2(b) is bookkeeping, no default term), c036-c040 L03 Definition 1.1 layer order, Definition 2.1 cover basis and Proposition 1.2 conservation, all agree with L03/L02 text.")
row("cards-c041-c050", "2.7-card-read", ALLCARDS + " BK4-c041..c050 (c043 line 346, c044 line 355)", "FAIL",
    "Card text agrees with the page (Example 1.5 and 1.6 arithmetic recomputed: 8, 12 and 1, 1, 0). The grade fails: c043 and c044 are C with basis 'Lab 1, Parts A1 and A2 (fixed fixture, not seeded)', but the values are derived on the page in L03.html Example 1.5 (block title line 104) and Example 1.6 (line 124) from Definition 1.1. The lab's Part A1/A2 inputs are the page's fixtures, not SIMULATED (tests/labs/BK4/lab-BK4-L03-1.py docstring). See cards-grade-rule9.",
    "Regrade c043 and c044 to T, basis 'Example 1.5 (worked on the page under Definition 1.1, with A1 and A2); Lab 1 Part A1 reproduces it' (and 'Example 1.6 ... Part A2'), the round-10 basis; regrade the matching L03.html key row (line 565) to T in the L03 builder's batch.")
row("cards-c051-c060", "2.7-card-read", ALLCARDS + " BK4-c051..c060", "PASS",
    "Initial margin, default fund, CCP capital, surviving member definitions; Remark 1.4 layer rule (c057); Definition 1.1 proportional sharing by default fund, not initial margin (c058); misconception statements agree with L03 Section 4-5.")
row("cards-c061-c070", "2.7-card-read", ALLCARDS + " BK4-c061..c070", "PASS",
    "L04 Definitions 1.1, 1.2, 2.1, 3.1 and the claim/reserve/redemption vocabulary read against the lesson text; Proposition 2.2 hypotheses (C_0>0, 0<=x<1, x<=rho) and the formula (rho-x)/(1-x) agree; tokenization card states no speed, cost or legal claim, as Definition 3.1 does.")
row("cards-c071-c080", "2.7-card-read", ALLCARDS + " BK4-c071..c080", "PASS",
    "Propositions 2.4-2.7, Remark 2.8 (9000, 11000, 9416 bps), Remark 4.1 threshold 20/19 under Assumption 4, misconceptions c074-c076 (rho=1 haircut case; halving; unchanged ratio) all agree with L04 text and recomputed values.")
row("cards-c081-c090", "2.7-card-read", ALLCARDS + " BK4-c081..c090 (c083 line 649 now PASS; c086 line 667 FAIL)", "FAIL",
    "c081, c083 (A2 now in the hypotheses), c084, c088, c089 (169/512, 3/8, p), c090 (1875) agree with L05 and recomputed values. c086 is C with basis 'Lab 1, Part B; SIMULATED parameters, one set', but L05.html Example 2.8 (block title line 152, text line 153) derives E[C] = 1/8 * 2500 * 7 = 4375/2 = 2187.5 on the page from Proposition 2.1 at the same parameters. See cards-grade-rule9.",
    "Regrade c086 to T with basis 'Example 2.8 (Proposition 2.1 at p = 1/8, kappa = 2500, ell = (1,2,4)); Lab 1 Part B prints 4375/2'; regrade the L05.html key row at line 486 to T in the L05 builder's batch.")
row("cards-c091-c094", "2.7-card-read", ALLCARDS + " BK4-c091..c094 (c094 line 735 FAIL)", "FAIL",
    "c091 (net debit definition), c092 (gross notional 7596300 = sum of receivables, Lab 1 Part B), c093 (claims outstanding), c094 agree with the text and recomputed values; c094's value 2188 is the same page-derived result as c086 (L05.html Example 2.8, 'is 2188 cents'). Graded C with basis 'Lab 1, Part B; SIMULATED parameters, one set'. See cards-grade-rule9.",
    "Regrade c094 to T with basis 'Example 2.8 (the rounding rule of Lab 1, applied once to 2187.5)'.")
row("cards-c095-c098", "2.7-card-read", ALLCARDS + " BK4-c095..c098", "PASS",
    "Multilateral netting definition (c095), variation margin (c096: initial margin only, as L03 Section 3 says), admissible share (c097, Remark 2.3), joint law definition (c098) agree with the lesson text.")
row("cards-c099", "2.7-card-read", ALLCARDS + " BK4-c099", "PASS",
    "A zero iff every n_i zero argument matches L02 Misconception 1 and Proposition 2.2(b).")
row("cards-c100-c101", "2.7-card-read", ALLCARDS + " BK4-c100, BK4-c101", "PASS",
    "c100 (Proposition 2.4 under A4, same value; proof of Prop 2.1 applies unchanged) and c101 (Example 2.6 DNS debit 50) agree with the lesson and recomputed values.")
row("cards-c102-c104", "2.7-card-read", ALLCARDS + " BK4-c102..c104", "PASS",
    "Problem R1 (10000 bps iff A=0), Problem P3 (10000 bps, A=0) and Proposition 1.3 survivor bound x_i+1 <= DF_i (c104) agree with the lesson text.")
row("cards-c105", "2.7-card-read", ALLCARDS + " BK4-c105", "PASS",
    "Scenario set definition (S >= 1, non-negative integer cents) agrees with L03 Definition 2.1.")
row("cards-scope-claims", "2.7-scope", ALLCARDS + " all scope words (only, all, every, exactly, never, any, whatever, same)", "PASS",
    "Each scope word in a card is backed by a stated computation or hypothesis: 'only' in c056 and c057 (count-only cover; margin alone pays inside margin), 'exactly' in c102 (Problem R1), 'never changes' in c015 (Remark 2.5), 'whatever the reserve assets are worth' in c074 (conditional on Assumption 4), 'the same' in c080/c100 (Proposition 2.1 and 2.4).")
row("cards-refs-live", "2.7-refs-live", "references/references.json (duffie2011central at line 7412); tools/verify_refs.py --offline", "PASS",
    "verify_refs.py --offline: 560 entries, 0 problems (" + OUT + "/verify_refs_offline.txt). duffie2011central checked live (Crossref, see cards-attribution-duffie). bisndbasel is cited by no card (L05 cites it at index level only, outside this card slice) and was not re-fetched; not counted here.")
row("cards-delta-round7", "2.7-delta", "cards.json history before round 8 pin", "PASS",
    "Carried from round 10 (history commits before the round-8 pin are immutable; no byte change since): " + "round-7 delta was verified in E-BK4-d.round7.json and is unchanged in the history.")
row("cards-delta-round8", "2.7-delta", "cards.json history between round-7 and round-8 pins", "PASS",
    "Carried from round 10 (commit range between the round-7 and round-8 pins is immutable; no byte change since).")
row("cards-delta-round9", "2.7-delta", "cards.json delta c93dd526..00a84795 (BK4-c075 front, BK4-c105 back) and lesson hunks L01-L05, index, project", "PASS",
    "Carried from round 10 (commit range c93dd526..00a84795 is immutable; its effects are re-read in full in this round).")
row("cards-delta-round10", "2.7-delta", "course/modules/BK/BK4 and tests/labs/BK4 at 00a84795 vs c93dd526", "PASS",
    "Carried from round 10 (commit range immutable). Round-10 delta items are re-verified fresh in cards-hypotheses and cards-c081-c090.")
row("cards-delta-round11", "2.7-delta", "course/modules/BK/BK4 and tests/labs/BK4 at 11d7077 vs 00a84795", "PASS",
    "git diff 00a84795 11d7077: cards.json only c043 (lines 346-349) and c044 (lines 355-358) grade T to C and basis changed; references/references.json used_by (BK4 added to bisndbasel, LX1 to another key) and generated_at; project.html and grader/test_project.py changed (not card-cited). git diff --quiet: L01-L05, index.html, tests/labs/BK4, notation/ and tools/ byte-identical to 00a84795 (exit 0). All card rows re-verified fresh (cards.json changed).")
row("cards-property-checks", "2.7-T-propositions", "T-graded propositions and lesson statements behind cards (51 T cards)", "PASS",
    "Every T card's statement was re-checked against its proposition's hypotheses and proof (listed in cards-hypotheses) and the identities by exact Fraction arithmetic in " + RECHECK + " (e.g. difference identity -31/784, sign rule, Prop 2.6 identity 1/16, Prop 2.4 identity, P^2(3-p) identity 162/343).")
row("cards-grade-rule9", "2.7-grade-rule (verifier rules item 9; plan §9 'Grade T for every derived result')", "cards.json lines 346, 355 (c043, c044), 667 (c086), 735 (c094); L03.html lines 104, 124, 565; L05.html lines 152-153, 486", "FAIL",
    "Five cards are graded C where the value is derived on the page, not read off a SIMULATED lab. c043/c044: Example 1.5 and 1.6 (L03.html lines 104, 124) compute 8, 12 and 1, 1, 0 from Definition 1.1; the lab's Parts A1/A2 use the page's fixture (lab docstring), so C naming a 'fixed fixture, not seeded' is not one of the C categories. c086/c094: Example 2.8 (L05.html lines 152-153) derives 4375/2 = 2187.5 and the 2188 rounding at the same parameters from Proposition 2.1. Values read only from lab output (c010, c011, c012, c014, c031, c049, c050, c087 numbers, c092) are correctly C and PASS. The grade is a claim about epistemic status; a C that understates a page-derived result is a grade defect.",
    "Regrade c043, c044, c086, c094 to T with the page derivation as basis (round-10 basis for c043/c044 was right: 'Example 1.5 (arithmetic on the page under Definition 1.1, with A1 and A2)'); in the same batch regrade the lesson key rows L03.html line 565 and L05.html line 486 (and the L05 key row for the 2188 rounding) to T, which the L03 and L05 builders own. Alternative only if the Architect rules that fixed-fixture and SIMULATED-parameter values are graded C naming the lab: amend BUILDER_RULES/plan §9 first, then keep C.")
row("cards-gates", "gates", "run_labs, page_smoke, check_dag, verify_refs --offline, check_pages on BK4", "PASS",
    "run_labs --unit BK4: PASS (8/8). check_pages --unit BK4: PASS. check_dag --unit BK4: PASS. page_smoke --unit BK4: PASS (alone). verify_refs --offline: 560 entries, 0 problems. ruff on tests/labs/BK4 and grader: not re-run this round (no Python file in this slice changed since round 10; carried from round 10).")

counts = {"PASS": sum(r["status"] == "PASS" for r in rows), "FAIL": sum(r["status"] == "FAIL" for r in rows), "UNVERIFIABLE": sum(r["status"] == "UNVERIFIABLE" for r in rows)}
frag = {
    "unit": "BK4",
    "slice": "BK4-d",
    "round": 11,
    "verifier": "Claude Haiku 5.5, independent verifier for BK4-d (ALL cards.json against L01-L05), round 11; did not build BK4",
    "pin": "11d7077a290f7960b183d3a5a6631af4773888f9 (detached; HEAD of the checkout)",
    "base": "00a84795 (round-10 pin). Delta: cards.json (c043, c044 grade T to C and basis); references/references.json (used_by, generated_at); project.html and grader/test_project.py (not card-cited). Lessons L01-L05, index, tests/labs/BK4, notation/, tools/ unchanged.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE11-BK4-d",
    "scratch": "/Users/billyribeiro/.fanout/scratch-BK4-d-r11 (L01-L05 stripped text, read in full)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL" if counts["FAIL"] or counts["UNVERIFIABLE"] else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "duffie2011central: live Crossref matched (title, container, 2011); registry record unchanged except used_by",
        "bisndbasel: cited at index level by L05 lesson text only; no card cites it; not re-fetched this round",
    ],
    "freshness_flags": [
        "Only cited work with a card: Duffie and Zhu (2011), question-level; no 2025-2026 literature checked for freshness",
    ],
    "notes": (
        "Slice d is cards.json only: no grader in this slice, so no mutants. Round-10 FAIL rows: cards-hypotheses (c083) is now PASS (A2 restored in the front); "
        "cards-grades-vs-keyresults is now PASS (card and key row agree on C); the grade category is the new FAIL in cards-grade-rule9. "
        "Judgment recorded: a C grade is for claims that depend on SIMULATED lab output (c010, c011, c012, c014, c031, c049, c050, c092 and the c087 values, whose "
        "formulas are not stated as numbers on the page); a value that Example 1.5, 1.6 or 2.8 computes on the page is T (c043, c044, c086, c094). "
        "c014 is accepted as C: its general claim is proved (Problem R3 on L01, the three-payment cycle with zero net debit) but its card answer is the Bank A figure from the lab. "
        "Not checked: lesson prose outside what cards cite (owned by the lesson slices, not re-verified row by row); project.html, the grader and the project labs (other slices); ruff and mypy on the whole repo; build_site --check; fetch_data --check; run_graders; mutate_graders; verify_refs live for bisndbasel; the Basel III operational-risk section (not cited by any card)."
    ),
    "summary": (
        f"BK4-d round 11: FAIL. {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, 0 UNVERIFIABLE. All 100 cards re-read in full against the current L01-L05; "
        "every card number recomputed independently (recheck_numbers.py: 0 failures after correcting two errors in the verifier's own script, a wrong defaulter DF and a malformed expression); lab twins run alone (exit 0) and their printed values match the cards; "
        "duplicate scan, xref and notation clean; c083 hypothesis omission fixed. FAIL: the c043/c044 regrade to C is not a rule-9 category (the values are derived on the page, Example 1.5 and 1.6), "
        "and c086/c094 are graded C for values Example 2.8 derives on the page. Fix: regrade these four to T and the matching L03 line 565 and L05 line 486 key rows to T."
    ),
}
assert frag["summary"]
with open("ledgers/BK4/BK4-d.json", "w", encoding="utf-8") as f:
    json.dump(frag, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("rows", len(rows), counts, frag["verdict"])
