"""Round-3 verifier D (M4 slice d): builds ledgers/M4/M4-d.json from the rows verified in this round.

Mutant rows are parsed from the mutation run's own output (mutate_M4_0-9_with_v6.out), so every listed mutant is one the
tool reported as KILLED. Usage: python -I build_fragment_m4d_r3.py <checkout_root>
"""
import json
import pathlib
import re
import sys
from datetime import datetime, timezone

root = pathlib.Path(sys.argv[1])
S = "ledgers/M4/scripts/M4-d-r3/"
mut_lines = (root / S / "mutate_M4_0-9_with_v6.out").read_text().splitlines()
mutants = []
for line in mut_lines:
    m = re.match(r"KILLED (\S+?): (.*) -> (\S+) \(seed (\d+)\)$", line)
    if m:
        mutants.append({"name": m.group(1), "description": m.group(2), "killed_by": f"{m.group(3)} (seed {m.group(4)})"})
assert len(mutants) == 123, len(mutants)

R = []


def row(id_, check, location, status, evidence, fix=""):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)


row("d1-2.6-ladder", "2.6 ladder", "course/modules/M/M4/project.html#ladder, #rungs, #spec, #stretch", "PASS",
    "Read project.html lines 40-49 (four rungs in order), 51-192 (Lab 1 rung 1 worked example, Lab 2 completion with three blanks replaced by ___, rung 3 spec), 471-478 (stretch). Rung 1 solved and annotated; rung 2 graded by lab-M4-project-2 (class completion); rung 3 matches the M4 scope; rung 4 open-ended.")
row("d1-2.6-spec-questions", "2.6 spec: questions a competent student would ask", "course/modules/M/M4/project.html#spec; grader/reference.py", "PASS",
    "Spec read in full (lines 194-229). Signatures match grader/starter.py (checked by running starter: 136 failed on seed 0). Conditions list (lines 219-225) is matched by the suite's ValueError tests. Remaining questions a student might ask are answered by Conventions items 1-5 and the 'What the suite does not test' paragraph.")
row("d1-2.6-hours", "2.6 hours: component sum and own estimate within 30 %", "course/modules/M/M4/project.html#budget; data-hours-project=30", "PASS",
    "Components 2+2+12+8+4+2 = 30 = data-hours-project (line 33) = hub figure. Own estimate: rung 1 2 h; rung 2 2 h; simulator with 3 functions and about 30 conditions 10-14 h; appendix A1-A4 6-10 h; report and self-assessment 4-6 h; self-check 2 h; total 26-36 h, inside 30 +/- 30 %.")
row("d1-2.6-autograder-reference", "2.6 autograder: run_graders on reference.py, seeds 0-49", "course/modules/M/M4/grader/reference.py; tools/run_graders.py", "PASS",
    f"'tools/run_graders.py --unit M4 --seeds 0-49': PASS (reference 50/50 seeds, slowest 0.9 s) ({S}run_graders_M4_0-49.out). Pytest on reference with seeds 0, 1093, 3, 1 ({S}grader_runs_r3.sh): 137 passed/1 skipped (seeds 0, 1093; nu 4 and 3), 138 passed (seed 3, nu 7).")
row("d1-2.6-instances", "2.6 instances: 20 sampled seeds valid, instances differ", "course/modules/M/M4/grader/instance.py", "PASS",
    f"{S}instances_sample_r3.py: seeds 0-19 and 1000-1019: 40/40 valid (positions positive whole cents, 2 or 3 assets, nu in 3..8, n_draws <= 20000 and not a multiple of 100, covariance symmetric and positive definite by Cholesky), 40 distinct (positions, nu, n_draws) triples.")
row("d1-2.6-mut-own", "2.6 mutation: at least 3 verifier-written student-error mutants, all killed", "ledgers/M4/mutants/v6_01..v6_05 (generator ledgers/M4/scripts/M4-d-r3/make_mutants_r3.py)", "PASS",
    "Five new student-error mutants written from reference.py, each differing in one place: v6_01 chi-square with 2 nu degrees of freedom; v6_02 one chi-square variable for the whole run; v6_03 third position dropped; v6_04 quantile of absolute losses; v6_05 inverted matched ratio in the chi-square scale. All killed by tools/mutate_graders.py --unit M4 --seeds 0-9 (" + S + "mutate_M4_0-9_with_v6.out).")
