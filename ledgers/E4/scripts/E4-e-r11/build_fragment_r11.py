"""Round 11: write ledgers/E4/E4-e.json (slice e of unit E4, round 11) from the rows below.

Every row names the script or command output that backs it under ledgers/E4/scripts/E4-e-r11/. Run from the checkout
root. The ledger validator (tools/ledger.py, ledger.validate) is run afterwards by the verifier."""
import json
from datetime import datetime, timezone

PIN = "11d7077a290f7960b183d3a5a6631af4773888f9"
BASE = "00a84795f276456fce19d4181373cc4efba11a36"
S = "ledgers/E4/scripts/E4-e-r11/"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


CARDS = "course/modules/E/E4/cards.json"

row("E4-e-r4-cards-L01", "2.7-cards-vs-lesson (round 11, all 17 cards re-read)",
    f"{CARDS} E4-c001..c016, E4-c221 vs course/modules/E/E4/L01.html",
    "PASS",
    f"Every card read against the current L01 text (rendered by {S}html_to_text.py). Changed cards c001, c006, c016 match: "
    "Def 1.6 now says the vector q is called the Arrow-Debreu security price vector (c006 matches); Lab 1 checks the "
    "unequal probabilities once, at the start of main(), before Part A (tests/labs/E4/lab-E4-L01-1.py, c016 matches). "
    f"Numbers recomputed: 340/3, 56, 596/3 (2x-(1/2)y value = 200/2+50/3-60/4+485/5), 235/4, and the prices differ from "
    f"the probabilities in every state (c014). Twin output {S}lab_L01-1.out is unchanged from round 10.")

row("E4-e-r4-cards-L02", "2.7-cards-vs-lesson (round 11, all 24 cards re-read)",
    f"{CARDS} E4-c017..c038, E4-c237, E4-c238 vs course/modules/E/E4/L02.html",
    "PASS",
    f"All 24 cards read against current L02 text. Changed c024 (A5 is a hypothesis; the Section 4 example exhibits an "
    f"equilibrium) matches. Example 2.11 prices (1/8,1/32,1/16), demands (9/4,9/2,9/4), (7/4,7/2,7/4), residuals 0, "
    f"ratios 16/9 and 16/7 match {S}lab_L02-1.out. c037 value 1/8-1/32 = 3/32 recomputed. c035/c038 match Remark 2.10 and "
    f"Misconception 3. The L02 hunks (full-sharing sentence, A5 explain block) are cited by no card.")

row("E4-e-r4-cards-L03", "2.7-cards-vs-lesson (round 11, all 16 cards re-read)",
    f"{CARDS} E4-c039..c052, E4-c214, E4-c225 vs course/modules/E/E4/L03.html",
    "PASS",
    f"All 16 cards read against current L03 text. MRS 4, 2, 1/2 (c046) recomputed from x=(9/4,9/2,9/4) and equal the price "
    f"ratios; Lab 3 Part A and Part B match {S}lab_L03-1.out (0 improvements of the equilibrium on the 125-point grid, 2 of "
    f"the endowment, first witness (2,4,3)/(2,4,1)). c049 derivatives 1/12 and 1/4 recomputed from the R2 trade. New L03 "
    f"sentence (witness raises each utility by (1/4)ln(4/3)) equals 1/2 ln2 - 1/4 ln3 exactly; no card cites it.")

row("E4-e-r4-cards-L04", "2.7-cards-vs-lesson (round 11, all 33 cards re-read)",
    f"{CARDS} E4-c053..c073, E4-c215..c218, E4-c226..c228, E4-c234..c236, E4-c239, E4-c240, E4-c249 vs course/modules/E/E4/L04.html",
    "PASS",
    f"All 33 cards read against current L04 text. A0 block added in L04 (A0 real entries) is matched by c249 and by the "
    f"Lemma 2.1 cards c061, c215, c227, which now cite A0 as the lemma does. Lab 1 values match {S}lab_L04-1.out: ranks "
    f"2 and 3, completeness True/False, attainability True/False/False and augmented ranks 2, 3, 3 (c065). c058 now states "
    f"'otherwise incomplete' (Definition 1.3), which covers removed c248. Prop 4.2 cone wording (c069, c228) matches.")

