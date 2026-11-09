import json
C = "Carried from round 4 (carried subject byte-identical since edbb7aa8): "
F = "Fresh in round 5 (dde0486b): "
R5 = "ledgers/M5/scripts/M5-a-r5/"
rows = []
def row(id_, check, location, evidence, status="PASS"):
    rows.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence})

# ---- hub (index.html byte-identical since edbb7aa8)
row("A1-hub-structure", "2.9 structure", "course/modules/M/M5/index.html:1-174",
    C + "index.html unchanged (git diff --quiet edbb7aa8 dde0486b). " + R5 + "r5_check_pages_M5.out 'check_pages M5: PASS'.")
row("A1-hub-hours", "2.9 hours arithmetic", "index.html:29, 31, 42; L01-L10 data-hours",
    C + "index.html:29 data-hours-lessons=104, data-hours-project=26 (130 h; 26/130=20%). Fresh grep at dde0486b: data-hours L01-L06=10, L07-L10=11, 6*10+4*11=104 (matches index.html:131 text). No data-hours line lies in a delta hunk.")
row("A1-hub-objectives", "2.9 objectives", "index.html:45-56",
    F + "index.html unchanged. Block titles re-grepped at dde0486b for every objective: L01 Theorem 1.2 (L01.html:67) and Corollary 1.4 (:97); L02 unchanged; L03 Proposition 1.4 and 3.1 (L03.html:80, 203); L04 metric axioms (L04.html:59) and Proposition 2.1 (:243); L05 Proposition 2.1 (:180); L07 Theorem 2.1 and Corollary 3.2 (L07.html:99, 181); L08 Theorem 2.2 (:101); L09 Theorem 2.4 (:116); L10 Corollary 3.2 (:136). All present.")
row("A1-hub-prereqs", "2.9 prerequisites and concept links", "index.html:58-67; course/concepts.html anchors",
    C + "index.html unchanged; course/concepts.html regenerated output identical (" + R5 + "r5_build_site_check.out 'site data current: 6 outputs').")
row("A1-hub-placement-structure", "2.9 placement diagnostic", "index.html:69-127",
    C + "index.html unchanged; data-mastery=0.8 and nine items (ledgers/M5/scripts/M5-a-r3/recompute_a_r3.out).")
row("A1-hub-placement-answers", "2.2 numbers in prose and answer keys", "index.html:73-124",
    C + "index.html unchanged; 71 answer-key recomputations PASS (ledgers/M5/scripts/M5-a-r3/recompute_a_r3.out).")
row("A1-hub-placement-rung1-skill", "5.1 placement item tests rung-1 skill", "index.html:116-119; course/modules/M/M5/project.html:44, 113-114",
    C + "index.html unchanged. project.html delta hunks (git diff -U0 edbb7aa8 dde0486b) are at 142, 215, 289, 294-296, 373, 411: none touches lines 44 or 113-114, so the cited locators still hold.")
row("A1-hub-placement-rung2-skill", "5.1 placement item tests rung-2 skill", "index.html:121-124; project.html:45",
    C + "index.html unchanged; project.html:45 not in any delta hunk.")
row("A1-hub-lesson-map", "2.9 lesson map and card text", "index.html:129-144",
    F + "index.html unchanged. Lesson-map card claims re-grepped at dde0486b: L01 (L01.html:67, 82, 128), L02 unchanged, L03 (L03.html:172, 203), L04 (L04.html:59, 213, 243, 265 — none is a delta hunk line), L07 Theorem 2.1/Corollary 3.2, L08 Theorem 2.2, L09 Theorem 2.4, L10 Corollary 3.2 present.")
row("A1-hub-ladder", "2.9 ladder and rung titles", "index.html:146-155; project.html:44-47",
    C + "index.html unchanged; project.html:44-47 not in any delta hunk.")
row("A1-hub-data-status", "2.8/2.9 data status", "index.html:157-160; L08.html:138; L09.html:132; L10.html:177",
    F + "grep at dde0486b: 'data-files' count 0 in index, L01-L04; SIMULATED label at L08.html:138, L09.html:132, L10.html:177 (lines not in any delta hunk); currency grep (dollar|USD|EUR|cents) 0 matches in index and L01-L04.")
row("A1-hub-reading", "2.1 citations and reading list", "index.html:162-169; references/references.json; tools/verify_refs.py",
    C + "index.html, references/, tools/, course/modules/M/M1 unchanged in the delta (git diff --quiet). See A1-gate-verify-refs.")

