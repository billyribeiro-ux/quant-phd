"""Round-9 verifier (M4, slice d): builds the fragment ledgers/M4/M4-d.json from the round-9 outputs in this checkout.

Mutant rows are parsed from ledgers/M4/scripts/M4-d-r9/mutate_M4_0-9_with_new.out (tools/mutate_graders.py --unit M4
--seeds 0-9). Run from the checkout root: python -I ledgers/M4/scripts/M4-d-r9/build_fragment_slice_d_r9.py
"""
import json
import pathlib
import re
import sys
from datetime import UTC, datetime

ROOT = pathlib.Path.cwd()
S = "ledgers/M4/scripts/M4-d-r9"
R = "ledgers/M4/scripts/M4-d-r9"

# ---- mutants from the gate output -------------------------------------------------------------------------------
mutants = []
pat = re.compile(r"^(KILLED|SURVIVED) (\S+?\.py): (.*) -> (\S.*)$")
for line in (ROOT / S / "mutate_M4_0-9_with_new.out").read_text(encoding="utf-8").splitlines():
    m = pat.match(line)
    if not m:
        continue
    status, name, desc, killer = m.groups()
    killed_by = None if killer.strip() == "None" else killer.strip()
    mutants.append({"name": name, "description": desc.strip(), "killed_by": killed_by, "status_in_gate": status})
assert len(mutants) == 150, len(mutants)
assert sum(1 for m in mutants if m["killed_by"]) == 149

GATE = f"{S}/mutate_M4_0-9_with_new.out"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


def carried(files):
    return ("Carried from round 8 (" + files + " byte-identical since the round-8 pin 2d755599; the round-9 delta "
            "does not touch them): ")


# ---- hours, instances, starter, rubric, atlas, studio, citations, data, structure ---------------------------------
row("d1-2.6-hours", "2.6 hours: component sum and own estimate within 30 %",
    "course/modules/M/M4/project.html:33, 234-245 (table#hours)", "PASS",
    carried("project.html lines 33 and 234-245") + "components 2+2+12+8+4+2 = 30 = data-hours-project=30 (line 33). "
    "Own estimate (see d9-2.6-hours-own-estimate) is 22.5 h, 25 % below 30, inside the 30 % band.")
row("d1-2.6-instances", "2.6 instances: valid, and answers change across seeds",
    "course/modules/M/M4/grader/instance.py", "PASS",
    f"{S}/checks/instances_sample_r9.py (fresh 20 seeds: 11, 37, 101, ..., 9090) -> {S}/checks/instances_sample_r9.out: "
    "all 20 valid (label SIMULATED, 2 or 3 whole positive-cent positions in 100000..5000000, nu in 3..8, draws not a "
    "multiple of 100 and <= 19987, symmetric covariance, reference runs without ValueError so every pivot is positive); "
    "20 distinct Student-t 99% losses and 20 distinct Gaussian 99% losses.")
row("d1-2.6-starter", "2.6 starter signatures", "course/modules/M/M4/grader/starter.py:15-34", "PASS",
    carried("grader/starter.py and project.html line 202") + "starter signatures "
    "matched_scale(nu: int) -> float, simulate_losses(...) -> list[int], quantile_99(losses_cents: list[int]) -> int "
    "match project.html:202 and reference.py (checked by eye and by the repr in project.html).")
row("d1-rubric-observable", "rubric observable levels", "course/modules/M/M4/project.html:330-343 (table#rubric)",
    "PASS", carried("project.html lines 330-343") + "every descriptor is observable; C1 level 2 and C5 level 1 are "
    "defined by their cells (the scoring rule at project.html:328); no vague descriptor found on re-read.")
row("d1-rubric-calibration", "2.6 rubric calibration: blind scores vs official, within one level",
    "course/modules/M/M4/project.html:348-462 (exemplars A and B)", "PASS",
    "Blind scoring from the rubric alone (project.html:330-343), fresh this round: Exemplar A C1 2, C2 2, C3 2, C4 2, "
    "C5 2 (official 2,2,2,2,2; a strict reading of C5 level 1 'no appendix' gives 1, within one level). Exemplar B "
    "C1 4, C2 4, C3 4, C4 4, C5 3 (official 4,4,4,4,3). Word counts: "
    f"{S}/checks/exemplar_numbers_r9.out (Exemplar A body 90, headings 10; Exemplar B body 682, Summary 70).")
row("d1-rubric-question-bank", "no question bank", "course/modules/M/M4/project.html; plans/M4-build-plan.md section 5.7",
    "PASS", carried("project.html lines 330-343 and plans/M4-build-plan.md") + "the project is not adversarial, so no "
    "question bank is required.")
row("d1-atlas", "atlas entry", "curriculum/meta.yaml:194-276", "PASS",
    carried("curriculum/meta.yaml") + "no atlas milestone for M4 (index.html:37).")
row("d1-studio", "studio entry", "curriculum/01-foundations.yaml:73-76", "PASS",
    carried("curriculum/01-foundations.yaml") + "no studio change.")
row("d1-cites", "Reading citations", "course/modules/M/M4/project.html:482-486; references/references.json", "PASS",
    f"project.html:482-486 unchanged. {S}/gates/verify_refs_offline.out (tools/verify_refs.py --offline): "
    "560 entries, 0 problems. The page cites only blitzstein2019introduction and attributes no passage to it.")
row("d1-cards-c191-grade", "card M4-c191 grade T", "course/modules/M/M4/cards.json (M4-c191)", "PASS",
    carried("the M4-c191 object") + "grade T; its back is Example 2.5 hypotheses plus 'not proved here'.")
row("d1-data", "data references", "course/modules/M/M4/project.html:37, 200, 271-275; grader/instance.py:1-14, 42",
    "PASS", carried("project.html lines 37, 200, 271-275 and grader/instance.py") + "no data file is read; every input "
    "is SIMULATED (project.html:200, instance.py:1-14).")
