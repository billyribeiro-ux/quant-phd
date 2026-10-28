"""Assemble the round-5 M4-d fragment (ledgers/M4/M4-d.json) from the outputs stored in this folder.

Run from the checkout root: .venv/bin/python -I ledgers/M4/scripts/M4-d-r5/build_fragment_r5.py
Mutant rows are parsed from tools/mutate_graders.py output (mutate_70_seeds0-99_first_run.txt for the 70 mutants
present before the round-5 additions; the three v5 lines are copied from the final run in mutate_all73 output).
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

MUT = {}
for line in (HERE / "mutate_70_seeds0-99_first_run.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if m:
        status, name, desc, killed = m.groups()
        MUT[name[:-3]] = {"id": name[:-3], "description": desc, "killed_by": killed if status == "KILLED" else None,
                          "survived": status == "SURVIVED"}
for line in (HERE / "mutate_all73_seeds0-99_final.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(KILLED|SURVIVED) (v5_\S+?)\.py: (.*) -> (.*)$", line)
    if m:
        status, name, desc, killed = m.groups()
        MUT[name] = {"id": name, "description": desc, "killed_by": killed if status == "KILLED" else None,
                     "survived": status == "SURVIVED"}
mutants = [MUT[k] for k in sorted(MUT)]
for m in mutants:
    if m.get("survived") is None or not m.get("description"):
        raise SystemExit(f"mutant record incomplete: {m}")

R = "ledgers/M4/scripts/M4-d-r5/"
SWEEP = R + "sweep_0_2000_output.txt"
MUTATE = R + "mutate_all73_seeds0-99_final.txt"
ROWS = [
    # ---- commands and gates (re-run on 09b8751) ----
    dict(id="m4d-cmd-check-projects", check="Project gate for M4 (rubric, grader panel, ladder, hours, labs)",
         location="course/modules/M/M4/project.html; tools/check_projects.py",
         status="PASS", evidence=f"`.venv/bin/python tools/check_projects.py --unit M4` -> 'check_projects M4: PASS' ({R}check_projects_M4.txt)."),
    dict(id="m4d-cmd-check-pages-dag", check="Page gate and concept DAG for M4",
         location="course/modules/M/M4/*.html; tools/check_pages.py; tools/check_dag.py",
         status="PASS", evidence=f"`check_pages.py --unit M4` -> PASS; `check_dag.py --unit M4` -> PASS ({R}check_pages_M4.txt, {R}check_dag_M4.txt)."),
    dict(id="m4d-cmd-run-labs", check="Every M4 lab twin runs under python -I -W error and matches its page output",
         location="tests/labs/M4/*.py; course/modules/M/M4/*.html",
         status="PASS", evidence=f"`tools/run_labs.py --unit M4` -> 'run_labs M4: PASS (13/13)' ({R}run_labs_M4.txt)."),
    dict(id="m4d-lab-project-embedded-output", check="Project Labs 1-3 printed output equals the embedded expected blocks",
         location="course/modules/M/M4/project.html lab-M4-project-1..3; tests/labs/M4/lab-M4-project-*.py",
         status="PASS", evidence="run_labs PASS (13/13) includes the three project labs; Lab 1 printed 8400000000.0, 210946, 243004, 1.0017, 1.0447, 1.6667 and Lab 3 printed 213213 (run output via run_labs)."),
    dict(id="m4d-cmd-collect-count", check="Test count on the page equals the real collect-only count",
         location="course/modules/M/M4/project.html (Grading mode); grader/test_project.py",
         status="PASS", evidence="`pytest --collect-only -q test_project.py` in a workspace with reference.py as tail_risk.py: '124 tests collected'; page says 124 checks."),
    dict(id="m4d-cmd-run-graders-reference", check="Reference solution passes the suite on seeds 0-49",
         location="course/modules/M/M4/grader/reference.py; tools/run_graders.py",
         status="PASS", evidence=f"`tools/run_graders.py --unit M4 --seeds 0-49` -> 'run_graders M4: PASS (reference 50/50 seeds, slowest 0.3 s)' ({R}run_graders_M4_0-49.txt)."),
    dict(id="m4d-cmd-starter-fails", check="Starter does not pass the suite (it raises NotImplementedError)",
         location="course/modules/M/M4/grader/starter.py",
         status="PASS", evidence="Suite on starter.py as tail_risk.py, QF_SEED=0: '122 failed, 1 passed, 1 skipped'; the failures are NotImplementedError."),
    dict(id="m4d-cmd-lint-types", check="ruff and mypy on the slice",
         location="course/modules/M/M4/grader/*.py; tests/labs/M4/*.py",
         status="PASS", evidence="`ruff check .` -> 'All checks passed!'; `ruff format --check` on grader and labs -> formatted; `mypy --no-incremental` -> 'Success: no issues found in 255 source files' (exit 0)."),
    dict(id="m4d-cmd-page-smoke", check="Project page loads and runs in Chromium with no console errors or external requests",
         location="course/modules/M/M4/project.html; tools/page_smoke.py",
         status="PASS", evidence=f"`tools/page_smoke.py --unit M4 --pages project.html --skip-sweep` -> 'page_smoke M4: PASS' ({R}page_smoke_project.txt)."),
    dict(id="m4d-cmd-verify-refs", check="Registry integrity and the live entry for M4",
         location="references/references.json; tools/verify_refs.py",
         status="PASS", evidence=f"`verify_refs.py --unit M4` -> 'live re-verification of M4: 1 of 560 entries, 0 problems'; `verify_refs.py --offline` -> '560 entries, 0 problems' ({R}verify_refs_live_M4.txt, {R}verify_refs_offline.txt)."),
    # ---- grader numbers and claims ----
    dict(id="m4d-grader-tolerance-sweep-numbers", check="Reference's largest variance error per nu (seeds 0-1999) and the cited maxima",
         location="grader/test_project.py lines 31-39",
         status="PASS", evidence=f"Own sweep ({R}sweep_r5.py, output {SWEEP}): max relative error 0.1259 (nu 5), 0.0967 (nu 6), 0.0728 (nu 7), 0.0624 (nu 8); 0.30/0.1259 = 2.38 ('about 2.4'). Counts per nu: 347, 317, 343, 317."),
    dict(id="m4d-grader-missing-factor-claim", check="Missing matched factor is caught on all but a stated number of seeds",
         location="grader/test_project.py lines 36-39",
         status="PASS", evidence=f"Same sweep, mutant with scale sqrt(nu/W) (no matched factor): fails the 0.30 tolerance on 347/347 (nu 5), 317/317 (nu 6), 342/343 (nu 7), 288/317 (nu 8). All four counts equal the comment."),
    dict(id="m4d-grader-seed-1093-nu3", check="Reference at seed 1093 with nu = 3 misses the variance target",
         location="grader/test_project.py line 33",
         status="PASS", evidence=f"Sweep line '1093 3 12011 3 1.022030 5.066089': reference relative error 1.022 at nu = 3; the check is skipped at nu = 3 by design (line 42)."),
    dict(id="m4d-grader-gaussian-tolerance", check="Gaussian variance tolerance 0.10 does not reject a correct solution",
         location="grader/test_project.py line 40",
         status="PASS", evidence="Reference and the five builder alternatives and three verifier alternatives pass seeds 0-49 (and alt_r5_a/b/c seeds 0-149); the Gaussian check has no comment claim beyond that."),
    dict(id="m4d-grader-alt-verifier", check="Three verifier-written alternative implementations pass the suite",
         location="ledgers/M4/scripts/M4-d-r5/alt_r5_a.py, alt_r5_b.py, alt_r5_c.py",
         status="PASS", evidence=f"`run_alt_r5.py 0 50` and `run_alt_r5.py 50 150`: all three PASS ({R}alt_seeds0-49.txt; runner output for seeds 50-149). a: Box-Muller normals and chi-square as sum of squares; b: outer-product Cholesky, relative symmetry tolerance 1e-12, heap order statistic; c: gammavariate, factor applied after the draw."),
    dict(id="m4d-grader-alt-builder", check="Builder alternatives alt_1..alt_5 pass the suite",
         location="ledgers/M4/scripts/alt_1.py .. alt_5.py",
         status="PASS", evidence="Round-5 run: alt_1 PASS seeds 0-149; alt_2..alt_5 PASS seeds 0-49 (python -I, run_alt_r5 runner, output in this session)."),
    dict(id="m4d-grader-overconstraint-nu3", check="No test rejects a correct solution at nu = 3 or 4",
         location="grader/test_project.py lines 102-123, 215-217",
         status="PASS", evidence="All five alternatives (builder and verifier) pass seeds 0-49; the nu = 3 tests check only matched_scale(3) and a length, consistent with the page."),
    dict(id="m4d-grader-mutants-existing", check="Every existing mutant is killed or its survival is disclosed by the page",
         location="ledgers/M4/mutants/*.py (73 files)",
         status="PASS", evidence=f"`tools/mutate_graders.py --unit M4 --seeds 0-99` -> 'mutate_graders M4: FAIL (70/73 killed)'; survivors m11_loss_sign_flipped, m17_student_t_second_seed, v4_m02_matched_factor_skipped_for_small_nu. Each is disclosed: sign (project.html Constraints item 2 and 'What the suite does not test'), matched factor at nu 3 and 4 ('does not check the matched factor inside simulate_losses at those values'), and the stream/seed choice (conventions item 5). Summary: no undisclosed survivor. Run output {MUTATE}."),
    dict(id="m4d-grader-new-mutants", check="At least three new student-error mutants written by this verifier, and they are killed",
         location="ledgers/M4/mutants/v5_m01..v5_m03; ledgers/M4/scripts/M4-d-r5/make_v5_mutants.py",
         status="PASS", evidence=f"v5_m01 (matched factor not square-rooted) killed by test_student_t_loss_variance_matches_matched_covariance (seed 5); v5_m02 (positions reversed) killed by test_gaussian_loss_variance_matches_portfolio_covariance (seed 0); v5_m03 (quantile index rounded) killed by test_quantile_99_convention_on_small_lists (seed 0). {MUTATE}."),
    dict(id="m4d-grader-equivalent-mutant", check="Float ceil(0.99 n) equals the exact index (equivalent-mutant proof)",
         location="ledgers/M4/scripts/M4-d-r3/make_variants.py",
         status="UNVERIFIABLE", evidence="Scratch check: math.ceil(0.99*n) == (99n+99)//100 for n = 1..100000 and for the instance draw counts (scratch one-liner this session, not saved: 0 differences). No proof for all n; the mutant is not in the mutant list and the grader does not depend on it.",
         fix="Prove the equivalence for all n (or drop the row: the equivalence is not used by the suite)."),
    dict(id="m4d-grader-sign-mutant", check="The sign of the loss is untested and the page says so",
         location="course/modules/M/M4/project.html Constraints and 'What the suite does not test'; mutant m11_loss_sign_flipped",
         status="PASS", evidence="m11 survives seeds 0-99 (run output above); project.html Constraints lists the sign as not graded (item 2) and 'What the suite does not test' says the suite does not test the sign."),
    dict(id="m4d-grader-seed-sharing-mutant", check="Student-t drawn from seed+1 (m17) is accepted under the disclosed stream/seed gap",
         location="mutant m17_student_t_second_seed; project.html conventions item 5",
         status="PASS", evidence="m17 survives seeds 0-99. The page says the stream order of each family is not fixed and not checked (conventions item 5); the spec asks only that each run be reproducible from its seed. Accepted."),
    dict(id="m4d-grader-one-chi-square-per-asset", check="One chi-square per asset (n02) is killed",
         location="ledgers/M4/mutants/n02_one_chi_square_per_asset.py",
         status="PASS", evidence=f"Not in the SURVIVED list of {MUTATE}; killed in the 0-99 run."),
    dict(id="m4d-grader-rounding-comment-number", check="Grader comment numbers for the rounding tests: 4 + 1/12 (about 4.08) and about 2.7 for truncation",
         location="grader/test_project.py lines 229-237",
         status="PASS", evidence="r5_numeric_and_text_checks_output.txt: variance of round(loss) = 4.0835 (vs 4 + 1/12 = 4.0833), variance of trunc(loss) = 2.7043 on 2,000,000 draws of N(0, 4)."),
    dict(id="m4d-grader-conditions-coverage", check="Every named condition in project.html has a test; each ValueError test is for a named condition",
         location="course/modules/M/M4/project.html 'Conditions the functions must check'; grader/test_project.py",
         status="PASS", evidence="Read every test (124 collected). matched_scale: nu<=2, non-int (float, bool, str, None) -> tests at lines 108-123. simulate_losses: family, nu/None, n_draws (<=0 and non-int), positions (empty, float, bool), cov (size, symmetry, PD) -> tests lines 177-401. quantile_99: empty and non-int -> lines 440-446. Each expect_value_error is for a condition the page names."),
    dict(id="m4d-grader-messages-no-values", check="Failure messages never show a computed value or the answer",
         location="grader/test_project.py (every check() / expect_value_error message)",
         status="PASS", evidence="Read all messages: each names a property or condition; none formats a sample value."),
    dict(id="m4d-grader-instance-spec", check="instance.py ranges and cov construction match the docstring and the page",
         location="course/modules/M/M4/grader/instance.py; project.html Inputs",
         status="PASS", evidence="r5_numeric_and_text_checks_output.txt: 0 violations over seeds 0-1999 of positions in [100000, 5000000] cents, nu in 3..8, draws in the 6-value set (none a multiple of 100, max 19987), cov exactly symmetric; Cholesky pivots positive for all 2000 seeds."),
    dict(id="m4d-grader-new-mutants-r4", check="Round-4 student-error mutants v4_m01..v4_m03 are handled",
         location="ledgers/M4/mutants/v4_m01..v4_m03",
         status="PASS", evidence=f"v4_m01 killed (per-position rounding; killed in 0-99 run), v4_m03 killed (sign folded), v4_m02 survives and is disclosed (see m4d-r4-grader-v4-matched-factor-nu34). {MUTATE}."),
    # ---- project page prose ----
    dict(id="m4d-proj-matrix-and-moments", check="Matrix facts and the A1-A3 moment claims are correct",
         location="course/modules/M/M4/project.html Conventions, Lab 1 hypothesis, Appendix A1-A3 in exemplar B",
         status="PASS", evidence="Recomputed: w'Sigma w = 8.4e9; (nu-2)/nu = 0.6 at nu = 5; E[W^-1] = 1/(nu-2); E[W^-2] = 1/((nu-2)(nu-4)); Var(t) = nu/(nu-2); integrability of w^(nu/2-1) e^(-w/2) near 0 gives the divergence conditions; E[RR'] = Sigma. All checked by hand and against the lab outputs."),
    dict(id="m4d-proj-sign-untested-claim", check="The page's statement that the suite does not test the sign of the loss is correct",
         location="project.html 'What the suite does not test' (first claim)",
         status="PASS", evidence="m11_loss_sign_flipped survives seeds 0-99 (run output above). The sign-flip claim 'the distribution of the losses is unchanged' follows from the symmetry of Z (checked: the loss sign flip maps the sample to its negative)."),
    dict(id="m4d-proj-only-when-1-6", check="'if and only if' and 'only when' claims on the cards behind the project's rubric and conventions",
         location="cards c024, c040, c125 (no 'only when' claim in project.html)",
         status="PASS", evidence="c024: Var(X)=0 iff X takes one value (positive weights): true. c040: kappa >= 1 with equality iff two values each with probability 1/2: true (Y^2 constant with mean zero). c125: w'Sigma w = (2w1+w2)^2 + w2^2 is zero only at w = 0: checked algebraically."),
    dict(id="m4d-proj-hours", check="Hours split sums to the hub figure (arithmetic only; pace not judged)",
         location="project.html #hours table; data-hours-project",
         status="PASS", evidence="2 + 2 + 12 + 8 + 4 + 2 = 30 = data-hours-project=30 on <main>; the Total row states 30."),
    dict(id="m4d-proj-platform-claims", check="Browser-side claims: code saved in this browser; nothing leaves the browser",
         location="project.html Autograder and footer",
         status="UNVERIFIABLE", evidence="page_smoke checks zero requests to other hosts (PASS for the project page), but localStorage saving of the learner's code was not exercised in this session.",
         fix="Run the autograder panel in Chromium with a learner file and read localStorage, or drop the 'saved in this browser' sentence."),
    dict(id="m4d-proj-conditions-named", check="Conditions subsection: each named condition is tested and each accepted case is accepted",
         location="project.html #conditions; grader/test_project.py",
         status="PASS", evidence="Read against the test list (see m4d-grader-conditions-coverage). Accepted cases: n_draws = 1, nu = None for gaussian, nu = 3, one position with positive variance, quantile of one loss: each has a passing test (lines 187-217, 264-266, 401-403, 436-437)."),
    dict(id="m4d-proj-conventions-binding-claim", check="The conventions carve-out lists exactly the items the suite does not grade",
         location="project.html Constraints ('except the items the suite does not grade') and conventions items 1-5",
         status="PASS", evidence="Items the suite does not grade: the matched factor inside simulate_losses at nu 3 and 4 (no test, mutant v4_m02 survives), the sign (m11), the stream order and the one chi-square per draw (m17 and n02/ conventions item 5). The rest of item 1 and item 3 are graded (matched_scale tests, variance tests)."),
    dict(id="m4d-proj-test-comment-measure", check="Comments in test_project.py that state a measurement match the measurement",
         location="grader/test_project.py lines 31-39, 230-232, 316, 355",
         status="PASS", evidence="Measured: 0.1259, 0.0967, 0.0728, 0.0624 (sweep); 4.0835 and 2.7043 (rounding); 'the pair (1,2) is the one a first-row check would miss' is structural (cov[1][2] is not in row 0)."),
    dict(id="m4d-proj-process-words", check="No process words in learner text (project page and cards)",
         location="course/modules/M/M4/project.html; cards.json",
         status="PASS", evidence="Python scan of project.html text for builder, build, verifier, verif, round N, REQUEST, unit report, process, reviewer: 0 hits each."),
    dict(id="m4d-proj-scope-words", check="Scope words on the project page are backed or flagged",
         location="course/modules/M/M4/project.html (all prose)",
         status="PASS", evidence="'always' appears only in exemplar A (flagged there as unbacked, 'the Student-t model is always riskier'). Other 'every/all/only' uses are quantifiers in computed statements (Lab 1 'every' no; 'every seed tested' in the grader comment is backed by the 347/317/343/317 counts)."),
    dict(id="m4d-exemplar-a-scores", check="Exemplar A annotations: each 'misses' and 'meets' names a real defect or property",
         location="project.html #exemplar-a",
         status="PASS", evidence="Exemplar A 'about 2,100 dollars' vs 213213 cents (Lab 3): flagged as miss. Body word count: 100 words when the four subheadings are counted, 90 paragraph words (r5_numeric_and_text_checks_output.txt line 5-6). Annotation 'the body is 100 words' is correct on that basis."),
    dict(id="m4d-exemplar-b-scores", check="Exemplar B: every number and proof step and the 70-word summary",
         location="project.html #exemplar-b",
         status="PASS", evidence="Numbers recomputed: 213213 (Lab 3), 243004 and 210946 (Lab 1), 2267 = 213213-210946, 32058 = 243004-210946, 15.2 % = 32058/210946, 1.152 = 243004/210946, 4.5 % of 1 from 1.0447. Summary 70 words <= 80 (output line 7)."),
    dict(id="m4d-exemplar-intro-numbers", check="Exemplar intro: numbers come from the labs or formulas",
         location="project.html #exemplars intro paragraph",
         status="PASS", evidence="The exemplar figures used are the lab outputs and formulas checked above; the deliberately wrong 2,100 dollars is annotated as a miss."),
    dict(id="m4d-rubric-structure", check="Rubric has five criteria with four levels, and the bar is stated",
         location="project.html #rubric",
         status="PASS", evidence="Table rows C1..C5, each with four level cells; 'The report meets the bar at level 3 or above on every criterion' appears in the brief and the caption."),
    dict(id="m4d-lab1-step2-comment", check="Lab 1 Step 2 comment: sqrt(NU/W) times sqrt(matched) equals sqrt((NU-2)/W)",
         location="tests/labs/M4/lab-M4-project-1.py (Step 2); project.html Lab 1 code",
         status="PASS", evidence="Algebra: sqrt(nu/W) * sqrt((nu-2)/nu) = sqrt((nu-2)/W); code line 'scale = math.sqrt((NU - 2) / chi_square)' matches."),
    dict(id="m4d-lab1-hypothesis-numbers", check="Lab 1 hypothesis numbers: 8.4e9, 0.6, 19800, 5 % bound",
         location="project.html Lab 1 hypothesis paragraph",
         status="PASS", evidence="8.4e9 = 9e12*4e-4 + 4e12*9e-4 + 2*6e12*1e-4; ceil(0.99*20000) = 19800; both printed ratios (1.0017, 1.0447) are within 5 % of 1."),
    dict(id="m4d-lab3-closed-forms", check="Lab 3 closed forms and index rows",
         location="project.html Lab 3; tests/labs/M4/lab-M4-project-3.py",
         status="PASS", evidence="run_labs PASS for Lab 3; sqrt(8.4e9) = 91651.514; z = 2.326348; round(z*sd) = 213213; index rows n=101 ceil 100 floor 99; n=19987 index 19788/19787 (0.99n = 19787.13)."),
    dict(id="m4d-proj-numbers-prose", check="Prose numbers in the project page are computed or printed",
         location="project.html (Lab 1 interpretation, exemplars, Limitations)",
         status="PASS", evidence="1.152 (243004/210946 = 1.15195), 1.6667 (5/3), 1.0447 (printed), 4.5 % (0.0447), '1 draw in 16' not used on this page; all match."),
    dict(id="m4d-proj-lab3-docstring", check="Lab 3 docstring claims: unrounded formulas, only one value rounded, no random draws",
         location="tests/labs/M4/lab-M4-project-3.py docstring",
         status="PASS", evidence="Code: round() appears once (z99*sd); index via Fraction and math.ceil/floor; no random import."),
    # ---- cards ----
    dict(id="m4d-cards-inventory", check="cards.json inventory: 180 cards over L01-L10",
         location="course/modules/M/M4/cards.json",
         status="PASS", evidence="Python: 180 cards; lessons L01 17, L02 17, L03 15, L04 18, L05 17, L06 16, L07 15, L08 16, L09 23, L10 26; grades T 164, C 16."),
    dict(id="m4d-cards-duplicate", check="No duplicate ids, fronts or backs",
         location="course/modules/M/M4/cards.json",
         status="PASS", evidence="Python: 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs."),
    dict(id="m4d-cards-locators", check="Every card locator (Lesson/Section/Definition/Proposition) matches the current lesson",
         location="course/modules/M/M4/cards.json vs L01..L10.html",
         status="UNVERIFIABLE", evidence="Checked against the current lesson text: c007, c092-c098, c105, c107, c157, c163-c164, c173-c180, c073, c097, c124-c125, c134-c140 (see m4d-cards-numbers, m4d-card-c178-sample-mean and m4d-r5-cards-prop23-hypotheses). Not all 180 locators were read.",
         fix="Read each remaining card's locator against the current lesson and record it."),
    dict(id="m4d-cards-numbers", check="Every number on a card appears in its lab output or its lesson",
         location="course/modules/M/M4/cards.json",
         status="UNVERIFIABLE", evidence=f"{R}cards_numbers_in_lesson.py: every card number appears in its own lesson text (0 misses; weak, digits only). {R}all_labs_output.txt: the lab numbers on c030, c033, c047, c082, c083, c098, c112, c113, c126, c143, c161, c162, c166, c167, c169-c171, c172 all appear in the lab outputs. c157, c161, c168, c172 recomputed to the printed digits (r5_numeric output). Not every card number was recomputed.",
         fix="Recompute each card's numbers from unrounded values and cite the lab line for each."),
    dict(id="m4d-cards-c098-seed", check="c098 basis: seed 20260602 + nu, n = 100000",
         location="cards.json M4-c098; tests/labs/M4/lab-M4-L06-1.py (SEED = 20260602, N_DRAWS = 100000, Part A seeds 20260602 + nu)",
         status="PASS", evidence="Lab twin lines 8, 18-19: Part A seeds random.Random(20260602 + nu), N_DRAWS = 100000."),
    dict(id="m4d-cards-c098-rounding", check="c098 numbers: 1.669114, 1.666667, relative error 0.001469 from unrounded values",
         location="cards.json M4-c098; lab-M4-L06-1 output",
         status="PASS", evidence="Lab output 'nu 5 sample_variance 1.669114 formula 1.666667' and 'nu 5 relative_error 0.001469' (run this session); the lab computes the error from unrounded values (code line 56)."),
    dict(id="m4d-cards-c097", check="c097: N(mu, sigma^2) has mean mu and variance sigma^2 (Proposition 1.5, Assumption 1)",
         location="cards.json M4-c097; L06.html Proposition 1.5 and Assumption 1",
         status="PASS", evidence="L06 Lesson text: 'proves under Assumption 1 that the normal density integrates to one and that its two parameters are its mean and variance' (current L06)."),
    dict(id="m4d-cards-c073", check="c073: correlation of X and aX+b, a > 0, is 1 (Example 1.7)",
         location="cards.json M4-c073; L05.html Example 1.7",
         status="PASS", evidence="L05 Example 1.7 (current text): 'Let sigma_X > 0, let a > 0, and let Y = aX + b ... correlation one for an increasing affine map.'"),
    dict(id="m4d-cards-grade-basis", check="Every C card names a basis; no T card has a basis",
         location="cards.json",
         status="PASS", evidence="Python: 16 C cards all have a basis (e.g. 'Lab 1, Part A (SIMULATED), seed 20260602 + nu'); 0 T cards carry a basis."),
    dict(id="m4d-cards-sentence-level", check="Every card sentence against its lesson text",
         location="course/modules/M/M4/cards.json (180 cards)",
         status="UNVERIFIABLE", evidence="Read in full: all 180 fronts and backs were printed and scanned for scope words, quantifiers and hypotheses. Sentence-by-sentence comparison against the lesson was done for the changed and the numeric cards (listed in the other card rows) and not for all 180.",
         fix="Complete the sentence-level comparison for the remaining cards."),
    dict(id="m4d-card-c095-changed", check="c095 (changed in 2657ab5..09b8751): variance 1 is wrong, nu/(nu-2) with nu > 2",
         location="cards.json M4-c095; L06 Proposition 2.6",
         status="PASS", evidence="Card: 'No. A Student-t with nu > 2 degrees of freedom has mean 0 and variance nu/(nu - 2) ... For nu = 5 this is 5/3 (Proposition 2.6). Under Assumption 1.' Matches L06 Proposition 2.6 hypotheses (nu a positive integer, nu > 2)."),
    dict(id="m4d-card-c157-changed", check="c157 (changed in round 4): P(|C|>10) = (2/pi) arctan(0.1) = 0.063451, about 1 in 16, versus 1.5240e-23 for the normal",
         location="cards.json M4-c157; L10.html Remark / Proposition 1.4 and 1.5",
         status="PASS", evidence="Recomputed: (2/pi) arctan(0.1) = 0.0634510; 1/0.063451 = 15.76 ('about 1 in 16'); P(|Z|>10) = 1.523971e-23 = 1.5240e-23. Lab 1 Part A output line 'P(|C| > 10) = 0.063451' and 'P(|Z| > 10) = 1.5240e-23' (run this session)."),
    dict(id="m4d-card-c178-sample-mean", check="c178 'sample mean of the first n variables is the sum divided by n (Section 1)'",
         location="cards.json M4-c178; L09.html Section 1",
         status="FAIL", evidence="L09 Section 1 (current text) never defines X-bar_n or S_n: X-bar_n first appears in the statement of Proposition 1.2 and S_n first in its proof ('Var(S_n) = E[(S_n - n mu)^2]'), with no definition sentence. The card cites Section 1 for a definition the page does not state (basis: the lesson text read in this session; the defect is in the lesson, outside this slice).",
         fix="Lesson owner: add the definitions X-bar_n = (1/n) sum X_i and S_n = sum X_i in L09 Section 1; then the card's citation is correct. Or the card should cite Proposition 1.2's proof."),
    dict(id="m4d-cards-new-others", check="c173-c180 against the current lesson text",
         location="cards.json M4-c173..c180; L01, L06, L08, L09, L10",
         status="PASS", evidence="c173 (L01 Section 3 'defined in §3'), c174 (L06 Remark 2.2 independence, same wording), c175 (L08 Section 1 'A symmetric matrix Sigma is positive definite when w'Sigma w > 0 for every nonzero w'), c176 (L08 Section 3 divisor n-1), c177 and c179 (L09 Section 1 and 2 wording), c180 (L10 Section 1 'light-tailed' sentence). c178 is a separate FAIL row."),
    dict(id="m4d-dag-concepts", check="No out-of-closure concept by name or link on the project page or the cards",
         location="course/modules/M/M4/project.html; cards.json; plans/M4-build-plan.md 'Outside the closure'",
         status="PASS", evidence="grep of project.html for spectral, eigen, singular value, principal, orthogonal projection, least-squares, nearest correlation: 0 hits; project.html has 0 concept links (data-concept count 0). Cards mention 'semidefinite' (c076, c077) and 'multivariate normal' only; positive semidefiniteness is derived in L05 per the plan (prose-only, allowed). check_dag M4 PASS."),
    dict(id="m4d-dag-gamma-function", check="Gamma function used on the page is introduced in Assumption 1 before its use",
         location="project.html Conventions item 6 (Assumption 1) and Appendix A1",
         status="PASS", evidence="Assumption 1(a) defines Gamma before A1 uses it; prose-only term (plan: not a dfn). check_dag M4 PASS."),
    dict(id="m4d-reading-attribution", check="Reading section attributes nothing to the source and cites an existing key",
         location="project.html #reading; references/references.json blitzstein2019introduction",
         status="PASS", evidence="'This page attributes no statement to it'; verify_refs live run for M4 (1 of 560 entries, 0 problems) includes the key; the page makes no locator claim."),
    dict(id="m4d-r4-grader-v4-rounding-per-position", check="v4_m01 (loss rounded per position) is killed",
         location="ledgers/M4/mutants/v4_m01_loss_rounded_per_position.py",
         status="PASS", evidence="Killed in the 0-99 run (test_loss_is_rounded_once_for_the_portfolio_not_per_position). Round-4 FAIL is closed."),
    dict(id="m4d-r4-grader-v4-matched-factor-nu34", check="v4_m02 (no matched factor at nu 3 and 4) is disclosed",
         location="ledgers/M4/mutants/v4_m02_matched_factor_skipped_for_small_nu.py; project.html 'What the suite does not test'",
         status="PASS", evidence="Survives seeds 0-99; project.html says the suite does not check the matched factor inside simulate_losses at nu 3 and 4 and gives the reason (infinite fourth moment), and Constraints item 1 excludes it from the binding conventions. Round-4 FAIL is closed by disclosure."),
    dict(id="m4d-r4-grader-v4-sign-folded", check="v4_m03 (loss sign folded by absolute value) is killed",
         location="ledgers/M4/mutants/v4_m03_loss_sign_folded.py",
         status="PASS", evidence="Killed in the 0-99 run (test_gaussian_loss_variance_matches_portfolio_covariance, seed 0)."),
    dict(id="m4d-r4-grader-no-print", check="No function prints (test exists and catches a printing solution)",
         location="grader/test_project.py test_no_function_prints; scratch probe ledgers/M4/scripts/M4-d-r5/print_mutant_probe.py",
         status="PASS", evidence="Probe: reference with print('debug') inserted into simulate_losses fails test_no_function_prints (AssertionError) at seed 0 (run this session). Round-4 FAIL closed."),
    dict(id="m4d-r4-scope-words-cards", check="Scope words on cards are backed by a computation or a stated hypothesis",
         location="cards.json (scope words in fronts and backs)",
         status="PASS", evidence="Scanned all cards for always/only/all/every/any/same/drives: quantifiers are theorem statements (e.g. c124 'for every w') or are answered 'No' with a counterexample (c013, c027, c045, c065, c081, c096, c138, c158). c158 'not reduce by sqrt(n)': Cauchy has no finite variance (Proposition 2.1); c081 counterexample checked (2^2 <= 1 false)."),
    dict(id="m4d-r4-lab-project-3-rounding-claim", check="Lab 3 docstring rounding claim matches the code",
         location="tests/labs/M4/lab-M4-project-3.py docstring",
         status="PASS", evidence="Code: round() only on z99*sd; file byte-identical to the 2657ab5 pin (not in the delta)."),
    # ---- round-5 new rows ----
    dict(id="m4d-r5-cards-prop23-hypotheses", check="Cards c134, c135, c140 state Proposition 2.3 with its hypotheses (finitely valued variables; Assumption 2 for (b))",
         location="cards.json M4-c134, M4-c135, M4-c140; L09.html Proposition 2.3",
         status="FAIL", evidence="Current L09 Proposition 2.3: 'Under the i.i.d. hypotheses of this section, with the variables finitely valued and Z_n as defined above: (a) ...; (b) assuming Assumption 2, for every real t, phi_{Z_n}(t) -> e^{-t^2/2}'. c134 back drops 'finitely valued' and 'Assumption 2'; c135 says 'Proposition 2.3(b) is proved' with no Assumption 2; c140 says (b) gives the limit 'without assuming normality' and omits Assumption 2 (lesson_context.py output).",
         fix="In cards c134 add 'finitely valued' and 'assuming Assumption 2' to (b); in c135 and c140 say 'Proposition 2.3(b) is proved under Assumption 2'."),
    dict(id="m4d-r5-sign-stream-order-identity", check="The contract-notes sentence identifying a sign error with a different stream order",
         location="course/modules/M/M4/project.html #contract-notes (sentence 'A sign error is also the same as drawing every normal with the opposite sign, which is a different stream order')",
         status="FAIL", evidence="Negating every normal negates every return: that is a sign error in the draws, not a reordering of the random stream, so the identification is false. The sign error goes undetected for another reason: the variance check and the quantile check are invariant under negating all losses (test_quantile_99_is_the_exact_order_statistic compares with sorted(own losses)); m11 survives seeds 0-99 for that reason.",
         fix="Delete the sentence and state the actual reason: 'A sign error leaves the loss variance and the order-statistic check unchanged, because those checks use only the losses themselves.'"),
    dict(id="m4d-r5-doc-tab-escape", check="Docstrings with a backslash escape are not corrupted",
         location="grader/reference.py (_cholesky, simulate_losses); grader/instance.py (module docstring); tests/labs/M4/lab-M4-project-1.py (cholesky_2x2)",
         status="FAIL", evidence="The docstrings are not raw strings and contain 'L^\\top' / 'F F^\\top'; Python reads '\\t' as TAB (U+0009): ast.get_docstring shows '\\t' at the escape (r5_numeric_and_text_checks_output.txt lines 1-4; char check: 'L', '^', TAB, 'o'). Visible text in the page source is correct; the runtime docstrings are not.",
         fix="Make these docstrings raw (r\"\"\"...\"\"\") or write 'L^T' / 'F F^T'."),
    dict(id="m4d-r5-lab1-docstring-scale", check="Lab 1 docstring: the Student-t draws are scaled by the matched factor (nu - 2)/nu",
         location="tests/labs/M4/lab-M4-project-1.py module docstring; project.html Lab 1 code",
         status="FAIL", evidence="The code applies scale = sqrt((NU - 2) / chi_square) = sqrt(nu/W) * sqrt((nu-2)/nu); the factor (nu-2)/nu itself is not applied (the step 2 comment says so correctly). The docstring names the wrong factor.",
         fix="Write: 'scaled by sqrt((NU - 2) / W), the matched factor (nu - 2) / nu times sqrt(nu / W)'."),
    dict(id="m4d-r5-conventions-method-claims", check="Binding conventions name only what the suite grades (methods the suite cannot distinguish are not 'binding')",
         location="project.html #conventions items 2 and 4 with the Constraints carve-out",
         status="FAIL", evidence=f"Item 4 requires the index 'computed in exact integer arithmetic as (99n+99)//100' and item 2 requires rounding 'with round()', and the page says the conventions are binding except the listed items. The suite grades values only: alt_r5_c (float ceil with a 1e-12 offset) and alt_r5_a/b (other rounding and index code) pass seeds 0-149 ({R}alt_seeds0-49.txt). The method words are therefore claimed but not graded.",
         fix="Either state that the method is an example and the values are graded, or add 'the integer method and the round() call are not graded' to the carve-out."),
    dict(id="m4d-r5-exemplar-a-word-count", check="Exemplar A 'the body is 100 words' count basis",
         location="project.html #exemplar-a annotation",
         status="PASS", evidence="r5_numeric_and_text_checks_output.txt line 5: 100 words with the four subheadings counted (90 in paragraphs). The annotation's number is correct on that basis; the basis is not stated on the page."),
    dict(id="m4d-r5-tail-numbers", check="Tail numbers quoted in L10 and cards: t(3) at x = 1000, normal and Cauchy at x = 10",
         location="cards.json M4-c157, M4-c172; L10 Lab 1 Part D output",
         status="PASS", evidence="High-precision (Decimal, 50 digits): x^3 P(|V|>x) = 2.2053076 at x = 1000, printed 2.205308 (lab) correct, 4 sqrt(3)/pi = 2.2053156. P(|Z|>10) = 1.523971e-23; P(|C|>10) = 0.0634510; ratio 4.1635e21 (quoted 4.164e21 with the unrounded ratio)."),
]

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for row in ROWS:
    counts[row["status"]] += 1
verdict = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"
fragment = {
    "unit": "M4",
    "slice": "M4-d",
    "round": 5,
    "round_note": (
        "Round 5 of M4-d. Delta from the round-4 pin 2657ab5 to 09b8751: project.html (contract-notes sentence, "
        "Constraints carve-out, grader wording), grader/test_project.py (comments and tests), grader/instance.py and "
        "reference.py (docstrings), cards.json (c007, c092-c098, c105, c107, c163 text), tests/labs/M4/lab-M4-project-1.py "
        "(docstring), and mutants r5_01..r5_10 and v4_m01..v4_m03 in the mutant list. Lessons L01-L10 and index.html also "
        "changed in the delta (not owned by this slice); cards citing them were re-read against the current text. New "
        "round-5 verifier mutants v5_m01..v5_m03; round-5 verifier alternatives alt_r5_a..c. Previously FAIL rows re-verified "
        "from scratch; PASS rows re-run or re-read on the current pin."
    ),
    "verifier": "Claude Haiku 5.5, independent verifier, round 5 (did not build M4)",
    "pin": "09b8751 (detached checkout /tmp/verifyB5-M4-d)",
    "base": "none",
    "checkout": "/tmp/verifyB5-M4-d",
    "scratch": "/tmp/M4-v/d/r5/",
    "verified_at": "2026-10-28",
    "verdict": verdict,
    "rows": ROWS,
    "mutants": [
        {
            "id": m["id"],
            "description": m["description"],
            **({"killed_by": m["killed_by"]} if not m["survived"] else {"survived": True,
                "disposition": "disclosed on project.html (see the matching PASS row)"}),
        }
        for m in mutants
    ],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Mutants: all 73 files in ledgers/M4/mutants run at seeds 0-99 (70 killed, 3 survived: m11, m17, v4_m02, each disclosed). "
        "Alternatives: alt_1..alt_5 (builder) and alt_r5_a..c (verifier) pass seeds 0-49, and alt_1 and alt_r5_a..c pass seeds 0-149. "
        "Gates run: check_projects, check_pages, check_dag (M4), run_labs (M4, 13/13), run_graders (0-49), collect-only (124), "
        "starter (122 failed), ruff, mypy (repo, 255 files), page_smoke (project.html), verify_refs live (M4) and offline. "
        "Not checked: sentence-level read of all 180 cards; every card locator; per-card numbers beyond the ones named; "
        "browser-side localStorage claim; full DAG closure per concept. Lesson-owner findings outside this slice: L09 Section 1 "
        "does not define X-bar_n or S_n (basis of the c178 FAIL); L09 Proposition 2.3 hypotheses (basis of the c134/c135/c140 FAIL, "
        "which is a card defect)."
    ),
    "summary": {
        "rows": len(ROWS),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants": len(mutants),
        "mutants_killed": sum(1 for m in mutants if not m["survived"]),
    },
}
out = ROOT / "ledgers/M4/M4-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, counts, "verdict", verdict, "mutants", len(mutants))
