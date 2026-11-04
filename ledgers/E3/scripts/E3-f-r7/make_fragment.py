import json, datetime
PIN = "9373ef398589097500ea849e30ff9da423b98943"
CARRY = "Carried from round 6 (course/modules/E/E3/L01.html, tests/labs/E3/lab-E3-L01-1.py and the L01 card objects cards.json c001-c017, c173 are byte-identical or JSON-identical since the previous pin 142ecfc): "
S = "ledgers/E3/scripts/E3-f-r7/"
rows = []
def add(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        r["fix"] = fix
    rows.append(r)

# ---- L01 carried (subject byte-identical) ----
for i in range(1, 18):
    add(f"E3f-E3-c{i:03d}", "2.7-cards", f"course/modules/E/E3/cards.json (E3-c{i:03d}, L01)", "PASS",
        CARRY + f"card E3-c{i:03d} object identical; L01 text unchanged. Round-6 evidence stands.")
add("E3f-E3-c173", "2.7-cards", "course/modules/E/E3/cards.json (E3-c173, L01)", "PASS",
    CARRY + "card E3-c173 object identical; L01 text unchanged.")
add("E3f-lesson-numbers-L01", "2.2-numbers", "course/modules/E/E3/L01.html (prose, misconceptions, problems, quiz, key results)", "PASS",
    CARRY + "L01.html byte-identical to 142ecfc; numbers re-read against tests/labs/E3/lab-E3-L01-1.py output (ledgers/E3/scripts/E3-f-r7/run_labs_L01.out).")
add("E3f-lab-L01", "2.5-labs", "course/modules/E/E3/L01.html lab-E3-L01-1; tests/labs/E3/lab-E3-L01-1.py", "PASS",
    "Re-run this round: tools/run_labs.py --unit E3 --page L01 -> 'run_labs E3: PASS (1/1)' (run_labs_L01.out). Twin byte-identical to 142ecfc (git diff --quiet). " + "Carried from round 6 for the subject; re-run evidence added.")

# ---- L02 cards, re-verified against the current L02 text ----
l02_cards = {
 "c018": "Assumption A2 (L02.html:73)",
 "c019": "Proposition 1.1 and proof (L02.html:88-96)",
 "c020": "Definition 1.2 (L02.html:99-101)",
 "c021": "Definition 1.2 last sentence (on this page the risk premium is the CE risk premium only)",
 "c022": "Proposition 1.3(a) and proof, Steps 1-3 (L02.html:103-124)",
 "c023": "Proposition 1.3(b) and proof, Step 3 (L02.html:103-124)",
 "c024": "Definition 2.1 (L02.html:143-145); near-duplicate with c178 judged distinct (question differs)",
 "c025": "Proposition 2.2 (L02.html:147-156)",
 "c026": "Example 2.3 (L02.html:158-161), values 1/(2w), 1/2, 0.005, 0.5",
 "c027": "Proposition 3.1 (L02.html:172-175)",
 "c028": "Remark 3.2 (L02.html:203-205)",
 "c029": "Misconception 1 (section 5), 900, 4.5 and 5.065835 CU",
 "c030": "Definition 2.1 and Example 2.3; units",
 "c031": "Misconception 3 (section 5, third misconception)",
 "c032": "Lab 1 Part A expected output (L02.html expected block): ce_cents 9493, premium_cents 507, r_A 0.005000, r_R 0.500000, 5.065835, 4.500000, 0.565835",
 "c033": "Lab 1 Part B expected output: 5.065835 at eps=1 and 4.500046 at eps=0.01; gaps_shrink_as_eps_falls True",
 "c034": "Section 4 bullet 1 (11.17 percent) and E2 solution; 0.565835/5.065835 = 0.111696 (rederive_f7.out)",
 "c035": "Lab 1 Part C expected output: linear_premium_cents 0 at 1.0, 0.5, 0.1; linear_premium_zero_at_three_scales True",
 "c159": "Remark 1.4 (L02.html:130) and Proposition 1.3 proof",
 "c161": "Lab 1 Part B interpretation and Remark 3.2",
 "c162": "Remark 1.4 last sentence (u'' >= 0 case not stated as a result)",
 "c174": "Assumption A5 (L02.html:167)",
}
for k, where in l02_cards.items():
    add(f"E3f-E3-{k}", "2.7-cards", f"course/modules/E/E3/cards.json (E3-{k}, L02)", "PASS",
        "Re-verified this round against the current L02.html: " + where + ". Card matches the lesson text; card numbers appear in L02 (ledgers/E3/scripts/E3-f-r7/card_dump_slice.txt).")

# ---- L03 cards ----
l03_cards = ["c036","c037","c038","c039","c040","c041","c043","c044","c045","c046","c047","c048","c049","c050","c051","c052","c053","c054","c055","c160","c168","c171","c175","c177"]
for k in l03_cards:
    extra = ""
    if k == "c055": extra = " Problem E2 (L03.html E2 solution) gives M=9/80000; rederive_f7.out."
    if k == "c054": extra = " Lab 1 printed values 11250.0000, 10000.0000, 8888.8889, 7337.6161 match rederive_f7.out."
    add(f"E3f-E3-{k}", "2.7-cards", f"course/modules/E/E3/cards.json (E3-{k}, L03)", "PASS",
        "Re-verified this round against the current L03.html text and Lab 1 output (run_labs_L03.out, twin_L03.out)." + extra)
# ---- L04 cards ----
l04_cards = ["c056","c057","c058","c059","c060","c061","c062","c063","c064","c065","c066","c067","c068","c070","c071","c072","c073","c074","c075","c076","c077","c167"]
for k in l04_cards:
    extra = ""
    if k in ("c073","c075","c076"): extra = " Counts: 2 of 8 equal-mean no-ranking pairs are 16 and 19 (sosd_per_pair_f7.out); FOSD 3/10/1/10 and 24 of 24; SOSD 3/2/1/2 and 8 of 8 (rederive_f7.out)."
    if k == "c071": extra = " Matches Problem R3 solution (L04.html R3)."
    add(f"E3f-E3-{k}", "2.7-cards", f"course/modules/E/E3/cards.json (E3-{k}, L04)", "PASS",
        "Re-verified this round against the current L04.html text and Lab 1 output (run_labs_L04.out, twin_L04.out)." + extra)
add("E3f-cards-slice-scan", "2.7-cards-duplicates", "course/modules/E/E3/cards.json (all 87 slice cards)", "PASS",
    "Scan of all 171 cards (dup_scan_f7.out): 0 duplicate ids, 0 duplicate normalised fronts or backs; highest-similarity slice pairs (c018/c174, c059/c167, c060/c065, c160/c171, c043/c051) ask different questions.")

# ---- c178: changed card ----
add("E3f-E3-c178", "2.7-cards-duplicates + 2.7-cards accuracy", "course/modules/E/E3/cards.json:1182 (E3-c178, L03)", "FAIL",
    "The round-6 duplicate of E3-c024 is resolved: the question is now different (c024 asks the definition, c178 asks a hypothesis), so no duplicate is left. The card still does not answer its question. The front asks 'Which hypothesis must u satisfy ... to be defined at every w > 0?', a necessity question. The back gives u twice differentiable on (0,inf) with u'(w) > 0 for every w > 0, which is the hypothesis of Definition 1.6 (L03.html:111-113), a sufficient condition and stronger than needed. r_A(w) = -u''(w)/u'(w) is defined wherever u is twice differentiable and u'(w) is nonzero (L02.html Definition 2.1, which says u'(w) != 0). Counterexample: u(w) = -w is twice differentiable with u' = -1 at every w, so r_A(w) = 0 is defined, yet u'(w) > 0 fails. Grade T with this wording is a wrong necessity claim.",
    fix="Replace the front with 'What hypothesis on u does Definition 1.6 impose?' and the back with 'u is twice differentiable on (0, infinity) with u'(w) > 0 for every w > 0 (Definition 1.6). That makes u'(w) nonzero at every w, so r_A(w) = -u''(w)/u'(w) and r_R(w) = w r_A(w) are defined there. The definition needs only u'(w) != 0 at each w (L02 Definition 2.1).' Keep grade T. Then run tools/check_pages.py --unit E3.")
add("E3f-cards-near-duplicates", "2.7-cards-duplicates", "course/modules/E/E3/cards.json (all 171 cards; slice cards L01-L04)", "PASS",
    "Exact check: 0 duplicate ids, 0 duplicate normalised fronts or backs (dup_scan_f7.out). Near-duplicate scan over all pairs with front similarity > 0.5 or back similarity > 0.6 (dup_scan_f7.out) reviewed for slice cards: c018/c174/c175 are different assumptions; c059/c167 are nondecreasing vs concave; c060/c065 are FOSD vs SOSD characterisations; c160/c171 are different Lab 1 checks; c043/c051 and c045/c048 ask different questions. c040/c177 share Proposition 1.4 and are judged distinct as in round 6. No row is a duplicate.")

# ---- cards integrity, numbers, xrefs, grades, coverage ----
add("E3f-coverage-cards", "2.7-cards-coverage", "course/modules/E/E3/cards.json (cards for L01-L04)", "PASS",
    "Re-run: 87 slice cards (L01 18, L02 22, L03 25, L04 22) by lesson; every lesson has cards (dup_scan/card dump in card_dump_slice.txt).")
add("E3f-cards-integrity", "2.7-cards-integrity", "course/modules/E/E3/cards.json (171 cards, all lessons)", "PASS",
    "JSON parses; 171 cards; 0 duplicate ids; each slice card has front, back, lesson in L01-L04 and an id of the form E3-cNNN (dup_scan_f7.out). Card ids c042, c069 and c176 are absent at both pins (no card cites them).")
add("E3f-cards-numbers", "2.7-cards-numbers", "course/modules/E/E3/cards.json slice cards vs L01-L04.html", "PASS",
    "Every number on a slice card re-derived or read against the lesson: rederive_f7.out (CE 94.934165, premium 5.065835, 9493/507 cents, 4.500000, 0.565835, 11.17 percent, ratios 5.065835..4.500046; CE 11250/10932/10616/10000/8889/7338 cents, 80000/9; I values 500/1000/2000 and 250/500/1250/2000; FOSD/SOSD counts).")
add("E3f-cards-xrefs", "2.7-cards-refs", "course/modules/E/E3/cards.json labelled references in the slice", "PASS",
    "Each labelled reference resolves in its named lesson: L02 Definition 2.1, Proposition 1.3, Proposition 2.2, Example 2.3, Proposition 3.1, Remark 3.2, Remark 1.4, Problem R1/R2/R3, Section 3/4/5 and misconceptions; L03 Definitions 1.1, 1.3, 1.6, 2.3, Propositions 1.2, 1.4, 1.7, 2.4, 2.6, 2.7, Theorem 2.1, Remarks 2.2, 2.8, Examples 1.5, 2.5, Problems E2, R3, section 4; L04 Definitions 1.1, 1.3, 1.4, 2.1, Lemmas 1.2, 1.6, 2.2, Theorems 1.5, 2.3, Proposition 1.8, Examples 1.7, 2.5, Remark 2.4, Problems R3, section 3/4; L01 Proposition 3.3, Definition 3.2 (L01.html:147, card c006). Read against the current texts.")
add("E3f-cards-grades", "2.7-cards-grades", "course/modules/E/E3/cards.json grade and basis fields for the slice", "PASS",
    "Every C-graded slice card (c032, c033, c034, c035, c054, c073, c075, c076, c160, c161, c171) has a basis naming Lab 1 or a part; T cards are proved on the page (c178 grade T wording is FAIL above). Cards without a grade are definitions or statements of assumptions.")

# ---- lessons ----
add("E3f-lesson-numbers-L02", "2.2-numbers", "course/modules/E/E3/L02.html (Example 1.5, Example 2.3, Lab 1 prose, Section 4, E1-E3, misconceptions, M1-M3, P1-P3, R1-R3, quiz)", "PASS",
    "Recomputed in rederive_f7.py/out: E sqrt(W) 9.743416, CE 94.934165 (9493.4165 cents -> 9493), premium 5.065835 (506.5835 -> 507), approximation 4.5, error 0.565835 = 11.1696 percent of exact premium (11.17) and 12.5741 percent of approximation (12.57); Part B ratios 5.065835, 4.619495, 4.528811, 4.504565, 4.500046; E1 gap 0.004565 < 0.005 and factor 6.31 vs 6.25; M1 CE 9, premium 1; M2 r_A=1/w; M3 r_A=a; new Problem P2 claim: CE=E W=100 for all scales with outcomes in (0,inf). All match the text.")
add("E3f-lesson-numbers-L03", "2.2-numbers", "course/modules/E/E3/L03.html (Lab 1 prose, Example 2.5, M1-M3, E1-E3, misconceptions, R1-R3, quiz)", "PASS",
    "Recomputed (rederive_f7.out): CE 11250, 10931.7733, 10615.8009, 10000, 8888.8889, 7337.6161; 80000/9 = 8888.888...; Example 2.5 CE 1600 and 2000; M1 r_A(4)=1/8; M2 CE=3000 (expected 7000); M3 CE(3X)=9000; E2 M=9/80000; E3 (k+1)/2=5.5; R1 limit argument; quiz 3000.")
add("E3f-lesson-numbers-L04", "2.2-numbers", "course/modules/E/E3/L04.html (Examples 1.7, 2.5, 2.6; M1-M3; E1-E3; Lab 1 interpretation; quiz)", "PASS",
    "Recomputed (rederive_f7.out): Example 2.5 I_X = 0,0,500,1000,2000 and I_Y = 0,250,500,1250,2000 at 1000..5000; F values; Example 2.6 I_Y <= I_X; Example 1.7 F; M1 means 2500 and 2000; counts FOSD 3/10/1/10 (24), SOSD 3/2/1/2 (8); interpretation '24+8=32, 3+2=5, total 37, all agree' matches the lab output (run_labs_L04.out).")

# ---- lab L02, L03, L04 ----
add("E3f-lab-L02", "2.5-labs", "course/modules/E/E3/L02.html lab-E3-L02-1; tests/labs/E3/lab-E3-L02-1.py", "PASS",
    "run_labs --page L02 -> PASS (run_labs_L02.out); twin run under python -I -W error with no stderr (twin_L02.out, twin_L02.err empty); expected block equals output; hypothesis numbers 4.5 and 1800 re-derived. Interpretation 'Problem P2 gives a zero premium' consistent with P2 (CE = E X for outcomes in (0,inf)).")
add("E3f-lab-L03", "2.5-labs", "course/modules/E/E3/L03.html lab-E3-L03-1; tests/labs/E3/lab-E3-L03-1.py", "PASS",
    "run_labs --page L03 -> PASS (run_labs_L03.out); twin output equals expected block (twin_L03.out); hypothesis values 11250, 10000, 80000/9 -> 8889 re-derived in rederive_f7.out.")
add("E3f-lab-L04", "2.5-labs", "course/modules/E/E3/L04.html lab-E3-L04-1; tests/labs/E3/lab-E3-L04-1.py", "PASS",
    "run_labs --page L04 -> PASS (run_labs_L04.out); twin output equals expected block (twin_L04.out); named-pair and seeded-pair counts reproduced by an independent implementation (rederive_f7.out, sosd_per_pair_f7.out): FOSD 3/10/1/10, SOSD 3/2/1/2, pairs 16 and 19 are the SOSD no-ranking pairs.")

# ---- DAG ----
add("E3f-dag-L02-crra-forward-use", "2.9-define-before-use", "course/modules/E/E3/L02.html (Example 2.3, M2 solution, all of L02)", "PASS",
    "Re-read this round: L02.html contains no reference to CRRA, gamma or L03 content except the next-lesson navigation link (L02.html:623). Example 2.3 and the M2 solution use F6 and Proposition 2.2 only. check_dag.py --unit E3 PASS (check_dag_E3.out).")
add("E3f-dag-other-links", "2.9-define-before-use", "course/modules/E/E3/L01.html..L04.html data-concept links and <dfn> tags", "PASS",
    "check_dag.py --unit E3 PASS. L04 links only to L01 (expected-utility), L03 (crra-utility) and M4 concept anchors; L03 links to M1 (exponential-and-logarithm) and M2 (derivative) inside the closure. L04 'mean-preserving spread' (Example 2.5) is plain prose; no curriculum concept of that name exists (curriculum/curriculum.json grep). L02 and L03 'convex' do not occur except as plain prose in L01 (architect default).")

# ---- notation ----
add("E3f-notation", "2.13-notation", "course/modules/E/E3/L02.html:209 (Lab 1 hypothesis paragraph, '\\tfrac12 r_A(100)\\,\\mathrm{Var}(X)'); L01-L04 math vs notation/notation.json", "FAIL",
    "Registry check of the four lessons: no use of registered symbols with another meaning (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q are absent; gamma is the local CRRA coefficient; the registered \\E, \\Prob, \\Var, \\R, \\indic macros are used). One deviation from the macro rule: L02.html:209 writes the variance as the raw \\mathrm{Var}(X), while the registered macro \\Var is used on the other lines of L02 (grep -c '\\\\Var' = 11 lines) and BUILDER_RULES 3.1 and the plan 4 table say to use the macros. Same meaning, so no registry clash, but a macro-form violation.",
    fix="In course/modules/E/E3/L02.html line 209 replace \\mathrm{Var}(X) with \\Var(X). Then run tools/check_pages.py --unit E3.")

# ---- banned / process / hours ----
add("E3f-banned-and-process", "1.3-1.4-banned", "course/modules/E/E3/L01.html..L04.html and slice cards", "PASS",
    "check_pages.py --unit E3: PASS (check_pages_E3.out; BANNED patterns and process words); grep for builder, verifier, planner, architect, round N, TODO, placeholder in the four lessons and cards: no hits.")
add("E3f-hours", "2.12-hours", "course/modules/E/E3/L01.html..L04.html data-hours; index.html", "PASS",
    "All eight lesson pages data-hours=7 (grep); 8 x 7 = 56 equals the hub split recorded in the plan; check_pages.py PASS (hours arithmetic). index.html byte-identical to 142ecfc.")

# ---- delta and commands ----
add("E3f-delta", "0-delta", "git diff 142ecfc..9373ef3 for course/modules/E/E3 (slice files L01-L04, cards.json)", "PASS",
    "Delta in the slice: L02.html (A4 wording, Lab 1 interpretation and misconception 1 wording, references paragraph), L03.html (references paragraph), L04.html (why-it-matters, Example 2.5 title and body, Lab 1 interpretation, Section 2 solution E3), cards.json (c178 new card; c121, c131 outside the slice). L01.html and the four lab twins are byte-identical. Every hunk read (git diff output in this round).")
add("E3f-E3-r7-independent-rederivation", "2.2-numbers (independent)", "ledgers/E3/scripts/E3-f-r7/rederive_f7.py", "PASS",
    "Own script (Decimal 50 digits, Fraction, separate implementation of the seeded draws): output rederive_f7.out agrees with every number in the four lessons and cards, and with run_labs/twin outputs.")
add("E3f-cmd-check_pages", "check_pages.py --unit E3", "course/modules/E/E3/index.html, L01-L04 (and L05-L08 pages as part of unit)", "PASS", "tools/check_pages.py --unit E3: 'check_pages E3: PASS', rc 0 (check_pages_E3.out).")
add("E3f-cmd-check_dag", "check_dag.py --unit E3", "course/modules/E/E3/*.html", "PASS", "tools/check_dag.py --unit E3: 'check_dag E3: PASS', rc 0 (check_dag_E3.out).")
add("E3f-cmd-check_projects", "check_projects.py --unit E3", "course/modules/E/E3/project.html", "PASS", "tools/check_projects.py --unit E3: PASS, rc 0 (check_projects_E3.out). project.html is not in this slice.")
add("E3f-cmd-page_smoke", "page_smoke.py --unit E3 --pages L01 L02 L03 L04", "course/modules/E/E3/L01.html..L04.html", "PASS", "Chromium page smoke: 'page_smoke E3: PASS' rc 0 (page_smoke_L01-L04.out; labs boot and run).")
add("E3f-cmd-run_labs-L01-L04", "run_labs.py --unit E3 --page L0n", "tests/labs/E3/lab-E3-L01-1..L04-1.py", "PASS", "run_labs E3 PASS (1/1) for each of L01-L04 (run_labs_L0*.out); run_labs runs each twin under python -I -W error; I also ran the L02, L03 and L04 twins by hand with the same flags and empty stderr (twin_L02.out, twin_L03.out, twin_L04.out).")
add("E3f-cmd-pytest-labs", "pytest tests/test_labs.py -k E3", "tests/labs/E3/", "PASS", "pytest -q tests/test_labs.py -k E3: all tests passed, rc 0 (pytest_labs_E3.out).")
add("E3f-cmd-ruff-labs", "ruff check tests/labs/E3", "tests/labs/E3/lab-E3-L01-1.py..L04-1.py", "PASS", "ruff check tests/labs/E3: rc 0 (ruff_E3_twins.out).")
add("E3f-cmd-mypy-twins", "mypy --no-incremental on the four L01-L04 twins", "tests/labs/E3/lab-E3-L01-1.py..L04-1.py", "PASS", "mypy --no-incremental: 'Success: no issues found in 4 source files', rc 0 (mypy_E3_twins.out).")
add("E3f-cmd-verify_refs", "verify_refs.py --offline", "references/references.json (key pratt1964risk)", "PASS", "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', rc 0 (verify_refs_offline.out). references/ byte-identical since 142ecfc. Live Crossref run not repeated (not needed: no reference record changed).")

# ---- references paragraphs ----
add("E3f-references", "2.4-attributions", "course/modules/E/E3/L02.html:616 (References paragraph, registry key pratt1964risk)", "PASS",
    "Round-6 FAIL fix applied: the paragraph now reads 'Registry keys cited on this page: pratt1964risk, the registry entry for Pratt, Risk Aversion in the Small and in the Large, Econometrica (1964). This lesson names that work for the name only, and it attributes no passage, page or result to it.' references.json record pratt1964risk: title 'Risk Aversion in the Small and in the Large', container Econometrica, year 1964 (matches). The key is cited by the same convention as E2 L01 (L01 references paragraph, registry keys in code, no data-cite), so no structural change is required. No passage is attributed.")
add("E3f-L03-references", "2.4-attributions", "course/modules/E/E3/L03.html:564 (References paragraph, Module M1 Lesson 3 results)", "FAIL",
    "The paragraph enumerates the M1 Lesson 3 results that section 1 and section 2 cite: 'its Propositions 1.4 and 1.6(b), and its addition rule, which is that lesson's A2'. Section 2 also cites M1 Lesson 3 A3 (the uniqueness in A3, the defining property of the logarithm): Proposition 2.4's proof reads 'by Module M1, Lesson 3, Proposition 1.4 and the uniqueness in its A3' (L03.html Proposition 2.4 proof). M1 L03.html:56-61 states A3 (for every y > 0 there is exactly one real x with e^x = y). The enumeration omits a cited result.",
    fix="In course/modules/E/E3/L03.html References paragraph, after 'its addition rule, which is that lesson's A2' add 'and the uniqueness in its A3, which Proposition 2.4 uses' (keep the rest). Then run tools/check_pages.py --unit E3.")

fragment = {
    "unit": "E3",
    "slice": "f",
    "round": 7,
    "verifier": "Haiku independent verifier, E3-f round 7 (did not build E3)",
    "pin": PIN + " (9373ef3, detached)",
    "base": "142ecfc (round-6 pin; frags/D-E3-f.round6.json). Delta 142ecfc..9373ef3 touches the slice in L02.html (A4 wording, Lab 1 interpretation and misconception 1, references), L03.html (references paragraph), L04.html (why-it-matters, Example 2.5, Lab 1 interpretation, Section 2 solution), cards.json (E3-c178 changed; c121 and c131 are outside the slice). L01.html, the four slice twins, index.html and references/ are byte-identical.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD7-E3-f (detached at 9373ef3; .venv symlinked)",
    "scratch": "ledgers/E3/scripts/E3-f-r7/",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": [r for r in rows if r is not None],
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Mutants: not required. The slice is lessons and cards (ruling: lab twins are demonstrations; mutation testing applies to project graders only). No mutants were written, so mutants is empty.",
        "Observation (not a row): L02 Section 3 and the Lab 1 prose write the risk premium as \\pi(\\varepsilon) (about 14 uses). Plan section 4 says write the premium as a word or \\pi_{\\mathrm{rp}} and that \\pi is not registered. No registry symbol is reused, so no row; the architect may want the plan rule applied.",
        "Observation (not a row): 'mean-preserving spread' (L04 Example 2.5) is used as plain prose and is defined in the same sentence by construction. No curriculum concept of that name exists, so there is no DAG issue.",
        "Observation (not a row): 'convex' appears only as plain prose (L01 and the L04 quiz option), allowed by the architect default for concepts outside the closure.",
        "Observation (not a row): E3-c040 and E3-c177 both rest on Proposition 1.4 (the limit to ln w). Their questions differ (limit versus whether the log is a separate case), so they are kept as distinct, as in round 6.",
        "Observation (not a row): the E3-c178 back restates the Arrow-Pratt formulas of E3-c024. The question now differs, so this is not a duplicate; the fix above keeps it that way.",
        "Observation (not a row): the card id gaps c042, c069 and c176 are absent at both pins and cited by nothing in the slice.",
        "Not checked: the full gate (no push or merge, per the workflow); live Crossref verify_refs (references/ unchanged); ruff and mypy for the whole repo (only the four E3 twins were in scope); L05 to L08 and project.html (other slices); the browser-based theme screenshots (page_smoke covers the console and rendering checks it defines).",
    ],
    "summary": "E3 slice f, round 7 (lessons L01-L04 and cards for L01-L04). Verdict FAIL with three non-PASS rows: E3f-E3-c178 (card answers a necessity question with a sufficient hypothesis), E3f-L03-references (omits M1 Lesson 3 A3 uniqueness that Prop 2.4 cites), E3f-notation (L02.html:209 raw \\mathrm{Var} where the registered \\Var macro is the rule). The round-6 duplicate finding on c178 is resolved (the question now differs from c024), the L02 Pratt reference now carries the registry key in the E2 form, and no near-duplicate remains; the replacement c178 itself fails for accuracy (see E3f-E3-c178). All arithmetic, lab outputs and the L02-L04 delta hunks were re-derived independently.",
}
print(len(rows), sum(1 for r in rows if r["status"] == "PASS"), sum(1 for r in rows if r["status"] != "PASS"))
json.dump(fragment, open("ledgers/E3/E3-f.json", "w"), indent=2, ensure_ascii=False)
open("ledgers/E3/E3-f.json", "a").write("\n")