row("d1-tools-structure", "tools structure", "tools/*.py", "PASS",
    "git diff 2d755599 HEAD -- tools/ is empty (no tool changed since the round-8 pin). check_pages, check_dag, "
    f"check_projects, run_labs, run_graders, mutate_graders, page_smoke all run fresh (see d6 rows, gates in {S}/gates/).")

# ---- 2.6 contract, numbers, grades, prose -----------------------------------------------------------------------
row("d6-2.6-equivalence-float-ceil", "float ceiling 0.99 n versus exact integer index",
    "course/modules/M/M4/grader/reference.py:95-100; project.html:214", "PASS",
    f"Fresh check: math.ceil(0.99*n) equals (99n+99)//100 for every n in 1..2,000,000: {S}/checks/misc_numbers_r9.py, "
    f"line (a) of {S}/checks/misc_numbers_r9.out prints 'none'. The float product is therefore equivalent on every list length the page can "
    "reach, so no float-index mutant is listed. The page's sentence 'avoids a floating-point product' (Lab 2 text) "
    "describes the code, not an observable error.")
row("d6-prose-exemplar-words", "2.9/2.6 prose: exemplar annotation word counts",
    "course/modules/M/M4/project.html:359 (Exemplar A, C5 annotation)", "PASS",
    f"Fresh: {S}/checks/exemplar_numbers_r9.py -> .out: Exemplar A body 90 words, 4 headings 10 words, so 100 with "
    "headings; the annotation at project.html:359 now says '90 words of text (100 with its four headings)'. Matches. "
    "Round-8 values 97/107 are gone.")
row("d6-cards-sample", "round-6 card sample re-checked",
    "course/modules/M/M4/cards.json: M4-c001, c011, c030, c040, c063, c074, c098, c105, c120, c133, c141, c149, c157, c162",
    "PASS", carried("the 14 listed card objects") + "re-read this round against the lesson text: c001 (Def finite "
    "probability space), c011 (Example 3.5, n = 200), c105 (Prop 2.3 hypotheses, L07), c162 (Lab 1 Part C), all match.")
row("d1-2.6-ladder", "2.6 ladder: rung 1 solved, rung 2 instant, rung 3 scope, rung 4 open",
    "course/modules/M/M4/project.html:40-49, 51-192", "PASS",
    "Re-read in full this round. Rung 1 (Lab 1) has numbered steps and an interpretation; rung 2 (Lab 2) is a completion "
    "lab with expected output; rung 3 matches the spec; rung 4 (stretch, project.html:471-478) is open.")
row("d1-2.6-spec-questions", "2.6 spec: a competent student asks no clarifying question",
    "course/modules/M/M4/project.html:194-229", "PASS",
    "Re-read in full this round. Questions I would have had to ask, and where the page answers them: the Student-t "
    "draw order (answered: open, item 5), the sign of a Student-t loss (answered: not tested, line 228), the matched "
    "factor for nu = 2 (answered: ValueError, line 222), the median in the draw-share test (not defined on the page; "
    "the test uses the upper median and the 5-standard-error window tolerates it; noted, not a row).")
row("d1-2.6-autograder-reference", "2.6 autograder: run_graders seeds 0-49 on reference.py",
    "course/modules/M/M4/grader/reference.py", "PASS",
    f"{S}/gates/run_graders_M4_0-49.out: 'run_graders M4: PASS (reference 50/50 seeds, slowest 0.9 s)'. "
    f"Collect-only and per-seed runs: {S}/gates/collect_reference_r9.out (148 collected; seed 0 and 1093: 147 passed, 1 "
    "skipped; seed 1569954299: 148 passed).")
row("d1-2.6-mut-own", "2.6 mutation: verifier-written student-error mutants, all killed",
    "ledgers/M4/mutants/ (r9_04 to r9_07, and every earlier verifier mutant)", "FAIL",
    f"{S}/mutate_M4_0-9_with_new.out: 'mutate_graders M4: FAIL (149/150 killed)'. The survivor is "
    "r9_07_last_pivot_unchecked_for_three_positions.py (a non-positive last pivot of a three-position covariance is "
    "accepted). r9_04, r9_05 and r9_06 are killed. Row d9-2.6-three-position-pivot states the defect.",
    fix="Add a test to grader/test_project.py that calls simulate_losses with a three-position cov whose last pivot is "
        "not positive (e.g. [[1e-4, 0, 0], [0, 1e-4, 0], [0, 0, -1e-4]], and the singular [[1, 0, 1], [0, 1, 1], "
        "[1, 1, 1]] with last pivot -1) and expects ValueError for both families. Then r9_07 is killed.")
row("d1-2.6-mut-existing", "2.6 mutation: existing mutants on seeds 0-9",
    "ledgers/M4/mutants/*.py (146 files before this round)", "PASS",
    f"{S}/mutate_M4_0-9_with_new.out: all 146 mutants that were in the round-8 set are KILLED, with the killing test "
    "named per mutant (listed in the mutants array of this fragment).")
row("d1-2.6-mut-m11", "2.6 mutation: m11 loss sign flipped", "ledgers/M4/mutants/m11_loss_sign_flipped.py", "PASS",
    f"{S}/mutate_M4_0-9_with_new.out: KILLED by test_gaussian_stream_is_frozen_and_the_loss_is_minus_the_weighted_return (seed 0).")
row("d1-2.6-mut-r9_03", "2.6 mutation: r9_03 chi-square reused on alternate draws",
    "ledgers/M4/mutants/r9_03_student_t_chi_square_reused_every_second_draw.py", "PASS",
    f"{S}/mutate_M4_0-9_with_new.out: KILLED by test_student_t_draws_do_not_share_chi_square (seed 0).")
row("d1-2.6-mut-v4_m02", "2.6 mutation: v4_m02 matched factor skipped for small nu",
    "ledgers/M4/mutants/v4_m02_matched_factor_skipped_for_small_nu.py", "PASS",
    f"{S}/mutate_M4_0-9_with_new.out: KILLED by test_student_t_mean_absolute_loss_matches_the_matched_scale (seed 0).")
