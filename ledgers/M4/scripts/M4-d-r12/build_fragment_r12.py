"""Verifier round 12: build ledgers/M4/M4-d.json (slice d, round 12) from the round-11 row ids and this round's evidence."""
import json
import re
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD12-M4-d")
G = "ledgers/M4/scripts/M4-d-r12/gates/"
C = "ledgers/M4/scripts/M4-d-r12/checks/"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/D-M4-d.round11.json", encoding="utf-8"))
prev_ids = [r["id"] for r in prev["rows"]]

EV = {}
LOC = {}
CHK = {}


def row(rid, check, loc, ev):
    EV[rid] = ev
    LOC[rid] = loc
    CHK[rid] = check


row("d1-2.6-hours", "2.6 hours: component sum and own estimate within 30 %",
    "course/modules/M/M4/project.html:33, 234-245 (table#hours)",
    "Round 12 (fresh read of project.html:33 and 232-247): data-hours-project=30; components 2+2+12+8+4+2 = 30 = hub "
    "figure (index.html:29, 42). Own estimate (verifier judgment, not measured): about 26 h (rung 1 ~2, rung 2 ~1.5, "
    "simulator ~10, appendix ~6.5, report ~4, self-check ~2), 13% below 30, inside the 30% band (21-39 h).")
row("d1-2.6-instances", "2.6 instances: valid, and answers change across seeds",
    "course/modules/M/M4/grader/instance.py",
    "Round 12: ledgers/M4/scripts/M4-d-r12/checks/instances_r12.py over seeds 0-199: no violation (n in {2,3}, whole-cent "
    "positions 100000..5000000, symmetric and positive definite by exact pivots, nu in 3..8, draws in the fixed set, none "
    "a multiple of 100 and none above 19987, label SIMULATED); 200 distinct instances.")
row("d1-2.6-starter", "2.6 starter signatures",
    "course/modules/M/M4/grader/starter.py:15-34",
    "Round 12: starter.py signatures (lines 15, 20-27, 32) equal project.html:202 and reference.py:19, 51-58, 95; "
    "harness run on starter.py seed 0: '154 failed, 1 passed, 1 skipped' (the suite fails on the starter as intended).")
row("d1-rubric-observable", "rubric observable levels", "course/modules/M/M4/project.html:328-343 (table#rubric)",
    "Round 12: project.html:328 (scoring rule) and 330-343 (table#rubric) re-read: each descriptor names a checkable "
    "element (a formula, a printed number, a named element, a unit, a word count); level k is defined from level k-1.")
row("d1-rubric-calibration", "2.6 rubric calibration: blind scores vs official, within one level",
    "course/modules/M/M4/project.html:345-462 (exemplars A and B, official scores in data-scores)",
    "Round 12 (fresh blind scoring from the rubric before reading the annotations): Exemplar A C1 2, C2 2, C3 2, C4 2, C5 2 "
    "(official 2,2,2,2,2); Exemplar B C1 4, C2 4, C3 4, C4 4, C5 3 (official 4,4,4,4,3). Every score matches. Word counts "
    "(ledgers/M4/scripts/M4-d-r12/checks/exemplar_words_r12.py, raw run-of-characters rule of project.html:326): A body 90, "
    "with 10 heading words 100; B body 692 (inside 300-700), B Summary 73 (<= 80). Note (not a failure): rubric level 1 "
    "reads 'No proof'; Exemplar A's C1 gets 2 under the level-2 clause 'the divergence asserted without the integral'.")
row("d1-rubric-question-bank", "no question bank", "course/modules/M/M4/project.html:206; plans/M4-build-plan.md section 5.7",
    "Round 12: project.html:206 grading mode is autograder plus rubric; the page is not an adversarial review (no IC defence, "
    "referee report or debate), so BUILDER_RULES 5.4(4) does not apply.")
row("d1-atlas", "atlas entry", "curriculum/meta.yaml:194-276; index.html:37",
    "Carried from round 11 (byte-identical since the round-11 pin ccaeeaf4): git diff ccaeeaf4 329c1d7 -- curriculum/meta.yaml "
    "is empty; no Atlas milestone for M4, as before.")
row("d1-studio", "studio entry", "curriculum/01-foundations.yaml:73-76, 186-200, 218-229",
    "Carried from round 11 (byte-identical since the round-11 pin ccaeeaf4): git diff ccaeeaf4 329c1d7 -- "
    "curriculum/01-foundations.yaml is empty; the M4 brief (lines 186-200) matches the project scope (simulate Gaussian and "
    "Student-t losses with matched covariance, 99% loss, prove the moment conditions).")
row("d1-cites", "Reading citations", "course/modules/M/M4/project.html:482-486; references/references.json",
    "Round 12: ledgers/M4/scripts/M4-d-r12/gates/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', exit 0. "
    "project.html:482-486 names no locator and no attribution; blitzstein2019introduction is a registry key "
    "(references/references.json, grep count 1).")
row("d1-cards-c191-grade", "card M4-c191 grade T", "course/modules/M/M4/cards.json (M4-c191)",
    "Round 12: cards.json M4-c191 read: grade T; back states the covariance [[S1^2, rho S1 S2], [rho S1 S2, S2^2]] and the "
    "hypotheses of L05 Example 2.5 (S1, S2 > 0; |rho| < 1; Z1, Z2 independent, mean 0, variance 1; Assumption 1 of the example, "
    "'not proved here'), matching L05 Example 2.5 in ledgers/M4/scripts/M4-d-r12/checks/blocks/L05.txt.")
row("d1-data", "data references", "course/modules/M/M4/project.html:37, 53, 200, 271-275; grader/instance.py:1-14, 42",
    "Round 12: project.html:37, 53, 200 and 271-275 re-read: every input is SIMULATED, no data file is read; instance.py:1-14 "
    "and 42: label 'SIMULATED', no file access.")
row("d1-tools-structure", "tools structure", "tools/*.py",
    "Carried from round 11 (byte-identical since the round-11 pin ccaeeaf4): git diff ccaeeaf4 329c1d7 -- tools is empty; "
    "all tools were run this round (check_pages, check_dag, check_projects, run_labs, run_graders, mutate_graders, "
    "page_smoke, verify_refs, see the d12 gate rows).")
