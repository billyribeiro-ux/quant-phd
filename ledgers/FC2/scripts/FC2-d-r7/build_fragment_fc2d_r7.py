"""Build the FC2-d round-7 fragment (ledgers/FC2/FC2-d.json) from this round's checks.

Usage: python3 -I ledgers/FC2/scripts/FC2-d-r7/build_fragment_fc2d_r7.py <repo_root>
Every round-6 row id is kept. Rows whose subject is byte-identical since the round-6 pin (142ecfc) are carried with the
carry prefix; every other row carries the evidence of this round's checks (the script outputs in this directory).
"""

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
S = "ledgers/FC2/scripts/FC2-d-r7/"
r6 = json.loads(Path("/Users/billyribeiro/.fanout/frags/D-FC2-d.round6.json").read_text(encoding="utf-8"))
r6_rows = {r["id"]: r for r in r6["rows"]}

CARRY = "Carried from round 6 ({files} byte-identical since the previous pin 142ecfc): "
carried_files = {
    "fc2d-r2-numbers-lab1": "course/modules/FC/FC2/project.html lines 55-163 and grader/",
    "fc2d-r2-numbers-lab3": "course/modules/FC/FC2/project.html lines 376-486 (the lines 487 and 540 hunks lie outside it)",
    "fc2d-r2-reading-keys": "course/modules/FC/FC2/project.html lines 653-657, references/references.json, notation/notation.json",
    "fc2d-r2-autograder-panel-claims": "course/modules/FC/FC2/project.html lines 285 and 671, course/assets/js/grader.js",
    "fc2d-r2-hub-placement-claim": "course/modules/FC/FC2/project.html line 42 and index.html",
    "fc2d-r2-rubric-C2-level2": "course/modules/FC/FC2/project.html lines 504-512",
    "fc2d-r2-spec-questions": "course/modules/FC/FC2/project.html lines 280-336",
    "fc2d-r2-grader-messages": "course/modules/FC/FC2/grader/test_project.py and grader/reference.py lines 24-56",
    "fc2d-r2-grader-named-conditions-only": "course/modules/FC/FC2/grader/test_project.py and project.html lines 309-316",
    "fc2d-r2-grader-over-constraint-trade-verb": "course/modules/FC/FC2/grader/test_project.py",
    "fc2d-r3-instance-docstring-bounds": "course/modules/FC/FC2/grader/instance.py",
    "fc2d-r3-footer-no-upload": "course/modules/FC/FC2/project.html lines 285 and 671",
    "fc2d-r4-card-c093": "course/modules/FC/FC2/cards.json (FC2-c093) and L06.html",
    "fc2d-r4-card-c123": "course/modules/FC/FC2/cards.json (FC2-c123) and L08.html",
    "fc2d-r4-card-c124": "course/modules/FC/FC2/cards.json (FC2-c124) and L08.html",
    "fc2d-r4-card-c149": "course/modules/FC/FC2/cards.json (FC2-c149) and L06.html",
    "fc2d-r4-card-c150": "course/modules/FC/FC2/cards.json (FC2-c150) and L06.html",
    "fc2d-r4-card-c151": "course/modules/FC/FC2/cards.json (FC2-c151) and L08.html",
    "fc2d-r4-card-c152": "course/modules/FC/FC2/cards.json (FC2-c152) and L08.html",
    "fc2d-r4-card-c153": "course/modules/FC/FC2/cards.json (FC2-c153) and L05.html",
    "fc2d-r5-card-c005": "course/modules/FC/FC2/cards.json (FC2-c005) and L01.html",
    "fc2d-r5-card-c055": "course/modules/FC/FC2/cards.json (FC2-c055) and L04.html",
    "fc2d-r5-card-c154": "course/modules/FC/FC2/cards.json (FC2-c154) and L01.html",
    "fc2d-r5-page-hunk-lab1-hypothesis": "course/modules/FC/FC2/project.html line 55",
    "fc2d-r5-page-hunk-error-conditions": "course/modules/FC/FC2/project.html lines 309-316",
    "fc2d-r6-card-c103": "course/modules/FC/FC2/cards.json (FC2-c103) and L07.html",
    "fc2d-r6-card-c155": "course/modules/FC/FC2/cards.json (FC2-c155) and L05.html",
    "fc2d-r6-page-line321-anchor": "course/modules/FC/FC2/project.html line 321 and the id=exemplars anchor (line 517 unchanged)",
    "fc2d-r6-page-conventions-definitions": "course/modules/FC/FC2/project.html line 55 and lines 325-336",
}
for cid in ["c020", "c041", "c051", "c061", "c082", "c092", "c102", "c112", "c120", "c142"]:
    carried_files[f"fc2d-r2-card-{cid}"] = f"course/modules/FC/FC2/cards.json (FC2-{cid[1:].join(['c', ''])}) and its lesson"