row("E4-e-r4-cards-L05", "2.7-cards-vs-lesson (round 11, all 31 cards re-read)",
    f"{CARDS} E4-c074..c099, E4-c219, E4-c229, E4-c241..c243 vs course/modules/E/E4/L05.html",
    "PASS",
    f"All 31 cards read against current L05 text. Changed Def 1.2 sentence (conditional expectation is a function of z alone) "
    f"is consistent with c080. Lab 1 output {S}lab_L05-1.out matches c090-c094, c219, c243: c0*=4, c1*=-3/10, ratios -1/4; "
    f"sigma=beta path 0,5,0,5 with c0*=5/2; sigma=3 path 0,5,-5/2,35/4 with ratio -3/2; damped weight 4/5 gives (4,-3/10). "
    f"c098 unconditional mean c0* follows from A3 zero means (stated in the L05 misconception).")

row("E4-e-r4-cards-L06", "2.7-cards-vs-lesson (round 11, all 36 cards re-read)",
    f"{CARDS} E4-c100..c129, E4-c220, E4-c230, E4-c231, E4-c244, E4-c247, E4-c250 vs course/modules/E/E4/L06.html",
    "PASS",
    f"All 36 cards read against current L06 text. Changed cards c102, c104, c108, c109, c250 match the current definitions "
    f"(Def 6.6 with b and V_U from Lemma 6.4; Remark 6.5; Assumption G). Lab output {S}lab_L06-1.out: theta_s 3/7, theta_u 6/7, "
    f"sigma_eta^2 2, tau-bar 3/4, slope 7/9, posterior variance 2/3, x_I 1/7, 16 of 16 grid residuals zero, residual -9/85 at "
    f"theta_s=1/2 (recomputed by hand: b=49/67, V_U=85/134). x_U=-1/7 recomputed. SIMULATED c124/c125 values match Part E "
    f"(seed 6). Citation defect in the L06 proofs is a separate row.")

row("E4-e-r4-cards-L07", "2.7-cards-vs-lesson (round 11, all 21 cards re-read)",
    f"{CARDS} E4-c130..c150 vs course/modules/E/E4/L07.html",
    "PASS",
    f"L07.html is byte-identical to the round-10 pin, and all 21 cards were re-read. Lab output {S}lab_L07-1.out matches "
    f"c141-c146 (rho^2 1/3; sweep 4/9,1/3,1/6,1/18,1/66; Var(p) 729/1444 and 35937/4802; lambda sweep 1/6,1/3,9/22; a sweep "
    f"4/9,1/3,1/6; SIMULATED 0.330625 within 0.02 of 1/3). c136 basis now reads 'proof in Problem P3', and P3 of the L07 "
    f"problem set proves Remark 7.5. Misconceptions c147-c150 match the lesson's four misconceptions.")

row("E4-e-r4-cards-L08", "2.7-cards-vs-lesson (round 11, 42 of 43 cards; c155 separate)",
    f"{CARDS} E4-c151..c154, E4-c156..c188, E4-c222..c224, E4-c245, E4-c246 (all L08 cards except c155) vs course/modules/E/E4/L08.html",
    "PASS",
    f"42 cards read against current L08 text and {S}lab_L08-1.out. G(0)=ln2/4 and G(1)=ln(5/3)/4 recomputed from Def 4.3 "
    f"(lambda=1: Var(D_I)=1, V_I=1/2, Var(D_U)=2/3, V_U=5/6, ratio 5/3). Lab Part C: lambda* 0.657828572 with gap 1.83e-15 and "
    f"Corr^2 0.088941 at cost 0.15; boundary gaps 7.71e-03 and -6.71e-03 at costs 0.12 and 0.18. Part D: largest gain 0, no "
    f"interior equality. SIMULATED Part A: residual 1.332e-15, slope 0.1595 vs b_y/beta = 26/162 = 0.1605. c162/c163 "
    f"part labels (a) uniqueness and (b) p* clears match the proof text. Card c155 is a FAIL row (separate).")

row("E4-e-r4-cards-L09", "2.7-cards-vs-lesson (round 11, all 23 cards re-read)",
    f"{CARDS} E4-c189..c211, E4-c232 vs course/modules/E/E4/L09.html",
    "PASS",
    f"L09.html is byte-identical to the round-10 pin. All 23 cards read against the L09 text and {S}lab_L09-1.out (500 strict "
    f"bets at states 1 and 4, 0 nonnegative on the meet, 625 zero-posterior bets, 15625 bets). Changed c196 (Def 2.2 says "
    f"Theorem 2.1 says nothing about prices), c209 (Res 3: any union of cells) and c232 (cells of a partition) match the "
    f"text. Res 1 (c210) and Res 2 (c211) re-derived by hand and match the solutions. {S}rederive_r9_rerun.out: 79 checks, 0 failures.")