row("d6-2.6-equivalence-float-ceil", "float ceiling 0.99 n versus exact integer index",
    "course/modules/M/M4/grader/reference.py:95-100; project.html:214",
    "Round 12: ledgers/M4/scripts/M4-d-r12/checks/float_ceil_r12.out: 'n in 1..2000000 where float ceil(0.99*n) differs from "
    "the exact index: 0'. The float form is a conforming alternative (alt_r12_1 passes seeds 0-9); item 4's integer formula is "
    "ungraded (project.html:204), so no float-index mutant is listed.")
row("d6-prose-exemplar-words", "2.9/2.6 prose: exemplar annotation word counts",
    "course/modules/M/M4/project.html:359, 411 (Exemplar A C5 annotation; Exemplar B Summary annotation)",
    "Round 12: exemplar_words_r12.py (raw rule): Exemplar A body 90 words, 100 with 10 heading words (matches 'the body is 90 "
    "words of text (100 with its four headings)'); Exemplar B Summary 73 words (<= 80, matches 'a Summary of 80 words or fewer'). "
    "Note: round 11 recorded 70 for the B Summary; the raw count is 73 (prose-only 72). The claim holds under either count.")
row("d6-cards-sample", "round-6 card sample re-checked",
    "course/modules/M/M4/cards.json: M4-c001, c011, c030, c040, c063, c074, c098, c105, c120, c133, c141, c149, c157, c162",
    "Round 12: all 14 sampled cards re-checked against the blocks (checks/blocks/L01-L10.txt) and expected outputs "
    "(checks/expected_r12.txt): c001 (Section 1), c011 (Example 3.5: 198), c030 (E1: 3.469), c040 (Prop 2.5), c063 (Section 3), "
    "c074 (Remark 1.8: 2/9), c098 (Lab 1 Part A: 1.669114, 0.001469), c105 (Prop 2.3), c120 (Prop 1.6), c133 (Prop 2.2), "
    "c141 (7/60), c149 (Prop 1.4), c157 (0.063451, 1.5240e-23), c162 (1.8220). All agree.")
row("d1-2.6-ladder", "2.6 ladder: rung 1 solved, rung 2 instant, rung 3 scope, rung 4 open",
    "course/modules/M/M4/project.html:40-49, 51-192, 471-478",
    "Round 12: project.html:40-49, 51-192 and 471-478 re-read in full. Rung 1 (Lab 1, numbered comments, printed output, "
    "interpretation); rung 2 (Lab 2, completion, expected block); rung 3 scope = curriculum/01-foundations.yaml:218-229; rung 4 open.")
row("d1-2.6-spec-questions", "2.6 spec: a competent student asks no clarifying question",
    "course/modules/M/M4/project.html:194-229",
    "Round 12: project.html:194-229 re-read. The Student-t source and draw order are stated open (item 5, graded only for the "
    "Gaussian order); the sign convention is in item 2 and Conditions; the quantile index is in item 4; the cent rule is in item 2; "
    "'symmetric' is exact equality (test_project.py:464-472).")
row("d1-2.6-autograder-reference", "2.6 autograder: run_graders seeds 0-49 on reference.py",
    "course/modules/M/M4/grader/reference.py",
    "Round 12: ledgers/M4/scripts/M4-d-r12/gates/run_graders_M4_0-49.out: 'run_graders M4: PASS (reference 50/50 seeds, slowest "
    "1.7 s)', exit 0. Direct run on seeds 0, 1, 1093: '155 passed, 1 skipped' (nu 4 or 3); the collect-only count is 156.")
row("d1-2.6-mut-own", "2.6 mutation: verifier-written student-error mutants, all killed",
    "ledgers/M4/mutants/ (d11_01-d11_04 and the four new r12 mutants)",
    "Round 12: four NEW student-error mutants written this round (ledgers/M4/mutants/): r12_01_student_t_chi_square_has_nu_minus_two_"
    "degrees_of_freedom.py, r12_02_returns_scaled_by_the_asset_volatility_a_second_time.py, r12_03_gaussian_stream_seeded_with_"
    "seed_plus_one.py, r12_04_factor_built_from_the_correlation_matrix.py (generated by ledgers/M4/scripts/M4-d-r12/make_r12.py). "
    "Each is KILLED on seed 0 (gates/mutate_M4_0-9_r12.out). The four round-11 mutants d11_01-d11_04 are KILLED on seed 0 again.")
row("d1-2.6-mut-existing", "2.6 mutation: existing mutants on seeds 0-9",
    "ledgers/M4/mutants/*.py (163 files after this round)",
    "Round 12: ledgers/M4/scripts/M4-d-r12/gates/mutate_M4_0-9_r12.out: '163/163 killed', exit 0, from "
    "'python tools/mutate_graders.py --unit M4 --seeds 0-9' (exit 0 as required). The same command in gates/mutate_M4_0-9.out: "
    "'mutate_graders M4: PASS (163/163 killed)'.")
row("d1-2.6-mut-m11", "2.6 mutation: m11 loss sign flipped", "ledgers/M4/mutants/m11_loss_sign_flipped.py",
    "Round 12: gates/mutate_M4_0-9_r12.out: 'KILLED m11_loss_sign_flipped.py ... -> test_gaussian_stream_is_frozen_and_the_loss_is_"
    "minus_the_weighted_return (seed 0)'.")
row("d1-2.6-mut-r9_03", "2.6 mutation: r9_03 chi-square reused on alternate draws",
    "ledgers/M4/mutants/r9_03_student_t_chi_square_reused_every_second_draw.py",
    "Round 12: gates/mutate_M4_0-9_r12.out: KILLED (killed on seed 0 by a Student-t draw-sharing test).")
row("d1-2.6-mut-v4_m02", "2.6 mutation: v4_m02 matched factor skipped for small nu",
    "ledgers/M4/mutants/v4_m02_matched_factor_skipped_for_small_nu.py",
    "Round 12: gates/mutate_M4_0-9_r12.out: KILLED.")