row("d1-2.6-mut-m17", "2.6 mutation: m17 is an equivalent (conforming) mutant",
    "ledgers/M4/equivalent/m17_student_t_second_seed.py", "PASS",
    carried("ledgers/M4/equivalent/ (git diff 2d755599 HEAD is empty for that folder)") + "m17 changes only the seed of the "
    "Student-t second draw stream, which no conforming test can see; it is kept out of the mutants list.")
row("d1-2.6-alternatives", "2.6 alternatives: correct implementations pass seeds 0-9",
    f"{S}/alts/alt_r9_1_ldl_heap_exact.py, {S}/alts/alt_r9_2_relative_tolerance_floor_half.py, "
    f"{S}/alts/alt_r9_3_upper_factor_minors.py; ledgers/M4/scripts/M4-d-r8/alts/alt1..alt6", "PASS",
    f"{S}/alts_r9.out: reference, alt_r9_1, alt_r9_2, alt_r9_3 each PASS 10/10 seeds (run_alternatives.run_one, "
    f"the suite's own flags). {S}/alts_r8_rerun_r9.out: alt1..alt6 PASS 10/10 each. The three new alternatives use an "
    "LDL^T factor, a heapq order statistic, a relative symmetry tolerance of 1e-12, round-half-up by floor(x + 1/2), "
    "a chi-square as a sum of squared normals, and an upper factor with leading-minor reasoning.")
row("d1-2.6-messages", "2.6 messages: check() and expect_value_error() wording",
    "course/modules/M/M4/grader/test_project.py (all assertion messages, read in full)", "PASS",
    "Read every message this round. Each names the property (e.g. 'cov must be symmetric at every scale', 'quantile_99 "
    "must use the ceiling index ceil(0.99 n)') and none prints a computed value. Concept hints are plain prose.")
row("d1-2.6-count-and-pyodide", "2.6 test count and Pyodide statement",
    "course/modules/M/M4/grader/test_project.py; project.html:203-206", "PASS",
    f"project.html:206 says 148 checks (147 passed + 1 skipped where nu is 3 or 4). Collect-only: 148 tests collected "
    f"({S}/gates/collect_reference_r9.out). page_smoke in-browser: 'All 148 tests pass on seed 377315578' "
    f"({S}/gates/page_smoke_project.out).")
row("d1-2.6-grader-comment-numbers", "2.6 grader comment numbers (test_project.py comments)",
    "course/modules/M/M4/grader/test_project.py:31-47", "PASS",
    f"Fresh: {S}/checks/variance_sweep_r9.out (seed 1093 nu 3 reference relative error 1.0220; per-nu maxima 0.1259, 0.0967, "
    "0.0728, 0.0624; missing-factor failures 347/347, 317/317, 342/343, 288/317) and "
    f"{S}/checks/cross_r9.out (reference max 0.0239; relative errors 0.0677-0.0860 and 0.1406-0.1605 for the two "
    f"mutants at seeds 0-9); {S}/checks/misc_numbers_r9.out line (c): truncation variance 2.7042 and rounding variance 4.0833 "
    "for test_project.py:351-353. Every number in the comment matches.")
row("d1-prose-numbers", "2.2 prose numbers vs measured values",
    "course/modules/M/M4/project.html:203-206, 212, 215, 220, 228", "PASS",
    f"Fresh: {S}/checks/cross_r9.out (3 %: 0 of 50; 5 % minus: 31 of 50; 5 % plus: 19 of 50); "
    f"{S}/checks/chi_lag_r9.out (50, 50, 39, 44 of 50); {S}/checks/chi_lag4_disjoint_r9.out (disjoint lag-4 pairs 0 of 50; "
    f"the chain fails 38 of 50 via r7d_02 in chi_lag_r9.out); {S}/checks/variance_sweep_r9.out (1.0220 at seed 1093). "
    "Lab-printed numbers (213213, 243004, 210946, 1.0447, 2267, 32058, 15.2 %, 1.152) recomputed in "
    f"{S}/checks/exemplar_numbers_r9.out.")
row("d1-prose-scope", "scope words backed by a computation", "course/modules/M/M4/project.html:215, 228; grader/test_project.py:212-216",
    "PASS", f"Fresh: every scope claim in lines 215 and 228 has a computation in {S}/checks/chi_lag_r9.out, "
    f"{S}/checks/chi_lag4_disjoint_r9.out, {S}/checks/cross_r9.out. 'only at nu = 5' matches CROSS_TERM_NU = 5 and the "
    "one cross-term test (test_project.py:169-182). The round-8 FAIL is resolved. The term 'chain' is a separate row.")
row("d1-prose-process-words", "no process words in learner text",
    "course/modules/M/M4/project.html; L01-L04.html; cards.json; grader/test_project.py", "PASS",
    "Fresh grep for verifier, builder, round, slice, ledger, batch, pilot, TODO, placeholder, process: no hit in "
    "project.html or cards.json; test_project.py hits are code only.")
row("d1-prose-banned-phrases", "banned strings (BUILDER_RULES 1.3-1.4)",
    "course/modules/M/M4/project.html; cards.json; grader/*.py", "PASS",
    "Fresh grep for TODO, TBD, lorem, '...', 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', "
    "'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', 'obviously', "
    "'clearly', 'it can be shown', 'roughly half', 'historically', 'about 6%': no hit.")
row("d1-dag", "DAG: prerequisite closure and dfn assignment", "course/modules/M/M4/*.html", "PASS",
    "tools/check_dag.py --all; M4 line: 'check_dag M4: PASS' (gates/check_dag.out). project.html has no data-concept "
    "link, so no concept outside the closure is linked from it.")
row("d1-notation", "notation registry symbols", "notation/notation.json; course/modules/M/M4/project.html", "PASS",
    "Symbols in project.html math (F, F_n, L, Q, R, W, Z, Sigma, nu, ell, n, p, s, t, u, w, x, z, m, i, d, Gamma) "
    "and in cards.json: none is a registered symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) "
    "with a different meaning; \\mathbb{Q} and \\Phi are not used. Macros \\E, \\Var, \\Cov are used as registered.")
