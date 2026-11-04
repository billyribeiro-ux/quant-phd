# Round-6 rows for E4-c, executed by build_fragment.py (OVERRIDES, NEW, fresh, carry are defined there).
S = "ledgers/E4/scripts/E4-c-r6/out/"
PAGES = "course/modules/E/E4/"
TWIN = "tests/labs/E4/"

OVERRIDES["E4c-r4-delta-read"] = fresh(
    "E4c-r4-delta-read", "delta",
    PAGES + "L07.html:147-152, 533-585; L08.html:51, 79, 401; L09.html:410-412, 435; " + TWIN + "lab-E4-L07-1.py:17; "
    + TWIN + "lab-E4-L08-1.py:65; " + PAGES + "cards.json (changed lines listed in " + S + "linemap.out); " + PAGES + "L06.html:486, 503, 615 (outside slice)",
    "PASS",
    "Round-6 delta read hunk by hunk: git diff -U2 7376a5e2 4bd8cb94 for the slice files, output read in full. "
    "git diff --stat shows no change to references/, notation/, tools/, curriculum/, atlas/, course/assets/ or index.html. "
    "Changed slice hunks: L07 docstring (two sentences on exact Fraction values and the Part F float conversion); L07 quiz "
    "(fieldset style attribute; item 'Across the noise-volume sweep of Lab 1, Part B ...'); L08 why-it-matters and Example 1.1 wording; "
    "L08 page and twin gain_at_zero docstring; L09 Res 2 (p, r replaced by nu_1, nu_2) and its key-results row; L07 twin docstring; "
    "cards.json entries in L05 to L09 and L01 to L04 (not all in slice). Line map: " + S + "linemap.out (only L07 lines after 151 move, by +1). "
    "Each changed hunk is re-verified in its own row.")

OVERRIDES["E4c-r4-recheck-numbers"] = fresh(
    "E4c-r4-recheck-numbers", "2.2-numbers", PAGES + "L07.html, L08.html, L09.html (every printed and quoted number)", "PASS",
    "Round-6 independent recheck, stdlib, python -I -W error: ledgers/E4/scripts/E4-c-r6/recheck_r6.py, output " + S + "recheck_r6.out. "
    "It does not import the lab twins. L07: rho^2 = 4/9, 1/3, 1/6, 1/18, 1/66 for sigma_u in 1/4, 1/2, 1, 2, 4; sigma_eta^2 = 5/4, 2, 5, 17, 65; "
    "Var(p) = 729/1444 and 35937/4802 at the ends (theta from Proposition 6.7 recomputed); base rho^2 = 1/3; sigma_u = sqrt(1/2) for rho^2 = 1/4 and "
    "for half the benchmark; E1 ratio 0.1354 (quoted 0.135). L08: G(0) = 0.173287, G(0.5) = 0.158997, G(1) = 0.127706 = ln(5/3)/4, "
    "G(1e-6) - G(0) = -6.25e-14, b_y/beta = 13/81 = 0.160494 (quoted 0.1605), bisection roots at costs 0.13 to 0.17 equal the printed lam* "
    "to 4e-10, boundary gaps 7.71e-3 and -6.71e-3, Corr^2 at lam = 1/2 with sigma_u^2 = 1 equal 1/18. L09: 15625 bets; state 1 and state 4: "
    "500 strictly accepted, 0 of them nonnegative on the meet, 625 nonnegative on the meet, 0 of those with a nonzero posterior.")

OVERRIDES["E4c-cmd-check-pages"] = fresh(
    "E4c-cmd-check-pages", "2.9-structure", PAGES + "L07.html, L08.html, L09.html", "PASS",
    "Re-run alone on pin 4bd8cb94: .venv/bin/python tools/check_pages.py --unit E4 --page Lnn; outputs " + S + "check_pages_L07.out, _L08.out, _L09.out; "
    "each 'check_pages E4 Lnn: PASS' with exit=0 (script ledgers/E4/scripts/E4-c-r6/run_gates.sh).")
OVERRIDES["E4c-cmd-check-dag"] = fresh(
    "E4c-cmd-check-dag", "2.9-structure", PAGES + "*.html (unit E4)", "PASS",
    "tools/check_dag.py --unit E4 on the pin: " + S + "check_dag_E4.out 'check_dag E4: PASS', exit=0. Unlinked uses of plan D1 to D10 are "
    "scanned separately in E4c-dag-unlinked.")
OVERRIDES["E4c-cmd-check-projects"] = fresh(
    "E4c-cmd-check-projects", "2.6-projects", PAGES + "project.html and grader/ (unit gate)", "PASS",
    "tools/check_projects.py --unit E4 on the pin: " + S + "check_projects_E4.out 'check_projects E4: PASS', exit=0. Project content is another slice; "
    "the gate is run for completeness only.")