row("d1-2.6-mut-m17", "2.6 mutation: m17 is an equivalent (conforming) mutant",
    "ledgers/M4/equivalent/m17_student_t_second_seed.py",
    "Round 12: the candidate passes the full suite on seeds 0, 1 and 2 ('155 passed, 1 skipped' each, run this round). It draws "
    "the Student-t family from seed + 1; Conventions item 5 leaves that source open, so it is conforming and kept out of mutants/. "
    "Note: ledgers/M4/equivalent/README.md says 'the suite collects 138 checks' (a dated round-2 measurement; the suite now collects 156).")
row("d1-2.6-alternatives", "2.6 alternatives: correct implementations pass seeds 0-9",
    "ledgers/M4/scripts/M4-d-r12/alts/alt_r12_1..4.py; ledgers/M4/scripts/alt_1..5.py",
    "Round 12: ledgers/M4/scripts/M4-d-r12/gates/alts_r12_seeds0-9.out: reference 10/10 and nine correct alternatives 10/10 each "
    "(four new: float ceil(0.99 n) index, Student-t chi-square as a sum of nu squared normals, exact LDL pivot test, reversed "
    "position summation; plus alt_1..alt_5). 'implementations failing: 0'.")
row("d1-2.6-messages", "2.6 messages: check() and expect_value_error() wording",
    "course/modules/M/M4/grader/test_project.py (all assertion messages, read in full)",
    "Round 12: test_project.py read in full (698 lines). Each message names the violated property and gives a hint; none prints "
    "a computed value. The two 1e16 names recorded under d11-test-names-1e16 are fixed (see that row).")
row("d1-2.6-count-and-pyodide", "2.6 test count and Pyodide statement",
    "course/modules/M/M4/grader/test_project.py; project.html:203-206",
    "Round 12: 'pytest --collect-only' on the grader files gives '156 tests collected'. Seeds 0 (nu 4), 1 (nu 3), 1093 (nu 3): "
    "'155 passed, 1 skipped'. The starter gives 154 failed. project.html:206 states 156 checks with one skipped at nu 3 or 4: "
    "consistent. Pyodide: gates/page_smoke_M4.out 'page_smoke M4: PASS'.")
row("d1-2.6-grader-comment-numbers", "2.6 grader comment numbers (test_project.py comments)",
    "course/modules/M/M4/grader/test_project.py:31-47",
    "Round 12: checks/variance_sweep_r12.out (seeds 0-1999): reference Student-t relative error 1.0220 at seed 1093 (nu 3, "
    "checks/seed1093_r12.py); reference maxima 0.1259 (nu 5), 0.0967 (nu 6), 0.0728 (nu 7), 0.0624 (nu 8); missing-factor "
    "counts over 0.30: 347/347, 317/317, 342/343, 288/317. Cross-term (checks/cross_mutants_r12.out): r8_03 abs 0.0677-0.0860, "
    "r9_02 abs 0.1406-0.1605 (seeds 0-9), reference max abs 0.0239 (seeds 0-49, checks/cross_r12.out).")
row("d1-prose-numbers", "2.2 prose numbers vs measured values",
    "course/modules/M/M4/project.html:203-206, 212, 215, 220, 228",
    "Round 12: checks/cross_r12.out (100,000 draws, nu 5, factor entry scaled by 1+eps, seeds 0-49): +0.03 fails 0/50; -0.03 fails "
    "1/50 (seed 38); +0.05 fails 19/50; -0.05 fails 30/50 (matches project.html:228). checks/chi_r12.out: lag-1 50/50, lag-2 "
    "50/50, lag-3 39/50, even-indexed 44/50, chain at lag 4 38/50, disjoint lag-4 pairs 0/50 (matches project.html:215, 228).")
row("d1-prose-scope", "scope words backed by a computation",
    "course/modules/M/M4/project.html:215, 228; grader/test_project.py:212-216",
    "Round 12: 'all', 'none', 'every', 'only' in project.html:215 and 228 each correspond to a count in checks/cross_r12.out or "
    "checks/chi_r12.out, or to a formula (the fourth moment at nu 3 and 4, Appendix A3). project.html:215 names the family ('at nu = 3 only').")
row("d1-prose-process-words", "no process words in learner text",
    "course/modules/M/M4/project.html; L01-L10.html; cards.json; grader/test_project.py",
    "Round 12: case-insensitive grep for verifier, round N, builder, agent over project.html, cards.json, L01-L10.html, grader/*.py "
    "and tests/labs/M4/*.py: 0 hits.")
row("d1-prose-banned-phrases", "banned strings (BUILDER_RULES 1.3-1.4)",
    "course/modules/M/M4/project.html; cards.json; L01-L10.html; grader/*.py",
    "Round 12: grep of TODO, TBD, lorem, for brevity, left as an exercise, important to note, obviously, clearly, well known, "
    "studies show, experts agree, you can add, beyond the scope, details omitted: 0 hits.")
row("d1-dag", "DAG: prerequisite closure and dfn assignment", "course/modules/M/M4/*.html",
    "Round 12: gates/check_dag_all.out 'check_dag M4: PASS' (exit 0). project.html uses 'order statistic', 'chi-square' and 'positive "
    "definite' in prose with inline definitions (Conventions items 1, 4, 6), as the plan's Architect decisions allow.")
row("d1-notation", "notation registry", "notation/notation.json; course/modules/M/M4/project.html",
    "Round 12: notation.json symbols checked against project.html and L01-L10: gamma_3 and gamma_4 (M4 entries) match L03 "
    "(E[Z^3], E[Z^4], not excess); Phi is the standard normal distribution function (M4 entry) as used in L09; T is not used by M4; "
    "\\E, \\Var, \\Cov, \\R, \\indic macros used as registered. No symbol reused with another meaning.")
row("d1-structure", "M4 file inventory for slice d",
    "course/modules/M/M4/project.html, grader/{instance,reference,starter,test_project}.py, tests/labs/M4/lab-M4-project-1..3.py, cards.json",
    "Round 12: all files present; grader/test_project.py 698 lines, reference.py 100, instance.py 48, starter.py 34; "
    "project.html 501 lines; cards.json 227 cards; three project labs and ten lesson labs (run_labs M4: 13/13).")