row("d1-structure", "project structure and rungs", "course/modules/M/M4/project.html", "PASS",
    "Re-read in full: ladder (project.html:40-49), spec (194-229), budget (231-247), autograder panel (249-253), "
    "local run (255-260), report (262-314), brief, rubric, exemplars, self-assessment (464-468), stretch (471-478), "
    "reading and references (480-491). All present in BUILDER_RULES 5.2-5.4 order.")
row("d1-cards-schema", "card schema", "course/modules/M/M4/cards.json", "PASS",
    f"{S}/checks/cards_scan_r9.out: 230 cards, ids unique, keys {{id, lesson, front, back, grade}} plus basis on 34 "
    "cards; every C card has basis (31 C cards) and three T cards carry a lab basis that matches the L10 key-results "
    "table (c161, c168, c172).")
row("d1-cards-numbers-in-lesson", "card numbers appear in the card's lesson",
    "course/modules/M/M4/cards.json vs L01-L10.html", "PASS",
    f"{S}/checks/cards_scan_r9.out: 'card number tokens absent from the cited lesson: []' over all 230 cards.")
row("d1-cards-labs", "card lab results match the lab output and grades match their basis",
    "course/modules/M/M4/cards.json: M4-c165, M4-c185, M4-c233, M4-c234, M4-c235, M4-c236 (vs L09.html:417 key-results row)",
    "FAIL",
    "The six cards grade the exact Lab 1 Part A values C with basis 'Lab 1, Part A (exact Fraction arithmetic on the die; "
    "no simulation)'. The lesson's key-results row for the same values (L09.html:417) grades them T with the same basis. "
    "Values match the lab output (L09.html:257-261: 0.833333, 0.847994, 0.843496, 0.835793, 0.833926; gaps -0.0080, "
    f"+0.0066, +0.0022, -0.0056, -0.0074 match c185). Cards and lesson disagree on the grade (rule 10). Lab 1 Part A "
    f"is run by the lesson's own program, not SIMULATED and not proved on the page; see {S}/checks/cards_scan_r9.out.",
    fix="Make the six cards and the L09.html:417 row agree. Under BLUEPRINT 3, T means proved on the page, and these are "
        "program-computed exact values, so the lesson row should be C with the Part A basis (then cards c165, c185, c233-c236 "
        "need no change). If the author keeps T, the six cards must be T.")
row("d1-cards-math", "card mathematics re-derived",
    "cards.json: M4-c045, c161, c168, c172, c208, c233; c185; c040, c041, c043, c137, c160, c226", "PASS",
    f"Fresh: {S}/checks/misc_numbers_r9.out line (b): c045 (Bernoulli kurtosis 73/9 and 7/3), c031 (54486.24), "
    f"c168 (0.002128), c172 (2.205308), c161 (0.634510) re-computed in {S}/checks/misc_numbers_r9.out line (b), c208 "
    "(B = AQ = [[0,-2],[1,-1]], BB^T = [[4,2],[2,2]]), c233 and c185 (lab output, L09.html:257-261). "
    "Carried for the rest: those card objects are byte-identical since 2d755599.")
row("d1-cards-lesson-statements", "cards agree with the current lesson text",
    "cards.json: M4-c011, c021, c031, c038, c065, c076, c085, c095, c105, c114, c124, c134, c144, c153, c166, c176, c198, c208, c233",
    "PASS",
    "Fresh read against the lesson text: c011 (L01 Example 3.5, n = 200, pn = 198); c021 (L02 Definition 2.1); c031 (L02 "
    "Example 2.6, 2968750000 and 54486.24); c038 (L03 Proposition 2.3 hypotheses); c065 (L04 Example 2.5, 2/3 and 4/5); "
    "c076 (L05 Definition 2.2); c085 (L06 Proposition 1.2 under Assumption 1); c095 (L06 Proposition 2.6); c105 (L07 "
    "Proposition 2.3); c124 (L08 Proposition 1.3 and Example 1.5); c134 (L09 Proposition 2.3(a)); c144 (L10 Definition "
    "1.1); c153 (L10 Remark 2.2); c166 (L09 Part B line 265: 3.4689, gap 0.0311); c176 (L08 Section 3); c198 (L01 Remark "
    "3.3, left-continuity); c233 (L09 line 258 output). Carried for the rest (objects unchanged since 2d755599).")
row("d1-cards-hypotheses", "card hypotheses carry the proposition's hypotheses",
    "cards.json: M4-c038, c225, c039, c215, c242, c244", "PASS",
    "c038 re-read: 'at least two values, positive weights' matches L03 Proposition 2.3. The others carried (objects unchanged).")
row("d1-cards-duplicates", "no duplicate cards", "course/modules/M/M4/cards.json", "PASS",
    f"{S}/checks/cards_scan_r9.out: no exact or normalised duplicate front or back. {S}/checks/card_front_similarity_r9.py -> .out: "
    "76 pairs with front similarity >= 0.8; each checked by eye and each asks a different fact (e.g. c129 is the WLLN "
    "theorem, c130 its definition-level statement, Definition 1.4). The round-8 duplicate M4-c243 is reworded and "
    "M4-c066 is removed (see d9-cards-c066-c243).")
row("d1-cards-forward-reference", "no use before definition inside the lesson",
    "course/modules/M/M4/L03.html; cards.json", "PASS",
    "L03.html changed only at line 284 (a problem title, now 'A symmetric two-point law with mean 1'); the problem's "
    "values 0 and 2 give mean 1, m2 = 1, m3 = 0, m4 = 1, gamma4 = 1, consistent with the title. No new term is used.")