row("d1-2.6-mut-existing", "2.6 mutation: all existing mutants re-run on seeds 0-9", "ledgers/M4/mutants/*.py (123 files at the end of this round)", "PASS",
    f"'tools/mutate_graders.py --unit M4 --seeds 0-9': PASS (123/123 killed), EXIT=0 ({S}mutate_M4_0-9_with_v6.out). Per-mutant killer test and seed are in this fragment's mutants list.")
row("d1-2.6-mut-m11", "2.6 mutation: m11 loss sign flipped", "ledgers/M4/mutants/m11_loss_sign_flipped.py", "PASS",
    "Killed in the 123/123 run (see mutants list); killer is the frozen Gaussian stream test, which fixes the sign of the Gaussian loss.")
row("d1-2.6-mut-r9_03", "2.6 mutation: r9_03 chi-square reused on alternate draws", "ledgers/M4/mutants/r9_03_student_t_chi_square_reused_every_second_draw.py", "PASS",
    "Killed in the 123/123 run (test_student_t_draws_do_not_share_chi_square, see mutants list).")
row("d1-2.6-mut-v4_m02", "2.6 mutation: v4_m02 matched factor skipped for small nu", "ledgers/M4/mutants/v4_m02_matched_factor_skipped_for_small_nu.py", "PASS",
    "Killed in the 123/123 run (mean-absolute-loss test at nu 3 to 8, see mutants list).")
row("d1-2.6-mut-m17", "2.6 mutation: m17 Student-t source from seed + 1 (ruled a conforming alternative)", "ledgers/M4/equivalent/m17_student_t_second_seed.py; project.html Conventions item 5 (line 215)", "PASS",
    f"Not a fault under the page: Conventions item 5 (project.html line 215) states 'The source of the Student-t family's normals and the order of its draws are not fixed here', so m17 violates no sentence of the page. Run: m17 passes the suite on seeds 0-9 (10/10 via run_alternatives.run_one on {S}m17_copy_r3.py). It is therefore an alternative, not a mutant, and is not listed in mutants.")
row("d1-2.6-alternatives", "2.6 alternatives: five existing and three new correct implementations pass seeds 0-49", "ledgers/M4/scripts/alt_1..alt_5.py; ledgers/M4/scripts/M4-d-r3/alt_r3_a..c.py", "PASS",
    f"{S}run_alternatives_existing_0-49.out: reference and alt_1..alt_5 PASS (50/50 each). {S}run_r3_alts_0-49.out: alt_r3_a (chi-square drawn before the normals, heapq quantile, floor(x+0.5) rounding), alt_r3_b (isinstance validation, pivot floor 1e-300), alt_r3_c (Student-t normals from seed+1) PASS 50/50 each. No over-constraint found.")
row("d1-2.6-starter", "2.6 starter: signatures complete and unchanged; starter fails the suite", "course/modules/M/M4/grader/starter.py; project.html:201-202", "PASS",
    f"Signatures in starter.py match project.html lines 202 (three functions). Running the suite on starter.py at seed 0: 136 failed, 1 passed, 1 skipped ({S}grader_runs_r3.sh).")
row("d1-2.6-messages", "2.6 failure messages name the property and never leak the answer", "course/modules/M/M4/grader/test_project.py:115, 581-584, 599", "FAIL",
    "Messages that state the computed answer for the test input: line 115 'matched_scale(3) must return 1/3'; lines 581 to 584 'for n = 99 the index is ceil(98.01) = 99', 'for n = 100 the index is ceil(99) = 99', 'for n = 101 the index is ceil(99.99) = 100, not 99', 'for n = 2 the index is ceil(1.98) = 2'; line 599 'for n = 1 the index is ceil(0.99) = 1'. Each reveals the correct value (and for line 583 the wrong one) for the input under test. Other messages are property statements (line 111 repeats the spec formula, accepted as the page's own definition).",
    "Rewrite each of these messages to name the property only, with no computed value and no index: e.g. line 115 'matched_scale must return the factor the page defines at the boundary nu = 3'; lines 581-584 and 599 'quantile_99 must return the order statistic whose index is the ceiling of 0.99 n for this n (see Conventions item 4)'; line 583 may name n but not the index or the wrong value.")