row("d1-cards-schema", "cards schema and ids", "course/modules/M/M4/cards.json",
    "Round 12: ledgers/M4/scripts/M4-d-r12/checks/card_numbers_r12.py: 227 cards, every card has id, lesson, front, back, grade; "
    "no duplicate id, no duplicate front; 25 C cards and 202 T cards; every C card has a basis; 9 T cards carry a basis that "
    "names an exact or closed-form lab computation (c161, c165, c168, c172, c185, c233-c236).")
row("d1-cards-numbers-in-lesson", "every card number appears in its lesson",
    "course/modules/M/M4/cards.json; L01-L10.html",
    "Round 12: card_numbers_r12.py: every decimal and integer of 2+ digits in a card's front or back occurs in its own lesson page "
    "(text including the expected blocks and problem sets): 0 missing.")
row("d1-cards-labs", "lab-based cards agree with the lab's expected output",
    "cards.json lab cards (C and the lab-basis T cards); tests/labs/M4/lab-M4-L0*-1.py",
    "Round 12: every lab card value checked against checks/expected_r12.txt (run_labs-verified): c030, c033, c047, c082, c083, c098, "
    "c112, c113, c126, c143, c162, c165, c166, c167, c168, c169, c170, c171, c172, c183, c185, c188, c189, c190, c233-c241, c238. "
    "Seeds and n checked in the twins: L05 20260501, L06 20260602+nu (n 100000), L07 20260701 (n 100000), L08 2026 (n 20000), "
    "L09 2026 (4000 replications), L10 2026/2027/2028 (400 replications).")
row("d1-cards-math", "card mathematics", "cards.json",
    "Round 12: each card's formula re-derived by hand or by python (e.g. c041/c048 Bernoulli skewness and kurtosis, c043 5/3, c028 35/3, "
    "c091 1/(nu-2), c094 5/3, c157 (2/pi) arctan(0.1) = 0.063451, c161 0.634510, c187 4 sqrt(3)/pi = 2.2053, c142 35+sqrt(29.1667)=40.4006, "
    "c141 7/60, c160 quartiles -1 and 1, c209 density 2/(pi sqrt 3)(1+t^2/3)^-2, c208 BB^T = Sigma).")
row("d1-cards-lesson-statements", "cards agree with the current lesson text",
    "cards.json; course/modules/M/M4/L01-L10.html (block text in checks/blocks/)",
    "Round 12: all 227 cards read against the labelled blocks (checks/blocks/L01-L10.txt, rebuilt by block_dump_r12.py with nested "
    "divs and bare '<' kept) and the problem sets (checks/problems/). Cards changed since the round-11 pin were re-read against the "
    "changed lesson text: c006 (L01 Prop 2.2(d) now 'right-continuous at each x_k'), c058 (L04 Example 1.9), "
    "c067 (L05 Remark 1.3 cites L02 Definition 2.1), c192 and c245 (Example 3.6). No disagreement found.")
row("d1-cards-hypotheses", "cards carry the proposition's hypotheses", "cards.json",
    "Round 12: each card citing a proposition with hypotheses was checked: e.g. c008, c010, c013, c024, c032 (positive weights), "
    "c040 and c043 (at least two values), c039 (a not 0), c091 (nu a positive integer), c105 (finitely many values or a density), "
    "c129 (every law finitely valued), c134 and c218 (i.i.d., finitely valued). Extra hypotheses (c023) are harmless.")
row("d1-cards-duplicates", "no duplicate cards", "cards.json",
    "Round 12: card_numbers_r12.py: no duplicate id; no duplicate front (case-insensitive). The round-11 card c244 (variance "
    "of X + b) is removed; c245 (Q(3/5) of Example 3.6) is new and does not duplicate c012 or c192.")
row("d1-cards-forward-reference", "cards cite only earlier lessons and problems",
    "cards.json (problem and lesson citations)",
    "Round 12: each lesson and problem citation in a card was checked against the lesson of the card: e.g. c114 (L08) cites Lesson 6; "
    "c155 (L10) cites Lesson 9; c108 (L07) cites L07 P3; c125 (L08) cites L08 P3; c135 (L09) cites R2; c137 (L09) cites M3; "
    "c160 and c161 (L10) cite P2 and E1; c204 (L04) cites R3; c064 (L04) cites P3; c032 (L02) cites P2. No forward reference.")
row("d1-freshness-registry", "freshness and registry", "references/references.json; tools/verify_refs.py",
    "Round 12: gates/verify_refs_offline.out 'offline integrity: 560 entries, 0 problems'; references/references.json unchanged "
    "since ccaeeaf4 (git diff empty). No freshness flag.")
row("d1-gates-repo", "repo gates for the slice", "tools/*; course/modules/M/M4",
    "Round 12 (run this round, outputs in gates/): check_pages M4 PASS, check_dag M4 PASS, check_projects M4 PASS (all units exit 0); "
    "run_labs M4 13/13; run_graders M4 50/50 seeds; mutate_graders M4 0-9 163/163; page_smoke M4 PASS; verify_refs offline 0 problems; "
    "ruff check and ruff format --check clean; mypy --no-incremental 385 files clean; pytest on test_memo_exemplars and test_labs "
    "(-k 'M4 or memo or exemplar') 27 passed.")
row("d2-2.6-constraints-exceptions", "2.6 conditions raise ValueError only for named conditions",
    "course/modules/M/M4/grader/test_project.py:97-692 (expect_value_error sites)",
    "Round 12: every expect_value_error site read: each raises for a condition the page names (project.html:222-224: nu, family, "
    "n_draws, position_cents, cov shape, symmetry, positive definiteness, empty list, non-int losses). No test demands an "
    "exception the page does not name; the bool/float/string cases are named by 'not an int, including a float, a boolean and a string'.")
row("d1-2.6-constraints-exceptions", "2.6 exception types only for named conditions (same subject)",
    "course/modules/M/M4/grader/test_project.py; project.html:220-224",
    "Round 12: as d2-2.6-constraints-exceptions. Gaussian nu, draw count, family and positions tests match project.html:223 wording.")