row("d1-freshness-registry", "registry freshness", "references/references.json; ledgers/M4/scripts/M4-d-r9/gates/verify_refs_offline.out",
    "PASS", f"references/references.json unchanged since 2d755599; {S}/gates/verify_refs_offline.out: 560 entries, 0 problems. "
    "No freshness flag for this slice (the project page cites no working paper).")
row("d1-gates-repo", "gates: ruff, mypy, pytest, configuration", "pyproject.toml; tests/test_labs.py, test_memo_exemplars.py, test_curriculum.py, test_page_checks.py",
    "PASS", f"{S}/gates/ruff_check.out ('All checks passed!'), ruff_format.out ('4 files already formatted'), mypy.out "
    "('Success: no issues found in 385 source files'), pytest_relevant.out, pytest_memo_page.out (28 passed), pytest_labs_M4.out (passed).")
row("d2-2.6-constraints-exceptions", "2.6 constraints and exceptions match the code",
    "course/modules/M/M4/project.html:203-206, 212-220", "PASS",
    "Re-read this round: every condition at project.html:222-224 has a test in grader/test_project.py (matched_scale "
    "tests 110-131; simulate_losses family, nu, n_draws, positions, cov tests 298-549; quantile_99 tests 616-664). "
    "Each named exception type is ValueError and each test demands only conditions the page names.")
row("d1-2.6-constraints-exceptions", "2.6 constraints and exceptions match the code",
    "course/modules/M/M4/project.html:203-206 (Constraints, Grading mode), :212-220", "PASS",
    "Same evidence as d2-2.6-constraints-exceptions. Also: the page says the Student-t variance is skipped at nu 3 or 4 "
    "(line 206) and the test skips at nu < 5 (test_project.py:159-160).")
row("d3-2.6-mut-new-student-error", "round-5/7 student-error mutants are killed",
    "ledgers/M4/mutants/v9_01..v9_04, d5_01, r7d_01..r7d_04", "PASS",
    f"{S}/mutate_M4_0-9_with_new.out: all KILLED (v9_01..v9_04, d5_01, r7d_01..r7d_04).")
row("d1-2.6-contract-notes-chi-claim", "contract notes: chi-square sharing counts",
    "course/modules/M/M4/project.html:215, 228; grader/test_project.py:207-216", "PASS",
    f"Every count in the contract notes is re-run this round: {S}/checks/chi_lag_r9.out (2k/2k+1 50/50; 4j/4j+2 50/50; "
    f"6j/6j+3 39/50; even-indexed one-variable 44/50; r7d_02 chain 38 of 50 seeds), {S}/checks/chi_lag4_disjoint_r9.out "
    f"(disjoint lag-4 pairs 0/50), {S}/checks/cross_r9.out (cross term 3 %: 0/50; 5 % minus 31/50; 5 % plus 19/50). "
    "The round-8 FAIL is resolved.")
row("d1-2.6-mut-pairwise-survivor", "pairwise survivor d5_01 killed", "ledgers/M4/mutants/d5_01_chi_square_shared_by_draws_two_apart.py",
    "PASS", f"{S}/mutate_M4_0-9_with_new.out: KILLED by test_student_t_draws_do_not_share_chi_square (seed 0).")
row("d6-2.6-mut-integer-division-chi", "r6d_02 integer division chi shape",
    "ledgers/M4/mutants/r6d_02_integer_division_chi_shape.py", "PASS", f"{S}/mutate_M4_0-9_with_new.out: KILLED (seed 0).")
row("d6-2.6-mut-pivot-tolerance", "r6d_01 pivot tolerance 1e-15 (round-6 survivor)",
    "ledgers/M4/mutants/r6d_01_pivot_tolerance_1e15_rejects_tiny_variance.py; grader/test_project.py:541-", "PASS",
    f"{S}/mutate_M4_0-9_with_new.out: KILLED. The tiny-variance tests (test_project.py:552-613) reject it.")
row("d6-2.6-mut-lag3-sharing", "r6d_03 lag-three chi sharing (round-6 survivor)",
    "ledgers/M4/mutants/r6d_03_chi_square_shared_by_draws_six_apart_lag_three.py; project.html:215, :228", "PASS",
    f"{S}/mutate_M4_0-9_with_new.out: KILLED (seed 0). chi_lag_r9.out: the lag-3 sharing fails 39 of 50 seeds.")
row("d1-lab-project-1", "project lab 1 (rung 1 worked example)",
    "course/modules/M/M4/project.html:55-145; tests/labs/M4/lab-M4-project-1.py", "PASS",
    f"{S}/checks/labs_project_r9.out: page code == twin (after strip); twin runs under python -I -W error with exit 0 and "
    "no stderr; expected block == twin stdout (8 lines). Numbers recomputed: target 8400000000.0, 0.6, 19800, "
    "1.0447 (4.47 % above 1 within 5 %), 243004/210946 = 1.152.")
row("d1-lab-project-2", "project lab 2 (rung 2 completion)",
    "course/modules/M/M4/project.html:147-191; tests/labs/M4/lab-M4-project-2.py", "PASS",
    f"{S}/checks/labs_project_r9.out: the page code differs from the twin only at the two blanks (___ at project.html:164 "
    "and :171 versus (nu - 2) / nu and (99 * n + 99) // 100 in the twin): expected for a completion lab. Twin exits 0 "
    "under python -I -W error; expected block equals its output (5 lines).")
row("d1-lab-project-3", "project lab 3 (rung 4 stretch or interpretation)",
    "course/modules/M/M4/project.html:266-314; tests/labs/M4/lab-M4-project-3.py", "PASS",
    f"{S}/checks/labs_project_r9.out: page code == twin; twin exits 0 under python -I -W error; expected block equals output "
    "(11 lines). Recomputed: sd 91651.514, z 2.326348, parametric 99% loss 213213.30 -> 213213, index rows 99/99, 100/99, 19788/19787.")