OVERRIDES["E4c-cmd-run-labs"] = fresh(
    "E4c-cmd-run-labs", "2.5-labs", PAGES + "L07.html, L08.html, L09.html", "PASS",
    "tools/run_labs.py --unit E4 --page Lnn on the pin: " + S + "run_labs_L07.out, _L08.out, _L09.out, each 'run_labs E4: PASS (1/1)', exit=0.")
OVERRIDES["E4c-cmd-twins-standalone"] = fresh(
    "E4c-cmd-twins-standalone", "2.5-labs", TWIN + "lab-E4-L07-1.py, lab-E4-L08-1.py, lab-E4-L09-1.py", "PASS",
    "Each twin run from an empty temporary directory with env -i and python -I -W error (ledgers/E4/scripts/E4-c-r6/run_gates.sh): "
    "exit 0 and empty stderr for L07, L08 and L09 (" + S + "twin-L0n.exit, .stderr). Printed output: L07 Parts A to F (Part F 'sample_rho2 0.330625 "
    "population 0.333333 within True'); L08 Parts A to D (residual 1.332e-15; gain(0) 0.173287; lam* at 0.12 = 1, at 0.15 = 0.657828572, at 0.18 = 0; "
    "part D flags False); L09 Parts A to C (15625; 500; 0; 625). Re-run by hand in this round with the same output.")
OVERRIDES["E4c-expected-equals-output"] = fresh(
    "E4c-expected-equals-output", "2.5-labs", PAGES + "L07.html (data-run and expected blocks), L08.html, L09.html", "PASS",
    "ledgers/E4/scripts/E4-c-r6/embed_check.py (out/embed_check.out): for L07, L08 and L09 the data-run code block equals the twin source and the "
    "expected block equals the twin's standalone stdout: 'code blocks: 1 [True] | expected blocks: 1 [True] | twin exit 0 stderr bytes 0' for each page.")
OVERRIDES["E4c-cmd-page-smoke"] = fresh(
    "E4c-cmd-page-smoke", "2.9-structure", PAGES + "L07.html, L08.html, L09.html (light and dark, 360 px and desktop)", "PASS",
    "tools/page_smoke.py --unit E4 --pages L07 L08 L09 alone on the pin: " + S + "page_smoke_L07_L08_L09.out; 'page_smoke modules/E/E4/L07.html: PASS', "
    "L08 PASS, L09 PASS, 'page_smoke E4: PASS', exit=0. Lab run times in page smoke: L07 0.0 s, L08 0.1 s, L09 5.0 s (limit 10 s).")
OVERRIDES["E4c-cmd-ruff-mypy-twins"] = fresh(
    "E4c-cmd-ruff-mypy-twins", "2.5-labs", TWIN + "lab-E4-L07-1.py, lab-E4-L08-1.py, lab-E4-L09-1.py", "PASS",
    "ruff check: 'All checks passed!' (" + S + "ruff_check.out); ruff format --check: '3 files already formatted' (ruff_format.out); "
    "mypy --no-incremental on the three twins: 'Success: no issues found in 3 source files' (mypy_twins.out). All exit 0.")
OVERRIDES["E4c-cmd-pytest-labs"] = fresh(
    "E4c-cmd-pytest-labs", "2.5-labs", "tests/test_labs.py -k E4", "PASS",
    ".venv/bin/python -m pytest tests/test_labs.py -q -k E4: 13 passed (13 dots), exit 0 (" + S + "pytest_labs_E4.out).")
OVERRIDES["E4c-cmd-verify-refs"] = fresh(
    "E4c-cmd-verify-refs", "2.1-citations", "references/references.json (milgrom1982information, used by L09)", "PASS",
    "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', exit 0 (" + S + "verify_refs_offline.out). No live run: no reference "
    "record changed (references/ has no change since 7376a5e2). The live re-resolution of milgrom1982information belongs to the scheduled CI job and is not repeated here.")
OVERRIDES["E4c-cmd-run-graders"] = fresh(
    "E4c-cmd-run-graders", "2.6-projects", PAGES + "grader/ (unit gate)", "PASS",
    "tools/run_graders.py --unit E4 --seeds 0-49 on the pin: 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0 (" + S + "run_graders_E4.out). "
    "The grader is another slice; the gate is run for completeness.")

