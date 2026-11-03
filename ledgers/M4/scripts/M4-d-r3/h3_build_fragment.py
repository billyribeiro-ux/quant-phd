"""Builds ledgers/M4/M4-d.json for round 3 (independent verifier h3, slice d). Rows, evidence and mutants are
written from this round's runs; the round-2 row ids are kept. Run from the checkout root."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path.cwd()
S = "ledgers/M4/scripts/M4-d-r3"
prev = json.loads(Path("/Users/billyribeiro/.fanout/frags/D-M4-d.round2.json").read_text(encoding="utf-8"))
old = {r["id"]: r for r in prev["rows"]}

def carry(files: str, text: str) -> str:
    return f"Carried from round 2 ({files} byte-identical since the previous pin c737272f): {text}"

R: dict[str, tuple[str, str, str]] = {}  # id -> (status, evidence, fix)
def row(i: str, status: str, evidence: str, fix: str = "") -> None:
    R[i] = (status, evidence, fix)

row("d1-2.6-ladder", "PASS",
    "Re-verified (rungs prose, project.html:53 changed): tests/labs/M4/lab-M4-project-1.py:12-13 and lab-M4-project-3.py:14-15 "
    "both set POSITIONS = [3_000_000, 2_000_000] and COV = [[0.0004, 0.0001], [0.0001, 0.0009]]: volatilities 2 % and 3 %, "
    "correlation 0.0001/(0.02*0.03) = 1/6. lab-M4-project-2.py takes only nu and n, as the sentence says. Ladder, stretch and "
    "spec ids unchanged apart from hunks checked under other rows.")
row("d1-2.6-spec-questions", "PASS", carry("project.html #conditions (lines 219-226) and grader/reference.py",
    "the Conditions list is unchanged, and the reference's validation block (simulate_losses, quantile_99) matches it; "
    "run_graders M4 50/50 reference seeds pass (h3_run_graders_M4_0-49.out)."))
row("d1-2.6-hours", "PASS", carry("project.html #budget (lines 231-248)",
    "no delta hunk touches lines 231-248; hours arithmetic unchanged. Delta hunks in project.html are at lines 53, 204, 206, 215, 228, 359, 402."))
row("d1-2.6-autograder-reference", "PASS",
    "Re-run: tools/run_graders.py --unit M4 --seeds 0-49 -> 'run_graders M4: PASS (reference 50/50 seeds, slowest 0.8 s)', exit 0 "
    f"({S}/h3_run_graders_M4_0-49.out). grader/reference.py byte-identical to c737272f.")
row("d1-2.6-instances", "PASS",
    "Re-verified: grader/instance.py byte-identical to c737272f; make_instance over seeds 0-1999 gives nu counts "
    "{3: 346, 4: 330, 5: 347, 6: 317, 7: 343, 8: 317}, so nu of 3 or 4 occurs on about a third of seeds, consistent with the "
    "page's 137 + 1 statement. Seeds 0-49 pass the reference (run above).")
row("d1-2.6-mut-own", "PASS",
    "Re-run this round: tools/mutate_graders.py --unit M4 --seeds 0-9 -> KILLED for v1_01..v1_06 (exit 0, 127/127; "
    f"{S}/h3_mutate_M4_0-9.out).")
row("d1-2.6-mut-existing", "PASS",
    "Re-run this round: tools/mutate_graders.py --unit M4 --seeds 0-9 -> 'mutate_graders M4: PASS (127/127 killed)', exit 0 "
    f"({S}/h3_mutate_M4_0-9.out). ledgers/M4/mutants/ holds 127 files: the 118 of round 2, the four new v7_01..v7_04 written by "
    "this verifier, and five v6_01..v6_05 that were already present, untracked, in this checkout when the round started; they were "
    "run as existing mutants and were not written by this verifier. Zero SURVIVED lines.")
row("d1-2.6-mut-m11", "PASS",
    "Re-verified: m11_loss_sign_flipped.py KILLED by test_gaussian_stream_is_frozen_and_the_loss_is_minus_the_weighted_return (seed 0) "
    "in the 127/127 run. Conventions item 2 (project.html:212, 'The loss is ... positive when the portfolio falls') is outside every delta hunk.")
row("d1-2.6-mut-r9_03", "PASS",
    "Re-verified against the changed text: r9_03_student_t_chi_square_reused_every_second_draw.py KILLED by "
    "test_student_t_draws_do_not_share_chi_square (seed 0). The page still states the requirement it violates: item 5 "
    "'one chi-square variable per draw' (project.html:215) and the contract-notes paragraph (project.html:228).")
row("d1-2.6-mut-v4_m02", "PASS",
    "Re-verified: v4_m02_matched_factor_skipped_for_small_nu.py KILLED by test_student_t_mean_absolute_loss_matches_the_matched_scale "
    "(seed 0; grader/test_project.py:183). The page states the requirement: Grading mode (project.html:206, 'the mean absolute Student-t "
    "loss at nu of 3 to 8') and contract-notes (project.html:228, 'checks the matched factor through the mean absolute loss').")
row("d1-2.6-mut-m17", "PASS",
    "Re-verified against the round-3 text. m17 (Student-t normals from Random(seed + 1); variant built from the reference in "
    f"{S}/h3_sign_and_m17_variants.py, scratch copy, not in mutants/) SURVIVES seeds 0-9, 10/10 pass ({S}/h3_variants_0-9.out). "
    "It is ruled equivalent because project.html:215 now reads 'The Student-t family takes Z for each draw and one chi-square "
    "variable per draw ... The source of the Student-t family's normals and the order of its draws are not fixed here.' The round-2 "
    "phrase 'in the same way' is gone, so no sentence fixes the Student-t source. ledgers/M4/equivalent/README.md point 2 quotes "
    "this rule correctly. Only the Gaussian source is fixed (project.html:215, random.Random(seed).gauss).")
row("d1-2.6-alternatives", "PASS",
    "Round-2 objection met. Round 3 changed alt_1 and alt_2: alt_1 factors the covariance by LDL^T (ledgers/M4/scripts/alt_1.py:29-47, "
    "L = unit*sqrt(d)), a different algorithm from the row-by-row reference; alt_2 finds the 99% order statistic by counting distinct "
    "losses (alt_2.py:102-107, Counter), a different algorithm from sorting. alt_3 (column Cholesky), alt_4 (chi-square as a sum of "
    "squared normals) and alt_5 (heapq.nsmallest) are unchanged. Run this round: ledgers/M4/scripts/run_alternatives.py --seeds 0-9 -> "
    f"reference and alt_1..alt_5 each PASS 10/10 seeds ({S}/h3_run_alternatives_0-9.out). Seeds 0-49 not re-run this round.")
row("d1-2.6-starter", "PASS", carry("grader/starter.py", "the starter's signatures are unchanged."))
row("d1-2.6-messages", "PASS",
    "Re-verified: the delta in grader/test_project.py (lines 182-200) changes comments and one docstring only (Student-t variable "
    "renamed X_nu; code lines unchanged). Checked: E|T_nu| = 2 sqrt(nu) Gamma((nu+1)/2)/(sqrt(pi)(nu-1) Gamma(nu/2)) gives 1.1027 "
    "at nu = 3 (= 2 sqrt(3)/pi); sqrt(nu/(nu-2)) = 1.732 at nu = 3; the loop is range(3, 9) with 20_000 draws and tolerance 0.05 "
    "(lines 183-198). Collect-only count re-run: 138.")
row("d1-2.6-count-and-pyodide", "PASS",
    "Re-verified: pytest --collect-only on a copy of the grader -> 138 tests. QF_SEED 0, 1, 2 (nu 4, 3, 3) -> '137 passed, 1 skipped'; "
    "QF_SEED 3 (nu 7) -> '138 passed'. page_smoke --unit M4 --pages project -> 'in-browser grader: All 138 tests pass' "
    f"({S}/h3_page_smoke_project.out). project.html:206 states 138 and the 137 + 1 case; both verified.")
row("d1-2.6-grader-comment-numbers", "PASS",
    "test_project.py:31-48 byte-identical to c737272f (delta hunks start at line 182). The new comments at 182-200 are re-verified under "
    "d1-2.6-messages. Constants TOL_T_VARIANCE = 0.30 (line 41) and TOL_CROSS_TERM = 0.05 (line 48) unchanged.")
row("d1-rubric-observable", "PASS", carry("project.html #rubric (lines 330-344)",
    "no delta hunk touches the rubric table; the changed lines are at 359 and 402 (exemplars)."))
row("d1-rubric-calibration", "PASS",
    "Re-verified: exemplar A (project.html:348-399) and B (400-) changed at lines 359 and 402. (a) The exemplar A C5 note (line 359) "
    "quotes 'the Student-t is always riskier, so the Gaussian understates the loss'; the same words are in the exemplar A Summary. "
    "The note's body count: body 90 words + 10 heading words = 100 (python count of the memo text). (b) Exemplar B Summary = 70 words, "
    "under the 80-word bar in the C5 note. (c) Exemplar B's 'named constant of the autograder file': the Limitations (project.html:453) "
    "state a relative variance tolerance of 0.30, which equals TOL_T_VARIANCE = 0.30 (grader/test_project.py:41). (d) 213213 - 210946 = 2267; "
    "243004 - 210946 = 32058; 32058/210946 = 15.20 %; the labs print 210946, 243004, 1.0447 and 213213 (h3_labout/).")
row("d1-rubric-question-bank", "PASS", carry("project.html #rubric-heading, #brief and #self-assessment (lines 316-344, 464-470)",
    "no delta hunk touches these sections; the question bank is unchanged."))
row("d1-atlas", "PASS", carry("curriculum/meta.yaml (lines 194-276)",
    "the atlas block is byte-identical; the project.html changes do not change any deliverable the atlas names (report, grader, labs)."))
row("d1-studio", "PASS", carry("curriculum/01-foundations.yaml", "the studio entry is unchanged."))
row("d1-lab-project-1", "PASS",
    f"run_labs --unit M4: 'run_labs M4: PASS (13/13)', exit 0 ({S}/h3_run_labs_M4.out). Twin tests/labs/M4/lab-M4-project-1.py under "
    f"python3 -I -W error: exit 0, prints 8400000000.0, gaussian 99% loss 210946, student_t 243004, sample variance ratios 1.0017 and 1.0447, "
    f"unmatched inflation 1.6667 ({S}/h3_labout/lab-M4-project-1.out). The Lab 1 block is unchanged; the rung prose at line 53 is verified under d1-2.6-ladder.")
row("d1-lab-project-2", "PASS",
    f"run_labs 13/13 includes lab-M4-project-2 (exit 0). Twin under -I -W error prints matched factor 0.600000 at nu = 5, index 19800 at "
    f"n = 20000, index 100 at n = 101 ({S}/h3_labout/lab-M4-project-2.out). Twin and Lab 2 block byte-identical to c737272f.")
row("d1-lab-project-3", "PASS",
    f"Twin under -I -W error prints 8400000000.0, parametric 99% loss 213213 cents, index 100 for n = 101 (0.99 n = 99.99; ceil 100, floor 99) "
    f"({S}/h3_labout/lab-M4-project-3.out). The new sentence 'Lab 3 uses the same one' (project.html:53) is verified: POSITIONS and COV "
    "are identical to Lab 1 (lab-M4-project-3.py:14-15).")
row("d1-prose-numbers", "PASS",
    "Re-verified each number in the delta-touched prose: '138 checks' (collect-only 138); '137 passed and one skipped' at nu of 3 or 4 "
    "(QF_SEED 0, 1, 2); the portfolio values and volatilities 2 % and 3 % and correlation 1/6 (Lab 1 twin lines 12-13); '1.73 at nu = 3' "
    "(sqrt(3) = 1.732); '20,000 draws' and the 5 % tolerance (grader lines 183-198); exemplar numbers per d1-rubric-calibration.")
row("d1-prose-scope", "PASS",
    "Re-verified the new sentences at project.html:53, 204, 206, 215, 228, 359, 402 for scope words. 'always' occurs only inside the quoted "
    "exemplar A sentence that the note at line 359 criticises. 'every nu of 3 to 8' (grader comment line 185) is backed by range(3, 9) at line 186. "
    "'the same one' (line 53) is backed by identical POSITIONS and COV.")
row("d1-prose-process-words", "PASS",
    "Re-verified: project.html contains no process words (verifier, builder, ruling, round, fragment, architect, revised). The verb 'fixes' "
    "(lines 215, 228) is the ordinary sense.")
row("d1-prose-banned-phrases", "PASS",
    "Re-verified against BUILDER_RULES §1.2 to §1.4 (lines 38-60): a scan of project.html text for TODO, TBD, lorem, an ellipsis, 'for brevity', "
    "'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', "
    "'experts agree', 'it is well known', 'obviously', 'clearly', 'roughly half', 'historically', 'About N%', 'motivat' -> 0 hits.")
row("d1-dag", "PASS",
    f"Re-verified: check_dag --unit M4 -> 'check_dag M4: PASS', exit 0 ({S}/h3_check_dag.out). None of the changed lines adds a concept link.")
row("d1-notation", "PASS",
    "Re-verified: notation/notation.json registers T (S1), \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f and \\mathbb{Q}. project.html uses none "
    "of them with another meaning (grep: no \\Phi, \\gamma, R^\\ast, R_f, \\mathbb{Q}, or T as a symbol). The round-3 rename of the Student-t "
    "variable in a test comment from T_nu to X_nu removes a clash with the registered T. Exemplar B's E[W^{-1}] uses the registered \\E macro.")
row("d1-cites", "PASS", carry("references/references.json and project.html #reading (lines 480-487)",
    "no delta hunk touches the reading list; the bibliography is unchanged."))
row("d1-structure", "PASS",
    f"Re-verified: check_pages --unit M4 -> 'check_pages M4: PASS', exit 0 ({S}/h3_check_pages.out). Section ids and headings are unchanged; the delta changes body text only.")
row("d1-cards-schema", "PASS",
    "Re-verified: 212 entries (unchanged count); key sets: 192 entries {back, front, grade, id, lesson} and 20 {back, basis, front, grade, id, lesson}; "
    "grades 192 T and 20 C; every C has a basis and no T has one; no duplicate ids; no removals or additions between c737272f and a007712f "
    "(python diff of cards.json).")
row("d1-cards-numbers-in-lesson", "PASS",
    "Re-verified the nine changed cards (M4-c028, c029, c033, c047, c070, c084, c112, c140, c183) against their lessons: 250000 (L02.html:89, 141, 169); "
    "489 and 122250000 (L02 expected output, line 260); 500 (L02.html:363); the law on 0, 1, 2, 10 with 1/2, 1/4, 1/8, 1/8 (L03.html:138); "
    "2.065, 5.580, 2.073, 5.625 (L03.html expected output, line 256 and 280); N(0.5, 1.5^2), 7.11e-13 and 244.69193226 (L07.html:170 and the Part A "
    "expected output); 'Section 4' (L09.html:282-294, the misconceptions). Every card number appears in its lesson.")
row("d1-cards-labs", "PASS",
    f"Re-verified against lab output: c033 (489 losses, lab-M4-L02-1 output line 9; 489 x 250000 = 122250000); c047 and c183 (lab-M4-L03-1 output: "
    "skewness 2.065, kurtosis 5.580; exact 2.0730 and 5.6254 = 149461/26569); c112 (lab-M4-L07-1 output: 7.11e-13 at t = 2.0, closed form "
    f"244.69193226, MU = 0.5, SIGMA = 1.5 at L07.html:174). All in {S}/h3_labout/.")
row("d1-cards-math", "PASS",
    "Re-derived the nine changed cards: Var(2X) = 35/3 = 4 * 35/12 (c028); E[X^2] = 91/6, Var = 35/12, equal only when E[X] = 0 (c029); "
    "10000/20 = 500 (c033); exact skewness 18610596/4330747 = 2.0730 and kurtosis 149461/26569 = 5.6254 for the law with mean 7/4, m2 = 163/16 "
    "(c047, c183, recomputed by hand); E[e^(tX)] for N(0.5, 1.5^2) at t = 2 is exp(5.5) = 244.69193226 (c112); c084 density "
    "(sigma sqrt(2 pi))^-1 exp(-(x - mu)^2/(2 sigma^2)) matches L06.html Definition 1.1. The 203 unchanged entries are byte-identical per entry "
    "(cards.json diff: exactly nine entries changed); their math is carried from round 2.")
row("d1-cards-lesson-statements", "PASS",
    "Re-verified the nine changed cards against the current lesson text: L02 §1-§2 are stated for a finite probability space with positive weights "
    "(L02.html:55; Propositions 2.2 and 2.3 at L02.html:106, 115); L05 Propositions 1.1 and 1.2 for finitely many values (L05.html:60; c069, c070, c210); "
    "L06 Definition 1.1 (L06.html:64-66); L07 Part A (L07.html:170, 174); L09 Section 4 (L09.html:294) for c140. The one card whose hypothesis list is "
    "weaker than the proposition it cites (M4-c140 against Proposition 2.3(b)) is recorded under d1-cards-hypotheses.")
row("d1-cards-duplicates", "PASS",
    "Re-verified: no duplicate normalized fronts or backs among 212 cards (python). The round-1 pairs (M4-c066/c213, M4-c070/c211) are no longer duplicates; "
    "M4-c070 'How does covariance scale?' is unique.")
row("d1-cards-c191-grade", "PASS", carry("cards.json entry M4-c191 (line 1339)",
    "grade T; its back states Example 2.5's hypotheses and Assumption 1."))
row("d1-cards-hypotheses", "FAIL",
    "Round-2 FAILs fixed: M4-c028 (cards.json:192) now carries 'Hypothesis: finite probability space with positive weights' (L02.html:55, Proposition 2.3); "
    "M4-c029 (line 199) carries the same hypothesis (Proposition 2.2, L02.html:106); M4-c070 (line 489) carries 'Hypothesis: finitely many values' "
    "(L05.html:60, Proposition 1.2). NEW FAIL at M4-c140 (cards.json:978-981): its back reads 'The statement needs i.i.d. copies with finite positive variance "
    "sigma^2, and normality of X is not one of its hypotheses (Section 4). ... Proposition 2.3(b), under Assumption 1 of Section 2, gives the limit'. It cites "
    "Proposition 2.3(b) but omits 'finitely many values', which L09.html:132 states as a hypothesis of Proposition 2.3 ('Under the i.i.d. hypotheses of this section, "
    "with the variables finitely valued') and L09.html:55 states for Propositions 1.1, Theorem 1.3 and 2.1-2.3. The round-2 wording of c140 had the clause; round 3 removed it. "
    "The sibling card M4-c218 (cards.json:1486) states 'Hypotheses: i.i.d. variables with finitely many values, and Assumption 1 of Section 2 (Proposition 2.3(b))'.",
    "In course/modules/M/M4/cards.json entry M4-c140 (back, line 981) restore the clause: 'The statement needs i.i.d. copies with finitely many values and "
    "finite positive variance sigma^2, and normality of X is not one of its hypotheses (Section 4).' The same omission is in the lesson at "
    "course/modules/M/M4/L09.html:294 (misconception 'the central limit theorem needs the variables to be normal'), which the builder should correct in the same change "
    "(lesson file is outside this slice; not edited here).")
row("d1-data", "PASS",
    "Re-verified: the Inputs statement (project.html:53-54, 'Every input is SIMULATED. No file is read.') is unchanged in substance; grader/instance.py is byte-identical "
    "to c737272f; the project lab twins read no file (grep for open(/read_text in tests/labs/M4/lab-M4-project-*.py: no matches).")
row("d1-freshness-registry", "PASS", carry("references/references.json",
    "byte-identical; the blitzstein2019introduction entry is unchanged. verify_refs --offline: 'offline integrity: 560 entries, 0 problems' "
    f"({S}/h3_verify_refs_offline.out)."))
row("d1-gates-repo", "PASS",
    "M4 gate set re-run this round: check_pages, check_dag, check_projects M4 PASS; run_labs M4 13/13; mutate_graders M4 127/127; run_graders M4 50/50; "
    "page_smoke project PASS; ruff check . 'All checks passed!'; mypy --no-incremental 'Success: no issues found in 331 source files'; pytest "
    "tests/test_labs.py, test_memo_exemplars.py, test_page_checks.py, test_run_labs.py, test_page_smoke.py, test_curriculum.py, test_docs_figures.py exit 0; "
    "fetch_data --check 3 datasets, 0 problems. Outside this slice, not an M4 finding: ruff format --check . reports ledgers/M3/retired/"
    "v2d_06_eigh_uses_numpy_not_standard_library.py (noted under notes).")
row("d1-tools-structure", "PASS", carry("tools/ (no file changed)",
    "the M4 gate tools were run unchanged this round (check_*, run_labs, run_graders, mutate_graders, page_smoke, verify_refs, fetch_data)."))
row("d2-2.6-constraints-exceptions", "PASS",
    "Round-2 FAIL fixed. The Constraints paragraph (project.html:204) now lists 'the sign of the Student-t loss (item 2)' among the items the suite does not "
    "grade, and 'the source and the order of the Student-t family's draws (item 5; the Gaussian order is graded)'. contract-notes (project.html:228) says the "
    "suite does not test the Student-t sign. Item 2 (project.html:212) states the sign convention for both families, so the Student-t sign is an item-2 "
    "convention the list names. Confirmed by run: the Student-t-only sign flip (round(total) for student_t) SURVIVES seeds 0-9, 10/10 "
    "(h3_variants_0-9.out); the Gaussian-only sign flip is KILLED 10/10 by test_gaussian_stream_is_frozen_and_the_loss_is_minus_the_weighted_return.")
row("d3-2.6-mut-new-student-error", "PASS",
    "Four new student-error mutants written by this verifier, each one edit of the reference (generator "
    f"{S}/h3_make_mutants.py): v7_01 (one chi-square per position, not per draw): KILLED by test_student_t_cross_term_matches_matched_covariance (seed 0); "
    "v7_02 (99% index floor(0.99 n) + 1): KILLED by test_quantile_99_convention_on_small_lists (seed 0); v7_03 (each position rounded before the sum): "
    "KILLED by test_gaussian_stream_is_frozen_and_the_loss_is_minus_the_weighted_return (seed 0); v7_04 (chi-square scale 1.0): KILLED by "
    "test_student_t_cross_term_matches_matched_covariance (seed 0). Each violates a stated rule: 'one chi-square variable per draw' (project.html:215, 228), "
    "'ceil(0.99 n)' (project.html:214), 'rounded once and not per position' (project.html:206), 'chi-square with nu degrees of freedom' (project.html:211).")

rows = []
for rid, orow in old.items():
    if rid not in R:
        raise SystemExit(f"round-2 row without a round-3 decision: {rid}")
    status, evidence, fix = R[rid]
    r = {"id": rid, "check": orow["check"], "location": orow["location"], "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    if rid == "d1-cards-hypotheses":
        r["location"] = ("course/modules/M/M4/cards.json M4-c140 (back, line 981: FAIL); M4-c028 (line 192), M4-c029 (line 199), "
                         "M4-c070 (line 489): now pass")
    rows.append(r)
for rid in R:
    if rid not in old:
        status, evidence, fix = R[rid]
        r = {"id": rid, "check": "Round-3 new check: " + rid, "location": "ledgers/M4/mutants/v7_*.py; ledgers/M4/scripts/M4-d-r3/h3_make_mutants.py",
             "status": status, "evidence": evidence}
        rows.append(r)

mutants = []
for line in (ROOT / S / "h3_mutate_M4_0-9.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"KILLED (\S+)\.py: (.*?) -> (.*)$", line)
    if m:
        mutants.append({"id": m.group(1), "description": m.group(2), "killed_by": m.group(3),
                        "path": f"ledgers/M4/mutants/{m.group(1)}.py"})

n_fail = sum(1 for r in rows if r["status"] != "PASS")
fragment = {
    "unit": "M4",
    "slice": "d",
    "round": 3,
    "verifier": "independent verifier (Haiku, h3), not a builder of M4; round 3",
    "pin": "a007712f (checkout detached at the pin)",
    "base": "c737272f (round-2 pin; delta from git diff c737272f a007712f)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD3-M4-d",
    "scratch": "/tmp/M4-d-r3-h3 (scratch copies); outputs under ledgers/M4/scripts/M4-d-r3/h3_*",
    "verified_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(timespec="seconds"),
    "verdict": "FAIL" if n_fail else "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope: project.html (rubric, exemplars, Constraints, Grading mode, Conventions item 5, contract-notes, Lab 1 and Lab 3 rung prose), "
        "grader/ (test_project.py lines 182-200 changed; reference.py, instance.py, starter.py unchanged), the three project labs, cards.json "
        "(nine changed cards read against their lessons; 203 unchanged entries carried per entry), the 127 mutants and the alternatives.",
        "Delta c737272f..a007712f read hunk by hunk for every M4 slice file: project.html (6 hunks), test_project.py (1 hunk), cards.json (9 entries), "
        "L03.html and index.html (outside the slice; read only where a card cites them).",
        "Checkout state at start (not written by this verifier): ledgers/M4/M4-d.json was already modified (an older round-13 fragment content), the "
        "untracked ledgers/M4/scripts/M4-d-r3/ files of an earlier attempt (including a DONE marker, build_fragment_m4d_r3.py, mutate_M4_0-9*.out and "
        "others), and five untracked mutants v6_01..v6_05. None of them was used as evidence; every gate was re-run with h3_* outputs.",
        "Out of slice, observed: ruff format --check . fails on ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py (missing blank lines); "
        "ruff check . passes. Not an M4 finding.",
        "Could not check: (a) run_alternatives on seeds 0-49 (asked 0-9 this round); (b) a full line-by-line re-read of all 1,000-plus lines of project.html "
        "(only the delta hunks, the sections they touch, and the carried sections were read); (c) the Appendix A proof text beyond the changed exemplar passages; "
        "(d) an interactive browser run of the grader (page_smoke headless only); (e) verify_refs live (offline only); (f) the lesson pages L02, L03, L05, L06, L07, "
        "L09 read only at the lines the cards cite; (g) the 203 unchanged cards are carried per entry, not re-derived this round.",
    ],
    "summary": (f"Slice d round 3: {len(rows)} rows, {sum(1 for r in rows if r['status']=='PASS')} PASS, {n_fail} non-PASS. "
                f"The round-2 FAIL rows d1-2.6-mut-m17, d1-2.6-alternatives and d2-2.6-constraints-exceptions are fixed in the round-3 text and re-verified PASS. "
                f"d1-cards-hypotheses is FAIL on a new defect: M4-c140 drops the finitely-many-values hypothesis of Proposition 2.3(b). "
                f"Mutation gate 127/127 killed (tools/mutate_graders.py --unit M4 --seeds 0-9 exit 0); alternatives 10/10 for reference and alt_1..alt_5; "
                f"check_pages, check_dag, check_projects, run_labs (13/13), run_graders (50/50), page_smoke, ruff, mypy and the relevant pytest suites all pass."),
}
out = ROOT / "ledgers/M4/M4-d.json"
out.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "non-pass", n_fail, "mutants", len(mutants), "verdict", fragment["verdict"])