for cid in ["c020", "c041", "c051", "c061", "c082", "c092", "c102", "c112", "c120", "c142"]:
    carried_files[f"fc2d-r2-card-{cid}"] = f"course/modules/FC/FC2/cards.json (FC2-{cid}) and its lesson"

fresh = {}


def F(rid, status, evidence, fix=""):
    fresh[rid] = (status, evidence, fix)


# ---- gates (fresh on 9373ef3) ----
F("fc2d-r2-gate-mutate", "PASS", f"{S}mutate_fc2_r7.out: 'mutate_graders FC2: PASS (76/76 killed)', rc 0 "
  "(tools/mutate_graders.py --unit FC2 --seeds 0-9). The 72 earlier mutants and the four new s7_a..s7_d are all KILLED.")
F("fc2d-r2-gate-run-graders", "PASS", f"{S}run_graders.out: 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.2 s)', rc 0.")
F("fc2d-r2-gate-check-projects", "PASS", f"{S}check_projects_fc2.out: 'check_projects FC2: PASS' rc 0; "
  f"{S}check_projects_all.out: 'check_projects FC2: PASS', rc 0 (the last line reports PC3, the --all run is the gate).")
F("fc2d-r2-gate-check-dag", "PASS", f"{S}check_dag_fc2.out: 'check_dag FC2: PASS'; {S}check_dag_all.out: FC2 line PASS, rc 0.")
F("fc2d-r2-gate-check-pages", "PASS", f"{S}check_pages_fc2.out: 'check_pages FC2: PASS'; {S}check_pages_all.out: FC2 line PASS, rc 0.")
F("fc2d-r2-gate-run-labs", "PASS", f"{S}run_labs_fc2.out: 'run_labs FC2: PASS (11/11)', rc 0.")
F("fc2d-r2-lab-twins-isolated", "PASS", f"{S}twins_isolated.out (twins_isolated_r7.py, python -I -W error, empty temp dir): "
  "lab-FC2-project-1, -2, -3 each rc 0, stderr 0 bytes.")
F("fc2d-r2-lab-page-equals-twin", "PASS", f"{S}twins_isolated.out: expected block equals twin stdout for labs 1, 2, 3 (True); "
  "page code equals twin for labs 1 and 3 (True). Lab 2 is a completion lab: {S}lab2_completion_rule.out: 89 page lines = 89 twin lines, "
  "blanks only at lines 58, 60, 73 ('gap = ___', 'net = ___' x2), 'rule holds: True'.")
F("fc2d-r2-gate-page-smoke", "PASS", f"{S}page_smoke_project.out: 'page_smoke modules/FC/FC2/project.html: PASS', "
  "'in-browser grader: All 90 tests pass on seed 27301708', labs 1-3 run, rc 0.")
F("fc2d-r2-gate-ruff-mypy", "PASS", f"{S}ruff_check.out: 'All checks passed!' rc 0; {S}ruff_format_fc2.out: 15 files already formatted, rc 0; "
  "repo-wide 'ruff format --check .' now reports 551 files already formatted (the M3 file cited in round 6 is no longer reported); "
  f"{S}mypy_labs.out: 'Success: no issues found in 11 source files' rc 0; {S}mypy_grader_strict.out (mypy --strict on a scratch copy: "
  "reference.py as scanner.py, instance.py, test_project.py): 'Success: no issues found in 3 source files' rc 0.")
F("fc2d-r2-gate-pytest-fc2", "PASS", f"{S}pytest_fc2_r7.out: pytest tests/labs/FC2 tests/test_labs.py tests/test_run_labs.py "
  "tests/test_page_checks.py tests/test_memo_exemplars.py -k 'FC2 or fc2 or project or grader' -q: all dots, rc 0. "
  f"(The tracked {S}pytest_fc2.out was restored unchanged.)")
F("fc2d-r2-gate-verify-refs", "PASS", f"{S}verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', rc 0; "
  f"{S}verify_refs_unit_FC2.out: 'live re-verification of FC2: 3 of 560 entries, 0 problems', rc 0.")
F("fc2d-r2-collect-count", "PASS", f"{S}collect_count.out (collect_count_r7.py, python -I): 'collected 90 for 50 seeds' "
  "(seeds 0..49, reference.py as scanner.py). project.html line 320 states 90; the line is unchanged this round.")