OVERRIDES["E4c-L07-structure"] = fresh(
    "E4c-L07-structure", "2.9-structure", PAGES + "L07.html (whole page)", "PASS",
    "Whole page re-read as text (ledgers/E4/scripts/E4-c-r6/textify.py, out/L07.txt). Order of BUILDER_RULES 4.2: why it matters (117 words, at most 120); "
    "numbered sections 1 to 4 with Definitions 7.1 and 7.2, Lemmas 7.3 and 7.4, Remarks 7.5, 7.8 and 7.9, Propositions 7.6 and 7.7; inline Lab 1 before "
    "'Where the canon breaks'; canon (4 items); misconceptions (4); problem set (Mechanics M1 to M3, Proof P1 to P3, Empirical E1 to E3, Research R1 to R3); "
    "key results table; retrieval quiz (10 items, each with an explanation); references (no registry key; the closed form inherits L06). "
    "Hours: 8 study hours (check_pages PASS). Banned and process phrases: none (" + S + "text_scans.out).")
OVERRIDES["E4c-L07-quiz"] = fresh(
    "E4c-L07-quiz", "2.9-structure", PAGES + "L07.html:518-592 (quiz); item at L07.html:565-566 (changed)", "PASS",
    "Round-5 FAIL fixed. The item is now 'Across the noise-volume sweep of Lab 1, Part B, does a higher price variance imply a higher informativeness?' "
    "with options 'Yes, always', 'No: across the noise sweep the price variance rises while rho^2 falls (Lab 1, Part B)' (marked correct) and "
    "'Yes, but only when lambda = 1'. The printed Part B values support the key: Var(p) = 729/1444, 27/49, 27/32, 729/338, 35937/4802 (rising) "
    "and rho^2 = 4/9, 1/3, 1/6, 1/18, 1/66 (falling) (" + S + "twin-L07.stdout; recheck_r6.out). All ten items were re-read against the page this round. "
    "Items 1, 2, 4, 5, 6, 8, 9 and 10 are re-derived: 1/3; sigma_eta^2 = 5; strictly falling in sigma_u (Proposition 7.7); 9/22 = 0.4091; "
    "Corr in [0, 1] (Lemma 7.3); 1/2 benchmark; sqrt(1/2) = 0.7071; higher a lowers rho^2. "
    "The fieldset style attribute (min-inline-size: 0) is presentational and changes no option text.")
OVERRIDES["E4c-L07-lab1-values"] = fresh(
    "E4c-L07-lab1-values", "2.5-labs", PAGES + "L07.html:130-372 (lab 1, embedded code and expected block; lines 149-151 changed)", "PASS",
    "Re-derived this round (recheck_r6.out) and checked against the standalone twin run (" + S + "twin-L07.stdout). Part A: 1/3 from the moments and "
    "from the closed form (equal True). Part B: 4/9, 1/3, 1/6, 1/18, 1/66; Var(p) 729/1444 to 35937/4802. Part C: 1/6, 1/3, 9/22. Part D: 4/9, 1/3, 1/6. "
    "Part E: benchmark 1/2 and 2500/5001 at sigma_u = 1/100. Part F: 0.330625 against 1/3 (SIMULATED, seed 7). The expected block equals the twin "
    "stdout (E4c-expected-equals-output). The changed docstring lines are the Units paragraph, checked in E4c-L07-cents-docstring.")
OVERRIDES["E4c-L07-cents-docstring"] = fresh(
    "E4c-L07-cents-docstring", "2.5-labs",
    TWIN + "lab-E4-L07-1.py:16-18 and population float at :182; " + PAGES + "L07.html:149-151 (embedded copy)", "PASS",
    "Round-5 FAIL fixed. The docstring now reads 'Parts A to E print exact Fraction population values; Part F converts the exact population value to float "
    "for comparison with the sample.' The code agrees: Parts A to E print Fraction objects only (standalone output), and part_f sets "
    "population = float(rho2_closed(...)) (line 182) and prints 'population 0.333333'. The embedded copy equals the twin (E4c-expected-equals-output).")
OVERRIDES["E4c-r5-L07-docstring-exact-fraction"] = fresh(
    "E4c-r5-L07-docstring-exact-fraction", "2.5-labs",
    TWIN + "lab-E4-L07-1.py:16-18 and :182; " + PAGES + "L07.html:149-151 (embedded copy)", "PASS",
    "Round-5 FAIL fixed (same evidence as E4c-L07-cents-docstring): the docstring no longer says every population value is an exact Fraction; "
    "Part F's float conversion is named, and the standalone output 'population 0.333333' is consistent with it.")
OVERRIDES["E4c-L07-simulated-labels"] = fresh(
    "E4c-L07-simulated-labels", "2.8-data",
    PAGES + "L07.html (Part F docstring and expected line; hypothesis at L07.html:132); " + TWIN + "lab-E4-L07-1.py:14, 159-160", "PASS",
    "Part F is labelled SIMULATED in the lab docstring (twin line 14, and the embedded copy), in the function docstring (line 159) and in the printed line "
    "'Part F: SIMULATED sample check' (" + S + "twin-L07.stdout). The exact population values in Parts A to E are not labelled, as the plan requires. "
    "The lesson's lab hypothesis states the same SIMULATED Part F (L07.html:132).")