row("E4-e-r7-c154", "2.7-card-vs-current-lesson (carried from round 10)",
    f"{CARDS} E4-c154 vs course/modules/E/E4/L08.html Assumption A3",
    "PASS",
    "Carried from round 10 (L08.html and cards.json byte-identical for this card): the card's lambda in [0,1], informed "
    "observe s and p, and the clearing condition match the current A3 text (re-read this round).")

row("E4-e-r4-banned", "2.9-banned-phrases-and-process-words (round 11)",
    f"{CARDS} front, back and basis of all 244 cards; rendered lessons, project and index",
    "PASS",
    f"{S}banned_scan.py: banned-phrase hits 0 across the 11 rendered pages and every card field (BUILDER_RULES section 1). "
    "Process-word scan of the cards (round|builder|verifier|revised|previous|changed|fixed|we|I) found only the mathematical "
    "word 'fixed' and the subscript 'i'; no process words.")

row("E4-e-r4-check-pages", "2.9-structure-tools (round 11)",
    "tools/check_pages.py --all, tools/check_dag.py --all, tools/check_projects.py --all, tools/build_site.py --check",
    "PASS",
    f"{S}check_pages.out, {S}check_dag.out, {S}check_projects.out: all EXIT 0 (LX1, LX2, PC3 and E4 pages PASS). "
    f"{S}build_site_check.out: 'site data current: 6 outputs', EXIT 0.")

row("E4-e-r4-run-labs", "2.5-labs-printed-values (round 11)",
    "tests/labs/E4/lab-E4-L01-1.py .. L09-1.py, project-1..3; tools/run_labs.py --unit E4",
    "PASS",
    f"{S}run_labs_E4.out: 'run_labs E4: PASS (12/12)'. Each twin re-run alone under python -I -W error with EXIT 0 and "
    f"output saved (lab_L01-1.out .. lab_L09-1.out); outputs match the expected numbers on every card cited above.")

row("E4-e-r4-verify-refs", "2.1-citations-for-cards (round 11)",
    "tools/verify_refs.py --offline; references/references.json key muth1961rational (E4-c099)",
    "PASS",
    f"{S}verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems'. The references.json delta is only used_by "
    "lists and generated_at; muth1961rational is unchanged. Live check of c099 is in row E4-e-r11-muth-title.")

row("E4-e-r4-delta", "2.7-delta-read (round-10 pin to round-11 pin)",
    f"git diff {BASE[:7]}..{PIN[:7]} -- course/modules/E/E4 tests/labs/E4 references tools",
    "PASS",
    f"{S}card_delta.py: 243 old cards, 244 new; changed ids E4-c001, c016, c024, c055, c058, c061, c102, c104, c108, c109, c136, "
    "c155, c173, c179, c196, c209, c215, c227, c228, c232; new c249, c250; removed c248. Every changed lesson hunk was read "
    f"in the rendered diff (scratch/txt against scratch/old, L01, L02, L03, L04, L05, L06, L08, index, project) and assessed "
    "against every card that could cite it; grader and lab-project-3 hunks are outside this card slice and were read for "
    "the mutant analysis.")

row("E4-e-r7-new-cards", "2.7-new-cards (round 11)",
    f"{CARDS} E4-c249, E4-c250",
    "PASS",
    "c249 (A0 real entries) matches L04 Assumption A0 verbatim in substance; c250 (Remark 6.5: x_I, x_U, linear in (s,p)) "
    "matches L06 Remark 6.5. c248 removed; its content is in c058 (Definition 1.3, 'Otherwise the market is incomplete').")

row("E4-e-r7-ids-dups", "2.7-full-scan-duplicates (round 11)",
    f"{CARDS} (244 cards)",
    "PASS",
    "244 cards, 244 unique ids (card_delta.py and dump_cards.py). Lesson groups: L01 17, L02 24, L03 16, L04 33, L05 31, "
    "L06 36, L07 21, L08 43, L09 23 (sum 244).")

row("E4-e-r7-grades", "2.3-grades-on-cards (round 11)",
    f"{CARDS} grade and basis fields",
    "PASS",
    f"{S}card_numbers_r7_rerun.out: grades T 153, C 19, ungraded 72. The C cards are the lab-enumeration and SIMULATED items "
    "(c048, c122-c125, c141-c146, c181-c184, c188, c201, c214, c223) and match the lesson labelling of those items.")