row("d1-2.6-count-and-pyodide", "2.6 count and browser run: page's check count equals collect-only count; same file in Pyodide", "course/modules/M/M4/grader/test_project.py; project.html:206", "PASS",
    f"'pytest --collect-only' on the suite: 138 tests collected (seeds 0, 1093, 3). Page says 138 (line 206). Seed 0 and seed 1093 (nu 4, nu 3): 137 passed, 1 skipped, matching the page's parenthetical. Seed 3 (nu 7): 138 passed. page_smoke for the project page: PASS ({S}page_smoke_project_r3.out).")
row("d1-2.6-grader-comment-numbers", "2.6 grader comments: numbers quoted in comments are right", "course/modules/M/M4/grader/test_project.py:31-48, 168-170, 343-345, 186-187", "PASS",
    f"Re-derived by {S}sweep_tolerance_r3.py (seeds 0-1999, instance nu): nu 5 max 0.1259 (seed 238), nu 6 0.0967, nu 7 0.0728, nu 8 0.0624; the unmatched variant fails the 0.30 check on 347/347 (nu 5), 317/317 (nu 6), 342/343 (nu 7), 288/317 (nu 8) seeds, matching the comment; seed 1093 with nu 3 has reference error 1.022. Cross term ({S}cross_term_r3.py): reference max 0.0239 over seeds 0-49; matched factor on one asset only +0.29 mean; one chi-square per asset -0.15 mean over seeds 0-9. sqrt(1.5) and 1/12 claims checked by arithmetic.")
row("d1-rubric-observable", "2.6 rubric: every level descriptor is observable", "course/modules/M/M4/project.html#rubric (lines 332-343)", "PASS",
    "Read all five criteria and four levels. Descriptors name objects the reader can check (a formula, an integral, an index, a number with its unit or seed, a section under its heading, a word count, a named limitation). No descriptor relies on an unstated judgement.")
row("d1-rubric-calibration", "2.6 rubric: blind calibration of exemplars A and B", "course/modules/M/M4/project.html#exemplar-a, #exemplar-b (lines 348-462)", "PASS",
    "Blind scores from the rubric alone (before reading the annotations): Exemplar A C1 2 (formula and hypothesis, no integral), C2 2 (factor stated, independence and Gamma integral missing), C3 2 (index stated without ceiling derivation), C4 2 (2,130 dollars is not printed by Lab 3 or the run), C5 2 (four sections, 90 body words, two limitations); official 2,2,2,2,2. Exemplar B C1 4, C2 4, C3 4, C4 4, C5 3 (names the variance check's limit, no smallest detectable inflation); official 4,4,4,4,3. All within one level, and exact. Exemplar B prose is 705 words including headings (body 300-700 holds).")
row("d1-rubric-question-bank", "2.6 rubric: question bank for adversarial projects", "course/modules/M/M4/project.html", "PASS",
    f"The M4 project is not adversarial (rubric-graded with five criteria, no question bank required by the curriculum). {S}check_projects_M4.out: PASS.")
row("d1-atlas", "2.6 atlas: project entry matches the page", "curriculum/meta.yaml:194-276; course/modules/M/M4/project.html", "PASS",
    f"Carried from round 2 (curriculum/meta.yaml byte-identical since the previous pin; git diff c737272 a007712 lists no curriculum change for M4). {S}check_projects_M4.out: PASS.")
row("d1-studio", "2.6 studio: project studio entry", "curriculum/01-foundations.yaml:73-76", "PASS",
    "Carried from round 2 (curriculum/01-foundations.yaml byte-identical since the previous pin). Not an M4 studio change.")
row("d1-lab-project-1", "Project lab 1 (rung 1 worked example): twin, page code, expected block, prose numbers", "course/modules/M/M4/project.html#lab-M4-project-1; tests/labs/M4/lab-M4-project-1.py", "PASS",
    f"tools/run_labs.py --unit M4: PASS 13/13 ({S}run_labs_M4.out). Twin alone: python -I -W error exit 0 and output equal to the page's expected block (8 lines; 210946, 243004, 1.0017, 1.0447, 1.6667, 8400000000.0). Prose: ratio 243004/210946 = 1.152; 1.0447 is 4.5 % above 1; 5/3 = 1.6667; sample variances within 5 %.")
row("d1-lab-project-2", "Project lab 2 (rung 2 completion): blanks, twin, expected block", "course/modules/M/M4/project.html#lab-M4-project-2; tests/labs/M4/lab-M4-project-2.py", "PASS",
    "run_labs PASS (blanks are ___ lines matching the twin). Twin output equals the expected block (0.600000, 0.333333, 19800, 100, True). 19800 = (99*20000+99)//100; ceil(0.99*101) = 100.")
