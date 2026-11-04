"""Writes ledgers/M4/M4-d.json (round 8, slice d) from the rows and mutant results of this round.

Mutant rows are read from mutate_M4_0-9.out, the output of tools/mutate_graders.py --unit M4 --seeds 0-9.
Usage: python -I ledgers/M4/scripts/M4-d-r8/build_fragment_r8.py
"""

import json
import pathlib
import re
from datetime import UTC, datetime

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-M4-d")
S = "ledgers/M4/scripts/M4-d-r8"
ROUND7_FRAG = pathlib.Path("/Users/billyribeiro/.fanout/frags/D-M4-d.round7.json")
OLD_ROWS = {r["id"]: r for r in json.loads(ROUND7_FRAG.read_text(encoding="utf-8"))["rows"]}

PIN = "2d755599d8d74df292e3e43025f0458c4053802e"
CARRY = "Carried from round 8 (subject byte-identical since the round-7 pin 9373ef39): "


def carried(rid, subject, note):
    return {"id": rid, "check": OLD_ROWS[rid]["check"], "location": OLD_ROWS[rid]["location"], "status": "PASS",
            "evidence": CARRY + subject + ". " + note}


def fresh(rid, check, location, status, evidence, fix=None):
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    return row


rows = [
    carried("d1-2.6-hours", "course/modules/M/M4/project.html lines 33 and 234-245 (not in any hunk of git diff -U0 9373ef39 HEAD)",
            "Hours 2+2+12+8+4+2 = 30, equal to data-hours-project=30."),
    fresh("d1-2.6-instances", "2.6 instances: valid, and answers change across seeds", "course/modules/M/M4/grader/instance.py",
          "PASS", f"{S}/checks/instances_sample_r8.py (20 seeds: 0-9, 50, 123, 400, 777, 1000, 1093, 1500, 1999, 2500, 4096): "
          f"all valid (assets 2 or 3, whole positive cents, nu in 3..8, draws not a multiple of 100 and <= 20000, symmetric cov); "
          f"20 distinct reference Student-t 99% losses; output {S}/checks/instances_sample_r8.out."),
    carried("d1-2.6-starter", "course/modules/M/M4/grader/starter.py (file byte-identical)",
            "Signatures in project.html line 202 match reference.py (matched_scale, simulate_losses, quantile_99)."),
    carried("d1-rubric-observable", "course/modules/M/M4/project.html lines 330-343 (rubric table)",
            "Every level descriptor is observable; C5 level 3 names the 300-700 word bar and the 80-word Summary."),
    fresh("d1-rubric-calibration", "2.6 rubric calibration: blind scores vs official, within one level",
          "course/modules/M/M4/project.html:348-462 (exemplars A and B)", "PASS",
          "Blind scoring from the rubric alone: Exemplar A C1 2, C2 2, C3 2, C4 2, C5 2 (official 2,2,2,2,2). Exemplar B C1 4, "
          "C2 4, C3 4, C4 4, C5 3 (official 4,4,4,4,3). Exemplar B body 682 words (699 with headings), Summary 70 words "
          f"({S}/checks/exemplar_wordcount_r8.out). The Exemplar A word count printed in its C5 annotation is a separate row "
          "(d6-prose-exemplar-words)."),
    carried("d1-rubric-question-bank", "plans/M4-build-plan.md section 5.7 and project.html (no adversarial project)",
            "Not applicable: the M4 project is not adversarial."),
    carried("d1-atlas", "curriculum/meta.yaml lines 194-276 (file byte-identical)", "No atlas change in round 8."),
    carried("d1-studio", "curriculum/01-foundations.yaml lines 73-76 (file byte-identical)", "No studio change in round 8."),
    carried("d1-cites", "course/modules/M/M4/project.html lines 482-486; references/references.json (byte-identical)",
            f"verify_refs offline: {S}/gates/verify_refs_offline.out."),
    carried("d1-cards-c191-grade", "course/modules/M/M4/cards.json entry M4-c191 (object identical to round 7)",
            "grade T unchanged."),
    carried("d1-data", "project.html lines 37, 200, 271-275 and grader/instance.py (byte-identical)",
            "No file is read; every input is SIMULATED."),
    carried("d1-tools-structure", "tools/*.py (no change since round 7)", "check_pages, check_dag, check_projects PASS in this round."),
    carried("d6-2.6-equivalence-float-ceil", "grader/reference.py lines 95-100 and project.html line 214 (byte-identical)",
            "(99n+99)//100 equals ceil(0.99 n) for every n in 1..20000 (checked by a float/integer comparison)."),
    fresh("d6-prose-exemplar-words", "2.9/2.6 prose: exemplar annotation word counts",
          "course/modules/M/M4/project.html:359 (Exemplar A, C5 annotation)", "FAIL",
          f"{S}/checks/exemplar_wordcount_r8.py prints Exemplar A body 90 words, 100 with its four headings "
          f"({S}/checks/exemplar_wordcount_r8.out); the annotation at line 359 says 97 words and 107 with headings. The "
          "round-7 text said 90 and 100, so round 8 changed a correct number to a wrong one.",
          fix="project.html line 359: replace 'the body is 97 words of text (107 with its four headings)' with "
              "'the body is 90 words of text (100 with its four headings)'."),
    carried("d6-cards-sample", "cards.json objects M4-c001, c011, c030, c040, c063, c074, c098, c105, c120, c133, c141, c149, c157, c162 (identical)",
            "Re-checked against the lessons in round 6; none of these objects changed in round 8."),
    carried("d1-2.6-ladder", "course/modules/M/M4/project.html lines 40-49 and 51-192 (byte-identical)",
            "Rung 1 solved (lab 1), rung 2 graded instantly (lab 2), rung 3 spec, rung 4 open."),
    fresh("d1-2.6-spec-questions", "2.6 spec: a competent student asks no clarifying question",
          "course/modules/M/M4/project.html:194-229", "PASS",
          "Read project.html 194-229. The only open items are the ones the page states as open (the Student-t source and draw order, "
          "item 5), and the grader covers the Gaussian order. No further question arises."),
    fresh("d1-2.6-autograder-reference", "2.6 autograder: run_graders seeds 0-49 on reference.py",
          "course/modules/M/M4/grader/reference.py", "PASS",
          f"tools/run_graders.py --unit M4 --seeds 0-49: 'run_graders M4: PASS (reference 50/50 seeds, slowest 0.9 s)' "
          f"({S}/gates/run_graders_M4_0-49.out)."),
    fresh("d1-2.6-mut-own", "2.6 mutation: verifier-written student-error mutants, all killed",
          "ledgers/M4/mutants/ (v1_* through r8d_04)", "FAIL",
          f"Mutant gate ({S}/mutate_M4_0-9.out): 145 of 146 killed; the one survivor is r8d_01 (row d8-2.6-symmetry-tiny-scale). "
          "All earlier verifier mutants are killed.",
          fix="Add a grader test for symmetry at tiny scale (see d8-2.6-symmetry-tiny-scale); then r8d_01 is killed."),
    fresh("d1-2.6-mut-existing", "2.6 mutation: existing mutants on seeds 0-9", "ledgers/M4/mutants/*.py (142 files from earlier rounds)",
          "PASS", f"{S}/mutate_M4_0-9.out: every mutant from earlier rounds prints KILLED (count 145 KILLED, the new r8d_01 SURVIVED)."),
    fresh("d1-2.6-mut-m11", "2.6 mutation: m11 loss sign flipped", "ledgers/M4/mutants/m11_loss_sign_flipped.py", "PASS",
          f"KILLED in {S}/mutate_M4_0-9.out."),
    fresh("d1-2.6-mut-r9_03", "2.6 mutation: r9_03 chi-square reused on alternate draws",
          "ledgers/M4/mutants/r9_03_student_t_chi_square_reused_every_second_draw.py", "PASS", f"KILLED in {S}/mutate_M4_0-9.out."),
    fresh("d1-2.6-mut-v4_m02", "2.6 mutation: v4_m02 matched factor skipped for small nu",
          "ledgers/M4/mutants/v4_m02_matched_factor_skipped_for_small_nu.py", "PASS", f"KILLED in {S}/mutate_M4_0-9.out."),
    fresh("d1-2.6-mut-m17", "2.6 mutation: m17 is an equivalent (conforming) mutant",
          "ledgers/M4/equivalent/m17_student_t_second_seed.py", "PASS",
          "Passes all 146 tests on seeds 0-9 (grade_one.py: 145 passed, 1 skipped or 146 passed). Conventions item 5 leaves the "
          "Student-t source open, so seed+1 for the Student-t family is a conforming choice."),
    fresh("d1-2.6-alternatives", "2.6 alternatives: five (now six) alternative correct implementations pass",
          f"{S}/alts/alt1..alt5 (carried from round 7), {S}/alts/alt6_chi_before_normals.py", "PASS",
          f"{S}/checks/grade_one.py on seeds 0-9: every alternative prints rc 0 on all ten seeds (alt1 box-muller student, alt2 polar, "
          "alt3 column cholesky, alt4 chi-square as sum of normals, alt5 heapq quantile, alt6 chi-square drawn before the normals)."),
    fresh("d1-2.6-messages", "2.6 messages: check() and expect_value_error() wording",
          "course/modules/M/M4/grader/test_project.py (all assertion messages, read in full)", "PASS",
          "Every message is a static string that names the violated property and shows no computed value (read all lines 1-647)."),
    fresh("d1-2.6-count-and-pyodide", "2.6 test count and Pyodide statement",
          "course/modules/M/M4/grader/test_project.py; project.html:203-206", "PASS",
          f"pytest --collect-only: 146 tests (grade_one.py --count). Seed 0 gives 145 passed, 1 skipped. page_smoke "
          f"project: 'All 146 tests pass' in the browser ({S}/gates/page_smoke_project.out)."),
    fresh("d1-2.6-grader-comment-numbers", "2.6 grader comment numbers (test_project.py comments at lines 31-47)",
          "course/modules/M/M4/grader/test_project.py:31-47", "PASS",
          f"{S}/checks/cross_r8.out: reference max cross-term rel. error 0.0239 (seeds 0-49); r8_03 0.0677-0.0860 and r9_02 "
          f"0.1406-0.1605 (seeds 0-9). {S}/checks/variance_sweep_r8.out (seeds 0-1999): ref max rel. err 0.1259 (nu 5), 0.0967 (6), "
          "0.0728 (7), 0.0624 (8); no-matched-factor fails 347/347, 317/317, 342/343, 288/317; seed 1093 nu 3 ref error 1.022."),
    fresh("d1-prose-numbers", "2.2 prose numbers vs measured values", "course/modules/M/M4/project.html:203-206, 212, 215, 220, 228",
          "PASS", f"Recomputed: 146 checks, 145+1 skip, 1/4 share, 3 % (0 of 50), 5 % (19 of 50 and 31 of 50), 4 to 20 counts "
          f"(19 of 50 and 31 of 50 from {S}/checks/cross_r8.out); chi-square fail counts from {S}/checks/chi_lag_r8.out."),
    fresh("d1-prose-scope", "scope words backed by a computation", "course/modules/M/M4/project.html:215, 228; grader/test_project.py:214",
          "FAIL",
          "The sentence 'a sharing at a lag of four or more draws is not graded' (project.html:215) and 'is not read by this check' "
          "(project.html:228, and test_project.py:214 'A sharing at a lag of four or more is not read here') are universal "
          "claims with a counterexample. The chain in which draws 4j and 4j+4 share one variable, so all draws divisible by four "
          f"share one chi-square variable (mutant r7d_02), fails test_student_t_draws_do_not_share_chi_square on 38 of 50 seeds and the "
          f"full suite on 47 of 50 seeds ({S}/checks/chi_lag_r8.out). A disjoint lag-four pair sharing (draws 8m+4 reuse 8m) passes "
          f"50 of 50 and the full suite ({S}/checks/chi_lag4_disjoint_r8.out).",
          fix="Narrow both sentences: a sharing of one pair of draws at lag four or more is not read by the lag-one-to-three check "
              "(disjoint pairs pass 50 of 50), but a sharing that links many draws at lag four is caught on 38 of 50 seeds. Same edit "
              "in test_project.py:214."),
    carried("d1-prose-process-words", "project.html, L01-L04, cards.json, grader/test_project.py", "fresh grep: no 'verifier', 'builder', 'round 8'."),
    fresh("d1-prose-banned-phrases", "banned strings (BUILDER_RULES 1.3-1.4)", "course/modules/M/M4/project.html; cards.json; grader/*.py",
          "PASS", "grep -F -i over TODO, TBD, lorem, '...', 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', "
          "'you can add more', 'important to note', 'studies show', 'experts agree', 'well known', obviously, clearly, widely, roughly, "
          "historically, 'about 6': 0 hits. 'this round' matches only 'this rounding' (project.html:212)."),
    fresh("d1-dag", "DAG: prerequisite closure and dfn assignment", "course/modules/M/M4/*.html", "PASS",
          f"tools/check_dag.py --unit M4: PASS ({S}/gates/check_dag_M4.out)."),
    fresh("d1-notation", "notation registry symbols", "notation/notation.json; project.html", "PASS",
          "Registered macros used on the page: \\E only (expectation). Symbols used (nu, n, W, Z, R, L, Sigma, w, u, x, z, m, Q, Gamma, "
          "s, ell) are not registered with another meaning; \\mathbb{Q} (the registered measure) is not used on the page."),
    fresh("d1-structure", "project structure and rungs", "course/modules/M/M4/project.html", "PASS",
          f"tools/check_pages.py --unit M4: PASS ({S}/gates/check_pages_M4.out); sections in order ladder, rungs, spec, conventions, "
          "conditions, notes, budget, autograder, local, report, stretch, reading, references."),
    fresh("d1-cards-schema", "card schema", "course/modules/M/M4/cards.json", "PASS",
          f"231 cards, unique ids, keys {{id, lesson, front, back, grade}} (+ basis on 35 cards), grades T 201 and C 30 "
          f"({S}/checks/card_dupscan_r8.out)."),
    fresh("d1-cards-numbers-in-lesson", "card numbers appear in the card's lesson", "course/modules/M/M4/cards.json vs L01-L10.html",
          "PASS", f"{S}/checks/numcheck_r8.py: every number of 4 or more in every card front and back occurs in that card's lesson text: "
          "0 unmatched cards."),
    fresh("d1-cards-labs", "card lab results match the lab output and grades match their basis",
          "course/modules/M/M4/cards.json: M4-c165, M4-c233 to M4-c236 (and C cards)", "FAIL",
          "The values match Lab 1 Part A (L09 lines 308-312 print 0.833333, 0.847994, 0.843496, 0.835793, 0.833926). But card M4-c165 "
          "(n = 1, basis 'exact Fraction arithmetic on the die; no simulation') is graded T, while M4-c233 to M4-c236 with the same basis "
          "are graded C. The page does not prove any of these values (L09 line 321 says the probabilities are computed from the exact "
          "mass function). The same grade is required for all five (round-7 ruling: T only for values the page proves).",
          fix="Grade M4-c165 C, as M4-c233 to M4-c236 are, or add the n = 1 derivation (P(X <= 5) = 5/6 with threshold 5.207) to L09 "
              "and keep T with that basis, and then grade c233-c236 C with the same basis statement."),
    fresh("d1-cards-math", "card mathematics re-derived",
          "cards.json: M4-c040, c041, c043, c045, c048, c137, c160, c161, c168, c172, c226; c185, c233-c236 (now C); c220 removed", "PASS",
          "Re-derived by hand or in python (high-precision t(3) tail: x^3 P(|V|>1000) = 2.2053076 -> 2.205308, P(|V|>10) = 0.00212840 "
          "-> 0.002128; Cauchy x P(|C|>10) = 0.634510; kurtosis 5/3, 73/9, 7/3; gamma3^2 = 64/9; m3 = 2157/32 and m4 = 149461/256 "
          "computed from the moments; mean 7/4 and variance 163/16; Chebyshev bound 2 for n = 2, eps = 1/2, sigma^2 = 1)."),
    fresh("d1-cards-lesson-statements", "cards agree with the current lesson text",
          "cards.json: M4-c023, c038, c039, c040, c046, c081, c140, c195, c198, c214, c215, c218, c229; L02, L03, L05, L09 text", "PASS",
          "Each changed or sampled card agrees with its lesson text (L02 Proposition 2.3 and Definition 2.1; L03 Proposition 2.3-2.5 and "
          "Example 2.6; L05 Proposition 2.4 with the 4 <= 1 instance at L05 line 370; L09 section 4 misconception on normality; L09 "
          "Proposition 2.3(b); L01 Remark 3.3 and Proposition 2.2)."),
    fresh("d1-cards-hypotheses", "card hypotheses carry the proposition's hypotheses",
          "cards.json: M4-c038, c225, c039, c215, c242, c244", "PASS",
          "Each card names its hypotheses where the proposition has them (finite space with positive weights; at least two values; "
          "a not 0). M4-c244 and M4-c242 carry them. The T cards without an explicit hypothesis phrase (M4-c015, c016, c019, c053, c054, "
          "c057, c060, c061, c072, c080, c081, c100, c106, c107, c111, c120, c121, c131, c138, c152, c158, c159, c175, c192) state the "
          "hypothesis in the front or need none (checked by a scan of the cards that cite a Proposition)."),
    fresh("d1-cards-duplicates", "no duplicate cards", "course/modules/M/M4/cards.json", "FAIL",
          f"{S}/checks/card_dupscan_r8.out: 'What is the standard deviation of X?' is the front of both M4-c067 (L05, Definition 1.3) and "
          "M4-c243 (L02, Definition 2.1, added in round 8). Both fronts are identical, and the backs state the same definition. "
          "No other identical front exists; near-identical fronts differ in n, the lab part or the object.",
          fix="Delete M4-c243 (M4-c067 covers the question), or change M4-c243's front to a question the card set lacks, e.g. "
              "'In which units is the standard deviation of X expressed?'."),
    fresh("d1-cards-forward-reference", "no use before definition inside the lesson", "course/modules/M/M4/L03.html; cards.json", "PASS",
          "Round-7 references (L03 lines 118, 122-123, 262, 276, 401, and card M4-c220) are gone: grep -n 'Assumption 2.7|Proposition 2.8|"
          "Gaussian integral' in L03.html and cards.json finds none. M4-c220 is removed."),
    carried("d1-freshness-registry", "references/references.json (byte-identical)", "verify_refs --offline: 560 entries, 0 problems."),
    fresh("d1-gates-repo", "gates: ruff, mypy, pytest, configuration", "pyproject.toml; tests/test_run_labs.py, test_labs.py, "
          "test_memo_exemplars.py, test_curriculum.py", "PASS",
          f"ruff check: All checks passed; ruff format --check: 553 files formatted; mypy --no-incremental: no issues in 385 files; "
          f"pytest on the four files: all pass ({S}/gates/*.out)."),
    fresh("d2-2.6-constraints-exceptions", "2.6 constraints and exceptions match the code", "course/modules/M/M4/project.html:203-206, 212-220",
          "PASS", "Each listed condition (matched_scale, simulate_losses, quantile_99) is in reference.py and is tested by "
          "test_project.py, except the symmetry condition at tiny scale (see d8-2.6-symmetry-tiny-scale)."),
    fresh("d1-2.6-constraints-exceptions", "2.6 constraints and exceptions match the code",
          "course/modules/M/M4/project.html:203-206 (Constraints, Grading mode), :212-220", "PASS",
          "Re-read the Grading mode (146 checks, 145 with one skip at nu of 3 or 4, the 1/4 share and the rounding rule) against the test "
          "file: each item has a test (see d1-2.6-messages). The symmetry condition is stated and under-tested (d8-2.6-symmetry-tiny-scale)."),
    fresh("d3-2.6-mut-new-student-error", "round-5/7 student-error mutants are killed",
          "ledgers/M4/mutants/v9_01..v9_04, d5_01, r7d_01..r7d_04", "PASS",
          f"KILLED in {S}/mutate_M4_0-9.out (v9_01..v9_04, d5_01, r7d_01..r7d_04)."),
    fresh("d1-2.6-contract-notes-chi-claim", "contract notes: chi-square sharing counts",
          "course/modules/M/M4/project.html:228; grader/test_project.py:205-226", "FAIL",
          f"The counts in the paragraph reproduce: lag-1 sharing 50 of 50 seeds, lag-2 50 of 50, lag-3 39 of 50, even-indexed 44 of 50 "
          f"({S}/checks/chi_lag_r8.out). The sentence 'A sharing at a lag of four or more draws is not read by this check' is false for "
          "the chain of r7d_02 (38 of 50 seeds fail the lag test). See d1-prose-scope.",
          fix="As for d1-prose-scope: narrow the sentence to a single pair of draws at lag four or more."),
    carried("d1-2.6-mut-pairwise-survivor", "ledgers/M4/mutants/d5_01_chi_square_shared_by_draws_two_apart.py (byte-identical)",
            "KILLED by test_student_t_draws_do_not_share_chi_square (seed 0)."),
    carried("d6-2.6-mut-integer-division-chi", "ledgers/M4/mutants/r6d_02_integer_division_chi_shape.py (byte-identical)",
            "KILLED by test_student_t_cross_term_matches_matched_covariance (seed 0)."),
    carried("d6-2.6-mut-pivot-tolerance", "ledgers/M4/mutants/r6d_01 and grader/test_project.py:541-590 (byte-identical)",
            "KILLED by test_one_position_with_a_variance_of_1e16_or_1e30_is_accepted (seed 0)."),
    carried("d6-2.6-mut-lag3-sharing", "ledgers/M4/mutants/r6d_03_chi_square_shared_by_draws_six_apart_lag_three.py (byte-identical)",
            "KILLED by test_student_t_draws_do_not_share_chi_square (seed 0)."),
    fresh("d1-lab-project-1", "project lab 1 (rung 1 worked example)", "course/modules/M/M4/project.html:55-145; tests/labs/M4/lab-M4-project-1.py",
          "PASS", f"{S}/checks/lab_twin_r8.out: page code equals twin; twin runs under python -I -W error (exit 0); output equals the "
          "expected block. Hypothesis numbers 8.4e9, 0.6, 19800, 1.0017, 1.0447 and 1.6667 match the run."),
    fresh("d1-lab-project-2", "project lab 2 (rung 2 completion)", "course/modules/M/M4/project.html:147-191; tests/labs/M4/lab-M4-project-2.py",
          "PASS", f"{S}/checks/lab_twin_r8.out: the page code differs from the twin only by the two blanks, which the twin fills with "
          "(nu - 2) / nu and (99 n + 99) // 100 (the intended completion); the twin runs and its output equals the expected block."),
    fresh("d1-lab-project-3", "project lab 3 (rung 4 stretch or interpretation)", "course/modules/M/M4/project.html:266-314; tests/labs/M4/lab-M4-project-3.py",
          "PASS", f"{S}/checks/lab_twin_r8.out: page code equals twin; output equals expected. 91651.514, z = 2.326348, 213213, and the "
          "index rows 99/100/19788 re-derived."),
    fresh("d6-gate-mutate-m4", "gate: tools/mutate_graders.py --unit M4 --seeds 0-9 exits 0", "tools/mutate_graders.py; ledgers/M4/mutants/",
          "FAIL", f"{S}/mutate_M4_0-9.out: 'mutate_graders M4: FAIL (145/146 killed)' and EXIT 1. Survivor: r8d_01.",
          fix="Add the tiny-scale symmetry test (d8-2.6-symmetry-tiny-scale). Re-run tools/mutate_graders.py --unit M4 --seeds 0-9 to exit 0."),
    fresh("d6-gate-unit-checks", "gate: check_pages, check_dag, check_projects", "tools/check_*.py --unit M4", "PASS",
          f"{S}/gates/check_pages_M4.out, check_dag_M4.out, check_projects_M4.out: each PASS, EXIT 0."),
    fresh("d6-gate-labs", "gate: run_labs M4", "tests/labs/M4; course/modules/M/M4/*.html", "PASS",
          f"run_labs M4: PASS (13/13) ({S}/gates/run_labs_M4.out)."),
    fresh("d6-gate-grader-reference", "gate: run_graders M4 seeds 0-49", "course/modules/M/M4/grader/reference.py", "PASS",
          f"run_graders M4: PASS (reference 50/50 seeds) ({S}/gates/run_graders_M4_0-49.out)."),
    fresh("d6-gate-lint-types", "gate: ruff and mypy", "course/modules/M/M4/grader; tests/labs/M4; tools; tests", "PASS",
          f"ruff check, ruff format --check, mypy --no-incremental: all pass ({S}/gates/ruff_check.out, ruff_format.out, mypy.out)."),
    fresh("d6-gate-tests", "gate: relevant pytest", "tests/test_run_labs.py, tests/test_labs.py, tests/test_memo_exemplars.py, tests/test_curriculum.py",
          "PASS", f"pytest: all pass ({S}/gates/pytest_relevant.out)."),
    fresh("d6-gate-refs", "gate: verify_refs --offline", "tools/verify_refs.py", "PASS",
          f"560 entries, 0 problems ({S}/gates/verify_refs_offline.out)."),
    fresh("d6-gate-page-smoke", "gate: page_smoke for the project page (alone)", "course/modules/M/M4/project.html", "PASS",
          f"tools/page_smoke.py --unit M4 --pages project: PASS, 146 tests pass in the browser ({S}/gates/page_smoke_project.out)."),
    fresh("d6-2.6-alt-root-set", "alternatives: the other alternative roots", f"{S}/alts/", "PASS",
          "Alternatives 1-6 pass on seeds 0-9 (see d1-2.6-alternatives)."),
    fresh("d7-2.6-cross-term-threshold", "cross-term tolerance claim (the threshold)", "course/modules/M/M4/project.html:228; grader/test_project.py:43-47",
          "PASS", f"{S}/checks/cross_r8.out: scale +3 % cross term fails 0 of 50 seeds; +5 % fails 19 of 50; -5 % fails 31 of 50; "
          "reference max 0.0239; smallest mutant errors 0.068 (r8_03) and 0.141 (r9_02) on seeds 0-9. The claims of lines 43-47 and 228 agree."),
    carried("d7-2.6-negation-claim", "grader/test_project.py:231-241 and project.html:212, 220 (byte-identical)",
            "Negating every position negates every loss at 300 draws in both families (test passes on the reference)."),
    carried("d7-2.6-tiny-variance-claims", "grader/test_project.py:559-590 (byte-identical)",
            "The tiny-variance tests pass on the reference (grade_one seeds 0-9)."),
    fresh("d7-L01-L04-prose", "changed prose in L01-L04", "course/modules/M/M4/L02.html:271, 347; L03.html:262; L01.html:51; L04.html:52, 99",
          "PASS", "L02:271 the mean E[X] = 3/10 with weights 1, 2, 3, 2, 1, 1 over -2, -1, 0, 1, 2, 3 (Example 3.6 table, L01 line 141): "
          "(-2 - 2 + 0 + 2 + 2 + 3)/10 = 3/10 checked. L02:347 V = -U gives Var(U+V) = 0 and Var(U) + Var(V) = 2. L03:262 "
          "p = (1 - 1/sqrt(3))/2 gives pq = 1/6 and gamma4 = 3. L01 and L04 are byte-identical."),
    fresh("d7-L03-numerics", "L03 numerics and numbering after the renumbering", "course/modules/M/M4/L03.html (Sections 1-4, Problems, Misconceptions)",
          "PASS", "The deleted Assumption 2.7 and Proposition 2.8 were the last items of section 2, so no later number moves. No residual "
          "reference (grep). Section 3 moments 7/4, 163/16, 2157/32, 149461/256 and the Bernoulli values re-derived (see d1-cards-math)."),
    fresh("d7-cards-exact-lab-grade", "grade T only for values the page proves", "course/modules/M/M4/cards.json: M4-c165, M4-c185, M4-c233 to M4-c236",
          "FAIL", "M4-c185 and M4-c233 to M4-c236 are now C (round-8 change). M4-c165 (n = 1, same basis) remains T. See d1-cards-labs.",
          fix="Grade M4-c165 C (or derive it on the page and keep T for that card only)."),
    fresh("d8-2.6-symmetry-tiny-scale", "2.6 autograder: symmetry condition is tested at every scale (project.html:223; the suite checks each condition, project.html:220)",
          "course/modules/M/M4/grader/test_project.py (symmetry tests at lines 435-458); ledgers/M4/mutants/r8d_01_symmetry_checked_to_absolute_tolerance_1e9.py",
          "FAIL", f"Mutant r8d_01 (symmetry checked to an absolute tolerance of 1e-9) SURVIVES on seeds 0-9 ({S}/mutate_M4_0-9.out, "
          f"killed_by null). {S}/checks/tiny_asym_probe_r8.out: the reference raises ValueError('cov must be symmetric') for "
          "[[1e-14, 1e-15], [2e-15, 9e-14]]; the mutant returns 10 losses. The suite's symmetry tests use entries of order 4e-4 only.",
          fix="Add to grader/test_project.py a test, parametrized over FAMILY_CASES, that passes cov = [[1e-14, 1e-15], [2e-15, 9e-14]] "
              "to simulate_losses and expects ValueError ('cov must be symmetric'). The test count on the page changes from 146 "
              "to 148 (project.html:206 and the 145/146 numbers at lines 206 and 220 must be updated after the collect-only run)."),
    fresh("d8-2.6-mut-r8d-02", "2.6 mutation: r8d_02 Gaussian stream reseeded per draw", "ledgers/M4/mutants/r8d_02_gaussian_stream_reseeded_per_draw.py",
          "PASS", f"KILLED by test_gaussian_stream_is_frozen_and_the_loss_is_minus_the_weighted_return ({S}/mutate_M4_0-9.out)."),
    fresh("d8-2.6-mut-r8d-03", "2.6 mutation: r8d_03 positions read in reverse order", "ledgers/M4/mutants/r8d_03_positions_read_in_reverse_order.py",
          "PASS", f"KILLED by test_gaussian_loss_variance_matches_portfolio_covariance ({S}/mutate_M4_0-9.out)."),
    fresh("d8-2.6-mut-r8d-04", "2.6 mutation: r8d_04 Gaussian draws via normalvariate", "ledgers/M4/mutants/r8d_04_gaussian_draws_via_normalvariate.py",
          "PASS", f"KILLED by test_gaussian_stream_is_frozen_and_the_loss_is_minus_the_weighted_return ({S}/mutate_M4_0-9.out)."),
    fresh("d8-2.6-alt6-chi-order", "over-constraint check: Student-t draw order is open (Conventions item 5)",
          f"{S}/alts/alt6_chi_before_normals.py", "PASS", "Chi-square drawn before the normals of each Student-t draw: grade_one.py "
          "seeds 0-9 rc 0 on all ten seeds. The suite does not over-constrain the open order."),
    fresh("d8-2.6-lab-counts", "chi-square share counts and lag tests (project.html:228; test_project.py:207-228)", f"{S}/checks/chi_lag_r8.out",
          "PASS", "lag-1 pairs (2k, 2k+1) fail 50/50; lag-2 pairs (4j, 4j+2) fail 50/50; lag-3 pairs (6j, 6j+3) fail 39/50; even-indexed "
          "sharing fails 44/50; disjoint lag-four pairs pass 50/50 (chi_lag4_disjoint_r8.out)."),
    fresh("d8-cards-changed-and-new", "changed and new cards: M4-c023, c081, c140, c195, c198, c218, c241, c242, c244",
          "course/modules/M/M4/cards.json", "PASS", "Each checked against its lesson: c023 (Proposition 2.3), c081 (L05 line 370, 4 <= 1), "
          "c140 (L09 section 4 misconception), c195 (L01 Proposition 2.2), c198 (Remark 3.3 left-continuity), c218 (L09 Proposition 2.3(b)), "
          "c241 (lab numbers, L05), c242 (L05 Proposition 1.1(iv)), c244 (L02 Proposition 2.3). c243 is a duplicate (see d1-cards-duplicates)."),
    fresh("d8-2.6-variance-claims-lines-31-39", "grader comment numbers, lines 31-39 (tolerance and sweep claims)",
          "course/modules/M/M4/grader/test_project.py:31-39", "PASS",
          f"{S}/checks/variance_sweep_r8.out (seeds 0-1999): reproduces 0.126, 0.097, 0.073, 0.062; inflations 5/3, 3/2, 7/5, 4/3; "
          "counts 347, 317, 342 of 343, 288 of 317; seed 1093 nu 3 fails 0.30."),
]