# ---- L01
row("A1-L01-structure", "2.9 structure and template order", "course/modules/M/M5/L01.html:1-495",
    F + "The only L01 hunk is line 62 (one paragraph sentence added); no section, block or ordering changed. " + R5 + "r5_check_pages_M5.out PASS.")
row("A1-L01-math", "2.4 mathematics: theorems, proofs, notation", "L01.html:55-137, 233-245; hunk at L01.html:62",
    F + "Hunk at line 62 checked: 'The one exception is the irrationality of sqrt(2), which section 4, section 5 and Problem R2 cite from M1 (Lesson 2, Corollary 2.6) and do not reprove.' Cited places verified: L01.html:254 (canon break 1, cites M1 Corollary 2.6), :273 (misconception 3, cites M1 Corollary 2.6), :370 (R2, cites M1 Lesson 2 Corollary 2.6); M1 L02.html:132-133 states Corollary 2.6 (no rational number has square 2). Proofs of Thm 1.2, 1.3, 1.6, Prop 1.7 and Lemma 1.5 unchanged and re-read.")
row("A1-L01-numbers", "2.2 numbers in prose and lab output", "L01.html:146, 213-230, 338, 345, 352, 425, 439, 444, 456",
    C + "L01.html changed only at line 62; cited lines unchanged. Lab twin unchanged; " + R5 + "r5_lab_expected_vs_twin.out L01 expected==twin True.")
row("A1-L01-problems", "2.4/2.9 problem set with worked solutions", "L01.html:278-381",
    C + "L01.html:278-381 not in any delta hunk.")
row("A1-L01-quiz-keyresults", "2.9 quiz keys and key-results table", "L01.html:383-399, 400-480",
    C + "L01.html:383-480 not in any delta hunk. Note (LOW, not a row failure): the L01q7 explanation at L01.html:453 uses the irrationality of sqrt(2) without repeating the M1 citation; it points to 'the first canon break' (L01.html:254), which cites M1, so the chain is cited.")
row("A1-lab-L01-1", "2.5 lab: run, twin, page equals twin, expected equals output", "tests/labs/M5/lab-M5-L01-1.py; L01.html:144-231",
    F + R5 + "r5_lab_expected_vs_twin.out: L01 page_code==twin True, expected==twin_stdout True (17 output lines); r5_twin_L01.exit 0, r5_twin_L01.err 0 bytes under python -I -W error; r5_run_labs_L01.out 'run_labs M5: PASS (1/1)'.")

# ---- L02 (byte-identical since edbb7aa8)
row("A1-L02-structure", "2.9 structure and template order", "course/modules/M/M5/L02.html:1-548",
    C + "L02.html and its twin unchanged in the delta. " + R5 + "r5_check_pages_M5.out PASS.")
row("A1-L02-math", "2.4 mathematics: hypotheses, proofs, grades", "L02.html:145-147, 170-181, 308-311",
    C + "L02.html unchanged; round-4 fix (Proposition 3.3 has only H1) still in place (L02.html:172-174).")
row("A1-L02-numbers", "2.2 numbers in prose and lab output", "L02.html:213, 286-292, 293, 382-400, 449-536",
    C + "L02.html unchanged; " + R5 + "r5_lab_expected_vs_twin.out L02 expected==twin True.")
row("A1-L02-problems", "2.4/2.9 problem set with worked solutions", "L02.html:324-427",
    C + "L02.html unchanged.")
row("A1-L02-quiz-keyresults", "2.9 quiz keys and key-results table", "L02.html:429-446, 448-536",
    C + "L02.html unchanged.")
row("A1-lab-L02-1", "2.5 lab: run, twin, page equals twin, expected equals output", "tests/labs/M5/lab-M5-L02-1.py; L02.html:211-294",
    F + R5 + "r5_lab_expected_vs_twin.out L02 page_code==twin True, expected==twin_stdout True (7 lines); r5_twin_L02.exit 0, .err 0 bytes; r5_run_labs_L02.out PASS (1/1).")
row("A1-L02-attribution", "2.1/2.4 attribution of the cited M1 result", "L02.html:540; L02.html:300; L02.html:423",
    C + "L02.html unchanged; M1 unchanged (M1 L02.html:132-133 Corollary 2.6).")