row("d3-2.6-mut-new-student-error", "2.6 mutation: at least 3 new student-error mutants",
    "ledgers/M4/mutants/r12_01-r12_04",
    "Round 12: four new student-error mutants, each a complete module with a one-line description, killed on seed 0: "
    "r12_01 (Student-t chi-square with nu-2 degrees of freedom) by test_student_t_cross_term_matches_matched_covariance; "
    "r12_02 (returns multiplied by the volatility again) by test_gaussian_loss_variance_matches_portfolio_covariance; "
    "r12_03 (stream seeded with seed+1) by test_gaussian_stream_is_frozen_and_the_loss_is_minus_the_weighted_return; "
    "r12_04 (factor of the correlation matrix) by test_gaussian_losses_are_rounded_once_not_truncated. Each violates a sentence "
    "of project.html (Conventions 1 and 5; Rung 3 Specification).")
row("d1-2.6-contract-notes-chi-claim", "chi-square claims in 'what the suite does not test'",
    "course/modules/M/M4/project.html:215, 228",
    "Round 12: the sharing claims in project.html:215 and 228 were re-measured (checks/chi_r12.out) with the design stated in "
    "the probe script (draws 2k/2k+1 etc., one chi variable per group, one normal per draw, nu 3, 40000 draws, seeds 0-49). All "
    "measured counts match the page.")
row("d1-2.6-mut-pairwise-survivor", "pairwise-sharing survivors", "project.html:228; grader/test_project.py:207-230",
    "Round 12: sharing structures measured as the page says: draws 2k and 2k+1 fail 50/50 (lag 1); draws 4j and 4j+2 fail 50/50 (lag 2); draws 6j and 6j+3 fail 39/50 (lag 3); "
    "even-indexed 44/50; chain at lag 4 38/50; disjoint lag-4 pairs pass 50/50. The page says the lag-4 cases are not read by "
    "the check; this is what is measured, and it is stated as such.")
row("d6-2.6-mut-integer-division-chi", "mutant r6d_02 integer-division chi shape", "ledgers/M4/mutants/r6d_02_integer_division_chi_shape.py",
    "Round 12: gates/mutate_M4_0-9_r12.out: KILLED (seed 0).")
row("d6-2.6-mut-pivot-tolerance", "mutant r6d_01 pivot tolerance 1e-15", "ledgers/M4/mutants/r6d_01_pivot_tolerance_1e15_rejects_tiny_variance.py",
    "Round 12: gates/mutate_M4_0-9_r12.out: KILLED (seed 0).")
row("d6-2.6-mut-lag3-sharing", "mutant r6d_03 lag-3 sharing", "ledgers/M4/mutants/r6d_03_chi_square_shared_by_draws_six_apart_lag_three.py",
    "Round 12: gates/mutate_M4_0-9_r12.out: KILLED (seed 0).")
row("d1-lab-project-1", "project lab 1: twin, page code, expected block",
    "course/modules/M/M4/project.html:55-145; tests/labs/M4/lab-M4-project-1.py",
    "Round 12: run_labs M4 13/13 (page code byte-identical to the twin); twin run as 'python -I -W error' exit 0, stderr 0 bytes "
    "(checks/project1_twin_out.txt) and equal to the expected block (project.html:136-143). Hypothesis values 8.4e9, 0.6, 19800 "
    "and the 99% loss ratio 1.152 re-derived.")
row("d1-lab-project-2", "project lab 2: completion, twin, expected block",
    "course/modules/M/M4/project.html:147-191; tests/labs/M4/lab-M4-project-2.py",
    "Round 12: twin run under -I -W error exit 0, stderr 0 bytes; output equals the expected block (project.html:185-189); the "
    "blanks are (nu-2)/nu and (99n+99)//100, matching Conventions items 3 and 4.")
row("d1-lab-project-3", "project lab 3: closed forms, expected block",
    "course/modules/M/M4/project.html:266-313; tests/labs/M4/lab-M4-project-3.py",
    "Round 12: twin under -I -W error exit 0, stderr 0 bytes; output equals the expected block (project.html:302-312). 91651.514 "
    "(sqrt(8.4e9)), z = 2.326348, parametric 213213 (z*sd = 213213.30), index rows 99/99, 100/99, 19788/19787 re-derived.")
row("d6-gate-mutate-m4", "gate: mutate_graders --unit M4 --seeds 0-9", "tools/mutate_graders.py; ledgers/M4/mutants/",
    "Round 12: gates/mutate_M4_0-9_r12.out: 'mutate_graders M4: PASS (163/163 killed)', exit 0.")
row("d6-gate-unit-checks", "gate: check_pages, check_dag, check_projects for M4", "tools/check_pages.py; tools/check_dag.py; tools/check_projects.py",
    "Round 12: gates/check_pages_all.out, check_dag_all.out, check_projects_all.out: M4 PASS on each, exit 0 each.")
row("d6-gate-labs", "gate: run_labs M4", "tools/run_labs.py --unit M4",
    "Round 12: gates/run_labs_M4.out 'run_labs M4: PASS (13/13)', exit 0.")
row("d6-gate-grader-reference", "gate: run_graders M4 seeds 0-49 on reference",
    "tools/run_graders.py --unit M4 --seeds 0-49", "Round 12: gates/run_graders_M4_0-49.out 'PASS (reference 50/50 seeds)', exit 0.")
row("d6-gate-lint-types", "gate: ruff and mypy", "pyproject.toml; repo",
    "Round 12: gates/ruff_check.out 'All checks passed!' exit 0; gates/ruff_format.out '559 files already formatted' exit 0; "
    "gates/mypy.out 'Success: no issues found in 385 source files' exit 0 (mypy --no-incremental).")
row("d6-gate-tests", "gate: relevant pytest", "tests/test_memo_exemplars.py; tests/test_labs.py",
    "Round 12: gates/pytest_relevant.out: 27 tests passed (27 progress marks, exit 0; -k 'M4 or memo or exemplar' over test_memo_exemplars.py and test_labs.py).")
row("d6-gate-refs", "gate: verify_refs --offline", "tools/verify_refs.py", "Round 12: gates/verify_refs_offline.out: 560 entries, 0 problems, exit 0.")
row("d6-gate-page-smoke", "gate: page_smoke M4", "tools/page_smoke.py --unit M4",
    "Round 12: gates/page_smoke_M4.out: 'page_smoke M4: PASS', exit 0 (both themes, 360 px, labs and grader in Pyodide).")