row("d1-lab-project-3", "Project lab 3 (rung 3 closed forms): twin, expected block, numbers", "course/modules/M/M4/project.html#lab-M4-project-3; tests/labs/M4/lab-M4-project-3.py", "PASS",
    "Twin output equals the expected block (91651.514, 2.326348, 213213, factors and inflations for nu 3,4,5,8, index rows). Recomputed: sqrt(8.4e9) = 91651.514; z = 2.326348; 2.326348 * 91651.514 = 213213.3 -> 213213; 0.99*101 = 99.99; 0.99*19987 = 19787.13.")
row("d1-prose-numbers", "2.2 numbers in prose: derived, computed or quoted", "course/modules/M/M4/project.html (Labs, Report, Exemplars A and B)", "PASS",
    "Every displayed number in the changed hunks re-derived: 8.4e9 = 3e6^2*4e-4 + 2e6^2*9e-4 + 2*3e6*2e6*1e-4; 0.6, 1/3, 5/3, 1.5 = 3/2, 1.6667 and 1.4 etc.; 2267 = 213213 - 210946; 32058 = 243004 - 210946; 15.2 % = 32058/210946; 4.5 % = 0.0447; 19787.13; 1.152. Exemplar A's 2,130 dollars is the 213213-cent value in dollars (annotated as a miss).")
row("d1-prose-scope", "2.9 scope words (only, all, always, every, any, same, drives, exactly)", "course/modules/M/M4/project.html (changed hunks: lines 53, 200, 206, 212, 215, 228, 354, 359, 402)", "PASS",
    "'every input' (line 53) and 'every position is long in every instance' (line 200) are backed by instance.py (positions from randrange(100000, 5000001)). 'at nu of 3 to 8' (line 206) matches the mean-absolute test (test_project.py line 190, nu in range(3, 9)). 'always' appears only in Exemplar A, where its annotation (line 359) names it as a scope word that no printed number backs.")
row("d1-prose-process-words", "2.9 no process words in learner text", "course/modules/M/M4/project.html", "PASS",
    "grep for verifier, builder, round N, ledger, fragment, TODO, placeholder, pending: no hits in project.html.")
row("d1-prose-banned-phrases", "2.9 banned phrases absent", "course/modules/M/M4/project.html", "PASS",
    f"tools/check_pages.py --unit M4: PASS ({S}check_pages_M4.out), which scans visible prose of every M4 page for the BUILDER_RULES 1.3-1.4 banned strings.")
row("d1-dag", "2.9 / 2.6-14 DAG: concepts used and defined as the module assigns", "course/modules/M/M4/project.html; course/modules/M/M4/index.html (changed hunk: prerequisites)", "PASS",
    f"tools/check_dag.py --unit M4: PASS ({S}check_dag_M4.out). Project page uses only matrix, quadratic form and Gamma concepts from Lessons 5-6 and the hub prerequisites (the hub hunk at index.html line 59-62 now names Sigma as defined in Lesson 5).")
row("d1-notation", "2.4 notation: symbols match notation/notation.json and are not reused", "notation/notation.json; course/modules/M/M4/project.html", "PASS",
    "Registry entries T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, \\mathbb{Q}. The project page uses Sigma, L, W, Z, w, R_i, nu, n, Q (quantile, plain Q, not the registry's \\mathbb{Q}), F_n, ell, Gamma and Phi nowhere as a symbol with another meaning. No collision.")
row("d1-cites", "2.1 citations: registry key, reading section matches", "course/modules/M/M4/project.html#reading; references/references.json", "PASS",
    f"The only key is blitzstein2019introduction. Reading section states that no passage was read (line 482). tools/verify_refs.py --offline: 560 entries, 0 problems ({S}verify_refs_offline_r3.out). tools/verify_refs.py --unit M4 (live): 1 of 560 entries, 0 problems ({S}verify_refs_M4_live_r3.out).")
row("d1-structure", "2.9 structure: sections, headings, lab markup, page smoke", "course/modules/M/M4/project.html", "PASS",
    f"tools/check_pages.py --unit M4 PASS; tools/check_projects.py --unit M4 PASS ({S}check_projects_M4.out); tools/page_smoke.py --unit M4 --pages project: PASS (zero console errors, math rendered, no external requests, 360 px and light/dark) ({S}page_smoke_project_r3.out).")