# ---- L03
row("A1-L03-structure", "2.9 structure and template order", "course/modules/M/M5/L03.html:1-460",
    F + "The only L03 hunk is line 237 (one misconception paragraph); structure unchanged. " + R5 + "r5_check_pages_M5.out PASS.")
row("A1-L03-math", "2.4 mathematics", "L03.html:57-93, 171-196, 202-213",
    C + "Cited ranges unchanged (the only L03 hunk is line 237, outside them). Misconception hunk covered by A1-L03-misconception-3.")
row("A1-L03-misconception-3", "2.4 mathematics: changed misconception 3 counterexample", "course/modules/M/M5/L03.html:237",
    F + "New text: 'y_n = 2/(2n+1) ... 0 < y_n <= 1/n, so |y_n| < eps once n > 1/eps (Lesson 1, Theorem 1.2)' correct; 'y_n is not of the form 1/k (that would need 2k = 2n+1, an even number equal to an odd one)' correct (2/(2n+1)=1/k iff 2k=2n+1, impossible by parity); hence f(y_n)=1 for all n, f(0)=0, so f is not continuous at 0 by Proposition 2.1 (L03.html:172). f(x_n)=0 for x_n=1/n is correct. Card M5-c046 agrees with this text.")
row("A1-L03-numbers", "2.2 numbers in prose and lab output", "L03.html:108, 161-165, 166, 298-320",
    C + "Cited ranges unchanged. " + R5 + "r5_lab_expected_vs_twin.out L03 expected==twin True; expected block (L03.html:161-165) reads 401 of 401, 7, 7 of 7, 381/200, 14839/40000, 29.")
row("A1-L03-problems", "2.4/2.9 problem set with worked solutions", "L03.html:242-346",
    C + "Cited range unchanged (E2 seven points, R2 grid check, E3 count re-read).")
row("A1-L03-quiz-keyresults", "2.9 quiz keys and key-results table", "L03.html:347-363, 364-444",
    C + "Cited range unchanged; quiz explanation at L03.html:412 still names the third misconception, which is the one changed.")
row("A1-lab-L03-1", "2.5 lab: run, twin, page equals twin, expected equals output", "tests/labs/M5/lab-M5-L03-1.py; L03.html:106-168",
    F + R5 + "r5_lab_expected_vs_twin.out L03 page_code==twin True, expected==twin_stdout True (5 lines); r5_twin_L03.exit 0, .err 0 bytes; r5_run_labs_L03.out PASS (1/1).")

# ---- L04 (changed; fully re-read this round)
row("A1-L04-structure", "2.9 structure and template order", "course/modules/M/M5/L04.html:1-480",
    F + "Read in full at dde0486b (480 lines). Changes are word-level and single-line (lines 56, 80, 240, 246, 249, 296); section, block and quiz order unchanged. " + R5 + "r5_check_pages_M5.out PASS.")
row("A1-L04-math", "2.4 mathematics: theorems, proofs, hypotheses", "L04.html:56 (F1-F6), 78-95 (Prop 1.4), 221-236 (Prop 1.7), 240-250 (Prop 2.1), 257-297 (Prop 3.3, 3.4, Ex 3.6), 301-336",
    F + "Prop 1.4 hypothesis (3) = F1, and F1 is used: |u.v| <= |u||v| and |u+v| <= |u|+|v| are obtained from squares via F1 (L04.html:91-95). Prop 3.3 is L04's own (L04.html:270-276), so Ex 3.6's 'Proposition 3.3' citation is correct. Ex 3.6 chain re-derived: |x| <= |x-1/n|+|1/n| (F4), t_n -> 0 by F5 and Definition 3.1, F6 gives |x|=0, so x=0 not in (0,1]. Prop 2.1 proof with '<' now escaped (L04.html:249) is correct. Misconceptions 1-3 (L04.html:334-336) and canon breaks (L04.html:325-328) re-derived. Mechanics 2 six ordered triangle cases re-checked. Research 1 psi monotone and subadditive re-derived. No defect.")
row("A1-L04-numbers", "2.2 numbers in prose and lab output", "L04.html:105, 198-208, 209, 340-372, 393-464",
    F + R5 + "r5_lab_expected_vs_twin.out L04 expected==twin True (11 lines). Prose numbers re-derived: squared-distance failures at (0,1,2) and (2,1,0) (Empirical 2), 27 vectors and 27^3=19683 triples (Empirical 3), 25^3=15625 (Empirical 1), d2((1,2),(4,-2))=5, d_inf(x,x^2)=1/4 (Mechanics 3).")