row("E4-e-r7-numbers", "2.2-numbers-on-cards (round 11)",
    f"{CARDS} numbers on every card back",
    "PASS",
    f"{S}card_numbers_in_lessons.py: 453 numbers checked; 16 not found as plain text are LaTeX fractions present in the own "
    "lesson (c014, c016 1/8 and 3/8 etc.; c037 3/32 as \\tfrac{3}{32}; c048 1/4; c049 1/12 as \\tfrac{1}{12}; c051 9/4 etc.), "
    f"checked by hand. {S}card_numbers_r7_rerun.out: one flag (3/32) for the same reason. "
    f"{S}rederive_r8_rerun.out: SUMMARY checks 174 failures 0; {S}rederive_r9_rerun.out: checks 79 failures 0.")

row("E4-e-r7-notation", "2.7-notation-registry (round 11)",
    "notation/notation.json (8 registered symbols) vs E4 pages",
    "PASS",
    "notation.json registers T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f and blackboard Q. grep of the rendered E4 pages finds "
    "none of them in a symbol sense (the only 'T' matches are the word 'grade T'). The new local symbols in the changed hunks "
    "(b, V_U, P_U, Q, tau_eta', kappa') are defined in place, as notation.json's 'about' field allows for lesson-local letters.")

row("E4-e-r7-c185", "2.7-card-vs-current-lesson (round 7 FAIL, re-checked)",
    f"{CARDS} E4-c185 vs course/modules/E/E4/L08.html Proposition 5.1(a), Lemma 4.5, Problem Emp 3",
    "PASS",
    f"c185 back matches the current text. G(1) = ln(5/3)/4 recomputed in the Lab row above; G(0) = ln(2)/4 by Lemma 4.5.")

row("E4-e-r9-cards-L02-changed", "2.7-card-vs-current-lesson (changed or new cards, L02)",
    f"{CARDS} E4-c017, E4-c030, E4-c036, E4-c237, E4-c238",
    "PASS",
    "Re-read against the current L02 text; numbers recomputed (q* = (1/8,1/32,1/16), q*.ebar = 1, w_i = theta_i, Misconception 2 "
    "wording unchanged).")

row("E4-e-r9-cards-L04-changed", "2.7-card-vs-current-lesson (changed or new cards, L04)",
    f"{CARDS} E4-c226, E4-c228 (changed); E4-c053, c061, c066, c215, c239, c240 (carried)",
    "PASS",
    "Re-read against the current L04 text. c226 (augmented rank) and c228 (convex cone, Prop 4.2) match; c061 and c215 cite A0.")

row("E4-e-r9-cards-L05-changed", "2.7-card-vs-current-lesson (changed or new cards, L05)",
    f"{CARDS} E4-c077, c093, c095, c099, c241, c242, c243",
    "PASS",
    "Re-read against the current L05 text and lab output; c243 ratio -3/2 and c093 path 0,5,-5/2,35/4 match lab_L05-1.out.")

row("E4-e-r9-cards-L06-changed", "2.7-card-vs-current-lesson (changed or new cards, L06)",
    f"{CARDS} E4-c121, c124, c125, c220, c244, c247",
    "PASS",
    "Re-read against the current L06 text; Remark 6.10 (Y = v + eta, eta = eps - kappa u) and the SIMULATED values match.")

row("E4-e-r9-cards-L08-changed", "2.7-card-vs-current-lesson (changed or new cards, L08)",
    f"{CARDS} E4-c165, c169, c181, c223, c245, c246 (and c179, c182, c183, c184, c187, c188, c222, c224 re-read)",
    "PASS",
    f"Re-read against current L08 text and {S}lab_L08-1.out; the changed Proposition 5.2 and A4 wording matters to c179 and "
    "is checked there (no FAIL from that hunk except the A4 status card, which has its own row).")

row("E4-e-r9-cards-L08-re-read", "2.7-card-vs-current-lesson (L08 cards whose cited text changed nearby)",
    f"{CARDS} E4-c179, c182, c183, c184, c187, c188, c222, c224",
    "PASS",
    "Re-read. c179 (Proposition 5.2(c) conditional on A4; uniqueness not shown) matches the current text that says 'The interior "
    "root is not shown to be unique'. Lab numbers match lab_L08-1.out.")

