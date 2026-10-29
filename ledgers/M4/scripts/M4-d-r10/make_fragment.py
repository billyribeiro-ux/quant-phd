"""Assemble the round-10 fragment for M4 slice d from the scripts' outputs (no hand-typed counts)."""
import json, re, pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB10-M4-d")
D = ROOT / "ledgers/M4/scripts/M4-d-r10"
out = (D / "mutate_M4.out").read_text().splitlines()
mutants = []
for line in out:
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, kb = m.groups()
    killed_by = kb.strip()
    if killed_by == "None":
        killed_by = None
    mutants.append({"id": name, "description": desc, "killed_by": killed_by})
# the four survivors of the tool, with their dispositions under the page
DISPOSITION = {
    "m11_loss_sign_flipped.py": "SURVIVES; accepted: project.html:228 states the suite does not test the loss sign",
    "m17_student_t_second_seed.py": "SURVIVES; accepted: the page states only that every run is reproducible from its seed (project.html:198), which this mutant satisfies",
    "r9_03_student_t_chi_square_reused_every_second_draw.py": "SURVIVES; accepted: project.html:228 (added this round) states the suite does not check one chi-square per draw, and the mutant passes seeds 0-9 as stated",
    "v4_m02_matched_factor_skipped_for_small_nu.py": "SURVIVES; accepted: project.html:228 states the suite does not check the matched factor at nu of 3 and 4",
}
for m in mutants:
    if m["id"] in DISPOSITION:
        m["killed_by"] = None
        m["description"] += " [" + DISPOSITION[m["id"]] + "]"