row("A1-L04-problems", "2.4/2.9 problem set with worked solutions", "L04.html:340-372",
    F + "All twelve problems read at dde0486b; solutions re-derived (Mechanics 1-3, Proof 1-3, Empirical 1-3, Research 1-3). No defect.")
row("A1-L04-quiz-keyresults", "2.9 quiz keys and key-results table", "L04.html:376-391 (key results), 393-464 (quiz)",
    F + "Quiz L04q1-L04q9 keys and explanations re-checked against lesson text (L04q5 options and explanation at L04.html:425-429 verified: (0,0,1), (0,1,0), (0,1,1) give 1<=1, 0<=2, 1<=1). Key results rows grade T and point to proofs on the page.")
row("A1-lab-L04-1", "2.5 lab: run, twin, page equals twin, expected equals output", "tests/labs/M5/lab-M5-L04-1.py; L04.html:103-210",
    F + R5 + "r5_lab_expected_vs_twin.out L04 page_code==twin True, expected==twin_stdout True; r5_twin_L04.exit 0, .err 0 bytes; r5_run_labs_L04.out PASS (1/1).")
row("A1-L04-render-raw-less-than", "2.9 rendering: raw less-than characters that hide text", "course/modules/M/M5/L04.html:56, :240, :249 (round-4 FAIL)",
    F + "Round-4 FAIL is fixed. " + R5 + "raw_lt_scan2.py on dde0486b: every '<' followed by a letter in index, L01, L02, L03, L04 is a complete tag (0 offending, r5_raw_lt_scan2.out). Detector run on the edbb7aa8 L04 (ledgers/M5/scripts/M5-a-r5/L04_edbb7aa8.html) reports exactly the three offenders at lines 56, 240, 249, so the detector is live. The three sites now read '&lt;' (L04.html:56 'c&lt;c', :240 'd(x,y)&lt;r', :249 'd(x,y)&lt;r'). " + R5 + "raw_lt_scan.py: unknown tag names 0 on all five pages.")

# ---- cards
row("A1-cards-L01", "2.9 cards: L01 cards agree with the lesson", "course/modules/M/M5/cards.json: M5-c001-c016, c191, c216",
    F + "All 18 L01 cards read (r5_cards_L01_L04.txt). No L01 card text changed in the delta. Numbers checked: c010 bracket [181/128, 2897/2048] and width 1/2048 (twin output), c011 width 1/1024 at step 11 (2/2^n), c012 13 of 13, c013 canon break 1, c016 Misconception 3.")
row("A1-cards-L02", "2.9 cards: L02 cards agree with the lesson", "course/modules/M/M5/cards.json: M5-c017-c034, c213, c214, c217",
    F + "All 21 L02 cards read. c026 matches the round-4 fix (Proposition 3.3 hypothesis H_n only; L02.html:172). c028 Proposition 3.5 threshold 10 (sup of G_m-G_n over m>n>=N is 1/2^N); c032 200 of 200; c033 first index 10; c034 1830 pairs = C(61,2); c217 minimum gap 1/2 at N=1 (lab output). No defect.")
row("A1-cards-L03", "2.9 cards: L03 cards agree with the lesson", "course/modules/M/M5/cards.json: M5-c035-c049, c218, c219",
    F + "All 17 L03 cards read. c046 matches the changed misconception 3 (L03.html:237). c047 seven points; c048 29 (expected block L03.html:165); c049 401 points (L03.html:161); c218 seven of seven; c219 first failing grid point 381/200 (L03.html:164). No defect.")
row("A1-cards-L04", "2.9 cards: L04 cards agree with the CURRENT lesson text", "course/modules/M/M5/cards.json: M5-c050..c068, c190, c192, c193, c201, c215, c220",
    F + "All 24 L04 cards read. Changed: c055 (Proposition 1.4 hypothesis (3) = F1, matches L04.html:80); c064 (R and R^2 Cauchy convergence, Proposition 3.4 at L04.html:280, Misconception 2 at :335) correct; c067 removed (lab Part C card, no defect in removal; the printed values remain in the lab and in L04.html:208). Other cards (c061 Example 3.6, c062 Section 5 canon break 1, c065 Misconception 3, c066 15625, c068 19683, c190 Example 1.6, c192 Problem Proof 1, c220 zero failures) match the lesson. No duplicates.")