row("E4-e-r9-cards-L09-counts", "2.5-lesson-counts-on-cards (round 11)",
    f"{CARDS} E4-c201, E4-c203, E4-c204, E4-c232 (c233 absent)",
    "PASS",
    f"Counts 500, 0, 625, 15625 match {S}lab_L09-1.out. 5 x 5^3 = 625 recomputed. E4-c233 is absent from the file.")

row("E4-e-r8-rederive", "2.2-numbers-rederived (round-8 and round-9 rederivation scripts rerun)",
    "ledgers/E4/scripts/E4-e-r8/rederive_r8.py; ledgers/E4/scripts/E4-e-r9/rederive_r9.py",
    "PASS",
    f"Both re-run this round with python -I: {S}rederive_r8_rerun.out SUMMARY checks 174 failures 0; "
    f"{S}rederive_r9_rerun.out SUMMARY checks 79 failures 0.")

row("E4-e-r8-cited-labels", "2.7-cards-cite-existing-results (round 11)",
    f"{CARDS} basis and text labels vs the lesson headings",
    "PASS",
    "Every basis label read against the lesson's own results (Lemma, Proposition, Corollary, Remark, Definition, Lab part, "
    "Problem) for the 244 cards: each named item exists in its lesson, including Remark 7.5 / Problem P3 (c136), "
    "Corollary 2.4(b) (c160), and Lemma 6.3 (c111).")

row("E4-e-r8-lab-claims", "2.5-lesson-claims-about-labs (round 11)",
    f"course/modules/E/E4/L08.html Lab 1 Part C values; L06.html Lab 1 Part C grid; L07.html Lab 1 Part F",
    "PASS",
    f"{S}lab_L08-1.out: lambda* 0.657828572 at cost 0.15 and the Part C values quoted in the lesson; {S}lab_L06-1.out: 16 of 16 "
    f"grid residuals zero, including (1,0); {S}lab_L07-1.out: Part F sample 0.330625 within tolerance 0.02.")

row("E4-e-r10-gates", "2.9-tool gates (round 11)",
    "ruff check and ruff format --check (tests/labs/E4, course/modules/E/E4/grader); mypy --no-incremental; run_graders E4",
    "PASS",
    f"{S}ruff_check.out: 'All checks passed!'; {S}ruff_format.out: '16 files already formatted'; {S}mypy_strict.out: 'Success: no "
    f"issues found in 385 source files'; {S}run_graders_E4.out: 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.2 s)'.")

row("E4-e-r10-grader-collect", "2.6-project-test-count (round 11)",
    "course/modules/E/E4/grader/test_project.py vs course/modules/E/E4/project.html 'runs 43 checks'",
    "PASS",
    f"{S}collect_grader.sh (reference copied as solver.py in a scratch dir outside the checkout): '43 tests collected'; "
    "project.html states 'runs 43 checks'.")

row("E4-e-r10-grader-new-test", "2.6-new-grader-test and its docstring numbers (round 11)",
    "course/modules/E/E4/grader/test_project.py (the tiny-root accuracy test and its docstring)",
    "PASS",
    "The docstring's numbers (noise volume at least 1e-50, tau-bar at least 1e-2) are the Constraints numbers of project.html. "
    f"The reference passes 50/50 seeds ({S}run_graders_E4.out) and the five alternatives pass 50/50 each.")

row("E4-e-r10-alternatives", "2.6-alternative-correct-implementations (round 11)",
    "ledgers/E4/alternatives/alt_1.py .. alt_5.py run as solver.py under the suite, seeds 0-49",
    "PASS",
    f"{S}alternatives_seeds.sh and {S}alternatives_seeds0-49.out: alt_1 50/0, alt_2 50/0, alt_3 50/0, alt_4 50/0, alt_5 50/0 "
    "(passed/failed).")

row("E4-e-r10-mutants-existing", "2.6-mutation (full E4 set, round 11)",
    "tools/mutate_graders.py --unit E4 over ledgers/E4/mutants (83 files)",
    "FAIL",
    f"{S}mutate_E4_r11.out: 'mutate_graders E4: FAIL (82/83 killed)'. The sole survivor is "
    "mutant_r10_02_cost_factor_relative_error.py (see E4-e-r10-mutant-r10-02). All other 82 mutants, including the three "
    "new round-11 mutants (E4-e-r11-new-mutants), are killed.",
    fix="Make the one survivor fail: add an interior-gap oracle check at relative tolerance 1e-14 (the mutant deviates by "
        "1.56e-12 relative at interior fractions; see survivor_probe.py), or reword project.html line 'works in floating point "
        "at full precision' and move the mutant to ledgers/E4/equivalent/ with a proof.")