F("fc2d-r2-starter-suite-fails", "PASS", f"{S}instances_and_links.out: starter.py as scanner.py, QF_SEED=0: "
  "'starter.py suite rc 1', '82 failed, 8 passed'.")
F("fc2d-r2-hours", "PASS", "course/modules/FC/FC2/project.html line 33 data-hours-project=\"30\" (the main element) and the "
  "table lines 345-352: 2 + 3 + 5 + 9 + 3 + 5 + 3 = 30 (the total row 30). Only the rationale text of line 345 changed; the hour "
  "column is unchanged. index.html data-hours-project=\"30\" and data-hours-lessons=\"60\"; L01..L08 data-hours 6+8+9+7+8+8+8+6 = 60; "
  "60 + 30 = 90 = curriculum/02-economics-finance-core.yaml line 399 hours: 90. Rung 1 rationale 'The interpretation after Lab 1 gives the "
  "reason for each decision' checked against the Lab 1 interpretation (line 163): 9500 kept, 11000 gross 20 below cost 45, four zero "
  "gaps (puts agree with parity), 10500 convexity finding, the other interior strikes on or below the chord.")
F("fc2d-r2-numbers-exemplars", "PASS", "course/modules/FC/FC2/project.html lines 520-634, re-derived with exact fractions. "
  "Exemplar B (lines 526-566): 6500 parity: 151 - 1100 - (5000 - 6175) = 226, net 166; 7000 parity: 90 - 1200 - (5000 - 6650) = 540, "
  "net 480; convexity at 6000: (500 + 2 x 151)/3 = 802/3, minus 330 = -188/3, gross 63, net 3; 6175 = 6500 x 0.95, 6650 = 7000 x 0.95. "
  "Exemplar A (line 590): about 226, about 540, about 63 equal the exact values. Changed lines 543, 586 and 618 are annotation/verdict text "
  "only; no number changed.")
F("fc2d-r2-banned-phrases", "PASS", f"{S}page_text_checks.out (page_text_checks_r7.py over project.html, 673 lines): no banned-phrase "
  "hit and no process/pronoun hit printed; 'about' hedges at lines 486 (about 62.67 = 188/3 to two decimals) and 590 (about 226, about 540, "
  "about 63: equal to the exact values).")
F("fc2d-r2-notation", "PASS", f"{S}page_text_checks.out: 'macro commands []' (no backslash macro on the page). Symbols C, P, S, K, df, "
  "D and the labels P1-P6 are defined on the page (lines 325-336; P6 label line 333). None of the registered symbols of "
  "notation/notation.json is reused with another meaning.")
F("fc2d-r2-dag", "PASS", f"{S}check_dag_fc2.out: 'check_dag FC2: PASS'. The round-7 hunks add no concept link (lines 44, 345, 490, 543, "
  "586, 618 are prose); the prerequisites M4, CF1, FC1 are unchanged (curriculum/02-economics-finance-core.yaml lines 398-400).")
F("fc2d-r2-scope-curriculum-brief", "FAIL", "Re-verified from scratch on 9373ef3. curriculum/02-economics-finance-core.yaml lines "
  "427-429 still read 'Given an embedded option-chain snapshot, detect put-call parity and convexity violations'; the file is byte-identical "
  "to the round-6 pin. project.html line 285 says no market data is embedded and every chain is SIMULATED. The architect decision "
  "(plans/FC2-build-plan.md line 635) allows a SIMULATED chain with a DATA_REQUEST (plans/FC2-open-items.md D1), so the page follows the "
  "architect; the brief text the curriculum states is not met and no amendment has been made.",
  "Architect: amend the brief in curriculum/02-economics-finance-core.yaml lines 427-429 to the SIMULATED-chain scope in "
  "plans/FC2-build-plan.md line 635, or clear D1 with a sourced snapshot.")
F("fc2d-r2-rubric-calibration", "FAIL", "Blind scoring of exemplars with the rubric text only: Exemplar A C3 scores 2 blind "
  "(cell level 2 'Names assumptions for some findings' is met: the passage 'The parity findings depend on the discount factor' at "
  "project.html line 614 names an assumption for some findings). Official C3 is 1 (data-scores='2,1,1,2,1', line 584) with the verdict "
  "'no assumption is named by its label' (line 586) and the annotation 'Misses C3 level 2: names no assumption by label' (line 619). "
  "The level-1 cell is 'No assumption named', which the exemplar contradicts; the reason given for missing level 2 is a level-3 element "
  "(labels). Within one level, so the numeric calibration rule alone would pass, but the official score and its stated reason do not match "
  "the rubric cells; fail closed. Other exemplar scores agree blind (B 4,4,3,3,3; A C1 2, C2 1, C4 2, C5 1).",
  "Score Exemplar A C3 as 2 (data-scores='2,1,2,2,1', line 584), state in the verdict and annotation that it names the discount factor for "
  "the parity findings but no label P1 to P6 (level 3 missed), and keep the level-1 cell wording for C3.")