row("A1-cards-duplicates", "2.9 cards: no duplicate cards", "course/modules/M/M5/cards.json (233 cards, all lessons)",
    F + "233 cards (round 4 counted 235; the delta removed c067, c175, c222, c229 in other lessons and added c242, c243). Duplicate fronts 0, duplicate backs 0, no card with an empty lesson, front or back (checked with json.load under python -I).")

# ---- DAG, notation, wording, figures
row("A1-dag-concepts", "2.9 DAG: concepts outside the prerequisite closure", "check_dag M5; L01.html:59, L02.html:81, L03.html:59, L04.html:39; index.html:62-64",
    F + R5 + "r5_check_dag_M5.out 'check_dag M5: PASS' exit 0. The delta adds no concept link; new text cites only M1 (prerequisite), L01 Definition 1.1, L02 Theorem 2.5, L02 Problem P2 and L04's own F1-F6.")
row("A1-notation", "2.4 notation registry", "notation/notation.json; L01-L04.html; index.html",
    F + "Registry lists 8 program-wide symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) and macros. grep of index and L01-L04 for these tokens: none used. Changed text uses only registered macros (\\R, \\N) and local letters, which the registry says are local (notation.json 'about').")
row("A1-banned-phrases", "2.9 process words in learner text", "index.html; L01-L04.html; cards.json",
    F + "grep (round, verif, audit, builder, fix, ledger, previous, changed, revis, now, we, I, todo, tbd, draft, slice, reviewer, finding) over every added line of L01, L03, L04 and cards.json: 0 matches in slice text ('fixed point' in L08/L10 cards is a mathematical term outside the slice).")
row("A1-scope-words", "2.4 scope words without computation", "L01.html:62; L04.html:56, 80, 296; L03.html:237",
    F + "'The one exception' (L01.html:62) checked against every use of sqrt(2) irrationality in L01 (see A1-L01-math). L04.html:80 and :296 state their hypotheses (F1; F4-F6) explicitly. L03.html:237 states its computation. No unsupported 'every/all/only' claim found in changed sentences.")
row("A1-figures", "2.9 figures in the slice", "index.html; L01-L04.html",
    F + "Zero svg, figure, canvas or data-figure tokens in any L01/L03/L04 delta line (grep -c = 0); index and L02 unchanged; no figures-*.js in the delta.")

# ---- gates (fresh, dde0486b)
row("A1-gate-check-pages", "2.9 gate: check_pages", "tools/check_pages.py --unit M5", F + R5 + "r5_check_pages_M5.out 'check_pages M5: PASS', exit 0.")
row("A1-gate-check-dag", "2.9 gate: check_dag", "tools/check_dag.py --unit M5", F + R5 + "r5_check_dag_M5.out 'check_dag M5: PASS', exit 0.")
row("A1-gate-check-projects", "2.6 gate: check_projects (gate only; project not read by this slice)", "tools/check_projects.py --unit M5", F + R5 + "r5_check_projects_M5.out 'check_projects M5: PASS', exit 0.")
row("A1-gate-run-labs", "2.5 gate: run_labs for hub and L01-L04", "tools/run_labs.py --unit M5 --page index|L01|L02|L03|L04", F + R5 + "r5_run_labs_index.out 'PASS (0/0)'; r5_run_labs_L01..L04.out 'PASS (1/1)' each; all exit 0.")
row("A1-gate-page-smoke", "2.5/2.9 gate: page_smoke for hub and L01-L04 (alone)", "tools/page_smoke.py --unit M5 --pages index L01 L02 L03 L04", F + R5 + "r5_page_smoke_M5_a.out 'page_smoke M5: PASS', exit 0. Does not detect hidden text (the round-4 FAIL was found by raw_lt_scan2.py, not by this gate).")
row("A1-gate-ruff-mypy-twins", "2.5 gate: ruff, mypy strict, twins", ".venv/bin/ruff check .; ruff format --check .; mypy --no-incremental; python -I -W error on each twin",
    F + R5 + "r5_ruff_check.out 'All checks passed!' exit 0; r5_ruff_format.out '554 files already formatted' exit 0 (round 4 reported 553; difference not investigated, format-clean); r5_mypy.out 'Success: no issues found in 385 source files' exit 0; twins L01-L04 alone: r5_twin_L0k.exit 0, .err 0 bytes.")