OVERRIDES["E4c-L07-process-and-banned"] = fresh(
    "E4c-L07-process-and-banned", "2.9-structure", PAGES + "L07.html (body text)", "PASS",
    "ledgers/E4/scripts/E4-c-r6/text_scans.py (" + S + "text_scans.out): no banned phrase (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, "
    "left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly) and no process word "
    "(builder, verifier, requests, unit report, round 4 to 6) in the body text with tags, math and code removed.")

OVERRIDES["E4c-L08-structure"] = fresh(
    "E4c-L08-structure", "2.9-structure", PAGES + "L08.html (whole page)", "PASS",
    "Whole page re-read as text (out/L08.txt). Order of BUILDER_RULES 4.2: why it matters (118 words, at most 120); sections 1 to 5 with 5.1; "
    "inline Lab 1 before 'Where the canon breaks'; canon (4 items); misconceptions (4); problem set (Mech 1 to 3, Proof 1 to 3, Emp 1 to 3, Res 1 to 3); "
    "key results table (9 rows); retrieval quiz (9 items, each with an explanation); references (no registry key). Hours 8 (check_pages PASS).")
OVERRIDES["E4c-L08-A5"] = fresh(
    "E4c-L08-A5", "2.4-mathematics", PAGES + "L08.html:58, 65, 70, 314, 319-332, 573 (and 51, 79)", "PASS",
    "Assumption numbering on the pin: L08 defines A1 (preferences, line 58), A2 (normal information, line 65), A3 (price taking and clearing, line 70) and "
    "A4 (sign change, line 314, 'This is assumed here'). grep -c A5 over L08.html is 0, and cards.json has an A5 only in lesson L02 (" + S + "text_scans.out). "
    "Proposition 5.2(c) and the bisection rule (Section 5.1) are the only uses of A4 in the proofs, as line 51 says.")
OVERRIDES["E4c-L08-line51-zero-cost"] = fresh(
    "E4c-L08-line51-zero-cost", "2.9-structure",
    PAGES + "L08.html:51 (why it matters, changed this round); Definition 4.6 at L08.html:266-267; Proposition 5.1 at L08.html:285-296", "PASS",
    "The changed sentence 'no informed fraction lambda (Assumption A3) is an equilibrium informed fraction (Definition 4.6) at a cost c with 0 < c < G(0) "
    "(Proposition 5.1(b))' matches Definition 4.6 (i) and Proposition 5.1(b) (case (i) fails for 0 < c < G(0) when sigma_u^2 = 0). 'Definition 6.2 of Lesson "
    "L06' is the CARA definition at L06.html:66. The sentence says 'With no supply noise', which is the sigma_u^2 = 0 case of Proposition 5.1.")
OVERRIDES["E4c-L08-line51-existence"] = fresh(
    "E4c-L08-line51-existence", "2.4-mathematics", PAGES + "L08.html:51 (changed this round)", "PASS",
    "'equilibria exist outside (G(1), G(0))' matches Proposition 5.2(b) and (c): c >= G(0) gives lambda = 0 and c <= G(1) gives lambda = 1 without A4, and "
    "costs strictly between need A4. 'Inside that interval, existence uses Assumption A4' matches Proposition 5.2(c). Checked against the page text "
    "(out/L08.txt) and the twin's output (part C: lam* = 1 at 0.12 and 0 at 0.18; interior roots between).")
OVERRIDES["E4c-L08-G-before-definition"] = fresh(
    "E4c-L08-G-before-definition", "2.9-structure", PAGES + "L08.html:51, 79 (changed this round) vs Definition 4.3 (L08.html:232)", "PASS",
    "G(lambda) first appears at L08.html:51 with the forward label '(Definition 4.3; Lemma 4.5 for G(0))', and at line 79 in Example 1.1, which cites "
    "Lemma 4.5 and Lab 1. The definition block at L08.html:232 follows in Section 4. The forward references are explicit; no use precedes a definition without a label.")
OVERRIDES["E4c-L08-process-banned"] = fresh(
    "E4c-L08-process-banned", "2.9-structure", PAGES + "L08.html (body text)", "PASS",
    "ledgers/E4/scripts/E4-c-r6/text_scans.py (out/text_scans.out): no banned or process phrase in the body text of L08.")
OVERRIDES["E4c-L08-define-posterior"] = fresh(
    "E4c-L08-define-posterior", "2.9-structure", PAGES + "L08.html:123, 161, 257-258; " + PAGES + "L06.html:96 (the definition)", "PASS",
    "Corrected from round 5, which wrote 'L08.html:123 (dfn)': L08.html:123 has no <dfn>. It uses 'posterior' as a reference to Lesson L06's definition "
    "(L06.html:96 is <dfn>posterior</dfn>), so the term is defined before its use. The <dfn> tags of L08 are at lines 66, 71, 206, 233, 235, 267 and 281 "
    "(text_scans.py and grep -n '<dfn' L08.html).")