row("d6-gate-mutate-m4", "gate: tools/mutate_graders.py --unit M4 --seeds 0-9 exits 0",
    "tools/mutate_graders.py; ledgers/M4/mutants/", "FAIL",
    f"{GATE}: 'mutate_graders M4: FAIL (149/150 killed)', EXIT 1. Surviving: r9_07_last_pivot_unchecked_for_three_positions.py. "
    f"{S}/probe/run_probe_r9.out confirms it survives all seeds 0-9. The earlier round-9 run without the new mutants "
    f"({S}/mutate_M4_0-9.out) was 146/146 PASS.",
    fix="Add a three-position non-positive-pivot test (see d1-2.6-mut-own fix). Then rerun tools/mutate_graders.py --unit M4 "
        "--seeds 0-9 and require EXIT 0.")
row("d6-gate-unit-checks", "gate: check_pages, check_dag, check_projects", "tools/check_*.py --unit M4", "PASS",
    f"{S}/gates/check_pages_M4.out 'check_pages M4: PASS'; check_dag.out 'check_dag M4: PASS'; check_projects.out "
    "'check_projects M4: PASS' (all EXIT 0).")
row("d6-gate-labs", "gate: run_labs M4", "tests/labs/M4; course/modules/M/M4/*.html", "PASS",
    f"{S}/gates/run_labs_M4.out: 'run_labs M4: PASS (13/13)' EXIT 0.")
row("d6-gate-grader-reference", "gate: run_graders M4 seeds 0-49", "course/modules/M/M4/grader/reference.py", "PASS",
    f"{S}/gates/run_graders_M4_0-49.out: 'run_graders M4: PASS (reference 50/50 seeds, slowest 0.9 s)' EXIT 0.")
row("d6-gate-lint-types", "gate: ruff and mypy", "course/modules/M/M4/grader; tests/labs/M4; tools; tests", "PASS",
    f"{S}/gates/ruff_check.out 'All checks passed!'; ruff_format.out '4 files already formatted'; mypy.out 'Success: no issues "
    "found in 385 source files' (mypy --no-incremental, strict per pyproject.toml).")
row("d6-gate-tests", "gate: relevant pytest", "tests/test_labs.py, test_memo_exemplars.py, test_curriculum.py, test_page_checks.py",
    "PASS", f"{S}/gates/pytest_relevant.out (test_curriculum -k M4/project/grader: all passed), pytest_memo_page.out (28 "
    f"passed), pytest_labs_M4.out (passed). EXIT 0 each.")
row("d6-gate-refs", "gate: verify_refs --offline", "tools/verify_refs.py", "PASS",
    f"{S}/gates/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems'.")
row("d6-gate-page-smoke", "gate: page_smoke for the project page (alone)", "course/modules/M/M4/project.html", "PASS",
    f"{S}/gates/page_smoke_project.out: 'in-browser grader: All 148 tests pass on seed 377315578. (2.3 s)'; "
    "'page_smoke modules/M/M4/project.html: PASS'; 'page_smoke M4: PASS'; EXIT 0. Labs 1-3 ran in under 0.2 s each.")
row("d6-2.6-alt-root-set", "alternatives: the other alternative roots",
    "ledgers/M4/scripts/M4-d-r8/alts/; ledgers/M4/scripts/M4-d-r9/alts/", "PASS",
    "Both sets run on seeds 0-9 and pass (see d1-2.6-alternatives).")
row("d7-2.6-cross-term-threshold", "cross-term tolerance claim (the threshold)",
    "course/modules/M/M4/project.html:228; grader/test_project.py:43-47", "PASS",
    f"{S}/checks/cross_r9.out: reference max 0.0239 over seeds 0-49 (< 0.05); r8_03 mutant 0.0677-0.0860 and r9_02 0.1406-0.1605 "
    "over seeds 0-9 (both > 0.05). The threshold claim holds.")
row("d7-2.6-negation-claim", "negating every position negates every loss",
    "course/modules/M/M4/grader/test_project.py (test_a_short_position_is_valid_and_reverses_its_loss); project.html:212, :220",
    "PASS", "Read this round: 300 draws per family, two positions, the test checks flipped == -long and mixed_flipped == -mixed. "
    "Both family cases are parametrized, consistent with project.html:212 and :220.")
row("d7-2.6-tiny-variance-claims", "tiny-variance claims in the new tests",
    "course/modules/M/M4/grader/test_project.py (tiny-variance and tiny-scale tests)", "PASS",
    f"Read this round. The variance 1e-14 one-position loss variance is (1e13)^2 x 1e-14 = 1e12 (test comment, verified by "
    f"arithmetic). The new symmetry test at 1e-14 (test_covariance_must_be_symmetric_at_a_tiny_scale) is killed by "
    f"r8d_01 in {GATE}.")
row("d7-L01-L04-prose", "changed prose in L01-L04",
    "course/modules/M/M4/L01.html:278, 326, 376; L02.html:51, 94; L03.html:284; L04.html:543; index.html:37, 140", "PASS",
    "Fresh read of every changed sentence. L01:278: a floor of pn returns a lower index when pn is not an integer (true). "
    "L01:326: 40 x 0.901 = 36.04, ceiling 37; 40 x 0.9 = 36, ceiling 36 (checked). L01:376: consistent with Definition 3.1 "
    "and Proposition 3.2. L02:94: a density is nonnegative with integral 1 (correct definition). L04:543 footer consistent "
    "with the page's exact results. Unchanged lines carried from round 8.")
row("d7-L03-numerics", "L03 numerics and numbering after the renumbering",
    "course/modules/M/M4/L03.html (Sections 1-4, Problems, Misconceptions)", "PASS",
    "Only the problem title at line 284 changed; its solution (mech-2) is re-checked: mean 1, m2 1, m3 0, m4 1, gamma4 1, "
    "equal to the Proposition 2.5 equality case. Other numerics carried from round 8.")