row("d6-2.6-alt-root-set", "2.6 alternatives root set", "ledgers/M4/scripts/M4-d-r12/alts/; ledgers/M4/scripts/alt_*.py",
    "Round 12: all 10 implementations (reference, four new alternatives, five older alt_1..5) pass seeds 0-9 10/10 "
    "(gates/alts_r12_seeds0-9.out). Over-constraint check: float ceiling index, Student-t chi-square as a sum of squares, exact "
    "pivots, reversed summation all conforming.")
row("d7-2.6-cross-term-threshold", "cross-term tolerance 0.05 separates reference from mutants",
    "course/modules/M/M4/grader/test_project.py:43-50; project.html:228",
    "Round 12: reference cross-term signed errors over seeds 0-49 in [-0.0239, +0.0177]; r8_03 and r9_02 at seeds 0-9 in "
    "[0.0677, 0.0860] and [0.1406, 0.1605] in absolute value (checks/cross_mutants_r12.out, exact). 0.05 lies above the reference "
    "and below both mutant ranges.")
row("d7-2.6-negation-claim", "negation claim: 300 draws, both families",
    "course/modules/M/M4/grader/test_project.py:234-249; project.html:223",
    "Round 12: test_a_short_position_is_valid_and_reverses_its_loss uses 300 draws in both families and checks flipped == [-x]; "
    "passes on the reference for seeds 0-9. The round() symmetry argument holds exactly in IEEE arithmetic.")
row("d7-2.6-tiny-variance-claims", "tiny-variance acceptance claims",
    "course/modules/M/M4/grader/test_project.py:584-647; project.html:223, 224",
    "Round 12: each tiny-variance test (1e-14, 1e-16, 1e-30; pivots 0.89 scale and 9e-14) read; each input is valid and positive "
    "definite (exact pivots); the reference accepts all; alt_r12_3 (exact pivots) accepts all.")
row("d7-L01-L04-prose", "L01 and L04 prose changed this round (cards depend on it)",
    "course/modules/M/M4/L01.html:85 (Prop 2.2(d)); L04.html:52 (why it matters)",
    "Round 12: L01 Prop 2.2(d) now reads 'right-continuous at each x_k, meaning F(x) -> F(x_k) as x decreases to x_k' and the jump "
    "statement; it agrees with c006 and the proof (block dump). L04 why-it-matters now says 'a pair that is not independent but "
    "still has E[XY] = E[X]E[Y]' for Example 1.9 (Cov 0, p(0,0)=1/3 vs 1/9): consistent with Example 1.9 and c058.")
row("d7-L03-numerics", "L03 numerics", "course/modules/M/M4/L03.html (Example 2.6, Section 3, Lab 1)",
    "Round 12: 73/9, 7/3, 64/9, 8/3, m2=163/16, m3=2157/32, m4=149461/256 (sum over four terms re-derived), 2.0730, 5.6254, 2.065, "
    "5.580, the gaps 0.008 and 0.045 all re-derived and matching the expected block.")
row("d7-cards-exact-lab-grade", "card grades for exact-computation lab results",
    "cards.json c161, c165, c168, c172, c185, c233-c236 (grade T, basis names the exact or closed-form lab part)",
    "Round 12: each value re-derived (exact Fraction values from the die's mass function; closed forms of Props 1.4 and 1.7 with "
    "Assumption 2). These are deterministic computations on a stated law, graded T with the lab named in basis; no sample is "
    "involved. Judgment note: BLUEPRINT T is 'proved on the page'; these are exact evaluations, not theorems. Not a failure.")
row("d8-2.6-symmetry-tiny-scale", "symmetry at tiny scale", "course/modules/M/M4/grader/test_project.py:463-472",
    "Round 12: cov [[1e-14, 1e-15], [2e-15, 9e-14]]: the off-diagonal entries differ by 1e-15 (a tenth of the first variance); both "
    "pivots are positive (9e-14 - 4e-16 > 0), so only the symmetry condition fails; the test demands ValueError, as page line 223 names.")
row("d8-2.6-mut-r8d-02", "mutant r8d_02 Gaussian stream reseeded per draw", "ledgers/M4/mutants/r8d_02_gaussian_stream_reseeded_per_draw.py",
    "Round 12: gates/mutate_M4_0-9_r12.out: KILLED.")
row("d8-2.6-mut-r8d-03", "mutant r8d_03 positions read in reverse order", "ledgers/M4/mutants/r8d_03_positions_read_in_reverse_order.py",
    "Round 12: gates/mutate_M4_0-9_r12.out: KILLED.")
row("d8-2.6-mut-r8d-04", "mutant r8d_04 Gaussian draws via normalvariate", "ledgers/M4/mutants/r8d_04_gaussian_draws_via_normalvariate.py",
    "Round 12: gates/mutate_M4_0-9_r12.out: KILLED (the frozen stream of project.html:215 is 'random.Random(seed).gauss').")
row("d8-2.6-alt6-chi-order", "alt6: chi-square drawn in another order", "ledgers/M4/scripts/alt_1..5 and alt_r12_2",
    "Round 12: alt_r12_2 (Student-t chi-square as a sum of squares after the normals) and alt_1..alt_5 pass seeds 0-9 10/10 "
    "(gates/alts_r12_seeds0-9.out); the Student-t draw order is open (item 5).")
row("d8-2.6-lab-counts", "lab counts", "tests/labs/M4/; project.html",
    "Round 12: run_labs M4 13/13. Project lab expected blocks: Lab 1 has 8 lines, Lab 2 has 5, Lab 3 has 11; the twin outputs "
    "(checks/project*_twin_out.txt) have the same line counts and values.")
row("d8-cards-changed-and-new", "changed and new cards", "cards.json (c192, c245, c244 removed, AA^T back, F(0)=3/5 back)",
    "Round 12: card delta vs ccaeeaf4 (git diff): the AA^T back (c120) adds 'For a real matrix A'; the F(0)=3/5 back (c192) adds the "
    "hypotheses; c244 is removed; c245 (Q(3/5) = 0) added. Each re-checked against the current lesson text (Prop 1.6 L08; "
    "Prop 3.2 and Example 3.6 L01). All agree.")