row("E4-e-r10-mutant-v9-02", "2.6-mutation (survivor of round 10, re-verified)",
    "ledgers/E4/equivalent/mutant_v9_02_stop_rule_relative_to_lower_end.py; course/modules/E/E4/project.html Constraints",
    "PASS",
    "The round-10 survivor is no longer in mutants/ (moved to equivalent/ with a README argument). project.html Constraints now "
    "says 'its stop rule and its number of steps are yours to state' (rendered text line 318), so no stated stop rule is "
    f"violated. The lower-end variant's error is at most 0.16 of the allowed tolerance on 60 random interior instances in the "
    f"page's domain ({S}stop_rule_domain_probe.py), the same as the reference. Note: the model-answer paragraph at project.html "
    "line 618 describes the upper-end rule; it is an exemplar description, not a requirement.")

row("E4-e-r10-mutant-r10-02", "2.6-mutation (new survivor, round 10, still surviving)",
    "ledgers/E4/mutants/mutant_r10_02_cost_factor_relative_error.py vs course/modules/E/E4/project.html Constraints 'works in floating point at full precision'",
    "FAIL",
    f"{S}mutate_E4_r11.out: SURVIVED (no test fails). {S}survivor_probe.py: largest relative deviation from the reference "
    "1.564e-12 in the interior gap and 1.582e-12 in the interior root. The round-10 probe ledgers/E4/scripts/E4-e-r10/interior_oracle_check.out "
    "shows the reference within 1e-15 of the oracle at interior fractions and a cost-factor shift of 2.1e-13 for this mutant, so an oracle check at 1e-14 separates them. project.html states the solver 'works in floating point "
    "at full precision' and gives 1e-14 only at fraction 0, so the 1e-12 cost-factor error is a stated-behaviour violation the "
    "suite does not catch.",
    fix="Add to test_project.py an interior check: for a fraction strictly between 0 and 1, the reported gap must agree with the "
        "oracle gap to within 1e-14 relative to max(1, |gap|) (the reference passes it; the mutant fails it), and rerun the "
        "mutation gate.")

row("E4-e-r10-new-mutants", "2.6-new-student-error-mutants (round 10)",
    "ledgers/E4/mutants/mutant_r10_01_gap_zero_offset_1e-13.py, mutant_r10_03_cost_factor_missing_risk_aversion.py",
    "PASS",
    f"{S}mutate_E4_r11.out: both KILLED (r10_01 gap offset by 1e-13 at fraction 0; r10_03 exp(c) for exp(a c)).")

row("E4-e-r10-index-claims", "2.5-labs-arithmetic-claims (index.html hunks)",
    "course/modules/E/E4/index.html lines for 'Data:' and 'No real data' (labs and Fraction/float parts)",
    "PASS",
    "Index claims: L01, L02, L04, L05, L06 (Parts A-D), L07 (Parts A-E), L09 and L03 Part A use Fraction arithmetic; L03 Part B "
    "and L08 Parts B-D use double precision; L06 and L07 Part E/F add one SIMULATED seeded draw. Checked in "
    "tests/labs/E4/lab-E4-L06-1.py (float only in ols and Part E, lines 109 and 175-205) and lab-E4-L07-1.py (float only in "
    "Part F, lines 161-190), and by the L03 and L08 twins' float use.")

row("E4-e-r10-project-hunks", "2.2-numbers-on-project-page (changed hunks in this round)",
    "course/modules/E/E4/project.html: interface sentence (rendered line 229), Constraints (231, 318), starter comments (265, 277)",
    "PASS",
    "Changed hunks re-read. Interface and starter comments name TOLERANCE and the 200-halving cap, not a stated stop rule. "
    "Arithmetic: 2^200 is about 1.6e60, so 200 halvings reach 1e-12 times the root for roots above about 6.2e-49, which "
    "matches 'about 6e-49' in the starter comment. The Constraints line 231 now carries the 1e-10 / 1e-8 accuracy requirement "
    f"and the 1e-14 requirement at fraction 0, both checked in {S}survivor_probe.py and {S}stop_rule_domain_probe.py.")