F("fc2d-r2-rubric-C2-level2", "PASS", "Carried from round 6 (project.html lines 504-512 byte-identical since the previous pin 142ecfc).")
F("fc2d-r2-instances", "PASS", f"{S}instances_and_links.out (instances_and_links_r7.py): 40 seeds (0..19, 1000..1019) all valid, "
  "40 distinct (kind, index, amount, strikes, spot, df) tuples.")
F("fc2d-r2-grader-over-constraint-case", "PASS", f"{S}alts_r7.out (run_alts_r7.py, python -I, the suite on seeds 0..49): "
  "alt1_integer_only, alt2_slope_test, alt3_decimal, alt4_validate_first, alt5_floor_half, alt6_integer_crossmul, alt7_cross_multiplied_integers, "
  "alt8_forward_price_fraction: 50/50 each; each agrees with reference.py on 3000/3000 random chains (ties and zero costs included).")
F("fc2d-r2-alternatives-pass", "PASS", f"{S}alts_r7.out: eight alternative correct implementations pass seeds 0..49 (50/50 each) "
  "and agree with reference.py on 3000/3000 random chains (alt3 is decimal exact, not float; the float alternative of round 4 was not "
  "re-run and is not among the eight).")
F("fc2d-r2-mut-r7-docstrings", "PASS", f"{S}mutant_docstrings.out (mutant_docstrings_r7.py): 72 pre-existing mutants, zero REVIEW flags; "
  "every first docstring line names the error; changed-line counts 2 to 8. The docstring change of reference.py line 68 is mirrored in every mutant.")
F("fc2d-r2-mut-new-killed", "PASS", f"{S}mutate_fc2_r7.out: the round-2 mutants v07..v10 (for example v07_convexity_indices_returned_in_decreasing_order) "
  "are KILLED.")
F("fc2d-r2-mut-r5d-resolved", "PASS", "ledgers/FC2/mutants lists no r5_d file (ls, this round); r5_a, r5_b, r5_c are KILLED in mutate_fc2_r7.out.")
F("fc2d-r2-mut-equivalents", "PASS", f"{S}mutate_fc2_r7.out: 76 of 76 KILLED; a killed mutant is not equivalent to reference.py.")
F("fc2d-r2-cards-full-scan", "FAIL", f"{S}cards_scan.out (cards_scan_r7.py, 155 cards): ids, fronts and backs unique; grades T, C and "
  "ungraded recall cards; near-duplicate review finds two new near-duplicate pairs created this round: FC2-c139 (L02 A1) vs FC2-c156 "
  "(L04 A1), ratio 0.981, and FC2-c140 (L02 A2) vs FC2-c157 (L04 A2), ratio 0.892. Both pairs ask 'What does Assumption A1 (no income) "
  "of Lesson N say?' with the same answer content. The other pairs listed (ratio 0.6 to 0.87) are different questions and are not duplicates.",
  "Remove FC2-c156 and FC2-c157, or replace them with cards that ask something the L02 cards do not, e.g. 'Do Propositions 2.2 and 2.3 "
  "of Lesson 4 use A1?' (answer: no, L04.html line 310 says neither uses A1).")
F("fc2d-r2-cards-refs-numbers", "PASS", f"{S}cards_scan.out: 'card numbers not found in own lesson: [FC2-c076 Section 5]' is a scanner "
  "artefact: L05.html section 5 is 'Where the canon breaks' (h2 section-number 5; the claim 'the early-exercise bound for a put' is in its "
  "passage at L05 text line 397). Every other numbered citation of the changed cards occurs in its lesson (Proposition 1.4, Lab 1, Problem E3, R1, R2, M1, Remark 4.2, Section 4 of L07, Section 5 of L08).")
F("fc2d-r2-card-c010", "PASS", "course/modules/FC/FC2/cards.json FC2-c010 (back changed: 'No probabilities are assigned to the states'). "
  "L01.html text 'this lesson assigns no probabilities to the states' (Problem P3 paragraph); Example 3.4 psi_u = 1/20, psi_d = 17/20 sum to 9/10 (L01.html Example 3.4). PASS.")
F("fc2d-r2-card-c132", "PASS", "cards.json FC2-c132 (back changed). L05.html Remark 4.2: 'proved at date 0 only'; the lesson gives no rule for holding "
  "against exercising at a later date (L05.html line 337, section 4 closing paragraph). PASS.")