row("d7-cards-exact-lab-grade", "grade T only for values the page proves",
    "course/modules/M/M4/cards.json: M4-c165, M4-c185, M4-c233, M4-c234, M4-c235, M4-c236", "FAIL",
    "Same defect as d1-cards-labs, seen from the grade side: these six cards are C while L09.html:417 grades the same "
    "exact values T. Round 9 changed M4-c165 from T to C, which moved it onto the C side without changing the lesson. "
    "The six are not all proved on the page (they are program output).",
    fix="Align the six cards with the lesson row (see d1-cards-labs fix). Preferred: the lesson row becomes C with the "
        "Part A basis, since T is for results proved on the page.")
row("d8-2.6-symmetry-tiny-scale", "2.6 autograder: symmetry is tested at every scale",
    "course/modules/M/M4/grader/test_project.py:463-472; ledgers/M4/mutants/r8d_01_symmetry_checked_to_absolute_tolerance_1e9.py",
    "PASS", f"New test test_covariance_must_be_symmetric_at_a_tiny_scale (test_project.py:463-472) is in the file; "
    f"{GATE}: r8d_01 KILLED. The round-8 survivor is killed.")
row("d8-2.6-mut-r8d-02", "2.6 mutation: r8d_02 Gaussian stream reseeded per draw",
    "ledgers/M4/mutants/r8d_02_gaussian_stream_reseeded_per_draw.py", "PASS", f"{GATE}: KILLED (seed 0).")
row("d8-2.6-mut-r8d-03", "2.6 mutation: r8d_03 positions read in reverse order",
    "ledgers/M4/mutants/r8d_03_positions_read_in_reverse_order.py", "PASS", f"{GATE}: KILLED (seed 0).")
row("d8-2.6-mut-r8d-04", "2.6 mutation: r8d_04 Gaussian draws via normalvariate",
    "ledgers/M4/mutants/r8d_04_gaussian_draws_via_normalvariate.py", "PASS", f"{GATE}: KILLED (seed 0).")
row("d8-2.6-alt6-chi-order", "over-constraint check: Student-t draw order is open (Conventions item 5)",
    "ledgers/M4/scripts/M4-d-r8/alts/alt6_chi_before_normals.py", "PASS",
    f"{S}/alts_r8_rerun_r9.out: alt6_chi_before_normals.py PASS 10/10 seeds 0-9.")
row("d8-2.6-lab-counts", "chi-square share counts and lag tests (project.html:228; test_project.py:207-228)",
    "course/modules/M/M4/project.html:228; grader/test_project.py:207-228", "PASS",
    f"{S}/checks/chi_lag_r9.out re-run (50/50, 50/50, 39/50, 44/50, and the chain 38/50). Matches the page.")
row("d8-cards-changed-and-new", "changed and new cards: c023, c081, c140, c195, c198, c218, c241, c242, c244",
    "course/modules/M/M4/cards.json", "PASS",
    carried("these card objects") + "each object is byte-identical to 2d755599; the round-9 changes are M4-c066 (removed), "
    "M4-c165 (grade) and M4-c243 (front and back), covered by their own rows.")
row("d8-2.6-variance-claims-lines-31-39", "grader comment numbers, lines 31-39 (tolerance and sweep claims)",
    "course/modules/M/M4/grader/test_project.py:31-39", "PASS",
    f"{S}/checks/variance_sweep_r9.out re-run: 1.0220 at seed 1093; maxima 0.1259 (nu 5), 0.0967 (6), 0.0728 (7), 0.0624 (8); "
    "missing-factor counts 347/347, 317/317, 342/343, 288/317; 0.30/0.1259 = 2.38.")

# ---- round-9 rows --------------------------------------------------------------------------------------------------
row("d9-2.6-three-position-pivot",
    "2.6 conditions: a three-position covariance that is not positive definite raises ValueError",
    "course/modules/M/M4/project.html:220, 223; grader/test_project.py (no three-position positive-definiteness test); "
    "ledgers/M4/mutants/r9_07_last_pivot_unchecked_for_three_positions.py", "FAIL",
    "project.html:220 says 'These are the conditions that raise ValueError, and the suite checks each one', and line 223 "
    "lists 'cov ... is not positive definite'. The suite tests positive definiteness only for one and two positions "
    "(test_project.py:496-549, 2 x 2 matrices; the 3 x 3 tests at 430-460 test shape and symmetry). The reference rejects the "
    "proposed cases (checks/three_position_reference_r9.out). Mutant r9_07 "
    "(last Cholesky pivot unchecked for three positions) survives all seeds 0-9: "
    f"{S}/probe/run_probe_r9.out and {GATE}.",
    fix="Add to grader/test_project.py a parametrized test over both families: simulate_losses([1000, 1000, 1000], cov3, "
        "10, SEED, family, nu) for cov3 = [[1e-4, 0, 0], [0, 1e-4, 0], [0, 0, -1e-4]] and "
        "cov3 = [[1, 0, 1], [0, 1, 1], [1, 1, 1]] (last pivot -1), each expecting ValueError with a message that names "
        "positive definiteness. The reference raises for both.")
row("d9-2.6-mut-new-r9_04_05_06", "verifier round-9 mutants r9_04 to r9_06 are killed",
    "ledgers/M4/mutants/r9_04_gaussian_stream_skips_first_normal.py; r9_05_loss_floored_not_rounded.py; "
    "r9_06_matched_factor_squared_in_t_scale.py", "PASS",
    f"{GATE}: r9_04 KILLED by test_gaussian_stream_is_frozen_and_the_loss_is_minus_the_weighted_return (seed 0); r9_05 KILLED "
    "by test_a_short_position_is_valid_and_reverses_its_loss[gaussian-None] (seed 0); r9_06 KILLED by "
    "test_student_t_cross_term_matches_matched_covariance (seed 0).")
row("d9-2.6-student-t-sign-untested", "Student-t loss sign: the page says it is not tested, and a flip survives",
    "course/modules/M/M4/project.html:228 ('The suite does not test the sign of the Student-t losses'); "
    f"{S}/probe/probe_student_t_sign_flipped.py (not a mutant; not in ledgers/M4/mutants)", "PASS",
    f"{S}/probe/run_probe_r9.out: 'probe_student_t_sign_flipped.py survives all of seeds 0-9'. This matches the page's "
    "stated limit, so it is not a grader finding and the probe is kept out of the mutants list.")