mutants = []
pattern = re.compile(r"^(KILLED|SURVIVED) (\S+?): (.*?) -> (.*)$")
for line in (ROOT / S / "mutate_M4_0-9.out").read_text(encoding="utf-8").splitlines():
    m = pattern.match(line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    mutants.append({"id": name, "description": desc.split(". ")[0] if False else desc,
                    "killed_by": None if killed.strip() == "None" else killed.strip()})

fragment = {
    "unit": "M4",
    "slice": "d",
    "round": 8,
    "verifier": "independent verifier (Haiku), unit M4, slice d, round 8; not a builder of M4",
    "pin": PIN + " (detached HEAD in the checkout)",
    "base": "9373ef39 (round-7 pin). Delta for slice d: course/modules/M/M4/{project.html 206, 215, 228, 359; grader/test_project.py 44-47 (comments); cards.json; L02.html 271, 347; L03.html; index.html}; ledgers/M4/mutants r8d_01..04 added",
    "checkout": str(ROOT),
    "scratch": "ledgers/M4/scripts/M4-d-r8/ (all scripts and outputs are in the checkout); /tmp/m4d_r8_* copies of lesson text",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": None,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "gate_scope": "check_pages, check_dag, check_projects, run_labs, run_graders 0-49, page_smoke (project page), ruff check and format, mypy --no-incremental, pytest on four files, verify_refs --offline, tools/mutate_graders.py --unit M4 --seeds 0-9 (exit 1), alternatives 1-6 on seeds 0-9, instances (20 seeds)",
    "notes": [
        "Round-7 FAIL rows re-verified: d1-2.6-grader-comment-numbers, d7-2.6-cross-term-threshold and d1-cards-forward-reference now PASS; d1-prose-numbers PASS; d1-prose-scope still FAIL (lag-four sentence); d7-cards-exact-lab-grade still FAIL (c165).",
        "Round-8 changes that introduced errors: the Exemplar A word count (project.html:359) and the lag-four sentence was rewritten to a universal claim; the duplicate card M4-c243.",
        "Not checked: the 2.6 hours are not re-estimated because the table and the hub are byte-identical to round 7; the lesson-level proofs of L01-L10 (outside slice d) are not re-read beyond the lines cited here; the 146-test count will change if the symmetry test is added.",
    ],
}
rows_failed = [r for r in rows if r["status"] != "PASS"]
fragment["verdict"] = "FAIL" if rows_failed or any(m["killed_by"] is None for m in mutants) else "PASS"
fragment["summary"] = (
    f"Slice d round 8: {len(rows)} rows, {len(rows) - len(rows_failed)} PASS, {len(rows_failed)} FAIL. "
    f"Mutants: {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed (r8d_01 survives). Non-PASS: "
    + "; ".join(r["id"] for r in rows_failed)
)
out = ROOT / "ledgers/M4/M4-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "failed", len(rows_failed), "mutants", len(mutants))