OVERRIDES["E4c-L08-dfn-duplicates"] = fresh(
    "E4c-L08-dfn-duplicates", "2.9-structure", PAGES + "L08.html:66, 71; " + PAGES + "L06.html:72, 245, 673", "FAIL",
    "Round-5 row said 'no duplicate definition across L06 and L08'; that missed L06.html:72. L06.html:72 defines the terms in prose: "
    "'A fraction lambda in (0, 1) of the investors is informed. An informed investor observes s and the price p. An uninformed investor observes only p.' "
    "L08.html:71 then defines 'informed' and 'uninformed' again with <dfn>informed</dfn> and <dfn>uninformed</dfn>. L08.html:66 defines "
    "'noise-trader supply' with <dfn>, while the term is already used in L06 (L06.html:245, inside the embedded lab docstring; L06.html:673, a quiz prompt). "
    "The plan (section 2.2 item 5) and VERIFIER 2.9 require each term defined once, at its first use.",
    "Keep one plain <dfn> per term, at its first use. For 'informed', 'uninformed' and 'noise-trader supply' the first use is in L06 (L06.html:72, and the "
    "first use of 'noise-trader supply' before L06.html:245). In L08.html:66 and :71 remove the <dfn> tags and refer to L06 Assumption A2 and Definition 6.1 "
    "in prose. Owners: the L06 builder (plain <dfn> at L06.html:72 and at the first use of noise-trader supply) and the L08 builder (remove the tags).")

OVERRIDES["E4c-r3-first-use-before-definition"] = fresh(
    "E4c-r3-first-use-before-definition", "2.9-structure", PAGES + "L08.html:66, 71; " + PAGES + "L06.html:72, 245, 673", "FAIL",
    "Re-verified at 4bd8cb94. grep -n '<dfn' L08.html gives 'noise-trader supply' at line 66 and 'informed', 'uninformed' at line 71. Earlier uses: "
    "L06.html:72 ('informed' and 'uninformed', defined in prose without <dfn>), L06.html:245 ('noise-trader supply' in the embedded lab docstring) and "
    "L06.html:673 ('noise-trader supply' in a quiz prompt). L06 changed at lines 486, 503 and 615 only, so these first-use lines are unchanged.",
    "See E4c-L08-dfn-duplicates: one plain <dfn> at the first use in L06, and no second <dfn> in L08.html:66 and :71.")

OVERRIDES["E4c-r5-cards-duplicates"] = fresh(
    "E4c-r5-cards-duplicates", "2.7-cards", PAGES + "cards.json (220 cards)", "PASS",
    "Full scan this round (python -I): 220 cards, 0 duplicate ids, 0 duplicate fronts. Ids are not sequential (architect ruling 2 allows that).")
OVERRIDES["E4c-r5-cards-L07"] = fresh(
    "E4c-r5-cards-L07", "2.7-cards", PAGES + "cards.json:1030-1034 (E4-c139, changed) and E4-c130 to E4-c150 (21 cards)", "PASS",
    "All 21 L07 cards read against the L07 text. E4-c139 now reads 'Under the hypotheses of Proposition 7.6, Remark 7.8' (matches the page). "
    "Definitions 7.1 and 7.2, Lemmas 7.3 and 7.4, Propositions 7.6 and 7.7, Remarks 7.5, 7.8 and 7.9 match. Lab numbers E4-c141 to E4-c146 "
    "(1/3; 4/9, 1/3, 1/6, 1/18, 1/66; 729/1444 and 35937/4802; 1/6, 1/3, 9/22; 4/9, 1/3, 1/6; 0.330625 within 0.02) match " + S + "twin-L07.stdout. "
    "Misconception cards E4-c147 to E4-c150 match the page. Grades: finite checks C, the SIMULATED check C.")
OVERRIDES["E4c-r5-cards-L08"] = fresh(
    "E4c-r5-cards-L08", "2.7-cards",
    PAGES + "cards.json:1336-1341 (E4-c179, basis changed), 1381 (E4-c184, basis changed), E4-c151 to E4-c188 and E4-c222 to E4-c224 (41 cards)", "PASS",
    "Round-5 FAIL fixed: E4-c179 basis now reads 'Proposition 5.2(c); conditional on Assumption A4' (the page's assumption). E4-c184 basis now reads "
    "'finite grid of 999 interior fractions in (0, 1)' (matches the twin GRID = 999 and lam = k/(GRID+1)). All 41 L08 cards read against the L08 text; "
    "the numbers on the cards (1.332e-15; 0.088941; 7.71e-03; -6.71e-03; 0.0e+00; 0.1595; 0.1605; 0.173287; 0.127706; 0.657828572; 1.83e-15; 0.013061; "
    "0.166667) appear in the lesson's expected blocks or text (" + S + "twin-L08.stdout).")