F("fc2d-r2-card-c030", "PASS", "cards.json FC2-c030 (back changed to 'Whether every price inside the interval is arbitrage-free is not established'). "
  "L02.html R1 solution (line 507 text): 'The lesson does not prove that every price inside the interval is arbitrage-free.' Same claim. PASS.")
F("fc2d-r2-card-c071", "PASS", "cards.json FC2-c071 (back changed). L05.html Remark 4.2: 'It does not prove the equality V_A(t) = V_E(t) at a date t > 0, "
  "so that equality is a remark, not a proved result.' PASS.")
F("fc2d-r3-scope-changed-hunks", "PASS", f"{S}card_delta.out (card_delta_pins_r7.py 142ecfc..HEAD): 27 cards changed and 2 added "
  "(FC2-c156, FC2-c157); 126 identical. git diff 142ecfc..9373ef3 over course/modules/FC/FC2, tests/labs/FC2, tools, course/assets, "
  "references, notation, curriculum: the FC2 hunks are project.html lines 44, 345, 487, 540, 583, 615; grader/reference.py and "
  "grader/starter.py (docstring line only); cards.json; 27 changed cards; ledgers/FC2/mutants (docstring lines). Every hunk read.")
F("fc2d-r3-df-ppm-link", "PASS", f"{S}instances_and_links.out: 18 internal href targets in project.html, 0 missing.")
F("fc2d-r3-mut-new-killed", "PASS", f"{S}mutate_fc2_r7.out: q3_a_df_rounded_to_four_places, q3_b_gross_tie_toward_zero, "
  "q3_c_convexity_charges_two_legs, q3_d_convexity_explanation_omits_P5 are KILLED.")
F("fc2d-r3-mut-prior-untracked", "PASS", f"{S}mutate_fc2_r7.out: r3_a..r3_d KILLED.")
F("fc2d-r3-exemplar-scores-match-text", "PASS", "project.html exemplar annotations and verdicts (lines 543, 586, 618) agree with each other "
  "and with the data-scores attributes (B '4,4,3,3,3', A '2,1,1,2,1'). The C3 calibration of Exemplar A against the rubric cell is a separate FAIL row (fc2d-r2-rubric-calibration).")
F("fc2d-r4-cards-sample", "PASS", "One card in ten sampled from the 155 cards in the round-7 cards.json, plus all 29 changed or added cards "
  "(see the fc2d-r7-card-* rows). Carried sample rows are byte-identical objects (card_delta.out).")
F("fc2d-r4-mut-u4-new-killed", "PASS", f"{S}mutate_fc2_r7.out: u4_a_parity_explanation_omits_P6, u4_b_cost_ignores_half_spread, u4_c_discounted_strike_floor_division KILLED.")
F("fc2d-r5-mut-w5-new-killed", "PASS", f"{S}mutate_fc2_r7.out: w5_a_parity_gap_truncated_toward_zero, w5_b_length_check_rejects_only_short_lists, w5_c_gross_rounded_up_to_ceiling KILLED.")
F("fc2d-r5-alt7-cross-multiplied", "PASS", f"{S}alts_r7.out: alt7_cross_multiplied_integers 50/50 seeds; 3000/3000 agreement with reference.py.")
F("fc2d-r5-explanation-direction-untested", "PASS", f"{S}direction_probe.out (direction_probe_r7.py): a direction-swapped parity "
  "explanation passes seeds 0..9. Not a FAIL: the spec's Required outputs require the explanation to name the rule and the labels P1 to P6 "
  "('names the rule and the assumptions the finding depends on, by the labels'), not the trade direction. The direction is stated in the conventions "
  "(project.html line 'A positive gap means the call is rich ...'), but no explanation sentence is required to repeat it. Observation only.")
F("fc2d-r6-card-c072", "PASS", "cards.json FC2-c072 (front and back changed this round). L05.html Lab 1 expected block: "
  "'synthetic set: parity cost ... [0, 0, 0, 0, 0]' and 'parity portfolio payoff nonzero at 0 of 40 (strike, expiry spot) pairs'. "
  "Front asks for both; back: zero at each of five strikes 80 to 120 USD, none of 40 pairs nonzero. PASS.")
F("fc2d-r6-card-c073", "PASS", "cards.json FC2-c073 (front and back changed). L05.html Lab 1 expected: 'planted parity error ... [0, 0, -300, 0, 0]' "
  "(third strike = 100 USD) and 'nonzero at 0 of 40'; L05.html Research R1 ('Why the payoff check cannot see a parity error'). PASS.")
