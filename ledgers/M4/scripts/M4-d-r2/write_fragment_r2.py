"""Write the verifier D round-2 fragment ledgers/M4/M4-d.json (unit M4, slice d, round 2).

Rows are the round-1 row ids (all kept) plus new ids. Mutants are read from the final mutation-gate output
(ledgers/M4/scripts/M4-d-r2/mutate_M4_seeds0-9_final.out), one entry per KILLED line. The verdict is computed by
tools/ledger.py rules: PASS only if every row is PASS.
Run from the checkout root: .venv/bin/python ledgers/M4/scripts/M4-d-r2/write_fragment_r2.py
"""

from __future__ import annotations

import datetime
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "ledgers/M4/scripts/M4-d-r2"
GATE = OUT / "mutate_M4_seeds0-9_final.out"
FRAGMENT = ROOT / "ledgers/M4/M4-d.json"

CARRY = "Carried from round 1 ({files} byte-identical since the previous pin d0f39c09): "


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> dict[str, str]:
    entry = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        assert fix, rid
        entry["fix"] = fix
    return entry


ROWS: list[dict[str, str]] = [
    row(
        "d1-2.6-ladder",
        "2.6 ladder: rung 1 solved, rung 2 instant, rung 3 scope, rung 4 open",
        "course/modules/M/M4/project.html#ladder, #rungs, #spec, #stretch",
        "PASS",
        "#ladder and #stretch are byte-identical to d0f39c09. #rungs changed only at the Lab 1 interpretation sentence "
        "(project.html:144), which says the unmatched-variance line is a formula; tests/labs/M4/lab-M4-project-1.py:75 "
        "prints NU / (NU - 2) with no sampling. Rung 2 blanks: run_labs --unit M4 --page project gives 'run_labs M4: "
        "PASS (3/3)' (ledgers/M4/scripts/M4-d-r2/run_labs_M4_project.out). Rung 3 spec text is read in full (#spec).",
    ),
    row(
        "d1-2.6-spec-questions",
        "2.6 spec: questions a competent student would have to ask",
        "course/modules/M/M4/project.html#conditions; course/modules/M/M4/grader/reference.py:65",
        "PASS",
        "Round-1 FAIL (is a negative position valid?) is fixed. project.html:223 now accepts 'a negative position' and "
        "says it is a short position with the opposite sign; reference.py:65-66 accepts any whole number; "
        "test_a_short_position_is_valid_and_reverses_its_loss (test_project.py, FAMILY_CASES) passes on the reference "
        "for seeds 0-9 (signt_m17_collect_seeds.out) and on seeds 0-49 (run_graders_M4_0-49.out). The other interface "
        "questions (families, nu, n_draws, cov shape and symmetry, pivots, quantile types, units of cov) are answered on "
        "the page (Conventions items 1-5, Conditions). The sign-of-Student-t gap is a separate row (d2-2.6-constraints-"
        "exceptions).",
    ),
    row(
        "d1-2.6-hours",
        "2.6 hours: component sum and own estimate within 30 %",
        "course/modules/M/M4/project.html#budget; data-hours-project",
        "PASS",
        CARRY.format(files="course/modules/M/M4/project.html#budget (the section is byte-identical, 1672 characters)")
        + "components 2+2+12+8+4+2 = 30, equal to the total row and to the 30 h of the hub; the hub card for the project is "
        "unchanged.",
    ),
    row(
        "d1-2.6-autograder-reference",
        "2.6 autograder: run_graders seeds 0-49 on reference.py",
        "course/modules/M/M4/grader/reference.py",
        "PASS",
        "Re-run this round: '.venv/bin/python tools/run_graders.py --unit M4 --seeds 0-49' -> 'run_graders M4: PASS "
        "(reference 50/50 seeds, slowest 0.9 s)' (ledgers/M4/scripts/M4-d-r2/run_graders_M4_0-49.out). Collect-only "
        "138 tests = the page's '138 checks'. Page flags (QF_SEED=0..9, 1093; pytest -q -p no:cacheprovider --assert=plain "
        "-W error): all pass, with the one nu-dependent skip where nu < 5 (signt_m17_collect_seeds.out).",
    ),
    row(
        "d1-2.6-instances",
        "2.6 instances: valid, and answers change across seeds",
        "course/modules/M/M4/grader/instance.py",
        "PASS",
        CARRY.format(files="grader/instance.py")
        + "and re-checked this round: verifyD2_check_instances.py over seeds 0-1999: 0 invalid; every instance has 2 or 3 "
        "positive whole-cent positions in [100000, 5000000] cents; nu in {3,...,8}; n_draws at most 19987 and never a "
        "multiple of 100; label SIMULATED.",
    ),
    row(
        "d1-2.6-mut-own",
        "2.6 mutation: at least 3 verifier-written student-error mutants, all killed",
        "ledgers/M4/mutants/v1_01 .. v1_06 (generator ledgers/M4/scripts/M4-d-r1/verifyD1_make_mutants.py)",
        "PASS",
        "The six round-1 mutants v1_01..v1_06 are in the final gate output as KILLED (mutate_M4_seeds0-9_final.out): "
        "v1_01 by test_gaussian_loss_variance_matches_portfolio_covariance, v1_02 by "
        "test_a_short_position_is_valid_and_reverses_its_loss[student_t-5], v1_03 by test_quantile_99_convention_on_small_lists, "
        "v1_04 by test_a_short_position_is_valid_and_reverses_its_loss[gaussian-None], v1_05 by the variance test, "
        "v1_06 by test_student_t_cross_term_matches_matched_covariance. Four new round-2 mutants v2_01..v2_04 are also "
        "KILLED (rows in mutants).",
    ),
    row(
        "d1-2.6-mut-existing",
        "2.6 mutation: the existing mutants re-run on seeds 0-9",
        "ledgers/M4/mutants/*.py (118 files at the end of this round)",
        "PASS",
        "'.venv/bin/python tools/mutate_graders.py --unit M4 --seeds 0-9' exits 0 with 'mutate_graders M4: PASS (118/118 "
        "killed)' (ledgers/M4/scripts/M4-d-r2/mutate_M4_seeds0-9_final.out, EXIT=0). Before the four round-2 mutants were "
        "added the gate gave 114/114 (mutate_M4_seeds0-9.out, EXIT=0). Survivors of round 1 (m11, r9_03, v4_m02) are now "
        "killed (rows below); m17 left the mutants folder and is ruled on in d1-2.6-mut-m17.",
    ),
    row(
        "d1-2.6-mut-m11",
        "2.6 mutation: m11 loss sign flipped",
        "ledgers/M4/mutants/m11_loss_sign_flipped.py; project.html Conventions item 2",
        "PASS",
        "Killed on seed 0 by test_gaussian_stream_is_frozen_and_the_loss_is_minus_the_weighted_return (final gate output). "
        "The new test is backed by Conventions item 5 (frozen Gaussian stream) and item 2 (sign), project.html:212 and :215.",
    ),
    row(
        "d1-2.6-mut-r9_03",
        "2.6 mutation: r9_03 chi-square reused on alternate draws",
        "ledgers/M4/mutants/r9_03_*.py; project.html Conventions item 5 and #contract-notes",
        "PASS",
        "Killed on seed 0 by test_student_t_draws_do_not_share_chi_square (final gate output). The page states the check "
        "(project.html:228: 'at nu = 3 only ... share of 1/4 within five standard errors over 40,000 draws'), and the test "
        "uses exactly that tolerance (test_project.py, test_student_t_draws_do_not_share_chi_square).",
    ),
    row(
        "d1-2.6-mut-v4_m02",
        "2.6 mutation: v4_m02 matched factor skipped for small nu",
        "ledgers/M4/mutants/v4_m02_*.py; project.html Grading mode and #contract-notes; test_project.py",
        "PASS",
        "Killed on seed 0 by test_student_t_mean_absolute_loss_matches_the_matched_scale (final gate output). Grading mode "
        "(project.html:206) lists 'the mean absolute Student-t loss at nu of 3 to 8'; contract-notes (project.html:228) says the "
        "matched factor is checked through the mean absolute loss at nu = 3 and 4.",
    ),
    row(
        "d1-2.6-mut-m17",
        "2.6 mutation: m17 Student-t family drawn from seed + 1 survives; ruled equivalent",
        "ledgers/M4/equivalent/m17_student_t_second_seed.py and README.md; project.html:215 (Conventions item 5)",
        "FAIL",
        "m17 passes all 138 checks on seeds 0-49 (signt_m17_collect_seeds.out, from verifyD2_signt_and_m17.sh: 0 seeds with a failure), so it is a surviving "
        "mutant. It was moved to ledgers/M4/equivalent/ on the README's proof that Conventions item 5 leaves 'the order and the "
        "source' of the Student-t draws open. That reading is wrong: item 5 (project.html:215) says the Student-t family "
        "'takes Z for each draw in the same way' as the Gaussian family, which takes its normals from "
        "random.Random(seed).gauss(0.0, 1.0); only the order of the Student-t draws is left open. m17 takes the Student-t "
        "normals from random.Random(seed + 1), so it violates a behaviour the page states. README point 4 ('the only page "
        "sentence that ties the two families to one seed is the Lab 1 docstring') is also wrong: item 5 is such a sentence.",
        "Ruling 9 applies: either kill m17 with a new grader test that the page's Student-t stream source makes observable, "
        "or change Conventions item 5 so that the Student-t normal source is explicitly open (then the README is correct and "
        "m17 stays in equivalent/ with its proof corrected). The design choice is the owner's; the README must cite the "
        "sentence it relies on.",
    ),
    row(
        "d1-2.6-alternatives",
        "2.6 alternatives: five correct alternative implementations pass seeds 0-49",
        "ledgers/M4/scripts/alt_1.py .. alt_5.py; ledgers/M4/scripts/run_alternatives.py",
        "FAIL",
        "run_alternatives.py --seeds 0-49: reference, alt_1..alt_5 all PASS 50/50 (run_alternatives_0-49.out), so the "
        "criterion 'pass' holds. But alt_1 and alt_2 are not alternative algorithms: alt_1 differs from the reference only by "
        "summing over range(n) instead of range(i + 1), where the extra factor entries are exactly 0.0; alt_2 differs only by "
        "math.fsum in the loss sum. Over 300 seeds x 2 families (3 positions) both return the same losses as the reference "
        "in 600 of 600 cases each (cell comparison in this round). Ruling 10 requires alternatives of different styles or "
        "algorithms, so only alt_3 (column-oriented Cholesky), alt_4 (chi-square as a sum of squared normals) and alt_5 "
        "(heapq.nsmallest for the order statistic) count.",
        "Replace alt_1 and alt_2 with two correct implementations that differ in algorithm (for example a Cholesky written "
        "as LDL^T with the pivots, or a 99% quantile by counting order statistics), keep alt_3..alt_5, and re-run "
        "run_alternatives.py --seeds 0-49. Alternatives must conform to the frozen Gaussian stream in item 5 (Box-Muller and "
        "polar normals do not, and are not alternatives).",
    ),
    row(
        "d1-2.6-starter",
        "2.6 starter: signatures complete and unchanged",
        "course/modules/M/M4/grader/starter.py",
        "PASS",
        CARRY.format(files="grader/starter.py") + "the file is the same bytes as at d0f39c09 (git diff --quiet).",
    ),
    row(
        "d1-2.6-messages",
        "2.6 messages: failure messages name the property and show no computed value",
        "course/modules/M/M4/grader/test_project.py (new tests after line 180)",
        "PASS",
        "Read every message in the new tests: test_student_t_mean_absolute_loss_matches_the_matched_scale, "
        "test_student_t_draws_do_not_share_chi_square, test_a_short_position_is_valid_and_reverses_its_loss, "
        "test_gaussian_stream_is_frozen_and_the_loss_is_minus_the_weighted_return. Each message names the property or the "
        "factor to check and contains no formatted value. No new print or warn call (test_no_function_prints unchanged).",
    ),
    row(
        "d1-2.6-count-and-pyodide",
        "2.6 count and browser run: page's check count equals the real collect-only count; the browser runs the same file",
        "course/modules/M/M4/grader/test_project.py; course/modules/M/M4/project.html#grading-mode",
        "PASS",
        "pytest --collect-only: 138 tests = project.html:206 '138 checks'. The in-browser grader in the headless page smoke "
        "reports 'All 138 tests pass on seed 402849537' (ledgers/M4/scripts/M4-d-r2/page_smoke_project.out, page_smoke M4 PASS).",
    ),
    row(
        "d1-2.6-grader-comment-numbers",
        "2.6 grader comments: numbers quoted in comments are right",
        "course/modules/M/M4/grader/test_project.py:31-48 and the new comments",
        "PASS",
        CARRY.format(files="grader/test_project.py lines 1-179 (the diff starts at line 180); the comment block at 31-48")
        + "the round-1 sweep (ledgers/M4/scripts/M4-d-r1/verifyD1_outputs/variance_sweep_summary.out) is not re-run. New "
        "comment numbers checked now: E|T_3| closed form 2 sqrt(3)/pi = 1.1027 (verifyD1 prose check: 1.102658); "
        "E[Y^2] for truncation toward zero of N(0, 4) = 2.7042 (the comment says about 2.7) and 4 + 1/12 = 4.0833 for rounding; "
        "the seed-1093 claim: nu = 3 and a Student-t variance relative error of 1.022 on the reference (above the 0.30 "
        "tolerance); sqrt(nu/(nu-2)) = 1.73 at nu = 3.",
    ),
    row(
        "d1-rubric-observable",
        "2.6 rubric: observable levels",
        "course/modules/M/M4/project.html#rubric (table, line 332 onward)",
        "PASS",
        CARRY.format(files="project.html lines 332 onward (the rubric table; the changed hunks are at lines 143-227 only, "
                     "confirmed by a line diff)")
        + "not re-read this round.",
    ),
    row(
        "d1-rubric-calibration",
        "2.6 rubric: two exemplars calibrated to the rubric",
        "course/modules/M/M4/project.html#exemplar-a, #exemplar-b",
        "PASS",
        CARRY.format(files="project.html#exemplar-a and #exemplar-b (lines 345 onward)")
        + "carried without re-reading the exemplar text this round.",
    ),
    row(
        "d1-rubric-question-bank",
        "2.6 rubric: question bank (if any) matches the rubric",
        "course/modules/M/M4/project.html",
        "PASS",
        "grep -i question on project.html returns 0 lines: the page has no question bank. check_projects.py M4 PASS "
        "(check_projects_M4.out).",
    ),
    row(
        "d1-atlas",
        "2.6 atlas: project entry in the atlas matches the page",
        "curriculum/meta.yaml:194-276; course/modules/M/M4/project.html",
        "PASS",
        "Re-run: check_projects.py --unit M4 'check_projects M4: PASS' (check_projects_M4.out) and check_pages.py --unit M4 "
        "'check_pages M4: PASS' (check_pages_M4.out). curriculum/meta.yaml is byte-identical to d0f39c09.",
    ),
    row(
        "d1-studio",
        "2.6 studio: project studio entry",
        "curriculum/01-foundations.yaml:73-76",
        "PASS",
        CARRY.format(files="curriculum/01-foundations.yaml")
        + "the studio entry (lines 73-76) is unchanged.",
    ),
    row(
        "d1-lab-project-1",
        "Project lab 1 (rung 1 worked example): twin, page code, expected block, prose numbers",
        "course/modules/M/M4/project.html#lab-M4-project-1; tests/labs/M4/lab-M4-project-1.py",
        "PASS",
        "run_labs --unit M4 --page project: PASS (3/3) (run_labs_M4_project.out). tests/labs/M4 is byte-identical. The new "
        "interpretation text (project.html:144: the 1.6667 line 'is a formula, not a sample') matches lab line 75.",
    ),
    row(
        "d1-lab-project-2",
        "Project lab 2 (rung 2 completion): blanks, twin, expected block",
        "course/modules/M/M4/project.html#lab-M4-project-2; tests/labs/M4/lab-M4-project-2.py",
        "PASS",
        "run_labs --unit M4 --page project: PASS (3/3) (run_labs_M4_project.out). The lab section is byte-identical (2680 "
        "characters) and the twin is unchanged.",
    ),
    row(
        "d1-lab-project-3",
        "Project lab 3 (rung 3 closed forms): twin, expected block, numbers",
        "course/modules/M/M4/project.html#lab-M4-project-3; tests/labs/M4/lab-M4-project-3.py",
        "PASS",
        "run_labs --unit M4 --page project: PASS (3/3) (run_labs_M4_project.out). The lab section is unchanged.",
    ),
    row(
        "d1-prose-numbers",
        "Prose numbers: every displayed number re-derived from unrounded values",
        "course/modules/M/M4/project.html (Labs, Report, Exemplars A and B)",
        "PASS",
        "Re-run of verifyD1_prose_numbers.py (ledgers/M4/scripts/M4-d-r2/prose_numbers_r2.out): 'rows 19 all agree: True'. "
        "The new 138 count matches collect-only, and the 1.152 ratio, 1.6667 and 243004/210946 cents are unchanged.",
    ),
    row(
        "d1-prose-scope",
        "Prose scope words: every, only, all, always, exactly, same, drives",
        "course/modules/M/M4/project.html (exemplar A 'always'; new sentences at lines 200, 206, 215, 227)",
        "PASS",
        "New words checked: 'every position is long in every instance' (line 200) holds for seeds 0-1999 "
        "(verifyD2_check_instances.py: all positions positive); 'negating every position negates every loss' (line 222) is "
        "test_a_short_position...; 'every' in the Stream order item is the Gaussian definition. The only unbacked scope word, "
        "'always' in exemplar A, is unchanged and annotated as unbacked by the page itself.",
    ),
    row(
        "d1-prose-process-words",
        "Learner text carries no process words",
        "course/modules/M/M4/project.html",
        "PASS",
        "Regex over the page text with tags stripped: no hits for verifier, builder, fixer, reviewer, audit, ledger, fragment, "
        "mutant, agent, draft, TODO, FIXME, session, pending, task; 'round' appears only as the round() function.",
    ),
    row(
        "d1-prose-banned-phrases",
        "Banned phrases list",
        "course/modules/M/M4/project.html",
        "PASS",
        "check_pages.py --unit M4: 'check_pages M4: PASS' (check_pages_M4.out).",
    ),
    row(
        "d1-dag",
        "DAG: concepts used outside the unit's prerequisite closure",
        "course/modules/M/M4/project.html",
        "PASS",
        "check_dag.py --unit M4: 'check_dag M4: PASS' (check_dag_M4.out). The new text refers to Lesson 6 (Definition 2.1, "
        "Definition 2.5) and Assumption 1, all inside M4.",
    ),
    row(
        "d1-notation",
        "Notation: symbols match notation/notation.json and are not reused",
        "notation/notation.json; course/modules/M/M4/project.html",
        "PASS",
        "notation.json (byte-identical) registers the macros \\R, \\E, \\Var and the symbols T and gamma_4. The page uses \\E "
        "(registered) and no \\mathbb (grep count 0), no \\R, and no T symbol; gamma appears only in the Gamma function and "
        "in code. No symbol is reused with another meaning.",
    ),
    row(
        "d1-cites",
        "Cites: every citation is a registry key and the reading section matches",
        "course/modules/M/M4/project.html#reading; references/references.json",
        "PASS",
        CARRY.format(files="project.html#reading (section byte-identical, 476 characters) and references/references.json")
        + "verify_refs.py --offline: '560 entries, 0 problems' (verify_refs_offline.out); live re-verification of M4: "
        "'1 of 560 entries, 0 problems' (verify_refs_M4_live.out).",
    ),
    row(
        "d1-structure",
        "Structure: sections, headings, lab markup, and the page smoke",
        "course/modules/M/M4/project.html",
        "PASS",
        "check_pages.py --unit M4 PASS (check_pages_M4.out); page_smoke.py --unit M4 --pages project PASS with the in-browser "
        "grader (page_smoke_project.out).",
    ),
    row(
        "d1-cards-schema",
        "Cards schema: fields, ids, lesson coverage, grades, basis on C cards",
        "course/modules/M/M4/cards.json",
        "PASS",
        "ledgers/M4/scripts/M4-d-r2/cards_check_r2.out: 212 cards, 212 unique ids; lessons L01..L10 with 15 to 31 cards; "
        "grades 192 T and 20 C; every C card has a basis. Id gaps c123, c184, c196, c202, c203, c206, c211, c213 are allowed "
        "by architect ruling 2 (FINAL-ARCHITECT-RULINGS.md item 2). Round-1 C card c191 is now T (d1-cards-c191-grade).",
    ),
    row(
        "d1-cards-numbers-in-lesson",
        "Cards: every number and every theorem-style reference occurs in the card's own lesson",
        "course/modules/M/M4/cards.json vs course/modules/M/M4/L01.html..L10.html",
        "PASS",
        "verifyD1_cards_check.py re-run over the current pin (cards_check_r2.out): 'number tokens not found in own lesson: []' "
        "and 'theorem-style references not found in own lesson: []' over all 212 cards.",
    ),
    row(
        "d1-cards-labs",
        "Cards: C-card numbers match their lab output",
        "course/modules/M/M4/cards.json (the 20 C cards); tests/labs/M4/lab-M4-L02..L10-1.py",
        "PASS",
        CARRY.format(files="the 20 remaining C cards (entries unchanged) and tests/labs/M4 (byte-identical)")
        + "the round-1 check of each number against its lab output (labout/*.txt, ledgers/M4/scripts/M4-d-r1/verifyD1_outputs) "
        "stands. I re-read these cards this round: c112 and c113 quote the L07 Part A and C numbers exactly "
        "(L07 output: max absolute difference 7.11e-13 at t = 2; sample mean -0.062124 against -0.062110). Card c191 left the C set.",
    ),
    row(
        "d1-cards-math",
        "Cards: the mathematics on every card is correct",
        "course/modules/M/M4/cards.json (all 212 entries read)",
        "PASS",
        "All 212 entries read this round. Recomputed: c011 (198), c015 (149), c031 (sqrt(2968750000) = 54486.24), c040, c041, "
        "c042 (7/4, 163/16), c043 (5/3), c044 (gamma_3 = 0), c045 (73/9, 7/3), c048 (64/9), c058, c062 and c065 (E[X|Y] = 1, "
        "2/3, E[X] = 4/5), c074 (2/9), c094 and c096, c102, c107 (|phi|^2), c142 (40.4006 -> 40), c141 (7/60), c147 and c149 "
        "(t(3) cdf matches the standard formula; the tail in c149 follows from that cdf by algebra, checked), c157 (0.063451, about 1 in 16; normal 1.524e-23), "
        "c160, c161 (0.63451 vs 2/pi), c168 (0.002128), c172 and c187 (4 sqrt(3)/pi = 2.2053), c181, c185 (gaps of Phi(1)), "
        "c200 (m3 = 2157/32, m4 = 149461/256 exactly), c208 (BB^T = Sigma), c209 (density constant 2/(pi sqrt 3)), c216, "
        "c219 and c220 (moment integrals). No error found.",
    ),
    row(
        "d1-cards-lesson-statements",
        "Cards: each card agrees with the current lesson statement and its hypotheses",
        "course/modules/M/M4/cards.json vs L01..L10 propositions and examples",
        "PASS",
        "Changed cards checked against the current lesson text: c029 vs L02 Proposition 2.2 and the die example (agree); c191 vs "
        "L05 Example 2.5 (line 160: 'Assuming Assumption 1 ... Var(X1) = S1^2'); c219 and c220 vs L03 Definition 2.7, "
        "Assumption 2.6 and Proposition 2.8 (lines 46-53); c195 vs L01 Proposition 2.2(b)-(c). Reworded cards c005, c008, c010, "
        "c017, c075, c089, c114, c132 keep the lesson's statements.",
    ),
    row(
        "d1-cards-duplicates",
        "Cards: no duplicate cards",
        "course/modules/M/M4/cards.json: M4-c066/c213, M4-c070/c211 (round-1 duplicates)",
        "PASS",
        "M4-c211 and M4-c213 are deleted (cards.json diff); M4-c066 and M4-c070 remain. Exact duplicate fronts: none. "
        "Near-duplicate pairs (cards_check_r2.out) are different facts (kurtosis vs skewness under affine maps, mean vs variance "
        "of the sample mean, E[Z] vs E[Z^2], Lab parts with different seeds or laws).",
    ),
    row(
        "d1-cards-c191-grade",
        "Cards: grade of M4-c191 matches the rule for derivations under a stated assumption",
        "course/modules/M/M4/cards.json M4-c191",
        "PASS",
        "M4-c191 is now grade T and its back states the hypotheses of Example 2.5 (S1, S2 > 0; |rho| < 1; Z1, Z2 independent with "
        "mean 0 and variance 1) and 'assuming its Assumption 1' (not proved here), which is what the round-1 fix asked for. The "
        "lesson text (L05, Example 2.5, line 160) treats the same derivation as conditional on Assumption 1.",
    ),
    row(
        "d1-cards-hypotheses",
        "Cards: a card that cites a proposition carries that proposition's hypotheses",
        "course/modules/M/M4/cards.json M4-c028, M4-c029, M4-c070",
        "FAIL",
        "Three cards cite a proposition without its hypothesis, while their sibling cards for the same proposition state it: "
        "M4-c028 and M4-c029 cite Proposition 2.3 and 2.2 with no hypothesis, but M4-c023 and M4-c022 state 'Hypothesis: finite "
        "probability space with positive weights' for the same propositions; M4-c070 cites Proposition 1.2 with no "
        "hypothesis, while M4-c069 and M4-c210 state 'Hypothesis: finitely many values' for Proposition 1.1. "
        "Other cards that cite a proposition without restating the hypothesis rely on the page-wide finite-space setting "
        "(lesson text) or state it in the front; they are not listed.",
        "Prefix 'Hypothesis: finite probability space with positive weights.' to M4-c028 and M4-c029 and 'Hypothesis: finitely "
        "many values.' to M4-c070 (cards.json), then re-run verifyD1_cards_check.py.",
    ),
    row(
        "d1-data",
        "Data: no real data; every value SIMULATED",
        "course/modules/M/M4/project.html (Inputs); grader/instance.py",
        "PASS",
        "The Inputs text (project.html:200) says 'No data file' and 'Every value is SIMULATED'; instance.py label is SIMULATED "
        "for seeds 0-1999 (verifyD2_check_instances.py).",
    ),
    row(
        "d1-freshness-registry",
        "Registry freshness: references.json entries used by the slice verify",
        "references/references.json (blitzstein2019introduction)",
        "PASS",
        CARRY.format(files="references/references.json") + "verify_refs.py --offline: 560 entries, 0 problems.",
    ),
    row(
        "d1-gates-repo",
        "Repository gates relevant to the slice",
        "pyproject.toml; tests/labs/M4; tests/test_labs.py, test_run_labs.py, test_page_smoke.py, test_page_checks.py",
        "PASS",
        "ruff check . -> 'All checks passed!' (ruff_check.out); ruff format --check tests/labs/M4 -> 13 files already formatted "
        "(ruff_format_M4.out); mypy --no-incremental -> 'Success: no issues found in 331 source files' (mypy.out); pytest "
        "tests/test_labs.py tests/test_run_labs.py tests/test_page_smoke.py tests/test_page_checks.py -k 'M4 or project' -> "
        "EXIT=0 (pytest_M4_subset.out). Not run: the full pytest suite (targeted by the workflow rule).",
    ),
    row(
        "d1-tools-structure",
        "Tools: the tools used by the slice are unchanged and pass",
        "tools/*.py",
        "PASS",
        "git diff d0f39c09 c737272 -- tools has 0 lines, so the tools are byte-identical; their M4 outputs were re-run above "
        "(check_pages, check_dag, check_projects, page_smoke, run_labs, run_graders, mutate_graders, run_alternatives, verify_refs).",
    ),
    row(
        "d2-2.6-constraints-exceptions",
        "2.6 constraints: the list of conventions the suite does not grade is complete",
        "course/modules/M/M4/project.html:204 (Constraints) and :228 (What the suite does not test)",
        "FAIL",
        "The Constraints sentence says the conventions are binding 'except the items the suite does not grade' and lists item 1 "
        "(Student-t variance at nu 3 and 4), item 2 (the round() call), item 4 (the integer formula) and item 5 (Student-t draw "
        "order). It omits the sign of the Student-t loss, which What the suite does not test (project.html:228) says the suite "
        "does not test. Confirmed: a Student-t-only sign-flip mutant (the reference with round(total) for student_t; not added to "
        "mutants/) passes all of seeds 0-9 (signt_m17_collect_seeds.out). The page's contract-notes is correct; the Constraints "
        "list is incomplete. No test can detect this sign without a frozen Student-t draw order, which the page leaves open.",
        "Add 'the sign of the Student-t loss (item 2)' to the exception list in the Constraints sentence (project.html:204), so the "
        "list matches the contract-notes section.",
    ),
]