row("A1-gate-pytest", "2.5 gate: relevant pytest", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -q",
    F + R5 + "r5_pytest_M5_relevant.out: 190 tests (progress lines 72, 72, 46), exit 0. Full suite not run: no tool or test changed in the delta.")
row("A1-gate-verify-refs", "2.1 gate: verify_refs", "tools/verify_refs.py --offline; tools/verify_refs.py --unit M5",
    F + R5 + "r5_verify_refs_offline_all.out 'offline integrity: 560 entries, 0 problems', exit 0. The live M5 run is carried from round 4 (r4_verify_refs_M5_live.out: 2 of 560 entries, 0 problems): references/ and tools/ are byte-identical, and no network call was made in round 5.")
row("A1-gate-build-site", "2.9 gate: build_site --check", "tools/build_site.py --check", F + R5 + "r5_build_site_check.out 'site data current: 6 outputs', exit 0.")
row("A1-gate-render-curriculum", "3.1 gate: render_curriculum and diff", "tools/render_curriculum.py; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json",
    F + R5 + "r5_render_curriculum.out 'curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h (6.35 FTE years)'; r5_render_curriculum_diff.out exit 0 (no tracked change).")

assert len(rows) == 59, len(rows)
frag = {
  "unit": "M5",
  "slice": "a",
  "round": 5,
  "verifier": "Haiku independent verifier, M5 slice a round 5 (did not build M5)",
  "pin": "dde0486bb7d1ecf5b5fc1d8a0fcbc4b8a2d1c3e4",
  "base": "edbb7aa8de20e6d2f3035c463a79a318c22623c4 (round-4 pin); delta by git diff edbb7aa8 dde0486b",
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyS5-M5-a",
  "scratch": "ledgers/M5/scripts/M5-a-r5/ (scripts and outputs, repo paths)",
  "verified_at": "VERIFIED_AT",
  "verdict": "PASS",
  "rows": rows,
  "mutants": [],
  "registry_flags": [],
  "freshness_flags": [],
  "notes": [
    "Delta edbb7aa8..dde0486b for slice a: course/modules/M/M5/L01.html (line 62), L03.html (line 237), L04.html (lines 56, 80, 240, 246, 249, 296), cards.json (c055, c064 changed; c067 removed; deck now 233 cards). index.html, L02.html, tests/labs/M5/lab-M5-L01-1..L04-1.py, tools/, notation/, references/, curriculum/ are byte-identical (git diff --quiet). plans/FINAL-ARCHITECT-RULINGS.md and plans/KNOWN-ISSUES.md changed, but only about E3 (rulings 27-29); no M5 rule changed.",
    "Round-4 FAIL A1-L04-render-raw-less-than is fixed and re-verified PASS (raw '<' now escaped; scanner reports 0 on dde0486b, 3 on edbb7aa8).",
    "Changed subjects re-verified this round: L01 line 62, L03 line 237, every L04 hunk, all L01-L04 cards and the 233-card deck. Carried rows (subject byte-identical or cited lines outside every delta hunk) carry the 'Carried from round 4' prefix.",
    "LOW, not a row failure: L01.html:453 (quiz L01q7 explanation) uses the irrationality of sqrt(2) without repeating the M1 citation; the chain is cited via L01.html:254.",
    "Slice a has no grader and no project, so there are no mutants; mutation testing (VERIFIER_RULES section 2.6) does not apply to this slice.",
    "Could not check: Abbott and Rudin (not opened, no locator asserted); the live verify_refs run (not repeated, see gate row); the full pytest suite; run_graders (project slice); pixel comparison (page_smoke only, no figure in slice); rendering in browsers other than the one page_smoke drives; L05-L10 mathematics and cards (outside slice a, cited only by block-title grep for hub rows)."
  ],
  "summary": "Round 5, slice a (hub, L01-L04 pages, lab twins, slice cards). 59 rows: 59 PASS, 0 FAIL. Round-4 FAIL A1-L04-render-raw-less-than is fixed. Changed subjects (L01 line 62, L03 line 237, L04 hunks, cards c055/c064/c067) re-verified from scratch; one new row A1-L03-misconception-3 added. All gates re-run at dde0486b PASS (check_pages, check_dag, check_projects, run_labs, twins under -I -W error, page_smoke, ruff, mypy, relevant pytest, verify_refs offline, build_site, render_curriculum diff); live verify_refs carried from round 4."
}
import datetime, sys
frag["verified_at"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
json.dump(frag, open("ledgers/M5/M5-a.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("written", len(rows))