F("fc2d-r6-mut-w6-new-killed", "PASS", f"{S}mutate_fc2_r7.out: w6_a..w6_d KILLED.")
F("fc2d-r6-alt8-forward-price", "PASS", f"{S}alts_r7.out: alt8_forward_price_fraction 50/50 seeds and 3000/3000 agreement.")
F("fc2d-r7-page-rung1-line44", "PASS", "project.html line 44 (ladder, Rung 1): 'with the decision on each strike printed'. The Lab 1 expected block (project.html, pre.expected of lab-FC2-project-1) prints a verdict for each of the six strikes in step 1 and a verdict or 'no violation' for each interior strike in step 2; twins_isolated.out shows the expected block equals the twin stdout (True). PASS.")
F("fc2d-r7-page-brief-line490", "PASS", "project.html line 490: 'Write for a risk manager who knows Lessons 1 to 6 of this module'. "
  "Lessons 1 to 6 are L01.html..L06.html of FC2 (the module has eight lessons). PASS.")
F("fc2d-r7-exemplar-B-C3-annotation-line543", "PASS", "project.html line 543 (exemplar B C3, level 3): 'names P4 and P6 for the two parity "
  "findings' ↔ Model-free passage ('use the supplied discount factor ... (P4), and P6 for their cost'); 'P1, P2, P5 and P6 for the convexity "
  "finding' ↔ 'uses P1, P2 and P5 for its test and P6 for its cost'; 'P1 to P3 for the whole note (Limitations)' ↔ 'one expiry, European exercise "
  "and no income, which are P1 to P3'. Consistent with the exemplar text. PASS.")
F("fc2d-r7-exemplar-A-C4-annotation-line618", "PASS", "project.html line 618 (exemplar A C4): 'says the parity findings use the discount "
  "factor, without the label P4, and does not separate the convexity finding' ↔ passage 'The parity findings depend on the discount factor. "
  "The rest is standard.' (no P4 label, convexity not separated). Level 2 as scored. PASS.")
F("fc2d-r7-grader-convexity-docstring", "PASS", "grader/reference.py line 68 docstring: 'The interior indices j, in increasing order, at which "
  "the call lies strictly above the chord (convexity fails).' The code (line 76: _second_difference < 0) implements exactly this, and "
  "project.html line 300 states 'in increasing order, at which the call lies strictly above the chord'. grader/starter.py line 23 drops "
  "'strictly' ('lies above the chord of its two neighbours'). On an exact tie the test (grader/test_project.py lines 378-381, "
  "'a call exactly on the chord is not flagged') requires no flag, which 'above' also implies, so the stub gives the same reading. "
  "Observation: starter wording could say 'strictly'; not a FAIL.")
F("fc2d-r7-cards-delta-read", "PASS", f"{S}card_delta.out: changed = FC2-c007 c010 c014 c021 c030 c037 c046 c059 c060 c068 c069 c071 c072 "
  "c073 c076 c079 c080 c081 c094 c095 c113 c114 c125 c128 c132 c137 c145; added = c156 c157. Each changed card read against its lesson (rows below).")
F("fc2d-r7-mut-s7-new-killed", "PASS", f"{S}mutate_fc2_r7.out: s7_a_parity_gap_discounts_the_spot (killed by test_parity_gap_matches_exact_rounding_seed[0]), "
  "s7_b_convexity_loop_runs_past_last_strike (test_convexity_flags_the_last_interior_index), s7_c_convexity_net_omits_half_spread "
  "(test_scan_matches_exhaustive_oracle_second_chain), s7_d_parity_gap_floors_the_signed_gap (test_parity_gap_matches_exact_rounding_seed[0]): KILLED. "
  f"Written by {S}write_mutants_r7.py (one changed line each, the target text asserted to occur once).")

