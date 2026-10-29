"""Builds ledgers/M6/M6-d.json (round 5) from the outputs saved in ledgers/M6/scripts/M6-d-r5/.

Run from the checkout root with: python3 -I ledgers/M6/scripts/M6-d-r5/build_fragment_r5.py
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
S = ROOT / "ledgers/M6/scripts/M6-d-r5"
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

CARRY = "Carried from round 4 (%s byte-identical since the previous pin):"
OUTS = {
    "gates": "check_projects_r5.txt, check_pages_r5.txt, check_dag_r5.txt, run_labs_r5.txt, run_graders_r5.txt, "
    "mutate_all_r5.txt, page_smoke_project_r5.txt",
}


def P(rid: str, check: str, location: str, evidence: str) -> dict[str, str]:
    return {"id": rid, "check": check, "location": location, "status": "PASS", "evidence": evidence}


rows = [
    P("M6d-spec-01", "2.6-spec", "course/modules/M/M6/project.html:168-191; grader/starter.py:18-40",
      "Re-read the Rung 3 spec. starter.py defines the five signatures at lines 18, 23, 28, 33, 38, matching the list "
      "at project.html:176. The stopping convention at project.html:186 (stop level checked from k>=1) is unchanged and "
      "matches grader/test_project.py. Reference passes 50/50 seeds: " + S.as_posix() + "/run_graders_r5.txt and "
      "reference_r5.txt. Questions a competent student would still ask: none found."),
    P("M6d-ladder-01", "2.6-ladder", "course/modules/M/M6/project.html:40-49,51-166,602-608",
      "Rung 1 = Lab 1 solved and annotated (run_labs 15/15 in run_labs_r5.txt); Rung 2 = Lab 2 blanks; Rung 3 = spec; "
      "Rung 4 = open stretch at project.html:602-608 (unchanged). check_projects M6 PASS (check_projects_r5.txt)."),
    P("M6d-hours-01", "2.6-hours", "course/modules/M/M6/project.html:222-238; course/modules/M/M6/index.html:29-30",
      "Table 3+4+17+10+5+3 = 42 (project.html:222-238, unchanged, outside every delta hunk). index.html:29 "
      "data-hours-project=\"42\" and index.html:30 '108 h lessons ... 42 h project (28% of the 150 h module)'. "
      "108+42=150; 42/150=28%. Delta hunk at index.html:63 only."),
    P("M6d-grader-ref-01", "2.6-autograder-1", "course/modules/M/M6/grader/reference.py; tools/run_graders.py",
      "Run this round: 'run_graders M6: PASS (reference 50/50 seeds, slowest 0.5 s)' (run_graders_r5.txt)."),
    P("M6d-grader-inst-01", "2.6-autograder-2", "course/modules/M/M6/grader/instance.py:1-16,27-51",
      "Run this round: ledgers/M6/scripts/M6-d-r5/instance_sweep_r5.py over seeds 0-20000 (instance_sweep_r5.txt): "
      "violations 0; fair stopped value nonzero 0; control stopped value zero 0; bets_allowed != generator J 0; 19995 "
      "distinct instance+answer tuples. Label SIMULATED (seed 0 printed). Sample seeds 0-19 are a subset of this run."),
    P("M6d-grader-mut-01", "2.6-autograder-3", "ledgers/M6/mutants/ (52 files); tools/mutate_graders.py",
      "Run this round: 'mutate_graders M6: PASS (52/52 killed)' (mutate_all_r5.txt). Three NEW student-error mutants "
      "written this round by ledgers/M6/scripts/M6-d-r5/make_mutants_r5.py: r5_01 (dyadic value at x=1 indexes one past "
      "the last cell; killed by test_dyadic_value_is_the_cell_midpoint, seed 0), r5_02 (stopping rule takes cap-1 steps; "
      "killed by test_control_walk_breaks_the_identity[inst0]), r5_03 (Doob event uses a strict threshold; killed by "
      "test_doob_probability_and_bound_match_enumeration[inst0]). Round-4 mutants r4_01..r4_08 are re-killed."),
    P("M6d-grader-alt-01", "2.6-autograder-5-alternatives", "ledgers/M6/scripts/M6-d-r5/alternatives_r5.txt",
      "Re-run this round on the current suite, seeds 0-49: a1 50/50, a2 50/50, a3 50/50, a4 50/50, a6 50/50 (five correct "
      "alternatives). a5 (time-zero convention, against project.html:186) 0/50 is not counted. a7 (float money) is not "
      "counted, as in round 4: it conflicts with the exact-rounding test that project.html:178 describes; the plan "
      "conflict is recorded in notes."),
    P("M6d-grader-msg-01", "2.6-autograder-4-messages", "course/modules/M/M6/grader/test_project.py:706-711",
      CARRY % "grader/*.py and tests/labs/M6 (git diff b276325..04626e9 empty for these paths)" +
      " the round-4 full scan of every failure message; no message names a fixed answer."),
    P("M6d-grader-count-01", "2.6-autograder-count", "course/modules/M/M6/project.html:180",
      "project.html:180 says 'runs 130 tests'. Collect-only this round: '130 tests collected in 0.01s' (collect_r5.txt)."),
    P("M6d-conv-01", "2.4-convention / 2.6-grader", "course/modules/M/M6/project.html:186; grader/test_project.py",
      "project.html:186 states the k>=1 convention; reference.py and test_project.py unchanged (carry set identical); "
      "reference 50/50 and the convention-violating alternative a5 0/50 are consistent with it (alternatives_r5.txt)."),
    P("M6d-grader-pyodide-01", "2.6-browser", "course/modules/M/M6/project.html:243; course/assets/js/python.js:4",
      CARRY % "python.js and grader/*.py" + " project.html:243 is outside every delta hunk; page_smoke project PASS this "
      "round (page_smoke_project_r5.txt)."),
    P("M6d-grader-exc-01", "2.6-autograder-exceptions", "course/modules/M/M6/grader/test_project.py (must_raise tests); project.html:190",
      CARRY % "grader/test_project.py and project.html:190" + " exception list unchanged; must_raise tests name only the "
      "conditions page 190 names (round-4 scan)."),
    P("M6d-rubric-observe-01", "2.6-rubric-observable", "course/modules/M/M6/project.html:457-466",
      CARRY % "project.html:457-466 (no diff hunk in the rubric table)" + " every level descriptor is observable."),
    P("M6d-rubric-cal-01", "2.6-rubric-calibration", "course/modules/M/M6/project.html:528-530 (Exemplar B), 584 (C1 level-4 annotation), 579-580 (Limitations)",
      "Round-4 FAIL resolved. Exemplar B now names the unbounded doubling case as the case where P1's bound fails, "
      "with Prob(tau > N) = 2^-N > 0 (project.html:579-580 body, 584 annotation). Lab 1 Part B prints P_tau_greater_than_n "
      "= 2^-n (L10 Part B, run this round). My blind scores for Exemplar B: C1 3 or 4 (its P1-P3 assumptions are listed "
      "inline, not numbered as the rubric's level-3 element and project.html:450 require; that is one level below the "
      "official 4, within the one-level tolerance). Official C1 4 is supported."),
    P("M6d-rubric-bank-01", "2.6-rubric-question-bank", "course/modules/M/M6/project.html; course/modules/M/M6/index.html",
      "Not applicable: the question bank is required of adversarial projects only. grep -i adversarial finds 0 matches in "
      "project.html and index.html; curriculum/01-foundations.yaml M6 has grading: both (no adversarial mode)."),
    P("M6d-atlas-studio-01", "2.6-atlas-studios", "curriculum/meta.yaml; plans/M6-build-plan.md section 11.1",
      CARRY % "curriculum/meta.yaml and plans/M6-build-plan.md (git diff empty)" + " no atlas or studio requirement changed."),
    P("M6d-lab-P1-01", "2.5-lab", "course/modules/M/M6/project.html:55-123; tests/labs/M6/lab-M6-project-1.py",
      "Re-run this round: lab-M6-project-1.py under python -I -W error prints the 8 path rows (tau 1,1,1,1,3,3,3,3; "
      "S_tau +1,+1,+1,+1,+1,-1,-1,-3; weights 1/8) and E[S_(tau and k)] = 0 for k = 0..3. The page's 'Step 1..4' text at "
      "project.html:121-123 matches those values; the sum (1-1-1-3)/8 = -1/2 and the 4 paths of +1 contribute +1/2."),
    P("M6d-lab-P2-01", "2.5-lab", "course/modules/M/M6/project.html:125-165; tests/labs/M6/lab-M6-project-2.py",
      "Re-run this round: capital 100 base 1 cap 10 -> bets 6, wealth after losses 37; capital 1 -> 1 bet, wealth 0; "
      "capital 1000 cap 6 -> 6 bets, wealth 937; lines 125-165 are outside every delta hunk."),
    P("M6d-lab-P3-01", "2.5-lab", "course/modules/M/M6/project.html:257-439; tests/labs/M6/lab-M6-project-3.py",
      "Re-run this round: E[S_tau]=0 (fair), -79/81 (control, decimal -0.975309); Doob N=6 level 3: P = 7/16 = 0.4375, "
      "bound E|S_N|/3 = 5/8 = 0.625; doubling capital 100: bets 6, P(win) 63/64, P(ruin) 1/64, wealth 101/37, E = 100; "
      "control E = 69533/729 = 95.381344 -> 95 cents; dyadic levels 0,1,2,3,10 print 1/12, 1/48, 1/192, 1/768, 1/12582912 "
      "with closed form equal True. Every number quoted at project.html:437 and 565-584 matches. The lab text at line 437 "
      "is outside the lab code (the page text at 437 was changed; the twin is byte-identical)."),
    P("M6d-lint-01", "2.5-lint", "course/modules/M/M6/grader; tests/labs/M6",
      "Run this round: ruff format --check on grader, labs and scratch: 21 files already formatted. ruff check on "
      "course/modules/M/M6 and tests/labs/M6: clean. mypy --no-incremental on reference.py, starter.py, instance.py: "
      "Success, no issues in 3 files (run this round)."),
    P("M6d-numbers-01", "2.2-numbers", "course/modules/M/M6/project.html (all quoted numbers)",
      "Every number added or changed this round re-derived or printed: 2^-N (N>=0); 1 cent; 7/16; 5/8; -79/81; 63/64; 1/64; "
      "101; 37; 69533/729 = 95.3813443 (95.381344 to six places, rounds half up to 95); 1/(12*4^n) (n=0,1,2,3,10 printed); "
      "Lab 1 Part B 'Step' weights 1/8. No quoted number is missing from its lab output."),
    P("M6d-proofs-01", "2.4-proofs", "course/modules/M/M6/project.html:194-216",
      CARRY % "project.html:194-216 (no delta hunk overlaps; earlier hunks are 1:1 line replacements, so line positions are unchanged)" +
      " the statements section proofs and their citations."),
    P("M6d-proofs-02", "2.4-proofs", "course/modules/M/M6/project.html:593-595 (Exemplar B appendix)",
      "Re-read P1, P2 and P3 in the Exemplar B appendix this round. P1 uses tau <= N for integrability and the telescoping "
      "sum; P2 chains the submartingale inequality and ends with the attained case N=1, lambda=1 for |S| and 'It bounds a "
      "probability, not E[max X_k]'; P3 uses orthogonality (Lemma 12.1), Lemma 12.3, Doob for squared increments and "
      "continuity from below. Each step names a justification. No proof step is missing."),
    P("M6d-stop-01", "2.4-stopping", "course/modules/M/M6/project.html:218-219; course/modules/M/M6/L10.html (Prop 10.9, Part B)",
      "Re-read this round: project.html:218-219 states Prob(tau > k) = 2^-k for every whole k >= 0 and P1's identity fails "
      "for the unbounded tau. L10 Proposition 10.9 (a)-(c) and Part B of Lab 1 (P_tau_greater_than_n 2^-n, expected stopped "
      "value 0) support it. L10 lines moved since round 4; the cited claims were re-located by text search."),
    P("M6d-cites-01", "2.4-cross-references", "course/modules/M/M6/project.html; L08-L12.html",
      "Every Definition/Proposition/Lemma/Theorem/Corollary/Example/Remark/Problem/Result label cited in project.html exists "
      "in the M6 lessons (script over all cites: 0 missing). Lesson references AP1 and SC1 prerequisite claims checked "
      "against curriculum/03-markets.yaml:268 and :509."),
    P("M6d-refs-01", "2.1-references", "course/modules/M/M6/project.html:612-620; references/references.json",
      CARRY % "references/references.json and project.html:612-620" + " the reading section attributes nothing; no new "
      "reference was added this round."),
    P("M6d-browser-01", "2.5-browser", "course/modules/M/M6/project.html:178; course/assets/js/python.js:4",
      CARRY % "course/assets/js/python.js and project.html:178" + " no network or CDN use; page_smoke project PASS this round."),
    P("M6d-notation-01", "2.4-notation", "course/modules/M/M6/project.html; notation/notation.json",
      "Symbols used in the changed text: h (cell width), j, x, \\varepsilon, L^\\ast (P3), J, K, m, v_n, Y, M_n. "
      "notation/notation.json lists eight symbols (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}); "
      "none of the new symbols is one of them, and R^\\ast is not used by M6. L^\\ast is not registered and has one meaning "
      "on the page."),
    P("M6d-banned-01", "2.9-banned", "course/modules/M/M6/project.html; grader/*.py; cards.json",
      "Added lines in project.html and cards.json scanned for the process and filler words we, clearly, obviously, simply, "
      "trivially, note that, in this section, this lesson, our: 0 hits. check_pages M6 PASS (check_pages_r5.txt)."),
    P("M6d-struct-01", "2.9-structure", "course/modules/M/M6/project.html",
      "Section order and counts unchanged (diff hunks only change prose and one annotation row). check_pages M6 PASS and "
      "check_projects M6 PASS this round."),
    P("M6d-dag-01", "2.9-dag", "course/modules/M/M6/project.html; tools/check_dag.py; curriculum/01-foundations.yaml:261",
      "check_dag.py --unit M6: PASS this round (check_dag_r5.txt). The new lede prerequisite claim matches the DAG: "
      "AP1 prereqs [M6, ...] (curriculum/03-markets.yaml:268) and SC1 prereqs [M6] (:509)."),
    P("M6d-gates-01", "2.9-gates", "tools/check_pages.py, check_projects.py, check_dag.py, run_labs.py, run_graders.py, mutate_graders.py, page_smoke.py",
      "Run this round on pin 04626e9: " + OUTS["gates"] + ". Also pytest tests/test_page_checks.py tests/test_run_labs.py "
      "tests/test_docs_figures.py tests/test_refs.py: all pass. verify_refs.py --offline: 560 entries, 0 problems. Not run: "
      "the live verify_refs run (network job)."),
]

# Cards: the file grew from 123 (round 4) to 131 cards. All 131 cards were read in full this round.
CARD_READ = ("cards.json read in full this round (131 cards; round 4 counted 123; 8 added c130-c137, 27 changed, "
             "per diff of b276325..04626e9). ")
card_samples = [
    ("000", "M6-c001", "Definition 1.1 sigma-algebra axioms S1-S3 match L01 text; no number."),
    ("010", "M6-c012", "probability space definition matches L02 Definition 1.2; no number."),
    ("020", "M6-c023", "integral of a simple function, sum a_i mu(A_i), L03 Definition 2.1; no number."),
    ("030", "M6-c034", "L04 monotone convergence/ supremum definition; changed wording checked; no number."),
    ("040", "M6-c045", "general Fubini statement (Assumption F) as L05 states it; no number."),
    ("050", "M6-c055", "finite-set absolute continuity (Lemma 1.2) as L06 states it; no number."),
    ("060", "M6-c066", "L2 conditional expectation definition (Definition 2.1) as L07 states it; no number."),
    ("070", "M6-c076", "natural filtration properties (Proposition 2.1), L08; no number."),
    ("080", "M6-c086", "hitting-time stopping time (Proposition 9.5), L09 Assumptions; no number."),
    ("090", "M6-c096", "optional stopping bounded case (Theorem 10.3), L10; no number."),
    ("100", "M6-c106", "CHANGED card: submartingale definition 11.1 with CE note; L11 Definition 11.1 agrees."),
    ("110", "M6-c117", "martingale convergence general statement (Result 12.6) stated not proved; L12 agrees."),
    ("120", "M6-c127", "adaptedness (Definition 1.1, L08); no number."),
]
for idx, cid, note in card_samples:
    rows.append(P(f"M6d-card-sample-{idx}", "2.7-cards-sample", f"course/modules/M/M6/cards.json ({cid})",
                  CARD_READ + note + " Cited labels exist in the M6 lessons (script over all cards: 0 missing)."))

rows += [
    P("M6d-cards-dup-01", "2.7-cards-duplicates", "course/modules/M/M6/cards.json (full scan, 131 cards)",
      CARD_READ + "Duplicate ids 0, duplicate fronts 0, duplicate backs 0 (python scan this round)."),
    P("M6d-cards-numbers-01", "2.7-cards-numbers", "course/modules/M/M6/cards.json; course/modules/M/M6/L*.html",
      CARD_READ + "Every numeric token of every card appears in its lesson or is a notation/set-builder false positive "
      "(c016, c018: set braces). c136's 12582912 appears in L12 (grep). Changed-card numbers checked against lab output."),
    P("M6d-cards-lab-A-01", "2.7-cards-labs", "cards.json c007, c017, c030, c032, c040, c049, c061, c071; tests/labs/M6/lab-M6-L01..L07",
      "Each checked against twin output this round: c007 counts 4/16/8 and failing candidate (L01); c017 sum 9/10 (L02); "
      "c030 integral 1 and integral unchanged by value 5 at a point (L03); c032 I_1 0.1464, 1/3-I_1 = 0.1868867 vs bound "
      "0.5 (L03 Part B); c040 integrals equal 1 for n 1..20 (L04); c049 errors +/-1.3e-7 (L05); c061 densities 2,1/2,2,1/3 "
      "(L06); c071 1, 6/5, 6/7 (L07)."),
    P("M6d-cards-lab-B-01", "2.7-cards-labs", "cards.json c081, c090, c100, c102, c105, c110, c112, c113, c121; tests/labs/M6/lab-M6-L08..L12.py",
      "c081 1023 cells pass (L08 Part B); c090 186 / 0.7265625 (L09 Part A); c100 9 bets, 0.9980468750, 0.0019531250 (L10 "
      "Part A, K=1000); c102 and c105 follow from Proposition 10.7 and the printed ruin wealths (0,3,3,37,489); c110 and "
      "c112 P=1/2 with bound failing for signed walk (L11 Part C); c113 largest ratio 1.000000 at N=1 (L11 Part A); c121 "
      "largest grid error 1/2048 = 2^-11 at level 10 (L12 Part A)."),
    P("M6d-cards-grade-01", "2.7-cards-grade", "cards.json grade/basis fields; L05-L12 grade statements",
      "Card grades checked this round: 72 T, 43 ungraded definition/theorem cards, 16 C with a basis naming the lab "
      "(every C card has basis). Changed M6-c072 T->C with basis 'Lab 1, Part A'; M6-c081 and c134 name Lab 1 Part B. "
      "The two T cards that mention Lab 1 (c073, c091) state results proved on the page (Proposition 2.4, Definition 9.1)."),
    P("M6d-cards-c072-01", "2.7-cards-correctness", "course/modules/M/M6/cards.json M6-c072 (back); course/modules/M/M6/L07.html:316; tests/labs/M6/lab-M6-L07-1.py",
      "Round-4 FAIL resolved. The back now states the weights 1/16, 2/16, 1/16 on outcomes 0,1,2. Lab L07 twin P = (1,2,1,3,"
      "2,3,2,2)/16 and X(0..2) = (2,-1,4): cell probability 1/4, value (2*1 - 1*2 + 4*1)/4 = 1. Lab output "
      "'cell (0, 1, 2) prob 1/4 average 1' (run this round). L07 line 316 states the same weights."),
    P("M6d-cards-prop-01", "2.7-cards-cross-references", "course/modules/M/M6/cards.json (cards citing Proposition, Lemma, Theorem, Corollary, Definition, Example, Remark, Problem, Result)",
      "Every cited label in all 131 cards exists in some M6 lesson (script, 0 missing). Result labels cited on new cards c130-c137 "
      "are the lab-printed results, not new theorems."),
    P("M6d-cards-new-01", "2.7-cards-new", "cards.json M6-c130..M6-c137 and the 27 changed cards (diff b276325..04626e9)",
      "New cards checked against lab output: c130 602 of 729 pairs (L02 twin, 602 of 729; 729-64-64+1 = 602 by hand); c131 I_1 = "
      "(1/2)(1-sqrt(1/2)) = 0.1464466 (L03 Part B); c132 n=6 and n=51 = floor(1/x)+1 (L04 twin); c133 2.019877 and 4.197279 "
      "(L04 Part B); c134 biased walk passes 0 of 1023 cells, increment -1/3 (L08 Part B); c135 look-ahead fails k=0..7 "
      "(L09 Part B); c136 1/12582912 = 1/(12*4^10) (L12 Part A); c137 1001, 489, 1000 (L10 Part A, K=1000; 1001-512 = 489; "
      "(1-2^-9)*1001 + 2^-9*489 = 1000). Changed cards: typographic (ASCII dots to ellipsis) or wording aligned to the "
      "lesson text; the substantive changes (c072, c081, c090, c100, c103, c105, c106, c107, c121) were re-checked "
      "against the current lessons and lab outputs."),
    P("M6d-exemplar-A-01", "2.6-rubric-calibration", "course/modules/M/M6/project.html:473-526 (Exemplar A)",
      CARRY % "project.html:473-526 (delta hunks at 36, 121, 171, 218, 437 are 1:1 line replacements and 565+ come after)" +
      " Exemplar A's official scores (C1 2, C2 1, C3 2, C4 2, C5 2) and its annotations are unchanged."),
    P("M6d-rubric-cal-02", "2.6-rubric-calibration", "course/modules/M/M6/project.html:528-530, 465 (C5 row), 562 and 601 (C5 annotations), 562, 573, 593-594 (P1-P2)",
      "Round-4 FAIL resolved. The C5 level-3 element (why Doob's bound concerns a probability, with the attained case N=1, "
      "lambda=1 for |S|) is now in Exemplar B's appendix P2 (final sentences). First-power bound E[X_N]/lambda with constant 1 "
      "is in P2 and in 'The checks' (E|S_6|/3 = 5/8). The dyadic error 1/(12*4^n) is derived from the cell integral "
      "(project.html:568-573 passage). My blind C5 score for Exemplar B is 4, matching the official 4."),
    P("M6d-lede-attribution-01", "2.2-attribution", "course/modules/M/M6/project.html:37 (lede), :172 (Context)",
      "Round-4 FAIL resolved. The lede and Context now say 'The curriculum lists this unit as a prerequisite of the later "
      "modules AP1 and SC1', which matches the prereq edges curriculum/03-markets.yaml:268 (AP1 prereqs include M6) and :509 "
      "(SC1 prereqs [M6]). The claim is about DAG edges, not usage, and is worded that way."),
]

mutants = []
for line in (S / "mutate_all_r5.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"KILLED (\S+?)\.py: (.*?) -> (\S+?)(?:\[|\s|$)", line)
    if m:
        mutants.append({"id": m.group(1), "description": m.group(2), "killed_by": m.group(3)})

fragment = {
    "unit": "M6",
    "slice": "d",
    "round": 5,
    "verifier": "independent verifier, Haiku, round 5",
    "pin": "04626e99f75119a75c225f719c603a6e5c7f3e06",
    "base": "b276325f68b3032945c96810d651dcd39588b830",
    "checkout": str(ROOT),
    "scratch": "ledgers/M6/scripts/M6-d-r5 (collect-only via run_variant_r5.py --collect; instance sweep via instance_sweep_r5.py)",
    "verified_at": "2026-10-29T03:40:00+00:00",
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta read in full for slice d: project.html (hunks at 36, 121, 171, 218, 437, 565-584), cards.json (131 cards, all read), "
        "L07/L10 text for every card and passage cited, index.html:63. Grader, M6 labs, starter, references, notation, python.js and "
        "curriculum/meta.yaml are byte-identical to b276325, so they were re-run, not re-read.",
        "Rubric calibration: Exemplar B's P1-P3 assumptions are listed inline, not numbered. The rubric's C1 level-3 element says "
        "'numbered assumptions' (project.html:450 and 461). This is one level below the official C1 4 and within the one-level "
        "calibration tolerance, so it is recorded here and not as a row.",
        "Plan conflict (carried from round 4): plan section 6.5(4) asks for a float alternative within one cent. Plan 2.1 rule 8 and "
        "project.html:178 require exact rounding. Alternative a7 is therefore not counted.",
        "Not checked: repo-wide gates outside this slice (render_curriculum, build_site --check, fetch_data --check, full pytest suite, "
        "live verify_refs). mypy on test_project.py alone reports missing sibling modules; run_graders runs mypy on the three modules "
        "and passes. ruff check on the scratch helper script ledgers/M6/scripts/M6-d-r5/run_variant_r5.py flags RUF015; it is not "
        "a unit file.",
        "Not checked: a Chromium screenshot of the Exemplar B annotations (page_smoke passes the project page; visual check not done).",
    ],
    "summary": "Slice d (M6 project.html rubric, grader, project labs, cards.json): PASS. Round-4 FAIL rows M6d-rubric-cal-01, "
    "M6d-rubric-cal-02, M6d-lede-attribution-01 and M6d-cards-c072-01 are resolved and re-verified. 52/52 mutants killed (49 carried "
    "plus 3 new). 131 cards read in full; 0 duplicates; all cited labels exist.",
}

problems = ledger.validate(fragment, "M6-d")
if problems:
    raise SystemExit("\n".join(problems))
out = ROOT / "ledgers/M6/M6-d.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "mutants", len(mutants))