OVERRIDES["E4c-r5-cards-L09"] = fresh(
    "E4c-r5-cards-L09", "2.7-cards", PAGES + "cards.json:1570-1572 (E4-c211, lesson L09); " + PAGES + "L09.html:409-412 (Problem Res 2, changed this round)", "FAIL",
    "Card E4-c211 still uses the old symbols. Its front reads 'priors q_1(H) = p and q_2(H) = r, where p != r and 0 < p, r < 1' and its back reads "
    "'for theta = (p + r)/2 ... If p < r, exchange the labels'. The current Problem Res 2 (L09.html:410-412) uses nu_1 and nu_2 (nu_1 != nu_2, "
    "theta = (nu_1 + nu_2)/2, 'If nu_1 < nu_2'). The mathematics agrees, but the card no longer matches the current lesson text (VERIFIER 2.7), and p is the "
    "price symbol across E4 (plan 2.3). The other 21 L09 cards (every L09 card except E4-c211) were read against the text and agree.",
    "In cards.json, card E4-c211 (lines 1570-1572): front -> 'Assume two trivial-partition states H and L with priors q_1(H) = nu_1 and q_2(H) = nu_2, "
    "where nu_1 != nu_2 and 0 < nu_1, nu_2 < 1. Is there a bet with strictly positive expected receipts for both traders?'; back -> 'Yes. Take x(H) = 1 and "
    "x(L) = -t with t = theta/(1 - theta) for theta = (nu_1 + nu_2)/2, which lies strictly between nu_2 and nu_1. Both expected receipts are positive. "
    "If nu_1 < nu_2, exchange the labels H and L.' Then re-read the card against L09.html:409-412.")
OVERRIDES["E4c-r5-milgrom-record"] = fresh(
    "E4c-r5-milgrom-record", "2.1-citations", "references/references.json (key milgrom1982information); " + PAGES + "L09.html:512", "PASS",
    "Registry record read this round: title 'Information, trade and common knowledge', container 'Journal of Economic Theory', volume 26, issue 1, "
    "pages 17-27, year 1982, verified_by crossref, status verified. The page's line 512 states the same title, journal, volume, issue, pages and year, "
    "and types no author names. The attribution is limited to the topic (the lesson states no result of the paper).")
OVERRIDES["E4c-r5-notation-scan"] = fresh(
    "E4c-r5-notation-scan", "2.4-mathematics", PAGES + "L07.html, L08.html, L09.html; notation/notation.json", "PASS",
    "ledgers/E4/scripts/E4-c-r2/notation_scan.py (round-2 scanner) re-run on the pin: 'unknown macros = []' for each page (" + S + "notation_scan.out). "
    "Registered symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q): 0 bare uses inside math (text_scans.out). The macro nu appears in L09 only "
    "(unregistered, local; it replaces the old p and r). \\R is used in L08 and L09; there is no \\mathbb{R}.")
OVERRIDES["E4c-r5-figures"] = fresh(
    "E4c-r5-figures", "2.8-data", PAGES + "L07.html, L08.html, L09.html", "PASS",
    "data-chart count is 0 on each page (text_scans.out), so no chart or SVG needs axis, source or caption checks in this slice.")
OVERRIDES["E4c-r5-lab-sim-labels"] = fresh(
    "E4c-r5-lab-sim-labels", "2.8-data", TWIN + "lab-E4-L07-1.py (Part F), lab-E4-L08-1.py (Part A), lab-E4-L09-1.py (none)", "PASS",
    "Printed lines: 'Part F: SIMULATED sample check' (L07, " + S + "twin-L07.stdout) and 'part A (SIMULATED draws)' (L08, twin-L08.stdout). L09 imports only "
    "fractions and itertools, has no draws, and its docstring says so.")
OVERRIDES["E4c-r5-recheck-L07-prop-7.6"] = fresh(
    "E4c-r5-recheck-L07-prop-7.6", "2.4-mathematics", PAGES + "L07.html:97-118 (Propositions 7.6, 7.7 and their proofs); lab block", "PASS",
    "Re-run this round: ledgers/E4/scripts/E4-c-r5/recheck_L07.py (" + S + "rerun_r5_recheck_L07.out, exit 0; fixed-point recomputation of the price "
    "coefficients), and ledgers/E4/scripts/E4-c-r6/recheck_r6.py (closed forms and Var(p) by hand). Proposition 7.6 is checked by hand this round: "
    "Y = p/theta_s = v + eta with eta = eps - kappa u, so Corr^2 = sigma_v^2/(sigma_v^2 + sigma_eta^2).")
