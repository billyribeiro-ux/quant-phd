"""Builds ledgers/M6/M6-d.json (round 1, closing delta of slice d) from the outputs in ledgers/M6/scripts/M6-d-r1/.

Run from the checkout root with: python3 -I ledgers/M6/scripts/M6-d-r1/build_fragment_r1.py
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
S = "ledgers/M6/scripts/M6-d-r1"
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

BASE_PIN = "04626e99f75119a75c225f719c603a6e5c7f3e06"
HEAD = "95f3f8cb21c2cd9fc904430bd30a6b734d01f672"
CARRY = "Carried from round 5 (%s byte-identical since the previous pin %s): "
NOTHING_CHANGED = "course/modules/M/M6/project.html, course/modules/M/M6/grader/*.py, tests/labs/M6/lab-M6-project-1..3.py"


def P(rid: str, check: str, location: str, evidence: str) -> dict[str, str]:
    return {"id": rid, "check": check, "location": location, "status": "PASS", "evidence": evidence}


def carry(files: str, base_evidence: str) -> str:
    return CARRY % (files, BASE_PIN[:8]) + base_evidence


rows = [
    P("M6d-spec-01", "2.6-spec", "course/modules/M/M6/project.html:168-191; grader/starter.py:18-40",
      carry(NOTHING_CHANGED + ", grader/starter.py",
            "Rung 3 spec and starter signatures unchanged; reference passes 50/50 seeds this round (" + S +
            "/run_graders_r1.txt).")),
    P("M6d-ladder-01", "2.6-ladder", "course/modules/M/M6/project.html:40-49,51-166,602-608",
      carry(NOTHING_CHANGED, "Ladder unchanged. check_projects M6: PASS this round (" + S + "/check_projects_r1.txt).")),
    P("M6d-hours-01", "2.6-hours", "course/modules/M/M6/project.html:222-238; course/modules/M/M6/index.html:29-30",
      carry("course/modules/M/M6/project.html:222-238 and index.html:29-30 (the only index.html delta is line 138)",
            "Table 3+4+17+10+5+3 = 42; index.html:29 data-hours-project=\"42\"; 108+42=150; 42/150 = 28%. "
            "check_pages M6 PASS this round (" + S + "/check_pages_r1.txt).")),
    P("M6d-grader-ref-01", "2.6-autograder-1", "course/modules/M/M6/grader/reference.py; tools/run_graders.py",
      "Fresh this round: 'run_graders M6: PASS (reference 50/50 seeds, slowest 0.5 s)' (" + S + "/run_graders_r1.txt)."),
    P("M6d-grader-inst-01", "2.6-autograder-2", "course/modules/M/M6/grader/instance.py:1-16,27-51",
      carry("course/modules/M/M6/grader/instance.py",
            "Instance sweep over seeds 0-20000 from the base round (violations 0; fair stopped value nonzero 0; control "
            "stopped value zero 0; bets_allowed != generator J 0). Label SIMULATED.")),
    P("M6d-grader-mut-01", "2.6-autograder-3", "ledgers/M6/mutants/ (56 .py files); tools/mutate_graders.py",
      "Fresh this round: 'mutate_graders M6: PASS (56/56 killed)' (" + S + "/mutate_all_r1.txt). The 56 files are the 49 "
      "carried, the three r5_01..r5_03 added by commit 9fd6aedd, and four m6c_r6_* lab-twin files added by commit "
      "0d2d0f3f (slice c). Observation, not counted as a FAIL: the four m6c_r6_* files are lab twins, not grader "
      "student errors, and their 'KILLED' results come from test_capital_of_zero_or_less_raises_whatever_the_base[0] "
      "failing on a missing sol.doubling_outcome, an incidental kill (see notes)."),
    P("M6d-grader-alt-01", "2.6-autograder-5-alternatives", "ledgers/M6/scripts/M6-d-r5/alternatives_r5.txt",
      carry("course/modules/M/M6/grader/*.py and project.html:178 (no change)",
            "Five correct alternatives a1, a2, a3, a4, a6 at 50/50 on seeds 0-49 in the base round. a5 and a7 not counted, "
            "as in the base round (plan conflict recorded there).")),
    P("M6d-grader-msg-01", "2.6-autograder-4-messages", "course/modules/M/M6/grader/test_project.py:706-711",
      carry("course/modules/M/M6/grader/test_project.py", "Round-5 full scan of every failure message: no message names a fixed answer.")),
    P("M6d-grader-count-01", "2.6-autograder-count", "course/modules/M/M6/project.html:180",
      "project.html:180 says 'runs 130 tests'. Fresh collect-only on grader/test_project.py with the browser flags: "
      "'130 tests collected in 0.01s' (" + S + "/collect_r1.txt)."),
    P("M6d-conv-01", "2.4-convention / 2.6-grader", "course/modules/M/M6/project.html:186; grader/test_project.py",
      carry(NOTHING_CHANGED, "Stop-level convention k>=1 at project.html:186 matches the grader and the reference 50/50.")),
    P("M6d-grader-pyodide-01", "2.6-browser", "course/modules/M/M6/project.html:243; course/assets/js/python.js:4",
      carry("course/modules/M/M6/project.html and course/assets/js/python.js",
            "Fresh: page_smoke M6 project PASS (" + S + "/page_smoke_project_r1.txt).")),
    P("M6d-grader-exc-01", "2.6-autograder-exceptions", "course/modules/M/M6/grader/test_project.py (must_raise tests); project.html:190",
      carry("course/modules/M/M6/grader/test_project.py and project.html:190",
            "Exception list unchanged; must_raise tests name only the conditions page 190 names.")),
    P("M6d-rubric-observe-01", "2.6-rubric-observable", "course/modules/M/M6/project.html:457-466",
      carry("course/modules/M/M6/project.html:457-466", "Every level descriptor observable (base round).")),
    P("M6d-rubric-cal-01", "2.6-rubric-calibration", "course/modules/M/M6/project.html:528-530 (Exemplar B), 584, 579-580",
      carry("course/modules/M/M6/project.html:528-530, 579-584",
            "No dedicated blind scorer file for M6-d exists under ~/.fanout/blind/ (ruling 23), so the base calibration "
            "row is carried. Its cited L10 facts re-checked fresh: Lab 1 Part B prints P_tau_greater_than_n 2^-n and "
            "expected_stopped_value 0 (" + S + "/lessons_txt/L10.txt lines 185-188; run_labs M6 PASS).")),
    P("M6d-rubric-bank-01", "2.6-rubric-question-bank", "course/modules/M/M6/project.html; course/modules/M/M6/index.html",
      "Fresh: grep -i adversarial over project.html and index.html returns no match (" + S + "/adversarial_grep_r1.txt). "
      "The question bank is required only of adversarial projects, and M6 is grading: both."),
    P("M6d-atlas-studio-01", "2.6-atlas-studios", "curriculum/meta.yaml; plans/M6-build-plan.md section 11.1",
      carry("curriculum/meta.yaml and plans/M6-build-plan.md",
            "git diff 04626e99..HEAD over both paths is empty this round.")),
    P("M6d-lab-P1-01", "2.5-lab", "course/modules/M/M6/project.html:55-123; tests/labs/M6/lab-M6-project-1.py",
      carry("course/modules/M/M6/project.html:55-123 and tests/labs/M6/lab-M6-project-1.py",
            "Path rows tau 1,1,1,1,3,3,3,3 and weights 1/8; run_labs M6 15/15 fresh (" + S + "/run_labs_r1.txt).")),
    P("M6d-lab-P2-01", "2.5-lab", "course/modules/M/M6/project.html:125-165; tests/labs/M6/lab-M6-project-2.py",
      carry("course/modules/M/M6/project.html:125-165 and tests/labs/M6/lab-M6-project-2.py",
            "Capital 100 base 1 cap 10 -> 6 bets, wealth after losses 37; capital 1 -> 1 bet, wealth 0; capital 1000 cap 6 -> 6 bets, wealth 937.")),
    P("M6d-lab-P3-01", "2.5-lab", "course/modules/M/M6/project.html:257-439; tests/labs/M6/lab-M6-project-3.py",
      carry("course/modules/M/M6/project.html:257-439 and tests/labs/M6/lab-M6-project-3.py",
            "Doob N=6 level 3: P = 7/16, bound 5/8; control E = 69533/729 -> 95 cents; dyadic error 1/(12*4^n) at n = 0,1,2,3,10.")),
    P("M6d-lint-01", "2.5-lint", "course/modules/M/M6/grader; tests/labs/M6",
      "Fresh: ruff check on tests/labs/M6 and course/modules/M/M6/grader: 'All checks passed!'; ruff format --check: "
      "'19 files already formatted' (" + S + "/ruff_r1.txt). mypy --no-incremental on reference.py, starter.py, "
      "instance.py: 'Success: no issues found in 3 source files' (" + S + "/mypy_r1.txt)."),
    P("M6d-numbers-01", "2.2-numbers", "course/modules/M/M6/project.html (all quoted numbers)",
      carry("course/modules/M/M6/project.html", "No project number changed; the cards' numbers are re-checked in M6d-cards-numbers-01.")),
    P("M6d-proofs-01", "2.4-proofs", "course/modules/M/M6/project.html:194-216",
      carry("course/modules/M/M6/project.html:194-216", "Statements-section proofs and citations unchanged.")),
    P("M6d-proofs-02", "2.4-proofs", "course/modules/M/M6/project.html:593-595 (Exemplar B appendix)",
      carry("course/modules/M/M6/project.html:593-595", "P1-P3 of Exemplar B: each step has a justification (base round).")),
    P("M6d-stop-01", "2.4-stopping", "course/modules/M/M6/project.html:218-219; course/modules/M/M6/L10.html (Prop 10.9, Part B)",
      "Fresh: project.html:218-219 unchanged and states Prob(tau > k) = 2^-k. L10 Proposition 10.9 (a) P(tau=inf)=0 and D_tau=1 "
      "a.s.; (b) E[D_tau]=1 != 0; (c) E[D_{tau^n}]=0 under Assumption CE (" + S + "/lessons_txt/L10.txt lines 75-80). "
      "Lab 1 Part B output (run_labs M6 PASS; " + S + "/lessons_txt/L10.txt lines 185-188): P_tau_greater_than_n 0.5, 0.25, 0.125, 0.03125 "
      "= 2^-n; expected_stopped_value 0; wealth_when_all_lose -(2^n-1). Consistent with the page text."),
    P("M6d-cites-01", "2.4-cross-references", "course/modules/M/M6/project.html; L08-L12.html",
      "Fresh: every label cited in project.html (3 distinct) and in each of L01-L12 resolves to a Definition, Proposition, "
      "Lemma, Theorem, Corollary, Example, Remark, Problem, Result, Assumption or Misconception of the M6 lessons (" +
      S + "/lesson_cites_r1.txt, 0 missing). Lesson-to-lesson references in the changed passages (L07 Theorem 2.2(a); "
      "L10 Example 10.8 and Proposition 10.9(c); L12 Lemma 12.1 and Proposition 12.8) checked against their statements."),
    P("M6d-refs-01", "2.1-references", "course/modules/M/M6/project.html:626-627 (reading list); references/references.json",
      "Fresh: references/references.json changed only by generated_at and by used_by lists (BK1+BK4, DV1+FC2, E9+LX1; "
      "bisndbasel, black1973pricing, reinhart2009this). M6 cites only williams1991probability and billingsley2012probability, "
      "neither changed. verify_refs --offline: 'offline integrity: 560 entries, 0 problems' (" + S + "/verify_refs_offline_r1.txt). "
      "The project.html reading list is at lines 626-627 in this checkout."),
    P("M6d-browser-01", "2.5-browser", "course/modules/M/M6/project.html:178; course/assets/js/python.js:4",
      carry("course/modules/M/M6/project.html:178 and course/assets/js/python.js",
            "No network or CDN use; page_smoke M6 project PASS this round (" + S + "/page_smoke_project_r1.txt).")),
    P("M6d-notation-01", "2.4-notation", "course/modules/M/M6/project.html; notation/notation.json",
      carry("course/modules/M/M6/project.html and notation/notation.json",
            "Symbols of the project page are not among the eight registry symbols. Observation on the lesson side is in notes.")),
    P("M6d-banned-01", "2.9-banned", "course/modules/M/M6/project.html; grader/*.py; cards.json",
      "Fresh: added lines of cards.json in 04626e99..95f3f8cb (116 lines) scanned for we, clearly, obviously, simply, "
      "trivially, note that, in this section, this lesson, our: 0 hits. check_pages M6 PASS (" + S + "/check_pages_r1.txt)."),
    P("M6d-struct-01", "2.9-structure", "course/modules/M/M6/project.html",
      carry("course/modules/M/M6/project.html", "Section order and counts unchanged; check_pages M6 and check_projects M6 PASS fresh.")),
    P("M6d-dag-01", "2.9-dag", "course/modules/M/M6/project.html; tools/check_dag.py; curriculum/01-foundations.yaml:262",
      "Fresh: check_dag M6 PASS (" + S + "/check_dag_r1.txt). The M6 entry moved from line 261 (pin 04626e99) to line 262 in "
      "curriculum/01-foundations.yaml because of the +1 hunk at line 183; its content is unchanged. AP1 prereqs include M6 "
      "(curriculum/03-markets.yaml:268) and SC1 prereqs are [M6] (:509); both lines unchanged."),
    P("M6d-gates-01", "2.9-gates",
      "tools/check_pages.py, check_projects.py, check_dag.py, run_labs.py, run_graders.py, mutate_graders.py, page_smoke.py, verify_refs.py, render_curriculum.py, build_site.py",
      "Fresh on 95f3f8cb: check_pages M6 PASS; check_projects M6 PASS; check_dag M6 PASS; run_labs M6 15/15; run_graders M6 "
      "50/50; mutate_graders M6 56/56; page_smoke M6 PASS for L04, L10 and project; ruff and mypy PASS; pytest on "
      "test_page_checks, test_run_labs, test_docs_figures, test_refs, test_labs: all pass (" + S + "/pytest_r1.txt); "
      "verify_refs --offline 560 entries, 0 problems; render_curriculum regenerates with no diff (curriculum diff exit 0); "
      "build_site --check: 'site data current: 6 outputs'. Not run: the live verify_refs run (network), fetch_data --check "
      "(no data file changed), the full repo pytest suite (not in this slice)."),
]

SAMPLE_BASE = [
    ("M6d-card-sample-000", "M6-c001", "Definition 1.1 sigma-algebra axioms S1-S3 (L01)"),
    ("M6d-card-sample-010", "M6-c012", "probability space definition (L02 Definition 1.2)"),
    ("M6d-card-sample-020", "M6-c023", "integral of a simple function (L03 Definition 2.1)"),
    ("M6d-card-sample-030", "M6-c034", "monotone convergence / supremum definition (L04)"),
    ("M6d-card-sample-040", "M6-c045", "general Fubini statement, Assumption F (L05)"),
    ("M6d-card-sample-050", "M6-c055", "finite-set absolute continuity, Lemma 1.2 (L06)"),
    ("M6d-card-sample-060", "M6-c066", "conditional expectation, Definition 2.1 (L07)"),
    ("M6d-card-sample-070", "M6-c076", "natural filtration properties, Proposition 2.1 (L08)"),
    ("M6d-card-sample-080", "M6-c086", "hitting-time stopping time, Proposition 9.5 (L09)"),
    ("M6d-card-sample-090", "M6-c096", "optional stopping, bounded case, Theorem 10.3 (L10)"),
    ("M6d-card-sample-100", "M6-c106", "submartingale, Definition 11.1 (L11)"),
    ("M6d-card-sample-110", "M6-c117", "martingale convergence general statement, Result 12.6 (L12)"),
    ("M6d-card-sample-120", "M6-c127", "adaptedness, Definition 1.1 (L08)"),
]
for rid, card, what in SAMPLE_BASE:
    rows.append(P(rid, "2.7-cards-sample", "course/modules/M/M6/cards.json (" + card + ")",
                  carry("cards.json " + card + " (byte-identical in 04626e99..95f3f8cb: not among the 22 changed cards) and "
                        "its cited passage " + what + " (no delta hunk in the cited lines)",
                        "Card text re-read against the current lesson: consistent, no number, label cited exists.")))

rows += [
    P("M6d-cards-dup-01", "2.7-cards-dup", "course/modules/M/M6/cards.json (full scan, 141 cards)",
      "Fresh: 141 cards, duplicate ids 0, duplicate fronts 0, duplicate backs 0 (" + S + "/cards_numbers_grades_r1.txt). "
      "Base had 131; delta removed M6-c049 and M6-c137 and added M6-c138..M6-c149."),
    P("M6d-cards-numbers-01", "2.7-cards-numbers", "course/modules/M/M6/cards.json; course/modules/M/M6/L*.html",
      "Fresh: every numeric token of all 141 cards appears in the M6 lesson text (" + S + "/cards_numbers_grades_r1.txt, "
      "0 missing). Changed-card numbers were also checked against the lab outputs (see M6d-delta-cards-01)."),
    P("M6d-cards-lab-A-01", "2.7-cards-lab", "cards.json c007, c017, c030, c032, c040, c061, c071 (c049 removed); tests/labs/M6/lab-M6-L01..L07",
      "Re-verified (subject changed: c049 removed, c007, c017, c040 changed). c007 counts 4, 16, 8 and the candidate line "
      "(" + S + "/lessons_txt/L01.txt lines 141-149). c017 'total mass one False' for six weights 3/20 (L02 lab output). c040 integrals "
      "equal 1 for n 1..20 (L04 lab output: 'in every case: True'). c030, c032, c061, c071 identical; their lab outputs "
      "(L03 Part A/B, L06 densities 2, 1/2, 2, 1/3, L07 cell averages 1, 6/5, 6/7) unchanged in run_labs M6 PASS."),
    P("M6d-cards-lab-B-01", "2.7-cards-lab", "cards.json c081, c090, c100, c102, c105, c110, c112, c113, c121; tests/labs/M6/lab-M6-L08..L12",
      "Re-verified (subject changed: c102, c105, c110 changed). c102: K=1000 -> m=9, 1-2^-9 = 0.9980468750, wealth on ruin 489 "
      "(" + S + "/lessons_txt/L10.txt line 183; page text line 198). c105: K+1-2^m, zero iff K+1 power of two (K=1,3,7,15). c110: E[S_N^2] = N "
      "(L11 Problem R3). c081, c090, c100, c112, c113, c121 identical; their lab outputs unchanged (run_labs M6 PASS)."),
    P("M6d-cards-grade-01", "2.7-cards-grade", "cards.json grade/basis fields; L05-L12 grade statements",
      "Fresh: grades in 141 cards: T 81, C 18, no grade (definition/theorem cards) 42; every C card has a basis; no invalid grade "
      "(" + S + "/cards_numbers_grades_r1.txt). Changed cards re-graded: c040, c017, c007, c147, c149, c062, c130 are C with lab "
      "basis; c138-c146 and the other changed T cards state results proved on the page under their stated hypotheses (L02 "
      "Prop 1.3(c),(d); L06 Thm 2.2(c); L10 Prop 10.7, 10.9(a),(c) with Assumption CE named; L12 Lemma 12.1 with Assumption OA named)."),
    P("M6d-cards-c072-01", "2.7-cards-lab", "course/modules/M/M6/cards.json M6-c072 (back); course/modules/M/M6/L07.html:316; tests/labs/M6/lab-M6-L07-1.py",
      carry("cards.json M6-c072, course/modules/M/M6/L07.html:316 (outside every L07 delta hunk: 49, 102, 132, 291-297, 421, 487) "
            "and tests/labs/M6/lab-M6-L07-1.py",
            "Weights 1/16, 2/16, 1/16 and the cell average 1 (lab output 'cell (0, 1, 2) prob 1/4 average 1').")),
    P("M6d-cards-prop-01", "2.7-cards-prop", "course/modules/M/M6/cards.json (cards citing Proposition, Lemma, Theorem, Corollary, Definition, Example, Remark, Problem, Result)",
      "Fresh: 132 label citations in the 141 cards; all resolve to a label of an M6 lesson (" + S + "/card_cites_r1.txt, 0 missing). "
      "Cards c138-c149 cite labels that exist in L02, L06, L10, L11, L12 (statements re-read)."),
    P("M6d-cards-new-01", "2.7-cards-new", "cards.json M6-c130, M6-c138..M6-c149 (new or re-keyed)",
      "Re-verified this round: c130 602 = 729 - 127 (L02 Problem E1 solution; lab prints 602 of 729); c138 Prop 1.3(c); c139 "
      "Prop 1.3(d); c140 Thm 2.2(c) L06; c141 Example 10.8 (-(2^n-1), 2^-n); c142 Prop 10.9(c) with Assumption CE; c143 "
      "Prop 12.8(b); c144 Prop 12.8(c); c145 and c146 Lemma 12.1 with Assumption OA; c147 candidate family, complement {2,3} "
      "missing (L01 lab output); c148 Doob with Z_k = S_k^2, R3; c149 L03 Part B 'True' on each row n 1..10 with C grade. "
      "Removed c137 (wealth 1001/489/1000) is covered by c102, c105."),
    P("M6d-exemplar-A-01", "2.6-rubric-calibration", "course/modules/M/M6/project.html:473-526 (Exemplar A)",
      carry("course/modules/M/M6/project.html:473-526", "Exemplar A's official scores and annotations unchanged (no dedicated blind scorer file for M6-d; base row carried).")),
    P("M6d-rubric-cal-02", "2.6-rubric-calibration", "course/modules/M/M6/project.html:528-530, 465, 562, 601, 573, 593-594",
      carry("course/modules/M/M6/project.html:528-530, 465, 562, 601, 573, 593-594",
            "C5 level-3 element and P2 final sentences in Exemplar B; no dedicated blind scorer file for M6-d (ruling 23), base calibration row carried.")),
    P("M6d-lede-attribution-01", "2.9-dag", "course/modules/M/M6/project.html:37 (lede), :172 (Context)",
      carry("course/modules/M/M6/project.html:37 and :172, curriculum/03-markets.yaml:268 and :509",
            "AP1 prereqs include M6 (03-markets.yaml:268) and SC1 prereqs [M6] (:509); both unchanged in this delta.")),
    P("M6d-delta-cards-01", "2.7-cards-delta",
      "cards.json: changed M6-c002, c007, c013, c016, c017, c031, c040, c044, c058, c062, c073, c080, c101, c102, c104, c105, c110, c111, c114, c118, c122, c130; removed c049, c137; added c138-c149",
      "Every changed, added and removed card re-derived against its current lesson text (L01, L02, L03, L04, L05, L06, L07, L08, "
      "L10, L11, L12) and, where a lab is cited, against the page's lab output. Changes are wording alignments to the lesson "
      "text (ruling 10) plus the new cards. Removal of c049 (L05 Lab 1 integrability card) leaves L05 with its other cards "
      "(check_pages M6 PASS). Raw diff: " + S + "/cards_delta_r1.txt and M6_slice_delta_04626e99_95f3f8cb.diff."),
    P("M6d-delta-lessons-01", "2.4-proofs",
      "course/modules/M/M6/L07.html (Remark 2.3, 2.6, Thm 2.2, Part D text, Q6); L08.html (sec 1, Bias, P3, Q9); L10.html (why-it-matters, Prop 10.9, Example 10.8); L11.html (E2); L12.html (why-it-matters, R3)",
      "Each changed passage read in the current text: L07 Remark 2.3 (zero-weight point needs only Prob(B_j)>0, with Theorem 2.2 as stated), "
      "L07 Part D interpretation (125 candidates, not all G-measurable; Thm 2.2(a) unique minimizer), L08 sec 1 (weights w(omega) replacing p), "
      "L10 why-it-matters (Assumption CE of L07), L11 E2 (largest ratio at N=12), L12 why-it-matters (Assumption OA) and R3 (Lemma 12.1 "
      "under Assumption OA). Each statement agrees with its proof and its lab output. Observation on symbol w is in notes."),
    P("M6d-delta-labL04-01", "2.5-lab", "tests/labs/M6/lab-M6-L04-1.py (module docstring); course/modules/M/M6/L04.html embedded lab",
      "Module docstring now says 'except the two lines that are labelled rounded'; the output has two lines labelled rounded "
      "(partial sum to N = 10 and N = 100, " + S + "/lessons_txt/L04.txt). run_labs M6 15/15 fresh (page embeds the twin). "
      "page_smoke M6 L04 PASS (" + S + "/page_smoke_L04_L10_r1.txt)."),
    P("M6d-delta-curriculum-01", "2.9-dag", "curriculum/01-foundations.yaml (hunks at 172, 183, 442; M6 entry 262)",
      "The delta hunks in 01-foundations.yaml belong to other units: M3 (a concept label at 172, the covariance-matrix project brief at 183) and CS2 (the streaming-statistics project brief at 442). "
      "The M6 block is unchanged. render_curriculum regenerates CURRICULUM.md and curriculum.json with no diff (" + S +
      "/render_curriculum_r1.txt); build_site --check PASS (" + S + "/build_site_check_r1.txt)."),
    P("M6d-delta-index-01", "2.2-prose", "course/modules/M/M6/index.html:138",
      "The only index.html change is 'Lessons 1 and 2 build the measure space' becoming 'construct the measure space'. No number and no "
      "claim changed; hours (lines 29-30) unchanged; check_pages M6 PASS."),
]

# Mutants: all files in ledgers/M6/mutants, with the result of mutate_graders this round.
mutants = []
for line in (ROOT / S / "mutate_all_r1.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^KILLED (\S+\.py): (.*) -> (.*)$", line)
    if not m:
        continue
    fname, desc, killed = m.group(1), m.group(2), m.group(3)
    mutants.append({"id": fname[:-3], "description": desc, "killed_by": killed})

fragment = {
    "unit": "M6",
    "slice": "d",
    "round": 1,
    "verifier": "independent verifier (Haiku), M6 slice d, round 1 (closing delta, ruling 30; no new mutants, ruling 37)",
    "pin": HEAD,
    "base": BASE_PIN,
    "checkout": str(ROOT),
    "scratch": S,
    "verified_at": "2026-11-09T16:06:01+00:00",
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [
        "The base fragment is pinned at 04626e99, but its round-5 evidence cites mutants r5_01..r5_03 that were added by commit "
        "9fd6aedd, and mutants m6c_r6_* added by 0d2d0f3f. Both lie inside this delta and were re-run here (56/56 killed).",
        "references/references.json changed (used_by and generated_at only). M6 cites neither changed key.",
    ],
    "notes": [
        "Scope: the base fragment's notes (project.html, cards.json, L07/L10 cited passages, index.html, grader, labs, starter, references, notation, python.js, meta.yaml) were re-read against git diff 04626e99..95f3f8cb. Delta paths in slice d: cards.json (22 changed, 2 removed, 12 added), index.html:138, lab-M6-L04-1.py docstring, lessons L01-L12 passages cited by cards and the project page, references.json (used_by), curriculum/01-foundations.yaml (other units; M6 block unchanged). project.html, grader/*, tests/labs/M6/lab-M6-project-*.py, meta.yaml, the plan, python.js, notation.json are byte-identical to the pin.",
        "Carried rows carry the base evidence under the carry prefix (their cited subject is byte-identical). Fresh rows cite this round's outputs under " + S + "/.",
        "No new mutants were written (ruling 37). Observation (not a ruling-26 kind): ledgers/M6/mutants now holds four slice-c lab-twin files (m6c_r6_L09_depends_always_true, m6c_r6_L09_depends_check_skipped, m6c_r6_L10_ruin_off_by_one, m6c_r6_L11_grid_drops_last). They define run_capital, part_a, main and no doubling_outcome, so the grader's test_capital_of_zero_or_less_raises_whatever_the_base[0] fails on AttributeError, an incidental kill. They should move out of ledgers/M6/mutants (lab twins are demonstrations, not grader mutants). The count 56/56 therefore includes four vacuous kills; the 52 grader mutants are all killed.",
        "Observation (not a ruling-26 kind): symbol w is used with two meanings inside M6. The closing delta changed L08 section 1 to 'weights w(omega) > 0' (replacing p), while L10 Lemma 10.6 uses w for the index of the first win ('Let \\(w\\) be the index of the first win'). Not a registry symbol (notation/notation.json has none of these), so not a FAIL row; a LOW item for the lesson owner.",
        "Calibration: no dedicated blind exemplar scorer file for M6-d exists in ~/.fanout/blind/ (ruling 23). Rubric calibration rows (M6d-rubric-cal-01, M6d-rubric-cal-02, M6d-exemplar-A-01) are carried from the base as the verifier rules require.",
        "Plan conflict (carried from the base round): plan section 6.5(4) asks for a float alternative within one cent; plan 2.1 rule 8 and project.html:178 require exact rounding. Alternative a7 is not counted.",
        "Not checked: the live verify_refs run (network); page_smoke for the other lesson pages (L01-L03, L05-L09, L11, L12) and the full figure sweep (other slices); a Chromium screenshot of the Exemplar B annotations; fetch_data --check (no data changed); the full repo pytest suite (not in this slice).",
    ],
    "summary": (
        "Slice d closing delta (04626e99..95f3f8cb): PASS. 56 base rows; every non-PASS base row: none (base verdict PASS). "
        "Re-verified from scratch: cards subject (22 changed, 2 removed, 12 added), L07/L08/L10/L11/L12 cited passages, the L04 twin, "
        "references.json, the curriculum M6 DAG entry, index.html:138, mutants (56/56 killed), gates. Carried with the carry prefix: "
        "project.html, grader/*, project labs, the 13 sample cards (byte-identical), calibration rows (no blind scorer file)."
    ),
}

problems = ledger.validate(fragment, "M6-d")
print("validate:", problems)
out = ROOT / "ledgers/M6/M6-d.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