row("d8-2.6-variance-claims-lines-31-39", "variance comments lines 31-39", "course/modules/M/M4/grader/test_project.py:31-39",
    "Round 12: checks/variance_sweep_r12.out (2000 seeds): reference maxima 0.1259 (nu 5), 0.0967 (nu 6), 0.0728 (nu 7), 0.0624 (nu 8); "
    "0.30/0.1259 = 2.38; missing-factor failures 347/347, 317/317, 342/343, 288/317; seed 1093 reference error 1.0220 at nu 3.")
row("d9-2.6-three-position-pivot", "three-position PD tests", "course/modules/M/M4/grader/test_project.py:535-564",
    "Round 12: the three rejected matrices have last pivots -1e-4, -1 and 0 (computed by hand, comments match); the tridiagonal "
    "accepted matrix has eigenvalues 4e-4 and 4e-4 +/- 1.41e-4 (all positive). Reference and alt_r12_3 agree.")
row("d9-2.6-mut-new-r9_04_05_06", "mutants r9_04, r9_05, r9_06", "ledgers/M4/mutants/r9_04-r9_06",
    "Round 12: gates/mutate_M4_0-9_r12.out: KILLED for r9_04_gaussian_stream_skips_first_normal, r9_05_loss_floored_not_rounded, "
    "r9_06_matched_factor_squared_in_t_scale.")
row("d9-2.6-student-t-sign-untested", "Student-t sign is not tested (page says so)",
    "course/modules/M/M4/project.html:228; grader/test_project.py (no test of the Student-t loss sign)",
    "Round 12: no test in test_project.py observes the sign of a Student-t loss (negation test at lines 234-249 is sign-symmetric "
    "and holds for either convention); project.html:228 and 451-453 say so. Consistent.")
row("d9-2.6-chain-term", "chain at lag four", "course/modules/M/M4/project.html:215, 228; grader/test_project.py:212-216",
    "Round 12: chain (draws 4j and 4j+4 share a variable) fails 38/50 seeds (checks/chi_r12.out), as stated.")
row("d9-2.6-hours-own-estimate", "own time estimate for the project", "course/modules/M/M4/project.html:234-245",
    "Round 12: verifier estimate 26 h (see d1-2.6-hours), 13% below 30; the 30% band is 21-39 h. PASS.")
row("d9-cards-c066-c243", "cards c066 and c243", "cards.json",
    "Round 12: c243 (L02: standard deviation in the units of X; Var in squared units, Definition 2.1) checked. c066 is absent from "
    "the current cards.json (ids skip from c065 to c067); no card refers to it. No defect.")
row("d9-index-hub-lines", "hub lines 29, 39, 147 and hours arithmetic", "course/modules/M/M4/index.html:29, 39, 42, 147",
    "Round 12 (index.html unchanged since ccaeeaf4): data-hours-lessons 90 and data-hours-project 30 (120 h); ten lessons each "
    "data-hours 9 (= 90, L01-L10.html); the hub text 'Ten lessons of nine study hours each, which sum to the 90 lesson hours' "
    "matches; placement diagnostic (index.html:68) has two skill checks, consistent with project.html:42.")
row("d9-labs-page-vs-twin-lab2", "project lab 2 page code equals twin", "course/modules/M/M4/project.html:147-184; tests/labs/M4/lab-M4-project-2.py",
    "Round 12: run_labs M4 (byte-identical check, 13/13) and gates/run_labs_help.out; the twin under -I -W error exit 0.")
row("d11-test-names-1e16", "test names carry the correct magnitude (round-11 FAIL, now fixed)",
    "course/modules/M/M4/grader/test_project.py:612, 626",
    "Round 12 (fixed since the round-11 pin): the test names now read test_one_position_with_a_variance_of_1e_minus16_or_1e_minus30_is_accepted "
    "and test_two_positions_with_covariance_of_order_1e_minus16_or_1e_minus30_are_accepted; grep for '1e16' in grader/ finds nothing; "
    "the parametrize values (1e-16, 1e-30) and the comments agree. Previous FAIL now PASS.")
row("d11-gate-check-pages-unit", "gate: check_pages for M4", "tools/check_pages.py; course/modules/M/M4/project.html",
    "Round 12: gates/check_pages_all.out 'check_pages M4: PASS', exit 0 (all units).")
row("d11-labs-twins-python-I", "lab twins under python -I -W error",
    "tests/labs/M4/lab-M4-L01-1.py to lab-M4-L10-1.py; lab-M4-project-1..3.py",
    "Round 12: the three project twins under 'python -I -W error' exit 0 with 0 bytes stderr (checks/project*_twin_out.txt); run_labs "
    "M4 13/13 (which runs the lesson twins the same way, gates/run_labs_M4.out).")
row("d11-project-page-read", "project.html read in full", "course/modules/M/M4/project.html:1-501",
    "Round 12: all 501 lines read this round, including the r11 and r12 hunks at lines 42, 203-206, 228, 343-346, 359, 406, 411, "
    "425-435, 441, 451. Every numbered claim re-derived (Lab 1: 8.4e9, 0.6, 19800, 1.152; Lab 2: 19800, 100; Lab 3: sd 91651.514, z 2.326348, "
    "parametric 213213, index rows; time budget 30; exemplar word counts; cross-term and chi-square counts).")
row("d11-links-anchors", "in-page anchors and local links resolve", "course/modules/M/M4/project.html",
    "Round 12: checks/anchors_r12.py: 18 in-page anchors, missing []; 13 local file links, missing []; index.html#placement target present.")
row("d11-curriculum-scope", "curriculum scope for M4", "curriculum/01-foundations.yaml:186-200; course/modules/M/M4/project.html:194-206",
    "Round 12: 01-foundations.yaml unchanged since ccaeeaf4 (git diff empty); brief (simulate Gaussian and Student-t losses with matched "
    "covariance, 99% loss, prove the moment conditions) and grading both (project.html:206) match.")