def mutants_from_gate() -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    pattern = re.compile(r"^KILLED (\S+)\.py: (.*) -> (\S+) \(seed (\d+)\)$")
    for line in GATE.read_text(encoding="utf-8").splitlines():
        m = pattern.match(line)
        if not m:
            continue
        stem, description, killer, seed = m.group(1), m.group(2), m.group(3), m.group(4)
        found.append(
            {
                "id": stem,
                "description": description,
                "killed_by": f"{killer} (seed {seed})",
                "path": f"ledgers/M4/mutants/{stem}.py",
            }
        )
    return found


def main() -> None:
    mutants = mutants_from_gate()
    fails = [r for r in ROWS if r["status"] != "PASS"]
    passes = [r for r in ROWS if r["status"] == "PASS"]
    killed = sum(1 for m in mutants if m.get("killed_by"))
    verdict = "PASS" if not fails and killed == len(mutants) and mutants else "FAIL"
    notes = [
        "Scope: project.html (rubric and exemplars, the changed Lab 1, Constraints, Conventions, Conditions and contract-notes "
        "hunks), grader/ (reference.py, instance.py, starter.py, test_project.py), the three project labs, all 212 cards of "
        "cards.json, the mutants and the alternatives. Delta from d0f39c09 to c737272 read hunk by hunk for every file in the "
        "slice (project.html, test_project.py, cards.json, L01..L05 only as they bear on cards, FINAL-ARCHITECT-RULINGS.md, "
        "notation, references, tools, labs).",
        "Carried rows: byte-identical subjects only (instance.py, starter.py, reference.py, tests/labs/M4, the #budget, #rubric, "
        "#exemplar-a/b, #reading sections, test_project.py lines 1-179, references.json, curriculum/01-foundations.yaml, "
        "tools/). Every other row was re-run or re-derived this round.",
        "Round-1 FAIL rows now: d1-2.6-spec-questions fixed (PASS); d1-2.6-mut-m11, d1-2.6-mut-r9_03, d1-2.6-mut-v4_m02 killed "
        "(PASS); d1-cards-duplicates and d1-cards-c191-grade fixed (PASS); d1-2.6-mut-m17 and d1-2.6-alternatives still FAIL; "
        "d1-cards-hypotheses is FAIL now (round 1 passed it, which was lenient).",
        "Mutation gate: 'tools/mutate_graders.py --unit M4 --seeds 0-9' exits 0 with 118/118 killed (after adding v2_01..v2_04). "
        "The four round-2 mutants are student errors: short position read as long (v2_01), upper factor used as lower (v2_02), "
        "zero pivot accepted (v2_03), normals in reverse position order (v2_04). Each is killed. Generator: "
        "ledgers/M4/scripts/M4-d-r2/verifyD2_make_mutants.py.",
        "Non-blocking observations (not rows): M4-c033 front 'how many losses occur?' omits the threshold (the count is of "
        "draws at 250000 cents); M4-c112 does not state the Lab 1 Part A parameters mu = 0.5, sigma = 1.5; M4-c047 and "
        "M4-c183 say 'the skewed law' without defining it on the card. Of the fourteen proposition-citing cards that restate no hypothesis, "
        "eleven rely on the page-wide finite-space setting and are not failed; c028, c029 and c070 are the FAIL row.",
        "Could not check: (a) the browser grader interactively (the headless in-browser grader via page_smoke ran and passed "
        "138 tests); (b) the Appendix A proof text of project.html (lines 420-460) was not in the delta and was not re-proved "
        "this round; (c) the variance sweep over seeds 0-1999 for the tolerance comments was not re-run (carried from round 1); "
        "(d) the full verify_refs live check (only the tool's M4 sample of 1 of 560 entries ran); (e) the lesson pages L01..L10 "
        "were read only where the delta or a card cites them.",
        "Scratch copies used for the grader and mutant runs are under /tmp/M4-d-r2 (not in the checkout). The checkout's "
        "ledgers/M4/M4-d.json is this fragment; nothing outside ledgers/M4/ was edited, and no commit was made.",
    ]
    fragment = {
        "unit": "M4",
        "slice": "d",
        "round": 2,
        "verifier": "independent verifier (Haiku), not a builder of M4; round 2",
        "pin": "c737272f (checkout detached at the pin)",
        "base": "d0f39c09 (round-1 pin; delta computed with git diff d0f39c09 c737272)",
        "checkout": "/Users/billyribeiro/.fanout/wt/verifyD2-M4-d",
        "scratch": "/tmp/M4-d-r2",
        "verified_at": datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat(),
        "verdict": verdict,
        "rows": ROWS,
        "mutants": mutants,
        "registry_flags": [],
        "freshness_flags": [],
        "notes": notes,
        "summary": {
            "rows": len(ROWS),
            "pass": len(passes),
            "fail": len(fails),
            "unverifiable": 0,
            "mutants_killed": killed,
            "mutants": len(mutants),
        },
    }
    FRAGMENT.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {FRAGMENT.relative_to(ROOT)}: rows {len(ROWS)} pass {len(passes)} fail {len(fails)}; "
          f"mutants {len(mutants)} killed {killed}; verdict {verdict}")


if __name__ == "__main__":
    main()