OVERRIDES["E4c-r5-recheck-L08-gains"] = fresh(
    "E4c-r5-recheck-L08-gains", "2.2-numbers", PAGES + "L08.html:336, 544-563, 564, 587, 591, 595", "PASS",
    "ledgers/E4/scripts/E4-c-r5/recheck_L08.py re-run (" + S + "rerun_r5_recheck_L08.out, exit 0: independent theta_s = beta and theta_u = kappa*beta) and "
    "recheck_r6.py (G(0), G(0.5), G(1), bisection roots at costs 0.13 to 0.17 to 4e-10, boundary gaps). G(1) = ln(5/3)/4 is also derived by hand "
    "in this round: kappa = 2, tau_eta = 1/5, b_y = 1/6, V_I = 1/2, V_U = 5/6, beta = 1/2, Var(D_I) = 1, Var(D_U) = 2/3.")
OVERRIDES["E4c-r5-recheck-L09-counts"] = fresh(
    "E4c-r5-recheck-L09-counts", "2.2-numbers", PAGES + "L09.html:118-120, 126, 264-281 (lab block), 435", "PASS",
    "ledgers/E4/scripts/E4-c-r5/recheck_L09.py re-run (" + S + "rerun_r5_recheck_L09.out, exit 0: 'total bets: 15625', 'bets with g1 = g2 = 0 on {1,2,3}: 625') "
    "and recheck_r6.py (exact enumeration: 500 strict, 0 nonnegative on the meet, 625 nonnegative, 0 with a nonzero posterior, for state 1 and state 4).")

OVERRIDES["E4c-L09-res-2"] = fresh(
    "E4c-L09-res-2", "2.4-mathematics", PAGES + "L09.html:409-412 (Problem Res 2; statement and solution changed this round)", "PASS",
    "Re-derived. Trader 1's expected receipt is nu_1 - (1 - nu_1)t and trader 2's expected receipt of -x is (1 - nu_2)t - nu_2. With theta = t/(1 + t), "
    "trader 1's receipt equals (nu_1 - theta)/(1 - theta) and trader 2's equals (theta - nu_2)/(1 - theta); both are positive when nu_2 < theta < nu_1. "
    "theta = (nu_1 + nu_2)/2 lies in (0, 1) for 0 < nu_2 < nu_1 < 1, so t = theta/(1 - theta) > 0 gives the bet. If nu_1 < nu_2 the labels swap, "
    "the priors of H become 1 - nu_1 and 1 - nu_2 with 1 - nu_2 < 1 - nu_1, and the first case applies. Algebra checked by hand.")
OVERRIDES["E4c-L09-key-results"] = fresh(
    "E4c-L09-key-results", "2.4-mathematics", PAGES + "L09.html:431-435 (row at 435 changed this round)", "PASS",
    "The changed row ('With two priors nu_1 != nu_2 in (0, 1), a bet exists that both traders strictly accept', grade T, source Problem Res 2) matches "
    "Res 2. The other rows were re-read: Theorem 2.1, Corollary 2.3, Misconception 2, and the finite-check row (grade C, Lab 1 Parts B and C; "
    "recheck_r6.out: 0 of 500 nonnegative on the meet, 625 nonnegative with zero posteriors).")
OVERRIDES["E4c-L09-structure"] = fresh(
    "E4c-L09-structure", "2.9-structure", PAGES + "L09.html (whole page)", "PASS",
    "Whole page re-read as text (out/L09.txt). Order of BUILDER_RULES 4.2: why it matters (115 words); numbered sections 1 to 4 (Assumptions B1 to B3; "
    "Definitions 1.1 and 1.2; Theorem 2.1; Definition 2.2; Corollary 2.3; Example 2.4; Remark 2.5); inline Lab 1; canon (4 items); misconceptions (3); "
    "problem set (Mech 1 to 3, Proof 1 to 3, Emp 1 to 3, Res 1 to 3); key results; retrieval quiz (9 items); references. Hours: 8 (check_pages PASS).")
OVERRIDES["E4c-L09-process-banned"] = fresh(
    "E4c-L09-process-banned", "2.9-structure", PAGES + "L09.html (body text)", "PASS",
    "text_scans.py (out/text_scans.out): no banned or process phrase in the L09 body text.")
OVERRIDES["E4c-dag-unlinked"] = fresh(
    "E4c-dag-unlinked", "2.9-structure", PAGES + "L07.html, L08.html, L09.html (plan D1 to D10)", "PASS",
    "Plain-text scan of the three pages for D1 to D10 names (text_scans.py, out/text_scans.out): 'CARA' (D7; defined with a plain <dfn> in L06 and cited with "
    "its Definition 6.2 in L08), 'market clearing' (D9; plain prose), 'common knowledge' (D8; plain <dfn> at L09.html:79). No 'state price', "
    "'stochastic discount', 'law of one price', 'martingale', 'Bayes', 'Banach', 'Walras' or 'informationally efficient' appears in L07 to L09.")