row("E4-e-r10-L06-lemma-normality-citation", "2.1-proof-citations (Lemma 6.3, Lemma 6.4 and A1 statement; carried, still present)",
    "course/modules/E/E4/L06.html line 62 (A1: 'Hence (v, s, u) is jointly normal'), line 143 (Lemma 6.3 proof: '(e, s, u) is jointly normal by A1'), line 157 (Lemma 6.4 proof: 'a linear image of (v, s, u), so it is jointly normal by A1')",
    "FAIL",
    "All three steps are linear images of the A1 vector (v, eps, u), so their joint normality needs G(i) (linear image of a jointly "
    "normal vector is jointly normal), and A1 alone does not give it. The lesson's own Assumption G states that fact, but the three "
    "sentences cite only A1. The text is unchanged since the round-10 pin, so the round-10 defect stands.",
    fix="In L06.html line 62 change 'Hence (v, s, u) is jointly normal' to 'Hence (v, s, u) is jointly normal by A1 and G(i)'; "
        "at line 143 change 'is jointly normal by A1' to 'is jointly normal by A1 and G(i)'; at line 157 change "
        "'so it is jointly normal by A1' to 'so it is jointly normal by A1 and G(i)'. Then re-run embed/build checks.")

row("E4-e-r10-uncited-hunks", "2.7-changed-hunks-no-card (round 11)",
    "L01, L02, L03, L04, L05, L06, L08 hunks, index.html, project.html (rendered diffs)",
    "PASS",
    "Every changed hunk was read and tested against every card that could cite it. The L02 full-sharing sentence, A5 explain "
    "block, the L03 witness sentence, the L04 A0 block and Lemma 2.1 wording, the L05 Def 1.2 sentence, the L06 Why-it-matters "
    "and Cor 6.8 proof sentences, the L08 Prop 5.2 and A4 wording (A4 status is a separate FAIL row), and the index hub text "
    "are cited by no card that becomes wrong. The one card that cites A4 status is E4-c155.")

row("E4-e-r11-changed-cards", "2.7-card-vs-current-lesson (every changed, new or removed card id)",
    f"{CARDS} E4-c001, c016, c024, c055, c058, c061, c102, c104, c108, c109, c136, c173, c179, c196, c209, c215, c227, c228, c232, c249, c250 (new); c248 (removed)",
    "PASS",
    "Each changed card was re-read against the current lesson it cites (E4-c155 is the only exception; see its row). Changed "
    "cards agree with the text: c001 (def 1.1 wording), c016 (Lab 1 probability check), c024 (A5 hypothesis), c055 and c236 "
    "swapped positions with the same content, c058 ('Otherwise the market is incomplete'), c061 (Assume A0, Lemma 2.1), "
    "c102, c104, c108, c109 (Def 6.6 with b and V_U), c136 (Problem P3), c173 (paradox as defined), c179 (A4 conditional), "
    "c196 (Def 2.2), c209 (Res 3), c215, c227, c228 (A0 and Prop 4.2 wording), c232 (partition cells), c249 (A0), c250 "
    "(Remark 6.5). c248 removed; c249 and c250 added.")

row("E4-e-r11-cards-L08-A4-status", "2.7-card-vs-current-lesson (changed card, L08 Assumption A4)",
    f"{CARDS} E4-c155 back vs course/modules/E/E4/L08.html line 320 ('This is assumed here, in both parts. Part (i) holds on (0, 1] by the closed form ... at 0 it is the limit in Proposition 5.2(a), which this page proves ... The page does not prove part (ii) from earlier results.')",
    "FAIL",
    "The card says 'A4 is assumed, not proved from earlier results', which applies the 'not proved' status to both parts. The "
    "current lesson says A4 is assumed in both parts, that part (i) is proved on (0,1] by the closed form and at 0 by "
    "Proposition 5.2(a), and that only part (ii) is not proved from earlier results. The card's 'A4 is assumed' is right; its "
    "'not proved from earlier results' is not right for part (i).",
    fix="Replace the card back with: 'A4 is assumed here, in both parts. Part (i), continuity, is proved on (0, 1] by the closed "
        "form and at 0 by Proposition 5.2(a). Part (ii), the sign-change zero, is not proved from earlier results.'")

row("E4-e-r11-new-mutants", "2.6-new-student-error-mutants (round 11, three of my own)",
    "ledgers/E4/mutants/mutant_r11_01_cost_factor_first_order_taylor.py, mutant_r11_02_zero_limit_drops_cost_factor.py, mutant_r11_03_price_precision_is_signal_precision.py",
    "PASS",
    f"Generated from grader/reference.py by {S}make_r11_mutants.py (one edit each; the edited text is asserted to occur once). "
    f"{S}mutate_E4_r11.out: all three KILLED (r11_01 and r11_02 by test_info_cost_above_one_is_accepted; r11_03 by "
    "test_informativeness_is_the_squared_correlation).")