# card rows for the changed and added cards
card_text = {
    "c007": "L01.html Remark 3.3: 'Proposition 3.2 runs one way ... In the market of Example 3.4 they are unique' (uniqueness stated in Remark 3.3, as cited)",
    "c014": "L01.html Part A printed 'state prices (state u, state d): 1/20 17/20' (expected block) and 'Proposition 3.2 shows it, using the state prices that Part A prints' (Problem E3, title 'What the zero count in Part A does and does not show')",
    "c021": "L02.html Example 2.4: 50e^{0.025} = 51.2658, 51.27 to the cent, 'Lab 2, Part A, prints 5126.58'; expected block 'no-arbitrage forward price, in cents: 5126.58'",
    "c037": "L03.html Remark 1.4: 'Margin requirements ... are not modelled here, and the identity says nothing about whether the account is large enough to meet them'; Proposition 1.3 identity",
    "c046": "L03.html expected block (Part B): 'value to the fixed payer of a swap struck 1 percentage point higher, in cents: -4415468'; P2 solution 'printed value of minus 4,415,468 cents on a notional of 100,000,000 cents'",
    "c059": "L04.html Remark 2.4: 'it does not say that the inequality is strict'; L04.html line 258: 'This lesson does not claim that the inequality is strict for any put or call'",
    "c060": "L04.html after Proposition 2.2: 'Exercising at once is therefore never better than selling at the market price' (L04.html line 262); back 'Not as a rule' is the lesson's own qualification (L04.html line 262)",
    "c068": "L05.html Definition 3.1: lambda = (K3 - K2)/(K3 - K1); C(K2) <= lambda C(K1) + (1 - lambda) C(K3); 'the weight lambda depends on the strikes'",
    "c069": "L05.html Theorem 3.2 proof: 'We show g(s) >= 0 for every s >= 0, by four cases'",
    "c076": "L05.html section 5 'Where the canon breaks' (h2 section-number 5): 'with K = 100, S_t = 50, tau - t = 1 and r = 0.10, the bound is 100e^{-0.1} - 50 = 40.48'; 40.48 < 50 (exercise). The 'Section 5' citation is correct; see fc2d-r2-cards-refs-numbers",
    "c079": "L05.html Lab 1 expected block: 'convexity in strike, triples checked 10, violated 3' and the three lines 'call at 9000 cents lies above the chord of 8000 and 10000/11000/12000 cents' (same middle call)",
    "c080": "L05.html Remark 4.2: 'It requires r >= 0: with r < 0 the bound in Theorem 2.2(b) can fall below S_t - K'; Problem R2 solution (120 - 110.517 = 9.48 < 20)",
    "c081": "L06.html Definition 1.1: R_f = 1 + r_1, 1/R_f; the text 'The letter r without a subscript ... this lesson does not use it'",
    "c094": "L06.html Example 3.4: V(0,0) = 45 currency units; Lab 1 expected block 'V0 = 45 = 4500 cents'",
    "c095": "L06.html Lab 1 expected block: 'path uu: terminal wealth 125 = payoff 125: True', 'path ud/du/dd: ... True', 'self-financing strategy reproduces every node value and every payoff: True'",
    "c113": "L07.html Lab 1 expected block: 'put-call parity holds for the closed-form put to 1e-9: True'; Proposition 1.4 (put from call and parity)",
    "c114": "L07.html M1 solution ('Lab 1 prints the same values, d1 = 0.350000 and d2 = 0.150000') and Lab 1 expected block 'Black-Scholes d1=0.350000 d2=0.150000'",
    "c125": "L08.html Lab 1 expected table: 'halvings' column 37 in all nine rows",
    "c128": "L08.html section 5 'Misconceptions' (h2 section-number 5): 'The inversion check in Lab 1 starts from the formula's own price ... It does not test any quote, because no quote enters the lab'",
    "c132": "L05.html Remark 4.2 and the section 4 closing paragraph: 'gives no rule for holding against exercising at a later date'",
    "c137": "L06.html Example 3.4: V(1,1) = 75; Lab 1 expected block '75'",
    "c145": "L07.html section 4 'Where the canon breaks': 'The formula is stated as A8 and used, not derived'; A8 text 'is a premise of this lesson and is not proved here'",
    "c156": "L04.html A1 (line 60-81): 'The underlying pays no dividend, coupon or storage cost over the life of the contract.' (verbatim). Content is correct; the card duplicates FC2-c139 (see fc2d-r2-cards-full-scan)",
    "c157": "L04.html A2 (line 61): 'There are no transaction costs and no bid-ask spread. The underlying and the options can be sold short, and cash can be lent and borrowed at the riskless rate.' Content is correct; duplicates FC2-c140",
}
for cid, locs in card_text.items():
    rid = f"fc2d-r7-card-{cid}"
    status = "PASS"
    evidence = f"course/modules/FC/FC2/cards.json FC2-{cid} (changed or added this round). {locs}."
    fix = ""
    if cid in ("c156", "c157"):
        status = "PASS"
        evidence += " Content matches the lesson; the duplication is recorded in fc2d-r2-cards-full-scan."
    fresh[rid] = (status, evidence, fix)

F("fc2d-r2-cards-lab-numbers", "PASS", "Re-verified for FC2-c095 (changed this round): L06.html Lab 1 expected block prints True for paths uu, ud, du, dd and for the self-financing check (see fc2d-r7-card-c095). Carried from round 6 for FC2-c012, c013, c147 and c148: those card objects are byte-identical since 142ecfc (card_delta.out) and their lessons are unchanged this round.")