# round-10 new student-error mutants (re-run with run_mutant_seeds.sh on seeds 0-9)
mutants += [
    {"id": "r10_01_debug_print_on_long_runs.py",
     "description": "Verifier round-10 student-error mutant: leftover debug print in simulate_losses for n_draws >= 1000. SURVIVES seeds 0-9 (132 passed/133); project.html:204 says no function prints and :206 grades absence of printed output, so this is a FAIL (G-20).",
     "killed_by": None},
    {"id": "r10_02_quantile_sorts_absolute_losses.py",
     "description": "Verifier round-10 student-error mutant: quantile_99 takes the order statistic of absolute losses. Killed on seeds 0-9.",
     "killed_by": "test_quantile_99_is_the_exact_order_statistic (seed 0)"},
    {"id": "r10_03_matched_scale_debug_print_at_boundary.py",
     "description": "Verifier round-10 student-error mutant: leftover debug print in matched_scale at nu = 3. SURVIVES seeds 0-9; project.html:204 and :206 apply, so this is a FAIL (G-21).",
     "killed_by": None},
]
# alternative correct implementations (not mutants): recorded in the notes
PASS = "PASS"
rows = []
def row(i, check, location, status, evidence, fix=None):
    r = {"id": i, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != PASS:
        r["fix"] = fix
    rows.append(r)

S = "ledgers/M4/scripts/M4-d-r10/"
row("P-01", "Lab 1 hypothesis numbers and expected block", "course/modules/M/M4/project.html:57, 136-143", PASS,
    f"{S}labs_check.out 'lab 1: output == expected: True' (python -I -W error twin exit 0); 8.4e9 = 3.6e9 + 1.2e9 + 3.6e9 by hand; ceil(0.99*20000)=19800; (nu-2)/nu=0.6 at nu=5.")
row("P-02", "Lab 2 completion problem and expected block", "course/modules/M/M4/project.html:147-192", PASS,
    f"{S}labs_check.out: page code differs from twin only at the two blanks (diff: 'return ___' vs '(nu - 2) / nu' and '(99 * n + 99) // 100'); 'lab 2: output == expected: True'.")
row("P-03", "Lab 3 closed-form numbers and expected block", "course/modules/M/M4/project.html:266-314", PASS,
    f"{S}labs_check.out 'lab 3: output == expected: True'; sd=sqrt(8.4e9)=91651.514; z99=2.326348; round(z99*sd)=213213; n=101 ceil 100 floor 99; 0.99*19987=19787.13 (ceil 19788, floor 19787).")
row("P-04", "Lab 1 page code equals twin and runs under -I -W error", "course/modules/M/M4/project.html:58-135; tests/labs/M4/lab-M4-project-1.py", PASS,
    f"{S}labs_check.out: 0 differing lines between page code and twin (the only difference is the final newline of the twin); twin exit 0 with -I -W error.")
row("P-05", "Appendix A1 to A3 formulas and divergence claims", "course/modules/M/M4/project.html:325, 429", PASS,
    "Re-derived by hand: E[W^-1]=Gamma(nu/2-1)/(2 Gamma(nu/2))=1/(nu-2); E[W^-2]=1/((nu-2)(nu-4)); integrand exponents nu/2-2 (not integrable at 0 iff nu<=2) and nu/2-3 (iff nu<=4); density in u matches the chi-square density; Var(t)=nu E[W^-1]; matched identity E[RR^T]=Sigma.")
row("P-06", "Conventions items 1, 2 and 4 (formulas)", "course/modules/M/M4/project.html:209-217", PASS,
    "Re-read in full. sqrt((nu-2)/nu)*sqrt(nu/W)=sqrt((nu-2)/W); (99n+99)//100 equals ceil(0.99n) for every n in 1..20000 (integer identity; script found 0 mismatches against math.ceil(0.99*n)); loss sign and round() rule match reference.py.")
row("P-07", "Conventions item 1 notation and the Reading section", "course/modules/M/M4/project.html:211, 214, 482", PASS,
    "Lesson 6 Definition 2.1 (chi-square) and Definition 2.5 (Student-t) exist in course/modules/M/M4/L06.html text (cards c089, c092); Reading cites only blitzstein2019introduction, present in references/references.json (verify_refs --offline: 560 entries, 0 problems).")
row("P-08", "What the suite does not test: completeness of disclosures", "course/modules/M/M4/project.html:228", PASS,
    f"Round-9 FAIL is repaired: line 228 now states that a family reusing one chi-square variable on alternate draws passes the whole suite at seeds 0 to 9. Re-run: {S}run_mutant_seeds.sh on r9_03 gives 'passed' for seeds 0-9 (132 passed+1 skipped or 133 passed). Cross-term sentence (correlation 0.8, 100,000 draws, tolerance 0.05) matches test_project.py:43-48.")
row("P-09", "Grading-mode count 133 equals real collect-only count", "course/modules/M/M4/project.html:206", PASS,
    f"{S}collect.out: '133 tests collected'; reference seed 0 run: 132 passed, 1 skipped.")
row("P-10", "Rubric table and brief", "course/modules/M/M4/project.html:316-343", PASS,
    "Read in full. Levels nest as the scoring rule says; body 300-700 words and Summary at most 80 words (lines 319, 326) are used consistently by the rubric (line 340) and by the exemplars (71-word summary, 688-word body).")
row("P-11", "Numbers in exemplar A and B passages", "course/modules/M/M4/project.html:348-462", PASS,
    "2267 = 213213-210946; 32058 = 243004-210946; 15.2% = 32058/210946 = 0.15198; 1.152 = 243004/210946 = 1.15198; 4.5% of 1 = 1.0447-1; 'about 2,130 dollars' = 213213 cents ($2,132.13); exemplar A body is 100 words by script count (matches its annotation); exemplar B Summary 71 words (<= 80).")
row("P-12", "Exemplar scores and annotation consistency", "course/modules/M/M4/project.html:348-402", PASS,
    "data-scores 2,2,2,2,2 (A) and 4,4,4,4,3 (B) match the official-scoring text and the annotations (A: misses at level 3; B: misses C5 level 4 only).")
row("P-13", "Time budget and hub split", "course/modules/M/M4/project.html:33, 237-243; course/modules/M/M4/index.html:31, 42, 147", PASS,
    "2+2+12+8+4+2 = 30 = data-hours-project; hub: 10 lessons x 9 h = 90 plus 30 h project = 120 h (index.html line 31 'Tier F · 120 hours', line 42 '90 h lessons · 30 h project').")
row("P-14", "Anchors and relative links", "course/modules/M/M4/project.html (href targets)", PASS,
    "Every fragment href resolves to an id on the page; ../../../index.html and ../../../review.html exist (course/index.html, course/review.html); grader/*.py and L10.html exist.")
row("P-15", "File names and ids named on the page", "course/modules/M/M4/project.html; cards.json; grader/*.py", PASS,
    "tail_risk.py, report/run_report.py, report/report.md, report/self_assessment.md, grader/test_project.py, grader/instance.py, grader/starter.py, data-suite/data-starter attributes match the files in grader/.")
row("P-16", "Required signatures", "course/modules/M/M4/project.html:202; grader/starter.py:15-34", PASS,
    "The three signatures on the page match starter.py exactly (matched_scale(nu: int) -> float; simulate_losses(...) -> list[int] with nu: int | None; quantile_99(losses_cents: list[int]) -> int).")
row("P-17", "Named conditions vs tests", "course/modules/M/M4/project.html:220-224", PASS,
    "Each named ValueError condition has a test (test_project.py:118-129, 203-307, 500-501, 504-506); each named accepted input has a test (287, 210, 238, 430, 496); no named condition lacks one.")
row("P-18", "Stream order and one chi-square per draw vs suite", "course/modules/M/M4/project.html:204, 215, 228", PASS,
    "Round-9 FAIL repaired: lines 204 and 215 now both list the one-chi-square-per-draw rule among the ungraded item-5 points, consistent with line 228. Measured by cross.py: r9_02 (own chi-square per asset) moves the cross term 14.1-16.1% (seeds 0-9) and is killed; r8_03 moves it 6.8-8.6%.")
row("P-19", "Local run command and flags", "course/modules/M/M4/project.html:258-259", PASS,
    "The command equals the grader docstring (test_project.py:5); --assert=plain and -W error are pytest flags and the reference run with them exits 0 (132 passed, 1 skipped).")
row("P-20", "Autograder section attributes", "course/modules/M/M4/project.html:249-253", PASS,
    "data-suite=test_project.py, data-support=instance.py, data-solution=tail_risk.py, data-starter=starter.py all name files that exist in grader/ (or the solution the learner writes).")
row("P-21", "Lede and Lab 1 framing", "course/modules/M/M4/project.html:37, 57", PASS,
    "Every input is SIMULATED; Lab 1 reads no file (lab-M4-project-1.py has no open/read call).")
row("P-22", "Limitations: tolerance and nu scope", "course/modules/M/M4/project.html:453", PASS,
    "0.30 equals TOL_T_VARIANCE (test_project.py:41); 'nu of 5 or more' equals MIN_NU_FOR_T_VARIANCE_CHECK (42); the sign claim matches m11 surviving and line 228.")

# grader rows: fresh re-reads of the whole grader file, plus the sweeps and mutants run this round
row("G-01", "Suite conforms to the page's named conditions", "course/modules/M/M4/grader/test_project.py:89-511", PASS,
    f"Read the whole file (511 lines). Reference passes 132 + 1 skipped at seed 0 and {S}run_graders.out: 'reference 50/50 seeds'.")
row("G-02", "Starter file", "course/modules/M/M4/grader/starter.py:15-34", PASS,
    "Three functions raise NotImplementedError; signatures complete (see P-16).")
row("G-03", "Five-plus alternative correct implementations pass", "ledgers/M4/scripts/alt_1.py..alt_5.py; M4-d-r9/alt_stream_order_tail_risk.py; M4-d-r10/alt_r10_a_stream_order_fraction_index.py", PASS,
    "Each alternative run on grader seeds 0-49 (run_mutant_seeds.sh): 50 of 50 lines pass, 0 failures. alt_r10_a uses 1-2/nu, draws the chi-square before the normals, and Fraction index.")
row("G-04", "matched_scale tests vs page", "course/modules/M/M4/grader/test_project.py:105-130", PASS,
    "matched_scale tests: 3..8 exact; 3 accepted; 2 and 1, 0, -3 rejected; 3.0, True, '3', None rejected; each matches project.html:222.")
row("G-05", "Tolerance constants and comment numbers", "course/modules/M/M4/grader/test_project.py:31-48", PASS,
    f"{S}sweep_grader_comment_0-1999.txt re-derives every figure in the comment: max reference error nu=5 0.1259, nu=6 0.0967, nu=7 0.0728, nu=8 0.0624; unmatched fails 347/347 (nu=5), 317/317 (nu=6), 342/343 (nu=7), 288/317 (nu=8); seed 1093 nu=3 error 1.022 > 0.30; 0.30/0.1259 = 2.38. Cross term: reference max 0.0239 over seeds 0-49 ({S}cross_term_reference_0-49.txt); one-asset matched 6.8-8.6% and own-chi 14.1-16.1% (seeds 0-9).")
row("G-06", "Mutant: three-asset last factor column dropped", "ledgers/M4/mutants/r6_01_three_asset_last_factor_column_dropped.py", PASS, "mutate_M4.out: KILLED (see mutants list).")
row("G-07", "Mutant: Student-t chi-square twice the degrees", "ledgers/M4/mutants/r6_02_student_t_chi_square_twice_the_degrees.py", PASS, "mutate_M4.out: KILLED.")
row("G-08", "Mutant: pivot tolerance rejects small positive variance", "ledgers/M4/mutants/r6_03_pivot_tolerance_rejects_small_positive_variance.py", PASS, "mutate_M4.out: KILLED.")
row("G-09", "Mutant: loss sign flipped", "ledgers/M4/mutants/m11_loss_sign_flipped.py; course/modules/M/M4/project.html:212, 228", PASS,
    "mutate_M4.out: SURVIVED. Accepted: project.html:228 states the suite does not test the sign of the loss; the sign is a stated convention (line 212) that the page says must be checked by hand.")
row("G-10", "Mutant: Student-t second seed", "ledgers/M4/mutants/m17_student_t_second_seed.py", PASS,
    "mutate_M4.out: SURVIVED. Ungraded: the page states only that every run is reproducible from its seed (project.html:198), which this mutant satisfies; no sentence states that the families share a seed.")
row("G-11", "Mutant: one chi-square per asset", "ledgers/M4/mutants/n02_one_chi_square_per_asset.py", PASS, "mutate_M4.out: KILLED.")
row("G-12", "Mutant: matched factor skipped for small nu", "ledgers/M4/mutants/v4_m02_matched_factor_skipped_for_small_nu.py; course/modules/M/M4/project.html:228", PASS,
    "mutate_M4.out: SURVIVED. Accepted: project.html:228 states the suite does not check the matched factor at nu of 3 and 4.")
row("G-13", "Test count and rules", "course/modules/M/M4/grader/test_project.py:89-511", PASS, "collect-only 133 (collect.out); no print or warn in the suite except the capsys test (see G-20, G-21 for its gap).")
row("G-14", "Instance generator", "course/modules/M/M4/grader/instance.py:1-48", PASS,
    "Draw counts (6003, 8001, 9997, 12011, 15013, 19987) none a multiple of 100 and all <= 20000; nu in 3..8; 2 or 3 positions in 100,000..5,000,000 cents; covariance symmetric PD by construction.")
row("G-15", "Mutant: Student-t seed fixed", "ledgers/M4/mutants/r7_01_student_t_seed_fixed.py", PASS, "mutate_M4.out: KILLED.")
row("G-16", "Mutant: matched scale on first asset only", "ledgers/M4/mutants/r8_03_student_t_matched_scale_on_first_asset_only.py", PASS, "mutate_M4.out: KILLED; cross.py measured 6.8-8.6% over seeds 0-9.")
row("G-17", "Mutants: chi-square drawn once per run / index one low at multiples of 100", "ledgers/M4/mutants/r8_01_*.py; ledgers/M4/mutants/r8_02_*.py", PASS, "mutate_M4.out: both KILLED.")
row("G-18", "Mutant: chi-square reused every second draw", "ledgers/M4/mutants/r9_03_student_t_chi_square_reused_every_second_draw.py; course/modules/M/M4/project.html:228", PASS,
    "Round-9 FAIL repaired: mutate_M4.out SURVIVED, and the disclosure at project.html:228 now names this exact gap. run_mutant_seeds.sh: passes seeds 0-9.")
row("G-19", "Mutant: Student-t cross-term sign flipped for second asset", "ledgers/M4/mutants/r9_01_student_t_cross_term_sign_flipped_for_second_asset.py", PASS, "mutate_M4.out: KILLED.")
row("G-20", "NEW: debug print in simulate_losses for long runs survives the suite", "ledgers/M4/mutants/r10_01_debug_print_on_long_runs.py; course/modules/M/M4/project.html:204, 206; grader/test_project.py:278-284",
    "FAIL",
    f"{S}run_mutant_seeds.sh on r10_01, seeds 0-9: 132 passed / 133 passed on every seed; the print is never captured. project.html:204 says 'No function prints or warns' and :206 grades 'the absence of printed output'. test_no_function_prints only calls simulate_losses with 50 draws.",
    "Extend test_no_function_prints to call simulate_losses with the instance's N_DRAWS (both families) under capsys, and assert that out and err are empty.")
row("G-21", "NEW: debug print in matched_scale at nu = 3 survives the suite", "ledgers/M4/mutants/r10_03_matched_scale_debug_print_at_boundary.py; course/modules/M/M4/project.html:204, 206; grader/test_project.py:278-284",
    "FAIL",
    f"{S}run_mutant_seeds.sh on r10_03, seeds 0-9: passes every seed. test_matched_scale_is_nu_minus_two_over_nu and test_matched_scale_accepts_nu_just_above_two call matched_scale(3) without capsys, and test_no_function_prints calls matched_scale(5) only.",
    "Run matched_scale for each nu in range(3, 9) (and nu=3 explicitly) under capsys in test_no_function_prints and assert no output.")
row("G-22", "mutate_graders --unit M4 (all 98 mutants incl. the three new)", f"{S}mutate_M4.out; ledgers/M4/mutants/", "FAIL",
    "mutate_M4.out: 'FAIL (91/95 killed)' for the 95 existing mutants; with the 3 round-10 mutants 92 of 98 are killed. Survivors: m11, m17, v4_m02 and r9_03 (dispositions in the mutant list: accepted or not stated), r10_01 and r10_03 (G-20, G-21).",
    "Fix G-20 and G-21; then re-run mutate_graders --unit M4, whose only remaining survivors are the four dispositioned ones.")

# lab rows
row("L-01", "Project labs: run output, twins, page code", "tests/labs/M4/lab-M4-project-1.py, -2.py, -3.py", PASS,
    f"{S}labs_check.out: all three twins exit 0 under python -I -W error; each output equals its expected block; page code equals the twin except the two blanks of Lab 2.")
row("L-02", "Project lab page code vs twins (line level)", "course/modules/M/M4/project.html:58-135, 147-184, 269-301", PASS,
    "Lab 1 and Lab 3 page code equals the twin (modulo the final newline); Lab 2 differs only in the two blanks.")
row("L-03", "All M4 labs run", "tests/labs/M4/lab-M4-*.py", PASS,
    f"{S}run_labs.out: 'run_labs M4: PASS (13/13)', exit 0.")
row("L-04", "Carried from round 9 (tests/labs/M4/lab-M4-L10-1.py and course/modules/M/M4/L10.html:234-236 byte-identical since the previous pin; the L10 delta hunks are at lines 104, 117, 463, 488, 502 only): lab-M4-L10-1.py:60-65 vs L10.html:234-236", "tests/labs/M4/lab-M4-L10-1.py:60-65; course/modules/M/M4/L10.html:234-236", PASS,
    "Carried from round 9 (lab-M4-L10-1.py and L10.html:234-236 byte-identical since the previous pin): the lab's printed values are unchanged by this round, and run_labs.out (13/13) confirms the lab still runs.")

# cards
row("C-01", "cards.json structure", "course/modules/M/M4/cards.json", PASS,
    "Parses; 192 entries, 192 unique ids, no duplicate fronts or backs; grades T (171) and C (21); every C card carries a basis; ids run M4-c001 to M4-c192.")
row("C-02", "Cards agree with the current lesson text", "course/modules/M/M4/cards.json vs L01-L10.html", PASS,
    "Every changed card (c014, c029, c063, c085, c098, c101, c112, c124, c135, c186, c191, c192) was re-verified against the current lesson text: L01 Example 3.6 and Remark 3.3 (txt lines 141, 314), L02 Section 4 Misconceptions (c029), L04 Section 3 (c063), L06 Proposition 1.2 and Part A output (c085, c098), L07 Proposition 1.3 and Part A output (c101, c112), L08 Example 1.5 (c124), L09 Section 2 Assumption 1 and Problem R2 (c135), L05 Example 2.5 (c191), L10 Proposition 1.5(c) (c186). Cards on lessons not edited this round (L01, L02, L05-L08) are carried from round 9: card text and cited lesson text are byte-identical. Cards on L03, L04, L09 and L10 were checked against their edits: L03 is a variable rename in a proof, L04 is titles only, the L09 edit is a paragraph no card cites, and the L10 edits at lines 117, 463, 488 touch paragraphs no card cites.")
row("C-03", "Cards with specific checks: c014, c019, c119, c132, c137, c191", "course/modules/M/M4/cards.json (ids)", PASS,
    "c014 verified (L01 line 314, Remark 3.3); c119 verified by hand (AA^T=[[4,2],[2,2]], A^TA=[[5,1],[1,1]], B=AQ=[[0,-2],[1,-1]], BB^T=Sigma); c191 verified (L05 Example 2.5 Assumption 1); c019, c132, c137: carried from round 9 (cards and lesson statements byte-identical).")
row("C-04", "Grade C cards name a lab and its basis", "course/modules/M/M4/cards.json (grade C entries)", PASS,
    "All 21 C cards carry a basis naming Lab 1 Part, lab seed or 'numerical quadrature'; checked against the labs' printed lines where re-read (c098, c112 this round; c143, c167, c170 carried from round 9 with L09/L10 lab text unchanged except the L09 paragraph on standard error, which these cards do not cite).")
row("C-05", "Cards quoting lab numbers", "course/modules/M/M4/cards.json c098, c112, c191", PASS,
    "c098: 1.669114 / 1.666667 / 0.001469 (L06 lines 300-301, 452); c112: 7.11e-13 at t=2, 244.69193226 (L07 line 298); c191 basis matches Example 2.5 hypotheses.")
row("C-06", "Changed cards, individually", "course/modules/M/M4/cards.json (12 changed + c192)", PASS,
    "See C-02 for the lesson lines; c192 (new, grade T) verified: L01 line 314 gives Q(p)=1 exactly for p in (3/5, 4/5] from F(0)=3/5, F(1)=4/5 and Proposition 3.2; c186 matches L10 Proposition 1.5(c) (line 137) with L07 Proposition 1.3 and Assumption 1 present in L07.")
row("C-07", "Card numbers appear in their lesson", "course/modules/M/M4/cards.json", PASS,
    "Spot-checked changed-card numbers: 3/5 and 4/5 (L01 line 141), 1.669114 (L06 line 300), 244.69193226 (L07 line 298), 2/pi-type expressions unchanged; no card introduces a number absent from its lesson.")

# notation / DAG / process words / gates
row("N-01", "Notation vs notation/notation.json", "notation/notation.json; course/modules/M/M4/project.html; cards.json", PASS,
    "project.html uses \\nu, \\Sigma, \\Gamma, \\ell and the registered macro \\E; no registered symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R_f, \\Prob, \\Var, ...) takes a different meaning; cards use gamma_3/gamma_4 with the registered meaning (c037-c045).")
row("D-01", "DAG and concept closure, process words", "course/modules/M/M4/; check_dag", PASS,
    f"{S}check_dag.out: 'check_dag M4: PASS'. Project names Lessons 1, 2, 5 and 6 (brief, line 317; Lesson 6 Definition 2.1 and 2.5 at lines 211 and 326); all are in the unit closure per check_dag. No process words in project.html or cards.json (grep for verifier, builder, round, agent, ledger, batch, slice).")
row("T-01", "Relevant pytest files", "tests/test_memo_exemplars.py, tests/test_page_checks.py, tests/test_curriculum.py", PASS,
    "pytest -q -p no:cacheprovider on the three files: all tests pass, exit 0.")
row("GATE-01", "Gates: check_pages, check_dag, check_projects, page_smoke (project)", f"{S}check_pages.out, check_dag.out, check_projects.out, page_smoke_project.out", PASS,
    "check_pages M4: PASS; check_dag M4: PASS; check_projects M4: PASS; page_smoke project.html: PASS (all exit 0).")
row("GATE-02", "Gates: ruff, mypy, format", f"{S}ruff.out, mypy.out", PASS,
    "ruff check on course/modules/M/M4/grader and tests/labs/M4: All checks passed; ruff format --check on the same dirs: 17 files already formatted; mypy --no-incremental: no issues in 255 source files.")
row("GATE-03", "Gate: run_graders M4 (seeds 0-49) and verify_refs --offline", f"{S}run_graders.out, verify_refs.out", PASS,
    "run_graders M4: PASS (reference 50/50 seeds); verify_refs --offline: 560 entries, 0 problems, exit 0.")

mutant_counts = {"total": len(mutants), "killed": sum(1 for m in mutants if m.get("killed_by"))}
fragment = {
    "unit": "M4",
    "slice": "d",
    "round": 10,
    "verifier": "independent verifier (Haiku), not a builder of M4",
    "pin": "e8b10b8",
    "base": "b6865c7 (round-9 pin; previous fragment /Users/billyribeiro/.fanout/frags/B-M4-d.round9.json)",
    "checkout": str(ROOT),
    "scratch": "/tmp/M4-d-r10-scratch",
    "verified_at": "2026-10-29T04:50:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta b6865c7..e8b10b8 for slice d: project.html (9 hunks at old lines 149 Lab 2 hypothesis, 204 constraints, 206 grading mode, 216 Assumption 1 (w renamed u), 228 contract notes, 354/358/378 exemplar A numbers 2,100 to 2,130, 429 appendix A1-A3 (w renamed u)), cards.json (11 changed cards and c192 added), L03/L04/L09/L10/index.html (see C-02). Grader, instance, starter, labs and notation/references unchanged since the round-9 pin (git diff --stat). Lesson changes (L03, L04, L09, L10, index.html) were read for the cards and the project's citations.",
        "Full project.html read line by line this round (500 lines); full grader/test_project.py (511 lines), instance.py and starter.py read; cards.json read in full (192 cards).",
        "Round-9 FAIL rows P-08, P-18 and G-18 are repaired (project.html:204, 215, 228) and re-verified, not carried.",
        "Alternative correct implementations: 7 run on seeds 0-49, all pass. Stream order is not graded (project.html:204, 215), so the alternatives that change the draw order are not over-constrained.",
        "Observation, not a FAIL: appendix A2 (project.html:325) lists only 'assuming Assumption 1' for E[RR^T]=Sigma; the hypothesis nu > 2 that its proof needs is stated in A1 and in Conventions item 3, and the rubric's C2 level 3 chains through A1. The page could list nu > 2 explicitly in A2.",
        "Observation: the labs_check comparison is line-level; the page code of Labs 1 and 3 equals the twins modulo the final newline.",
        "Gate scope: check_pages, check_dag, check_projects, run_labs, run_graders, page_smoke (project), ruff, mypy, verify_refs and mutate_graders were run for M4 (not --all). Repo-wide suites were not run because they belong to other slices.",
    ],
    "summary": {"rows": len(rows), "pass": sum(1 for r in rows if r["status"] == "PASS"), "fail": sum(1 for r in rows if r["status"] == "FAIL"), "unverifiable": 0, "mutants_total": len(mutants), "mutants_killed": mutant_counts["killed"]},
}
out_path = ROOT / "ledgers/M4/M4-d.json"
out_path.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out_path, fragment["summary"])