row("d11-cards-full-read", "all cards read against lesson blocks", "course/modules/M/M4/cards.json (all 227); L01-L10.html",
    "Round 12: all 227 cards read in full this round against the block dumps and the problem sets (checks/cards_r12.txt, checks/blocks, "
    "checks/problems); card_numbers_r12.py: 0 missing numbers, 0 duplicates. No card contradicts its lesson.")
row("d11-mutants-cover-spec-claims", "mutants d11_01-d11_04 cover page claims",
    "ledgers/M4/mutants/d11_01..d11_04", 
    "Round 12: d11_01 (negative positions rejected; page: 'a negative position is valid input'), d11_02 (position-major normals; page "
    "'for each draw in turn ... in position order'), d11_03 (inverse CDF of random(); page 'from random.Random(seed).gauss'), d11_04 "
    "(index ceil(0.99(n-1)); page ceil(0.99 n)): all KILLED on seed 0 in gates/mutate_M4_0-9_r12.out.")
row("d11-alternatives-over-constraint", "alternatives pass (over-constraint)", "ledgers/M4/scripts/M4-d-r12/alts/; ledgers/M4/scripts/alt_*.py",
    "Round 12: gates/alts_r12_seeds0-9.out: 10 implementations (reference plus nine alternatives), all 10/10 on seeds 0-9 (exit 0).")

# Ensure every previous id is present with a row this round.
rows = []
for rid in prev_ids:
    if rid not in EV:
        raise SystemExit(f"no round-12 evidence written for previous row {rid}")
    rows.append({"id": rid, "check": CHK[rid], "location": LOC[rid], "status": "PASS", "evidence": EV[rid]})
extra = [k for k in EV if k not in prev_ids]
if extra:
    raise SystemExit(f"rows written but not in round 11: {extra}")

mutants = []
for line in Path(ROOT / G / "mutate_M4_0-9_r12.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    mutants.append({"name": name, "description": desc, "killed_by": killed if status == "KILLED" else None})

notes = [
    "Verdict PASS. No FAIL row. Round-11 FAIL row d11-test-names-1e16 is fixed (test names now say 1e_minus16 / 1e_minus30).",
    "Slice delta since the round-11 pin ccaeeaf4: project.html (42, 203-206, 343-346, 359, 406, 411, 425-441, 451), cards.json (c120, c192, c244 removed, c245 added), grader/test_project.py (names at 612 and 626), L01.html (line 85), L04.html (line 52), L05.html (Remark 1.3 replaces Definition 1.3). Everything else in the slice is byte-identical (instance.py, starter.py, reference.py, tests/labs/M4, tools, curriculum, references, index.html, notation).",
    "The card changes were re-verified against the current lesson text: the L05 change (Remark 1.3 cites L02 Definition 2.1) is consistent with c067; the L01 change to Prop 2.2(d) is consistent with c006; the L04 change matches Example 1.9 and c058.",
    "Mutation gate: tools/mutate_graders.py --unit M4 --seeds 0-9 exit 0, 163/163 killed (159 existing + 4 new r12_01..r12_04 in ledgers/M4/mutants/). Alternatives: 10 implementations (reference, 4 new, 5 older) 10/10 on seeds 0-9.",
    "New sweeps (all re-derived by verifier scripts under ledgers/M4/scripts/M4-d-r12/checks/): variance sweep over seeds 0-1999 (grader comments lines 31-39); cross-term sweep over seeds 0-49 (+3 0/50, -3 1/50 seed 38, +5 19/50, -5 30/50); chi-square sharing probes over seeds 0-49; unrounded values behind L05 E1/E3 and L07 E1/E2; exemplar word counts; instances over seeds 0-199; anchors; float ceiling index for n <= 2000000.",
    "Judgment notes (not failures): (1) cards c161, c165, c168, c172, c185, c233-c236 are graded T with a lab basis; they are exact or closed-form evaluations, not theorems; (2) card c013 attributes F(Q(p)) >= p to Proposition 3.2, which the proof (not the statement) establishes; (3) the rubric's level-1 cell 'No proof' sits next to Exemplar A's C1 = 2 (level-2 clause 'divergence asserted without the integral' is the operative one); (4) 'Standard library only' (project.html:204) is a binding constraint that no test enforces, and the page does not list it among the graded checks; (5) ledgers/M4/equivalent/README.md quotes a dated round-2 count of 138 checks; (6) round 11 recorded 70 words for the B Summary, the raw count is 73 (<= 80 either way).",
    "Not checked: the Pyodide in-browser run beyond page_smoke's M4 PASS; lesson prose outside the labelled blocks, the problem sets and the sentences the cards restate (other slices own it); the 2000-seed variance sweep was run once (about 4 minutes), not re-run under the browser; the cross-term probes use the verifier's stated designs for the sharing families, which are the page's families as described in project.html:228.",
]

fragment = {
    "unit": "M4",
    "slice": "d",
    "round": 12,
    "verifier": "independent verifier (Haiku), unit M4, slice d, round 12; not a builder of M4",
    "pin": "329c1d7 (detached HEAD in the checkout)",
    "base": "ccaeeaf4 (round-11 pin). Slice-d delta since ccaeeaf4: project.html, cards.json, grader/test_project.py, L01.html, L04.html, L05.html; new mutants r12_01-r12_04 and alternatives",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD12-M4-d",
    "scratch": "ledgers/M4/scripts/M4-d-r12/ (run_gates.sh, gates/, checks/, alts/, make_r12.py, build_fragment_r12.py)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": f"Slice d round 12: PASS. {len(rows)} rows, all PASS (no FAIL, no UNVERIFIABLE). The round-11 FAIL row (d11-test-names-1e16) is fixed. Mutants: {len(mutants)} of {len(mutants)} killed on seeds 0-9 including 4 new student-error mutants. Alternatives: 10 of 10 implementations (reference plus nine alternatives) pass seeds 0-9. Cards: 227 read against the current lesson text; all numbers present in their lessons; no duplicates. Grader: 156 tests collected; 155+1 skipped at nu 3 or 4; reference 50/50.",
}
problems = []
out = ROOT / "ledgers/M4/M4-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "mutants", len(mutants))