# ---- build rows: keep every round-6 id, then add the round-7 rows ----
rows = []
for rid, r6row in r6_rows.items():
    if rid in fresh:
        status, evidence, fix = fresh[rid]
        if status == "PASS" and evidence.startswith("Carried from round 6"):
            pass
    elif rid in carried_files:
        if r6row["status"] != "PASS":
            raise SystemExit(f"cannot carry a non-PASS row: {rid}")
        status = "PASS"
        body = re.sub(r"^Carried from round \d+ \(.*?\):\s*", "", r6row["evidence"], count=1)
        evidence = CARRY.format(files=carried_files[rid]) + body
        fix = ""
    else:
        raise SystemExit(f"no round-7 decision for {rid}")
    rows.append({"id": rid, "check": r6row["check"], "location": r6row["location"], "status": status,
                 "evidence": evidence, "fix": fix})
known = {r["id"] for r in rows}
for rid, (status, evidence, fix) in fresh.items():
    if rid not in known:
        src = {"fc2d-r7-card-c156": "2.6", "fc2d-r7-card-c157": "2.6"}
        rows.append({"id": rid, "check": "2.2/2.6" if rid.startswith("fc2d-r7-card-") else "2.2/2.6",
                     "location": rid, "status": status, "evidence": evidence, "fix": fix})
        known.add(rid)
for rid, (status, evidence, fix) in fresh.items():
    pass

# fix up the three card rows that the round-6 fragment has under a different check label (kept rows only)
mutants = []
for line in (root / S / "mutate_fc2_r7.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+)\.py: (.*?) -> (.*)$", line)
    if m:
        status, name, desc, killed = m.groups()
        mutants.append({"name": name, "description": desc,
                        "killed_by": killed if status == "KILLED" else "SURVIVED"})
frag = {
    "unit": "FC2",
    "slice": "FC2-d",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 7 (did not build FC2)",
    "pin": "9373ef398589097500ea849e30ff9da423b98943",
    "base": "142ecfc (round-6 pin); the delta is listed in notes",
    "checkout": str(root),
    "scratch": "/tmp/fc2d-r7-alts (correct alternatives), /tmp/fc2d-r7-mypy (strict mypy copy), /tmp/fc2d-r7-text (lesson text dumps)",
    "verified_at": "2026-11-04T07:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "",
    "summary": "",
}
n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] != "PASS")
frag["summary"] = (f"{len(rows)} rows: {n_pass} PASS, {n_fail} non-PASS. Non-PASS: fc2d-r2-scope-curriculum-brief (carried FAIL, architect "
                   "action), fc2d-r2-rubric-calibration (Exemplar A C3 score contradicts the level-1 cell), fc2d-r2-cards-full-scan "
                   "(duplicate cards FC2-c139/c156 and c140/c157). Mutants: 76, 76 killed (72 prior, 4 new s7_a..s7_d).")
frag["notes"] = (
    "Round 7 on pin 9373ef3 (round-6 pin 142ecfc). Delta inside FC2-d: project.html lines 44, 345, 490, 543, 586 and 618 (text only; "
    "no lab code, no number in an unchanged hunk); grader/reference.py and grader/starter.py (one docstring line each, convexity_violations); "
    "cards.json (27 changed, 2 added: FC2-c156, c157; per-card comparison in card_delta.out); ledgers/FC2/mutants (all 72 mutants gained "
    "the same docstring line through the reference change; w6 mutants already listed). No change to tests/labs/FC2, the grader tests, the "
    "lesson HTML, curriculum, plans, references or notation. Observations (not rows): (a) the starter docstring drops 'strictly' (fc2d-r7-grader-convexity-docstring); "
    "(b) the exemplar A calibration issue is a FAIL row; (c) round-6 observation (plan 5.5 item 3 float alternative vs project.html line 308 'exact fractions') "
    "is still open for the architect and was not counted; (d) round-6 observation on rubric C2 level 4 is unchanged. "
    "Pre-existing files in the checkout: ledgers/FC2/FC2-d.json (pin 0d2d0f3, another lineage) and tracked ledgers/FC2/scripts/FC2-d-r7/* "
    "(other lineages' scripts, referencing other checkouts) were not used; this round's outputs were written beside them with the _r7 suffix or distinct names. "
    "Not run: the full repo gate (render_curriculum.py, build_site.py --check, fetch_data.py --check, run_graders for other units, pytest for all of tests/); "
    "those belong to other slices or to the unit gate."
)
out = root / "ledgers" / "FC2" / "FC2-d.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(rows), "pass", n_pass, "non-pass", n_fail, "mutants", len(mutants))