row("d1-cards-schema", "2.7 cards schema: fields, ids, lesson coverage, grades, basis on C cards", "course/modules/M/M4/cards.json", "PASS",
    "212 cards; ids unique; fronts unique; fields back/front/grade/id/lesson (+basis on 20 C cards); grades T 192, C 20; every C card has a basis; lessons L01-L10 all present.")
row("d1-cards-numbers-in-lesson", "2.7 cards: every number of a card occurs in its own lesson", "course/modules/M/M4/cards.json vs L01..L10.html", "PASS",
    "Checked for every changed card: M4-c033 '250000' in L02; M4-c112 '0.5' and '1.5' in L07 (Lab 1 Part A MU = 0.5, SIGMA = 1.5); M4-c047/c183 '1/8' in L03 (Section 3 law); M4-c140 cites Section 4 of L09, the Misconceptions section that states the hypotheses. Unchanged cards carried per card (see d1-cards-lesson-statements).")
row("d1-cards-labs", "2.7 cards: numbers of C cards match lab output", "course/modules/M/M4/cards.json (20 C cards); tests/labs/M4/lab-M4-L02..L10-1.py", "PASS",
    f"Lab twins run alone (python -I -W error) and saved in {S}labout/. Matches: c030 3.469; c033 489 (threshold 250000, p 0.05, n 10000, seed 2027); c047 2.065 and c183 5.580 (seed 2026, n 20000, exact 2.073 and 5.625); c082 0.00002223 and 0.00016257; c083 0.592936 and -0.007064; c098 1.669114 and 0.001469; c112 7.11e-13 at t 2 (closed 244.69193226); c113 -0.062124/-0.062110; c126 0.0187; c143 0.8552 and SE 0.0056; c157/c161/c168/c172 ; c162 1.8220/1.8838; c165 exact values; c166 3.4689 and 0.0311; c167 0.8548/0.8518; c169 +0.9919 (seed 2028); c170 1.0211/0.9396; c171 0.8807/1.1987; c185 gaps; c188 (0.9770, -2.0055); c189 +0.0031; c190 -0.0235 (seed 2027).")
row("d1-cards-math", "2.4 cards: mathematics on every card is correct", "course/modules/M/M4/cards.json (all 212 entries read)", "PASS",
    "All 212 entries read. Recomputed by hand or script: Bernoulli skew/kurtosis (c041, c045, c048); law on -2,1,3 mean 0, m2 3, m4 15, kurtosis 5/3, gamma3 0 (c043, c044); 0,1,2,10 law mean 7/4, m2 163/16, m3 2157/32, m4 149461/256, exact skewness 2.0730, kurtosis 5.6254 (c042, c047, c183, c200); Cauchy and t(3) tails (c148, c149, c157, c161, c168, c172, c187); t(3) density (c209); E[1/W] = 1/(nu-2) (c091); E[e^{-sZ^2}] (c090); E[e^{tZ^2}] domain (c102); two-point characteristic function modulus (c107); MGF of a sum (c108, c110); cov(1_A,1_B) = -ab (c064); covariance matrix of Example 1.5 (c119, c124, c125, c207, c208); Chebyshev 7/60 (c141) and 2 (c137); 40 from 35 + sqrt(29.1667) (c142); Q(p) = 1 on (3/5, 4/5] (c192).")
row("d1-cards-lesson-statements", "2.7 cards agree with the current lesson statement and its hypotheses", "course/modules/M/M4/cards.json vs L01..L10 propositions", "PASS",
    "Changed cards checked against the current text: c028 (L02 Prop 2.3), c029 (Prop 2.2), c070 (L05 Prop 1.2; the card's finiteness hypothesis is harmless), c084 (L06 Def 1.1), c112 (L07 Lab 1 Part A), c140 (L09 Misconceptions, Section 4), c033, c047, c183 (labs). L03 changed in this delta (Example 2.5, Prop 2.8, Section 4): cards c041, c043, c044, c045, c048, c212, c219, c220 re-checked against the new text. Carried from round 2 for the other cards: their lesson sources L01, L02, L04-L10 are byte-identical since the previous pin and their card entries are byte-identical.",
    "")
row("d1-cards-duplicates", "2.7 cards: no duplicate cards", "course/modules/M/M4/cards.json", "PASS",
    "Scan for duplicate ids and duplicate fronts: none. The round-1 duplicate pairs (c066/c213, c070/c211) are gone (ids absent).")
