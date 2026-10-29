"""Build ledgers/M6/M6-d.json (round 4, slice d) from the round-4 runs. Evidence strings cite the outputs archived here."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyC4-M6-d")
SCRIPTS = "ledgers/M6/scripts/M6-d-r4"
PIN = "b276325f68b3032945c96810d651dcd39588b830"
BASE = "ccfdf4c18f5ae9d86e6fe1ca9141382fd6055f83"
CARRY = "Carried from round 3 (curriculum/meta.yaml, plans/M6-build-plan.md byte-identical since the previous pin):"

R3_IDS = [
    "M6d-spec-01", "M6d-ladder-01", "M6d-hours-01", "M6d-grader-ref-01", "M6d-grader-inst-01",
    "M6d-grader-mut-01", "M6d-grader-alt-01", "M6d-grader-msg-01", "M6d-grader-count-01", "M6d-conv-01",
    "M6d-grader-pyodide-01", "M6d-grader-exc-01", "M6d-rubric-observe-01", "M6d-rubric-cal-01",
    "M6d-rubric-bank-01", "M6d-atlas-studio-01", "M6d-lab-P1-01", "M6d-lab-P2-01", "M6d-lab-P3-01",
    "M6d-lint-01", "M6d-numbers-01", "M6d-proofs-01", "M6d-proofs-02", "M6d-stop-01", "M6d-cites-01",
    "M6d-refs-01", "M6d-browser-01", "M6d-notation-01", "M6d-banned-01", "M6d-struct-01", "M6d-dag-01",
    "M6d-gates-01",
    "M6d-card-sample-000", "M6d-card-sample-010", "M6d-card-sample-020", "M6d-card-sample-030",
    "M6d-card-sample-040", "M6d-card-sample-050", "M6d-card-sample-060", "M6d-card-sample-070",
    "M6d-card-sample-080", "M6d-card-sample-090", "M6d-card-sample-100", "M6d-card-sample-110",
    "M6d-card-sample-120", "M6d-cards-dup-01", "M6d-cards-numbers-01", "M6d-cards-lab-A-01",
    "M6d-cards-lab-B-01", "M6d-cards-grade-01", "M6d-cards-c072-01", "M6d-cards-prop-01",
    "M6d-exemplar-A-01",
]

ROW = {}


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> None:
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        r["fix"] = fix
    ROW[rid] = r


row("M6d-spec-01", "2.6-spec", "course/modules/M/M6/project.html:168-191; grader/starter.py:18-40", "PASS",
    "Read the whole Rung 3 spec. starter.py has the five required signatures (lines 18, 23, 28, 33, 38) matching project.html:176. "
    "Convention at project.html:186 now states k>=1 for the stopping level; test_project.py:606-612 and reference.py:36-60 agree. "
    "Exception list at project.html:190 matches the tests named in M6d-grader-exc-01. Reference 50/50 seeds: "
    f"{SCRIPTS}/run_variant.py output (50/50 seeds pass).")
row("M6d-ladder-01", "2.6-ladder", "course/modules/M/M6/project.html:40-49,51-166,602-608", "PASS",
    "Rung 1 = Lab 1 (solved, annotated, run_labs PASS); Rung 2 = Lab 2 completion with ___ blanks (run_labs completion rule satisfied); "
    "Rung 3 = spec; Rung 4 = open stretch (project.html:602-608). tools/check_projects.py --unit M6 -> PASS.")
row("M6d-hours-01", "2.6-hours", "course/modules/M/M6/project.html:222-238; course/modules/M/M6/index.html:29-30", "PASS",
    "Table components 3+4+17+10+5+3 = 42 (project.html:222-238); data-hours-project=42 (index.html:29); index.html:30 "
    "'108 h lessons · 42 h project (28% of the 150 h module)' and 108+42=150. Own estimate of the actual time is subjective and is not a row claim.")
row("M6d-grader-ref-01", "2.6-autograder-1", "course/modules/M/M6/grader/reference.py; tools/run_graders.py", "PASS",
    "tools/run_graders.py --unit M6 --seeds 0-49 -> 'run_graders M6: PASS (reference 50/50 seeds, slowest 0.5 s)' (run this round). "
    "Independent run: run_variant.py reference.py 0-49 -> 50/50; collect-only = '130 tests collected' (run this round).")
row("M6d-grader-inst-01", "2.6-autograder-2", "course/modules/M/M6/grader/instance.py:1-16,27-51", "PASS",
    f"{SCRIPTS}/instance_sweep.py (seeds 0-20000, run this round): violations 0; every instance has horizon 4-10, level in {{1,2}}, "
    "cap 1..N, barrier 1..N, stake 1-25, K>=s; bets_allowed equals the generator's J in every case (0 mismatches); "
    "fair stopped value 0 for all seeds; control stopped value nonzero for all seeds; 19995 distinct instance+answer tuples over 20001 seeds. "
    "Docstring claim (lines 8-9) re-derived by hand: wealth before bet k is s(2^J-2^(k-1))+e, so bet k is placed iff k<=J.")
row("M6d-grader-mut-01", "2.6-autograder-3", "ledgers/M6/mutants/ (49 files); tools/mutate_graders.py", "PASS",
    "tools/mutate_graders.py --unit M6 --seeds 0-9 -> 'mutate_graders M6: PASS (49/49 killed)' (run this round; "
    f"{SCRIPTS}/mutate_all_r4.txt). New student-error mutants written this round: r4_01 .. r4_08 (script {SCRIPTS}/make_mutants.py); "
    "each is killed (r4_01 by test_stopping_level_both_directions_matches_enumeration[win1-0]; r4_02 by test_capital_one_cent_is_accepted; "
    "r4_03 by test_expectation_is_rounded_from_the_exact_value_not_a_float; r4_04 by test_doubling_bets_and_wealths_match_enumeration; "
    "r4_05 by test_control_expected_wealth_rounded_half_up; r4_06 and r4_07 by test_control_walk_breaks_the_identity; r4_08 by test_dyadic_mean_square_error_closed_form[0]).")
row("M6d-grader-alt-01", "2.6-autograder-5-alternatives", f"{SCRIPTS}/alternatives_r4_summary.txt; ledgers/M6/scripts/M6-d-r3/alternatives/", "PASS",
    "Five correct alternatives run against the CURRENT test_project.py over seeds 0-49: a1 50/50, a2 50/50, a3 50/50, a4 50/50, a6 50/50. "
    "Not counted as correct: a5 (time-zero convention, violates the stated k>=1 convention at project.html:186, 0/50) and a7 float money "
    "(fails the exact-rounding test; page line 178 requires rounding 'from the exact value'; plan section 2.1 rule 8 forbids float money). "
    "Plan section 6.5(4) asks for a float alternative within one cent, which conflicts with plan 2.1 rule 8 and with page line 178. "
    "This is an architect decision, recorded in notes; it is not a page defect.")
row("M6d-grader-msg-01", "2.6-autograder-4-messages", "course/modules/M/M6/grader/test_project.py:706-711; all expect/pytest.fail messages", "PASS",
    "Round-3 defect fixed: line 710 now reads 'doubling: an expectation of exactly 5/2 cents must round half up, not to the even neighbour' (no value). "
    "Full scan of every failure message in test_project.py: none names a fixed answer. Messages that name a convention ('at time 1', line 611) state the "
    "convention the page now gives at project.html:186, not the answer for an input.")
row("M6d-grader-count-01", "2.6-autograder-count", "course/modules/M/M6/project.html:180", "PASS",
    "Round-3 defect fixed: project.html:180 now says 'runs 130 tests'. collect-only (this round, /tmp/m6d-r4-collect and run_variant.py --collect): '130 tests collected in 0.02s'. Matches.")
row("M6d-conv-01", "2.4-convention / 2.6-grader", "course/modules/M/M6/project.html:186; grader/test_project.py:248, 606-612", "PASS",
    "Round-3 defect fixed: project.html:186 now states tau = min(the first time k>=1 with S_k = stop_level, stop_cap) and that a level equal to S_0=0 is first checked after the first step. "
    "The level-0 cases (test_project.py:248, :606-612) now follow the stated convention; reference.py:36-60 implements it; alt_a5 is excluded for violating it.")
row("M6d-grader-pyodide-01", "2.6-autograder-5-browser", "course/modules/M/M6/project.html:243; course/assets/js/python.js:4", "PASS",
    f"tools/page_smoke.py --unit M6 --pages project.html -> 'page_smoke M6: PASS' (run this round; {SCRIPTS}/page_smoke_project_r4.txt). "
    "The grader panel (project.html:243) runs in Pyodide; python.js TIMEOUT_MS=120000 matches the 120 s statement at project.html:178.")
row("M6d-grader-exc-01", "2.6-autograder-exception-table", "course/modules/M/M6/grader/test_project.py (must_raise tests); project.html:190", "PASS",
    "Named conditions and their tests: horizon<1 (test_project.py:238-245, :331-338); cap>N (:221-226); level<=0 in Doob (:310-316); capital<=0 (:425-431, :696-701); "
    "stake>capital (:442-447, :689-693). must_raise is used only for these. must_accept covers the boundary cases the page does not name as invalid. "
    "reference.py also raises for p outside (0,1), base<=0, n<0 and x outside [0,1]; the page says nothing else is specified, so no test demands those.")
row("M6d-rubric-observe-01", "2.6-rubric-1-observable", "course/modules/M/M6/project.html:457-466", "PASS",
    "Each of the five criteria has four levels with observable elements (proof names, numbers with units, the N=1 attained case, the 2^-N example). Descriptors of C1 level 4 and C5 level 4 name specific objects a report can show.")
row("M6d-rubric-cal-01", "2.6-rubric-2-calibration", "course/modules/M/M6/project.html:528-530 (Exemplar B), 461 (C1 level 4 row)", "FAIL",
    "Exemplar B's official score C1 = 4 is not supported by its own text under the rubric rule ('the highest level whose every element the report shows', project.html:446-447). "
    "C1 level 4 requires that the report 'names the doubling case without a capital limit as a case in which the boundedness assumption of P1 fails, with P(tau>N)=2^-N>0'. "
    "Exemplar B's Limitations (project.html:568-574), Checks, Appendix and Summary never mention an uncapped doubling case. grep for 'capital limit', 'uncapped', 'unbounded' in project.html returns only rubric/Rung text, not Exemplar B. "
    "Exemplar B's P1 proof and P2 proof are otherwise correct (re-checked line by line: P1 indicator identity, telescoping; P2 A_k decomposition; P3 Cauchy argument).",
    "Either add to Exemplar B a sentence naming the uncapped doubling case and P(tau>N)=2^-N (C1 level 4), or change data-scores to 4,4,3,3,... and the exemplar-b verdict, annotations and data-level to C1 3. Re-run check_pages --unit M6 after the change.")
row("M6d-rubric-cal-02", "2.6-rubric-2-calibration", "course/modules/M/M6/project.html:528-530 (Exemplar B), 465 (C5 row), 562 (C5 annotation)", "FAIL",
    "Exemplar B's official score C5 = 4 is not supported: C5 level 3 requires that the report 'states the dyadic error as 1/(12*4^n) and derives it for at least one level from the cell integral'. "
    "Exemplar B states the dyadic error at levels 0,1,2,3,10 (project.html:533-541 Summary) but never derives it from the cell integral (grep 'cell integral' in project.html: only rubric row 465). "
    "Level 4 cannot stand without the level-3 element. The C5 annotations at lines 587-589 cite the P2 bound and the Lesson 11 attained case only.",
    "Add a one-line cell-integral derivation of the dyadic error for one level (each cell of width h = 2^-n contributes h^3/12, and 2^n cells give 1/(12*4^n)) to Exemplar B's checks, or lower C5 to 2 in data-scores and the exemplar-b verdict.")
row("M6d-rubric-bank-01", "2.6-rubric-3-question-bank", "course/modules/M/M6/project.html (whole page)", "PASS",
    "No question bank on the project page; the self-assessment form is the only interactive element (project.html:600-605 area). No question-bank text found.")
row("M6d-atlas-studio-01", "2.6-atlas-studios", "curriculum/meta.yaml; plans/M6-build-plan.md section 11.1", "PASS", CARRY + " no atlas studio is named by the M6 project page; carried.")
row("M6d-lab-P1-01", "2.5-labs", "course/modules/M/M6/project.html:55-123; tests/labs/M6/lab-M6-project-1.py", "PASS",
    "Twin run alone: python3 -I -W error tests/labs/M6/lab-M6-project-1.py -> rc 0, stderr empty, 14 lines. Page code equals twin (trailing newline aside). "
    "Expected block (project.html) equals the output for the 8 paths, the 4 expectations and the table (run_labs PASS, run_labs_r4.txt). The interpretation numbers (+1/2, -1/2, cancellation) re-derived by hand.")
row("M6d-lab-P2-01", "2.5-labs", "course/modules/M/M6/project.html:125-165; tests/labs/M6/lab-M6-project-2.py", "PASS",
    "Completion lab: page lines 19 and 21 are the ___ blanks (stake > ___ and wealth = ___); every other line equals the twin (run_labs completion rule). "
    "Twin run alone: rc 0, stderr empty, output '100/6/37, 1/1/0, 1000/6/937' equals the expected block. Hand check: stakes 1,2,4,8,16,32 sum to 63; 64 > 37.")
row("M6d-lab-P3-01", "2.5-labs", "course/modules/M/M6/project.html:257-439; tests/labs/M6/lab-M6-project-3.py", "PASS",
    f"Twin run alone: rc 0, stderr empty, 14 lines; page code equals twin; expected block equals output. Independent recomputation ({SCRIPTS}/recompute_lab3_numbers.py, python -I -W error): "
    "fair stopped E=0; control -79/81 (decimal -0.975309); Doob P=7/16, bound 5/8, E|S_6|=15/8; doubling fair E=100, control E=69533/729 = 95.381344 -> 95 cents; "
    "dyadic error 1/(12*4^n). All match the page.")
row("M6d-lint-01", "gates-ruff-mypy", "course/modules/M/M6/grader; tests/labs/M6", "PASS",
    "ruff check and ruff format --check on grader and tests/labs/M6: all passed. mypy --strict on reference/starter/instance is run by run_graders (PASS). "
    "mypy on test_project.py alone reports missing 'instance' and 'martingale_checks' modules; that is an artefact of checking the test file without its siblings, and run_graders passes.")
row("M6d-numbers-01", "2.2-numbers", "course/modules/M/M6/project.html (all quoted numbers)", "PASS",
    "Every number on the page re-derived: Lab 3 values (see M6d-lab-P3-01); Lab 2 values; Lab 1 values 1/8 weights and 0 expectations; dyadic errors; hours 42; 130 tests; "
    "the 6-decimal displays 0.975309, 0.625000, 0.437500, 95.381344. The rounding statements match (half up, once).")
row("M6d-proofs-01", "2.4-statements", "course/modules/M/M6/project.html:194-216", "PASS",
    "P1 hypotheses (probability space, filtration, martingale with integrable M_k, tau<=N) and conclusion are correct. P2 (nonnegative submartingale, N fixed, lambda>0) gives lambda P(max X_k>=lambda) <= E[X_N]; the bound in the statement is the right one. "
    "P3 (square-integrable martingale with E[M_n^2]<=L) gives a.s. convergence (Theorem 12.4 of L12 is the matching statement).")
row("M6d-proofs-02", "2.4-exemplar-proofs", "course/modules/M/M6/project.html:581-583 (Exemplar B appendix)", "PASS",
    "Exemplar B's P1, P2 and P3 proofs were checked line by line: P1 indicator identity and telescoping, P2 A_k decomposition and chaining, P3 orthogonality, Doob for squared increments, "
    "G = union over j of intersection over m of D_m(1/(2j)), and the bound 4j^2(L*-v_m) -> 0. No step is wrong. The calibration defects are in M6d-rubric-cal-01 and -02, not in these proofs.")
row("M6d-stop-01", "2.4-stopping-rule", "course/modules/M/M6/project.html:218-219; course/modules/M/M6/L10.html:552, 212", "PASS",
    "project.html:219 gives P(tau>n)=2^-n, no fixed N bounds tau, and the stopped gain equals 1 a.s. with start 0. L10 Proposition 10.9 (line 552) states P(tau=infinity)=0, D_tau=1 a.s., E[D_tau]=1 != 0=E[D_0] with the same P(tau>n)=2^-n. Consistent.")
row("M6d-cites-01", "2.9-lesson-references", "course/modules/M/M6/project.html:37, 45, 55, 172, 216, 219, 248, 528-590; L08-L12.html", "PASS",
    "Links resolve: L08.html, L10.html, L12.html, index.html#placement (index.html has id=placement, count 1), grader files. Lesson numbers cited (Lesson 8, 10, 11, 12) exist. "
    "The AP1/SC1 claim is a separate row (M6d-lede-attribution-01).")
row("M6d-refs-01", "2.1-citations", "course/modules/M/M6/project.html:612-620; references/references.json", "PASS",
    f"Both keys williams1991probability and billingsley2012probability present in references/references.json entries. verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' ({SCRIPTS}/verify_refs_offline_r4.txt). "
    "The page states that neither book was read and that no locator or theorem number is attributed: honest.")
row("M6d-browser-01", "2.6-constraints", "course/modules/M/M6/project.html:178; course/assets/js/python.js:4", "PASS",
    "'A run in your browser stops after 120 seconds' matches TIMEOUT_MS = 120000 in python.js:4. Standard library only: reference.py and instance.py import only math, fractions, random, typing.")
row("M6d-notation-01", "2.4-notation", "course/modules/M/M6/project.html; notation/notation.json", "PASS",
    "Macros used on the page: \\E, \\Prob, \\indic (all registered in notation.json macros); the other commands are standard LaTeX. No registered symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) appears with another meaning. L^\\ast (exemplar B P3) is a different symbol from R^\\ast.")
row("M6d-banned-01", "2.9-banned-process", "course/modules/M/M6/project.html; grader/*.py; cards.json", "PASS",
    "grep -i for verifier|builder|round|agent|TODO|FIXME|placeholder|draft in project.html, grader/*.py and cards.json: no matches.")
row("M6d-struct-01", "2.9-structure", "course/modules/M/M6/project.html", "PASS",
    "tools/check_pages.py --unit M6 -> 'check_pages M6: PASS' (run this round). Page contract, sections, and the lab/rubric structure pass.")
row("M6d-dag-01", "2.9-DAG", "course/modules/M/M6/project.html; tools/check_dag.py; curriculum/01-foundations.yaml:261-275", "PASS",
    "tools/check_dag.py --unit M6 -> 'check_dag M6: PASS' (run this round). AP1 (curriculum/03-markets.yaml:268) and SC1 (:509) list M6 as a prerequisite; the project page cites them as later modules only (see M6d-lede-attribution-01 for the claim about which results they use).")
row("M6d-lede-attribution-01", "2.1-citations / 2.9-scope", "course/modules/M/M6/project.html:37 (lede), :172 (Context)", "FAIL",
    "The lede says 'the three results that the later modules AP1 and SC1 use', and the Context row says 'The curriculum names the later modules AP1 and SC1 as users of the three martingale results of this unit'. "
    "The curriculum records only prerequisite edges: AP1 prereqs [M6, AP2, FC1, FC2, M8, E4] (curriculum/03-markets.yaml:268) and SC1 prereqs [M6] (:509). "
    "Neither entry names optional stopping, Doob's inequality or martingale convergence as used by AP1 or SC1 (grep of 03-markets.yaml for 'optional stopping|doob|martingale convergence' returns nothing). "
    "The claim is therefore not supported by the curriculum text.",
    "Reword project.html:37 and :172 to 'AP1 and SC1 require this unit (curriculum/03-markets.yaml:268, :509)', and drop 'the curriculum names ... as users of the three results', unless the architect supplies the usage source.")
row("M6d-gates-01", "gates", "tools/check_pages.py, check_projects.py, check_dag.py, run_labs.py, run_graders.py, mutate_graders.py, page_smoke.py (M6 project)", "PASS",
    "Run this round: check_projects M6 PASS; check_pages M6 PASS; check_dag M6 PASS; run_labs M6 PASS (15/15); run_graders M6 PASS (50/50); mutate_graders M6 PASS (49/49); page_smoke M6 (project.html) PASS. "
    "Not run here: the repo-wide gates (render_curriculum, build_site --check, check_pages --all, fetch_data --check).")

# Cards: 13 sampled rows (every tenth card, plus the last) were read in full; all 123 cards were read this round.
for idx, cid in zip(range(0, 130, 10), ["M6-c001", "M6-c012", "M6-c023", "M6-c034", "M6-c045", "M6-c055", "M6-c066",
                                         "M6-c076", "M6-c086", "M6-c096", "M6-c106", "M6-c117", "M6-c127"]):
    rid = f"M6d-card-sample-{idx:03d}"
    row(rid, "2.7-cards-sample", f"course/modules/M/M6/cards.json ({cid})", "PASS",
        f"{cid} read in full this round against its lesson text (lesson files as they are at b276325). The back is correct and matches the lesson's statement, and its cited proposition/definition exists in that lesson (see M6d-cards-prop-01).")
row("M6d-cards-dup-01", "2.7-duplicates", "course/modules/M/M6/cards.json (full scan, 123 cards)", "PASS",
    "Python scan this round: 123 cards, no duplicate id, no duplicate front (case-folded), no duplicate back. The new card M6-c129 (Assumption OA) is unique.")
row("M6d-cards-numbers-01", "2.7-card-numbers", "course/modules/M/M6/cards.json; course/modules/M/M6/L*.html", "PASS",
    "Every number on a card (e.g. 186, 0.7265625, 1001, 489, 9 bets, 0.9980468750, 1/2048, 1/12582912, 602, 3/20, 6/5, 6/7, 2.019877, 4.197279, 0.3217505544, 1.000000) appears in its lesson's text or key-results table (grep across L01-L12.html). "
    "Card c072's value 1 is a lab computation with weights not stated (see M6d-cards-c072-01).")
row("M6d-cards-lab-A-01", "2.7-card-numbers-lab-L01-L07", "cards.json c007, c017, c030, c032, c040, c049, c061, c071; tests/labs/M6/lab-M6-L01..L07-1.py", "PASS",
    "Run this round (python3 -I -W error): L01 counts 4, 16, 8 and the failing candidate; L02 602 of 729 and 3/20 total mass 9/10; L03 integral 1 with the point of value 5, I_1 = 0.1464, 1/3 - I_1 = 0.1869; "
    "L04 integrals 1, zero at n=6 and n=51, partial sums 2.019877 and 4.197279; L05 +/-pi/4, errors 1.30e-07, block 0.3217505544; L06 densities 2, 1/2, 2, 1/3; L07 cell averages 1, 6/5, 6/7. All match the cards.")
row("M6d-cards-lab-B-01", "2.7-card-numbers-lab-L08-L12", "cards.json c081, c090, c100, c102, c105, c110, c112, c113, c121; tests/labs/M6/lab-M6-L08..L12-1.py", "PASS",
    "Run this round: L08 1023 of 1023 cells (fair), 0 of 1023 (p=1/3), increment -1/3; L09 186/256 = 0.7265625, Part A known_by_first_k True, look-ahead fails k=0..7; "
    "L10 K=1000: 9 bets, 0.9980468750, 0.0019531250, wealth 1001 and 489, expected 1000; L11 largest ratio 1.000000 at N=1,2,4, and Part C N=1 P=1/2, E S_N=0, bound fails; "
    "L12 largest grid error 1/2048 and E error^2 = 1/12582912 at n=10. All match the cards.")
row("M6d-cards-grade-01", "2.3-grades-cards-vs-lessons", "cards.json c049, c061, c071, c090, c100, c112, c113, c121 vs L05-L12.html grade rows", "PASS",
    "Round-3 FAIL resolved by option 2 of its fix: grade and basis removed from the lab-result cards. Check: L05-L07 and L09-L12 have only the legend row of data-grade=C (grep). "
    "L01-L04 and L08 keep key-results rows with grade C (L01.html:395, L02.html:446, L03.html:415, L04.html:398,400, L08.html:409), and their cards c007, c017, c030, c032, c037, c040, c081 keep grade C with basis. "
    "Now consistent: a lab result is graded C only where the lesson grades it.")
row("M6d-cards-c072-01", "2.7-card-correctness", "course/modules/M/M6/cards.json M6-c072 (back); course/modules/M/M6/L07.html:316", "FAIL",
    "Round-3 defect NOT fixed. The back says 'On the cell {0, 1, 2}, X takes the values 2, -1 and 4, and the conditional expectation there is the probability-weighted average of those values, which Part A of Lab 1 prints as 1 (Theorem 2.2)'. "
    "The value 1 holds only with the lab's weights (1,2,1)/16 on outcomes 0,1,2 (tests/labs/M6/lab-M6-L07-1.py:21, P = (1,2,1,3,2,3,2,2)/16); with equal weights it would be 5/3. "
    "The card still does not state the weights, and its grade is T with basis 'Theorem 2.2', although 1 is a lab computation. The lesson at L07.html:316 also omits the weights.",
    "Add to the card back the weights: 'with probabilities 1/16, 2/16 and 1/16 on outcomes 0, 1 and 2, (2*1 - 1*2 + 4*1)/4 = 1'. Either re-grade as C with basis 'Lab 1, Part A' or keep T and state the weights. Make the same edit in L07.html:316.")
row("M6d-cards-prop-01", "2.7-hypotheses", "course/modules/M/M6/cards.json (cards citing Proposition, Lemma, Theorem, Corollary, Result)", "PASS",
    "Every cited proposition/lemma/theorem/corollary/result in cards exists in its lesson (grep this round: Lemma 10.2, 10.6, Theorem 10.3, Proposition 10.7, 10.9, Corollary 11.4, Theorem 11.3, Definition 11.1, Lemma 12.1, 12.3, Theorem 12.4, Proposition 12.8, 12.10, Result 12.6, Example 12.7, 12.9, Proposition 9.5, Lemma 9.7, Problem R2/R3, Assumption CE, OA, C, L, F, T, RN). "
    "Cards with a T grade that cite a result carry the hypotheses (e.g. c095/c096/c098/c101 now name Assumption CE; c114-c116 name Assumption OA, consistent with L12 lines 70, 80, 83, 112, 140).")
row("M6d-exemplar-A-01", "2.6-exemplar-annotations", "course/modules/M/M6/project.html:473-526 (Exemplar A)", "PASS",
    "Official scores C1 2, C2 1, C3 2, C4 2, C5 2 (data-scores=2,1,2,2,2) match the annotations: each 'Misses ... level 3' and 'Meets ... level 2' pair is consistent with the score. Each annotation cites a passage of the exemplar text. The deliberate defects (E[X_N^2]/3, 'about 95 cents', 'every horizon', P1 integrability) are present.")

# Assemble rows in r3 order, then new rows.
rows = []
for rid in R3_IDS:
    if rid not in ROW:
        raise SystemExit(f"missing row {rid}")
    rows.append(ROW[rid])
for rid in ["M6d-rubric-cal-02", "M6d-lede-attribution-01"]:
    rows.append(ROW[rid])

mut_lines = (ROOT / SCRIPTS / "mutate_all_r4.txt").read_text().splitlines()
mutants = []
for l in mut_lines:
    m = re.match(r"KILLED (\S+?\.py): (.*) -> (.*)$", l)
    if m:
        mutants.append({"name": m.group(1), "description": m.group(2), "killed_by": m.group(3)})

statuses = [r["status"] for r in rows]
frag = {
    "unit": "M6",
    "slice": "d",
    "round": 4,
    "verifier": "independent verifier, Haiku, round 4",
    "pin": PIN,
    "base": PIN,
    "checkout": str(ROOT),
    "scratch": "/tmp/m6d-r4-collect (collect-only copy); run_variant.py uses a fresh mkdtemp per run",
    "verified_at": "2026-10-29T00:00:00+00:00",
    "verdict": "PASS" if all(s == "PASS" for s in statuses) else "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        f"Delta since the previous pin {BASE} (ccfdf4c) read in full for slice d: project.html (rubric, exemplars, grader panel, labs, spec), grader/test_project.py and reference.py, cards.json (all 123 cards), L05-L12 lesson text for every cited result.",
        "Round-3 defects: M6d-grader-msg-01, M6d-grader-count-01, M6d-conv-01 are fixed and re-verified. M6d-cards-grade-01 is resolved by removing grade from the lab-result cards, consistent with the lessons. M6d-cards-c072-01 is NOT fixed.",
        "Plan conflict for the architect: plan section 6.5(4) asks for a float alternative within one cent, but plan section 2.1 rule 8 (no float money) and project.html:178 (rounding from the exact value) require exact rounding. alt_a7 is therefore not counted; the suite's exact-rounding test is kept.",
        "Alternative a5 (time-zero convention) is not counted: it violates the convention now stated at project.html:186.",
        "Exemplar scoring: Exemplar B's C1 and C5 official scores are not supported by its text under the rubric's own rule (M6d-rubric-cal-01, -02). Exemplar A's scores are consistent.",
        "The mypy --strict message on test_project.py alone (missing modules instance and martingale_checks) is an artefact of checking the test file on its own; run_graders runs mypy on reference, starter and instance and passes.",
        "Not checked: live verify_refs (network job; offline run only); repo-wide gates (render_curriculum, build_site --check, check_pages --all, fetch_data --check, pytest suites outside test_page_checks and test_run_labs); a Chromium screenshot of Exemplar B's annotations; the cards were read in full, not sampled.",
        "Rows carried from round 3 by the carry rule: only M6d-atlas-studio-01 (curriculum/meta.yaml and plans/M6-build-plan.md byte-identical since ccfdf4c). Every other row was re-verified in this round.",
    ],
    "summary": (
        "Slice d: FAIL. 2 page/cards defects and 3 new findings, 2 rubric calibration rows. "
        "FAIL rows: M6d-rubric-cal-01 (Exemplar B C1 4 unsupported), M6d-rubric-cal-02 (Exemplar B C5 4 unsupported), "
        "M6d-lede-attribution-01 (project.html:37, :172 claim the curriculum names AP1/SC1 as users of the three results; it records only prerequisite edges), "
        "M6d-cards-c072-01 (round-3 defect not fixed: weights of the card's value 1 are not stated). "
        "Round-3 defects M6d-grader-msg-01, M6d-grader-count-01, M6d-conv-01 are fixed; M6d-cards-grade-01 is resolved. "
        "Reference 50/50 seeds, 49/49 mutants killed (8 new, all killed), run_labs 15/15, page_smoke project PASS, check_pages/check_projects/check_dag PASS, 130 tests collected (page says 130)."
    ),
}
out = ROOT / "ledgers/M6/M6-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
counts = {s: statuses.count(s) for s in set(statuses)}
print("rows", len(rows), counts, "mutants", len(mutants), "verdict", frag["verdict"])