OVERRIDES["E4c-notation-registered"] = fresh(
    "E4c-notation-registered", "2.4-mathematics", PAGES + "L07.html, L08.html, L09.html; notation/notation.json", "PASS",
    "Round-6 scan: notation_scan.py (round-2 script) 'unknown macros = []' for each page; no registered symbol used with another meaning (text_scans.out). "
    "Local symbols (p, q, r, x, y, eta, theta, chi, kappa, Y, D, b, c, nu) are defined on the page where first used or are standard in the proof.")
OVERRIDES["E4c-twin-L07-1"] = fresh(
    "E4c-twin-L07-1", "2.5-labs", TWIN + "lab-E4-L07-1.py (docstring lines 16-18 changed; code unchanged)", "PASS",
    "Standalone run (empty directory, env -i, python -I -W error): exit 0, empty stderr, output in " + S + "twin-L07.stdout. ruff and mypy clean "
    "(E4c-cmd-ruff-mypy-twins). The one changed block is the docstring Units paragraph (checked in E4c-L07-cents-docstring).")
OVERRIDES["E4c-twin-L08-1"] = fresh(
    "E4c-twin-L08-1", "2.5-labs", TWIN + "lab-E4-L08-1.py:65-66 (gain_at_zero docstring, changed)", "PASS",
    "Standalone run: exit 0, empty stderr (" + S + "twin-L08.stdout). The docstring now reads 'the price is the prior mean minus CARA*VAR_V*u', matching "
    "Lemma 4.5 (p = v-bar - a sigma_v^2 u). The code's noise term CARA^2 VAR_V^2 var_u = a^2 sigma_v^4 sigma_u^2 equals Var(D_U) at lambda = 0 "
    "(L08.html Lemma 4.5 proof), and the denominator 1 + noise/VAR_V equals 1 + X_0.")
OVERRIDES["E4c-r2-delta-read"] = fresh(
    "E4c-r2-delta-read", "delta", PAGES + "L07.html, L08.html, L09.html, index.html; " + TWIN + "lab-E4-L07-1.py, lab-E4-L08-1.py, lab-E4-L09-1.py", "PASS",
    "Round-6 delta from 7376a5e2 to 4bd8cb94 read in full (see E4c-r4-delta-read). index.html is unchanged. The L07 and L08 card titles and hours were "
    "re-checked by check_pages (PASS).")

NEW.append(fresh(
    "E4c-r6-L08-why-it-matters", "2.9-structure", PAGES + "L08.html:51 (changed this round)", "PASS",
    "Each claim checked: 'Definition 6.2 of Lesson L06' is the CARA definition (L06.html:66); 'Definition 4.3' and 'Lemma 4.5 for G(0)' exist; "
    "'no informed fraction lambda (Assumption A3) is an equilibrium informed fraction (Definition 4.6) at a cost c with 0 < c < G(0) (Proposition 5.1(b))' "
    "matches Proposition 5.1(b) and the twin's Part D; 'equilibria exist outside (G(1), G(0))' and 'existence uses Assumption A4' match Proposition 5.2. "
    "Word count 118 (check_pages PASS)."))
NEW.append(fresh(
    "E4c-r6-L08-example-1.1", "2.4-mathematics",
    PAGES + "L08.html:79 (changed this round); L08.html:241-245 and 286-292 (proofs); " + TWIN + "lab-E4-L08-1.py equilibrium()", "PASS",
    "The changed sentence says the prior mean does not enter any gain or informativeness measure, because Corollary 3.2 and Proposition 4.1 express them "
    "through the variances, a and lambda. Checked against the proofs: Corr^2 = sigma_v^2/(sigma_v^2 + sigma_eps^2 + kappa^2 sigma_u^2) has no v-bar, and "
    "D_I = (b_s - beta)(s - v-bar) + kappa beta u and D_U = (b_y - beta)(y - v-bar) have mean zero and variances free of v-bar. The twin's equilibrium() takes "
    "no prior-mean argument, and the printed gains depend on a, lambda and the variances only."))
NEW.append(fresh(
    "E4c-r6-L08-definition-6.2-link", "2.9-structure", PAGES + "L08.html:51, 59; " + PAGES + "L06.html:66", "PASS",
    "'CARA utility (Definition 6.2 of Lesson L06)' at L08.html:59 and in the why-it-matters at line 51 cites L06.html:66, which reads "
    "'Definition 6.2 (CARA utility)'. The page-level reference is exact."))