row("d1-cards-c191-grade", "2.7 cards: grade of M4-c191", "course/modules/M/M4/cards.json M4-c191", "PASS",
    "Carried from round 2: entry M4-c191 is byte-identical since the previous pin. Grade T for a derivation under stated hypotheses and Assumption 1.")
row("d1-cards-hypotheses", "2.7 cards: a card that cites a proposition carries that proposition's hypotheses", "course/modules/M/M4/cards.json M4-c014, M4-c015 (lesson L01 Remark 3.3 at line 104; Proposition 3.4 at line 120)", "FAIL",
    "Round 2 FAIL cards c028, c029, c070 now carry their hypotheses (PASS). Two cards that cite results stated for distinct values still omit that hypothesis: M4-c014 cites Remark 3.3, which the lesson states 'Let X be as in Proposition 2.2' (positive weights, distinct values x_1 < ... < x_m); M4-c015 cites Proposition 3.4, which the lesson states for 'n >= 1 distinct real numbers' with probability 1/n each. The page-wide finite-space setting does not supply distinct values.",
    "M4-c014 back: prepend 'Hypotheses: positive weights and distinct values.' M4-c015 back: prepend 'Hypotheses: distinct values, each with probability 1/n.' (cards.json is not produced by any tool here; edit the two entries directly and rerun tools/check_pages.py --unit M4.)")
row("d1-data", "2.8 data: no real data; every value SIMULATED", "course/modules/M/M4/project.html (Inputs); grader/instance.py", "PASS",
    "instance.py returns label 'SIMULATED' and draws all values from random.Random; the page says so (line 37, 200). No data-files attribute on project labs.")
row("d1-freshness-registry", "2.1 freshness: references.json entries used by the slice verify", "references/references.json (blitzstein2019introduction)", "PASS",
    "verify_refs offline 560/0 problems; live 1/560 0 problems for M4. No 2025-2026 work is cited on the project page, so no freshness flag.")
row("d1-gates-repo", "Repository gates relevant to the slice", "pyproject.toml; tests/labs/M4; tests/test_labs.py", "PASS",
    f"ruff check . PASS; mypy --no-incremental: 331 files, no issues ({S}mypy_nocache.out); pytest tests/test_labs.py -k M4: 13 passed ({S}pytest_m4_labs.out). Outside the slice and not an M4 finding: ruff format --check . fails on ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py ({S}ruff_format.out); reported for the M3 owner, not an M4 row.")
row("d1-tools-structure", "Tools used by the slice are unchanged and pass", "tools/*.py", "PASS",
    f"tools/check_pages.py, check_dag.py, check_projects.py, run_labs.py, run_graders.py, mutate_graders.py, page_smoke.py, verify_refs.py: all run here on the pin a007712 and pass for M4 (outputs in {S}). Tool files are not in the delta.")
row("d2-2.6-constraints-exceptions", "2.6 constraints: the list of conventions the suite does not grade is complete", "course/modules/M/M4/project.html:204 (Constraints) and :228 (What the suite does not test)", "FAIL",
    "Two stated binding requirements are neither graded nor listed as not graded. (a) Constraints (line 204) 'Standard library only': test_project.py contains no import check (grep for stdlib, numpy, import inspection: none), so a module that imports numpy passes every test. (b) Conventions item 1 (line 211) 'W is independent of Z': no test checks the independence of W and Z; only the cross-term and variance tests respond to dependence indirectly. The listed not-graded items (item 1 variance at nu 3-4, item 2 Student-t sign, item 2 round() call, item 4 formula, item 5 Student-t source and order) are complete for everything else I checked.",
    "Either add a test that parses tail_risk.py and rejects any import outside sys.stdlib_module_names, and state in the page that the suite checks it; or add 'standard library only' to the not-graded list in line 204. For (b) add 'the independence of W and Z (item 1)' to that list, or add a test on the joint law of the returns of two assets at nu 5.")
row("d3-2.6-grading-list", "2.9 prose: the Grading mode enumeration describes what the suite checks", "course/modules/M/M4/project.html:206 (Grading mode)", "FAIL",
    "The enumeration lists 'the Student-t cross term at nu of 5' and then 'the covariance of two asset returns', which are one test (test_student_t_cross_term_matches_matched_covariance). The second item describes no further check, so the sentence counts one check twice.",
    "Delete the item 'the covariance of two asset returns (see what the suite does not test)' from the Grading mode list on line 206, keeping 'the Student-t cross term at nu of 5 (defined under what the suite does not test)'.")