row("d9-2.6-chain-term", "terms used before definition: 'chain'",
    "course/modules/M/M4/project.html:215 (uses 'a chain that links many draws at lag four'); defined at project.html:228",
    "FAIL",
    "'chain' is first used in Conventions item 5 (line 215) and only defined inline in the contract notes (line 228: "
    "'draws 4j and 4j + 4 sharing one variable'). Rule 5 (terms before definition) is not met.",
    fix="At project.html:215 replace 'a chain that links many draws at lag four' with 'draws 4j and 4j + 4 sharing one "
        "variable (a chain of sharings at lag four)'. The number 38 of 50 is unchanged (chi_lag_r9.out).")
row("d9-2.6-hours-own-estimate", "2.6 hours: own estimate within 30 % of 30",
    "course/modules/M/M4/project.html:234-245", "PASS",
    "My estimate: rung 1 1.5 h, rung 2 1 h, simulator and conditions 8 h, proof appendix A1-A4 6 h, report with run_report "
    "and self-assessment 4 h, self-check 2 h = 22.5 h. |22.5 - 30| / 30 = 25 %, inside 30 %.")
row("d9-cards-c066-c243", "removed M4-c066 and reworded M4-c243",
    "course/modules/M/M4/cards.json (c066 removed; c243 front and back changed)", "PASS",
    f"{S}/checks/cards_scan_r9.out: removed ids ['M4-c066']; changed c243 front 'In which units is the standard deviation of "
    "X measured?' (was the same front as M4-c067, now unique) with back matching L02 Definition 2.1 ('variance is in "
    "squared units ... standard deviation is in the units of X'). No card refers to M4-c066 (grep of course/ is empty).")
row("d9-index-hub-lines", "hub changes: index.html:37 and :140",
    "course/modules/M/M4/index.html:37, 140", "PASS",
    "Line 37 (data sentence) and line 140 (skill check explanation): the scale rule is stated as a hypothesis, "
    "Lesson 2 Proposition 2.3 is scale and shift for finite laws (L02.html:115-116), Var(V) = 5/3 from Lesson 6 "
    "Proposition 2.6, and 1/(5/3) = 0.6 (arithmetic verified).")
row("d9-labs-page-vs-twin-lab2", "completion lab: page code versus twin",
    "course/modules/M/M4/project.html:147-191", "PASS",
    "The completion lab's twin holds the solved expressions; the page holds ___ at the two blanks. This is the designed "
    "difference (labs_project_r9.out prints the diff). Not a finding.")

counts = {"PASS": sum(1 for r in rows if r["status"] == "PASS"), "FAIL": sum(1 for r in rows if r["status"] == "FAIL")}
frag = {
    "unit": "M4",
    "slice": "d",
    "round": 9,
    "verifier": "independent verifier (Haiku), unit M4, slice d, round 9; not a builder of M4",
    "pin": "1e272e5a641f18412703b37778a44db6f7391a69 (detached HEAD in the checkout)",
    "base": "2d755599 (round-8 pin). Delta for slice d: course/modules/M/M4/{project.html 206, 215, 228, 359; "
            "grader/test_project.py (comments 31-47, tests 212-216, new tiny-scale test 463-472, quantile messages 629-650); "
            "cards.json (c066 removed, c165 T->C, c243 reworded); L01-L04 and index.html changed sentences}; "
            "ledgers/M4/mutants r9_04..r9_07 added",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD9-M4-d",
    "scratch": f"{S}/ (all scripts, outputs and probes in the checkout)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [{"name": m["name"], "description": m["description"], "killed_by": m["killed_by"]} for m in mutants],
    "registry_flags": [],
    "freshness_flags": [],
    "gate_scope": "project.html, grader/ (reference, instance, starter, test_project), project labs 1-3, cards.json, "
                  "mutants (all 150), alternatives (9 implementations, seeds 0-9), check_pages/dag/projects, run_labs, "
                  "run_graders 0-49, page_smoke for the project page, ruff, mypy, relevant pytest, verify_refs --offline",
    "notes": [
        "Round-8 FAIL rows re-verified and now PASS: d6-prose-exemplar-words, d1-prose-scope, d1-2.6-contract-notes-chi-claim, "
        "d1-cards-duplicates, d8-2.6-symmetry-tiny-scale.",
        "Round-8 FAIL rows still FAIL: d1-2.6-mut-own and d6-gate-mutate-m4 (new survivor r9_07), d1-cards-labs and "
        "d7-cards-exact-lab-grade (grade mismatch, now C on the cards against T on L09.html:417).",
        "New FAIL rows: d9-2.6-three-position-pivot, d9-2.6-chain-term.",
        "Exemplar blind scoring: A 2,2,2,2,2 (C5 could read 1 under a strict 'no appendix' reading; within one level either "
        "way), B 4,4,4,4,3.",
        "The median in the draw-share test (test_project.py:220) is the upper median for an even count (n = 40000); the page "
        "does not define it. The 5-standard-error window makes the choice immaterial; noted, not a row.",
        "Not checked: lesson-level proofs of L01-L10 beyond the changed sentences (other slices); the full text of every "
        "other lesson card beyond the 23-card sample plus changed cards; the Pyodide run of the 3 alternatives (local pytest "
        "only); the original PDF/online source of blitzstein2019introduction (not read, and the page attributes nothing to it).",
    ],
    "summary": (f"Slice d round 9: {len(rows)} rows, {counts['PASS']} PASS, {counts['FAIL']} FAIL. Mutants: 149/150 killed; "
                "r9_07 survives. Non-PASS: d1-2.6-mut-own, d1-cards-labs, d6-gate-mutate-m4, d7-cards-exact-lab-grade, "
                "d9-2.6-three-position-pivot, d9-2.6-chain-term."),
}
out = ROOT / "ledgers/M4/M4-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), counts)