row("E4-e-r11-page-smoke", "2.9-page_smoke (round 11, E4 pages alone)",
    "tools/page_smoke.py --unit E4",
    "PASS",
    f"{S}page_smoke_E4.out: 'page_smoke E4: PASS' (index, L01-L09, project, EXIT 0).")

row("E4-e-r11-pytest-labs", "2.5-pytest-lab-twins (round 11)",
    "tests/test_labs.py and tests/test_run_labs.py, -k E4",
    "PASS",
    f"{S}pytest_labs_E4.out: 13 tests passed, EXIT 0.")

row("E4-e-r11-muth-title", "2.1-citation-live-check (E4-c099, muth1961rational)",
    "references/references.json muth1961rational; card E4-c099",
    "PASS",
    "Live plain-curl check of https://api.crossref.org/works/10.2307/1909635 returns title 'Rational Expectations and the Theory "
    "of Price Movements', Econometrica, volume 29, issue 3, page 315, 1961. The card's statement (the phrase appears in the title; "
    "only the title is used) matches.")

mutants = [
    {"id": "mutant_r11_01_cost_factor_first_order_taylor.py",
     "description": "Student shortcut: exp(a c) replaced by 1 + a c in the gap at 0 and at a fraction.",
     "killed_by": "test_info_cost_above_one_is_accepted (seed 0)"},
    {"id": "mutant_r11_02_zero_limit_drops_cost_factor.py",
     "description": "Student error: the gap at fraction 0 forgets the information cost factor exp(a c).",
     "killed_by": "test_info_cost_above_one_is_accepted (seed 0)"},
    {"id": "mutant_r11_03_price_precision_is_signal_precision.py",
     "description": "Student error: the uninformed precision tau_y is the signal precision tau_e, not the price-signal precision.",
     "killed_by": "test_informativeness_is_the_squared_correlation[first] (seed 0)"},
    {"id": "mutant_r10_02_cost_factor_relative_error.py",
     "description": "Scales exp(a c) by 1 + 1e-12 at every fraction (round-10 mutant, survives the suite).",
     "killed_by": None},
]

fragment = {
    "unit": "E4",
    "slice": "e",
    "round": 11,
    "verifier": "independent verifier (Haiku 5.5), unit E4, slice e: all 244 cards in course/modules/E/E4/cards.json against L01-L09, project, index, grader (round 11)",
    "pin": PIN,
    "base": BASE + " (round-10 pin; delta 00a8479..11d7077 read for the E4 slice)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE11-E4-e",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyE11-E4-e/scratch/txt (rendered lesson text, not committed; reproduced by ledgers/E4/scripts/E4-e-r11/html_to_text.py)",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "All 244 cards were re-read against the current lessons this round (L01-L09). Lesson text, labs and grader were re-run.",
        "Lab twins re-run alone under python -I -W error: L01-L09 all exit 0; outputs saved under ledgers/E4/scripts/E4-e-r11/.",
        "Mutation gate: 82/83 killed; the one survivor is mutant_r10_02 (FAIL row). mutant_v9_02 is in ledgers/E4/equivalent/ and is accepted as output-equivalent on the page's domain.",
        "Not checked: the full project grader against the solver of any other student; the hub and project prose beyond the changed hunks (other slices); live Crossref for references other than muth1961rational.",
        "The 16 numbers flagged by the naive number scan are LaTeX-form fractions present in the lessons; checked by hand.",
    ],
    "summary": "",
}
fail = [r for r in rows if r["status"] != "PASS"]
passed = [r for r in rows if r["status"] == "PASS"]
fragment["summary"] = (
    f"Cards 244 (T 153, C 19, ungraded 72). Rows: total {len(rows)}, PASS {len(passed)}, FAIL {len(fail)}. "
    "FAIL rows: E4-e-r11-cards-L08-A4-status (card E4-c155, A4 status overstated), E4-e-r10-L06-lemma-normality-citation "
    "(A1 cited for linear-image joint normality at L06.html lines 62, 143, 157), E4-e-r10-mutant-r10-02 and "
    "E4-e-r10-mutants-existing (surviving cost-factor mutant, 1.56e-12 relative deviation at interior fractions). "
    "Mutation 82/83 killed. Verdict FAIL."
)

with open("ledgers/E4/E4-e.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("wrote ledgers/E4/E4-e.json rows", len(rows), "fail", len(fail))