row("d3-2.6-disclosed-survivor", "2.6 mutation: a surviving behaviour the page discloses as untested", "ledgers/M4/scripts/M4-d-r3/disclosed_survivor_student_t_loss_sign_flipped.py; project.html:228", "PASS",
    f"Student-t loss sign flipped (not a counted mutant) passes the suite on seeds 0 and 5 ({S}grader_runs_r3.sh). project.html line 228 states 'The suite does not test the sign of the Student-t losses' and gives the reason (the law is symmetric; the Student-t draws have no fixed order). The disclosure is accurate and complete for this survivor.")
row("d3-2.6-tolerance-comments", "2.6 grader comments: tolerance and sweep claims", "course/modules/M/M4/grader/test_project.py:31-42", "PASS",
    f"{S}sweep_tolerance_r3_0-1999.out (seeds 0-1999 at each instance nu): maxima 0.1259, 0.0967, 0.0728, 0.0624 as stated; unmatched fail counts 347/347, 317/317, 342/343, 288/317 as stated; seed 1093 nu 3 reference error 1.022.")
row("d3-2.6-cross-term-comment", "2.6 grader comments and page: cross-term claims", "course/modules/M/M4/grader/test_project.py:43-48; project.html:228", "PASS",
    f"{S}cross_term_r3.out: reference max |rel err| 0.0239 over seeds 0-49 (claim 0.024); matched factor on one asset only: mean +0.290 over seeds 0-9 (claim about 29 %); one chi-square per asset: mean -0.152 (claim about 15 %); tolerance 0.05 lies between them.")

verdict = "PASS" if all(r["status"] == "PASS" for r in R) else "FAIL"
counts = {s: sum(1 for r in R if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
notes = [
    "Scope: project.html (whole page read line by line; delta hunks at 53, 204, 206, 212, 215, 228, 354, 359, 402), grader/ (instance.py, reference.py, starter.py, test_project.py read in full), tests/labs/M4 project labs and the eight lesson labs (outputs saved), cards.json (all 212 cards read; numbers and maths checked; lesson statements checked for the changed cards and the L03 changes), mutants (123 incl. v6_01..v6_05), alternatives (5 existing, 3 new).",
    "Delta since the round-2 pin c737272: project.html, grader/test_project.py (lines 183-201 only), cards.json (nine cards), L03.html (Lesson 3 hunks), index.html (hub hunks), ledgers/M4/equivalent/README.md, ledgers/M4/scripts/alt_1.py and alt_2.py, mutants v2_01..v2_04 (unchanged in this round's run).",
    "Non-blocking observations (no row): the Exemplar A annotation word count (90 body words) is exact. The Lab 1 hypothesis and interpretation sentences match the printed output. Card M4-c070 states a finiteness hypothesis that Proposition 1.2 of L05 does not state; it is harmless because the proof uses Proposition 1.1. The ruff format failure is outside M4.",
    "Could not check: (a) the in-browser grader interactively (page_smoke runs the project page only, headless); (b) the lesson statements of the unchanged cards word for word (carried per card by byte identity from round 2, not re-read in this round); (c) live Crossref for all 560 registry entries (one M4 entry live, the offline check for all); (d) the M4 proofs are the student's, so no appendix proof text was graded beyond the exemplars.",
    "Scratch: the grader runs used mktemp copies under /tmp and removed them. The pinned checkout's pre-existing M4-d-r3 files from an earlier run (sweep.py, sweep_2000_output.txt, mutate_r3.out, altA-C, build_fragment_r3.py, fix_c.py, make_variants.py) were not used as evidence; their sweep used forced nu and a different window, and was superseded by sweep_tolerance_r3.py.",
]
frag = {
    "unit": "M4",
    "slice": "d",
    "round": 3,
    "verifier": "independent verifier (Haiku), not a builder of M4; round 3",
    "pin": "a007712 (checkout detached at the pin)",
    "base": "c737272 (round-2 pin; delta computed with git diff c737272 a007712)",
    "checkout": str(root),
    "scratch": "ledgers/M4/scripts/M4-d-r3/ (scripts kept in the checkout; grader copies removed after each run)",
    "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "verdict": verdict,
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": {"rows": len(R), **counts, "mutants_killed": len(mutants), "mutants": len(mutants)},
}
out = root / "ledgers/M4/M4-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "verdict", verdict, counts, "mutants", len(mutants))
