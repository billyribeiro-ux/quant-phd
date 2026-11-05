"""Build the round-10 fragment ledgers/M2/M2-e.json for slice e (verifier D10). Evidence strings cite the round-10 scripts."""
import json
import pathlib
import re
import sys
from datetime import datetime, UTC

root = pathlib.Path(sys.argv[1])
S = "ledgers/M2/scripts/M2-e-r10"
PIN = "47a36d8c78633793ccc762ae19dcd5e19b780d19"
BASE = "1e272e5a641f18412703b37778a44db6f7391a69"
P9 = "Carried from round 9 (%s byte-identical since the previous pin 1e272e5a):"

rows = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


def carry(id_, check, location, files, prev_evidence):
    row(id_, check, location, "PASS", (P9 % files) + " " + prev_evidence)


# ---------- gates and runs (fresh this round) ----------
row("e2-check-pages", "2.9 structure", "course/modules/M/M2/", "PASS",
    f"`.venv/bin/python tools/check_pages.py --unit M2` -> 'check_pages M2: PASS', exit 0 ({S}/check_pages_M2.out). Includes the banned-string scan of visible prose.")
row("e2-check-dag", "2.9 DAG", "course/modules/M/M2/", "PASS",
    f"`tools/check_dag.py --unit M2` -> 'check_dag M2: PASS', exit 0 ({S}/check_dag_M2.out).")
row("e2-check-projects", "2.6 spec, ladder, hours, rubric", "course/modules/M/M2/project.html", "PASS",
    f"`tools/check_projects.py --unit M2` -> 'check_projects M2: PASS', exit 0 ({S}/check_projects_M2.out). project.html changed since the previous pin (rubric wording, Lab 1/3 hypotheses, grading-mode count 87 to 89), so re-run.")
row("e2-run-graders", "2.6 autograder 1", "course/modules/M/M2/grader/reference.py", "PASS",
    f"`tools/run_graders.py --unit M2 --seeds 0-49` -> 'run_graders M2: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0 ({S}/run_graders_M2.out).")
row("e2-run-labs-project", "2.5 labs", "project.html lab-M2-project-1..3", "PASS",
    f"`tools/run_labs.py --unit M2 --page project` -> 'run_labs M2: PASS (3/3)', exit 0 ({S}/run_labs_M2_project.out); full unit `tools/run_labs.py --unit M2` -> 'PASS (27/27)', exit 0 ({S}/run_labs_M2.out).")
row("e2-lab-page-code-equals-twin", "2.5 labs: page code equals twin", "project.html lab blocks 1-3; tests/labs/M2/lab-M2-project-1..3.py", "PASS",
    f"`{S}/page_code_vs_twin_r10.py` (run this round) extracts each data-run block and compares it with its twin after strip: lab-M2-project-1 and -3 identical (49 and 79 lines); lab-M2-project-2 differs from its twin only in two lines, `return Dual(self.value * o.value, ___)` and `return ___` in second_difference, which is the completion blanking (ruling 11). Output {S}/page_code_vs_twin_r10.out.")
row("e2-lab-twin-clean-and-expected", "2.5 labs: twin under python -I -W error; expected block equals output", "tests/labs/M2/lab-M2-*.py (27 twins)", "PASS",
    f"Each of the 27 twins run alone as `python -I -W error` from /tmp: 27 exit 0 ({S}/twins_alone_r10.out). `run_labs.py --unit M2` PASS 27/27 (expected blocks equal printed output). Lab 1 expected block 9 lines, Lab 2 expected 4 lines, Lab 3 expected 27 lines.")
row("e2-page-smoke-project", "2.9 page_smoke", "course/modules/M/M2/project.html", "PASS",
    f"`tools/page_smoke.py --unit M2 --pages project` -> 'page_smoke M2: PASS'; in-browser grader 'All 89 tests pass on seed 577397640' ({S}/page_smoke_project_r10.out). The round-9 copy is not reused.")
row("e2-pytest-local-and-count", "2.6 autograder 5 and page test count", "course/modules/M/M2/grader/test_project.py", "PASS",
    f"In a scratch copy (reference as sensitivity_engine.py): `pytest --collect-only` -> '89 tests collected' ({S}/pytest_collect_M2.out), equal to the 89 on project.html 'Grading mode'. Seeds 0-3, `-W error --assert=plain`: 89 passed each ({S}/pytest_M2_seed0.out .. seed3.out).")
row("e2-ruff", "gate: ruff", "tests/labs/M2, course/modules/M/M2/grader", "PASS",
    f"`ruff check` -> 'All checks passed!' ({S}/ruff_check_M2_r10.out); `ruff format --check` -> '31 files already formatted', exit 0 ({S}/ruff_format_M2_r10.out).")
row("e2-mypy-labs", "gate: mypy strict on labs", "tests/labs/M2", "PASS",
    f"`mypy tests/labs/M2 --no-incremental` -> 'Success: no issues found in 27 source files', exit 0 ({S}/mypy_labs_M2_r10.out).")
row("e2-mypy-grader-command", "plan section 8 grader mypy command", "course/modules/M/M2/grader/test_project.py", "PASS",
    f"`mypy --strict --no-incremental test_project.py instance.py sensitivity_engine.py` in a scratch copy -> 'Success: no issues found in 3 source files', exit 0 ({S}/mypy_grader_strict_M2_r10.out).")
row("e2-pytest-labs-tests", "gate: pytest for lab tests", "tests/test_labs.py, tests/test_run_labs.py -k M2", "PASS",
    f"`pytest tests/test_labs.py tests/test_run_labs.py -k M2 -q` -> 27 dots, exit 0 ({S}/pytest_labs_M2_r10.out).")
row("e2-verify-refs", "2.1 citations: keys cited by project.html", "references/references.json; course/modules/M/M2/project.html", "PASS",
    f"project.html cites spivak2008calculus and hubbard2015vector (data-cite, Reading list); both present with status 'verified' in references/references.json. `tools/verify_refs.py --offline` -> '560 entries, 0 problems' ({S}/verify_refs_offline_r10.out). Live: `tools/verify_refs.py --unit M2` -> 'live re-verification of M2: 2 of 560 entries, 0 problems', exit 0 ({S}/verify_refs_unit_M2_r10.out). The note attributes no statement to either source (page Reading section), so no locator is checked.")
row("e2-hours-arithmetic", "hours arithmetic: hub split vs lesson hours", "course/modules/M/M2/index.html; project.html time budget", "PASS",
    "index.html line 29 data-hours-lessons=240 and data-hours-project=60; 24 lesson pages each declare data-hours=10 (sum 240, computed this round); curriculum/01-foundations.yaml M2 hours 300. project.html time budget rows 4+6+22+6+14+8 = 60 (line ~ 'Total' row). Arithmetically consistent, which is the only hours failure the ruling names.")
row("e2-project-lab1-numbers", "numbers in prose vs unrounded values (Lab 1)", "course/modules/M/M2/project.html Lab 1 hypothesis and interpretation", "PASS",
    f"Lab 1 expected block (run_labs PASS) gives 1081108.9578, -8514667.3953, 83766485.1192, 7.875864 and differences 1.56e-02 and 8.36e+00. Re-derived by hand: 1.56e-02/8514667.40 = 1.83e-9 (page '1.8e-9'); 8.36/83766485.12 = 9.98e-8 (page '1.0e-7'); 1081108.9578 rounds to 1081109; duration 7.875864 rounds to 7.88. Interpretation claim 'error smallest at 1e-6 and larger at every other printed step' checked against the Lab 3 sweep, not Lab 1; Lab 3 sweep verified in e2-project-lab3-numbers.")
row("e2-project-lab2-numbers", "numbers in prose vs unrounded values (Lab 2)", "course/modules/M/M2/project.html Lab 2", "PASS",
    "Hypothesis: second difference 8.4 and AD 3.76 with error below 1e-7 and 1e-15; expected block gives 5.11e-08 and 4.44e-16. Test cubic 1 - 2x + 3x^2 + 0.5x^3 at 0.8: f'' = 6 + 3x = 8.4, f' = -2 + 6x + 1.5x^2 = 3.76 (hand check). Interpretation: a central second difference of a cubic is exact in exact arithmetic (fourth derivative zero) (checked).")
row("e2-project-lab3-numbers", "numbers in prose vs unrounded values (Lab 3)", "course/modules/M/M2/project.html Lab 3 hypothesis and interpretation", "PASS",
    f"Hypothesis: 2721581.2909, 2721581, -23407826.805475, 7.111207e-04 at step 1e-6 (smallest central error, checked against the 12-row sweep), orders 0.984 and 2.000 (recomputed as log10 of the error ratios at 1e-2 and 1e-3: 9.63 -> 0.984; 100.1 -> 2.000), kink +1/-1/0, cancellation rows. Interpretation: forward error ~tenfold per decade over 1e-3..1e-6 (1.297e5, 1.302e4, 1.303e3, 1.303e2: ratios 9.96-10.00); smallest printed forward error 1.490103 at 1e-8; central error larger than its minimum at every printed step below 1e-6 (checked row by row). Independent recomputation of the price 2721581.2909 and dP/dy in {S}/card_numbers_r10.py.")
row("e2-project-exemplar-numbers", "numbers in exemplars A and B", "course/modules/M/M2/project.html Exemplars A and B", "PASS",
    "Exemplar A: 'more accurate at every printed step' checked for all 12 steps (central < forward at 1e-1..1e-12); derivative 'about -23407827' = round(-23407826.8). Exemplar B: 2^-31 = 4.66e-10 ('about 4.7e-10', price in [2^21,2^22)); 2^-26 = 1.49e-8; 2h/spacing at 1e-8 = 1.34 ('about 1.3'); 1/(2h) at 1e-12 = 5e11; 1.49e-8 spacing; 3e-11 relative error (7.111e-4/2.34e7). All recomputed this round.")
row("e2-project-spec-signatures", "spec signatures vs starter and reference", "project.html Rung 3; grader/starter.py; grader/reference.py", "PASS",
    "starter.py signatures fd_derivative(f,x,h,scheme)->float, ad_derivative(f,x)->float, hessian_fd(f,x,h)->list[list[float]], bond_price_cents(instance)->int, sensitivities(instance)->dict[str,float] equal the Rung 3 text. Instance keys face_cents, coupon_bps, maturity_years, yield_bps named in the Rung 3 report bullet match instance.py. reference.py returns those types (tests check them).")
row("e2-project-tolerances-conventions", "tolerances and conventions", "project.html Conventions and Tolerances; grader/test_project.py", "PASS",
    f"Each tolerance in project.html was matched to its test in test_project.py this round: 1e-6 central cubic at 1e-5; 1e-9 AD cubic and at 1e5; 1e-5 Hessian at 1e-4; 1e-9 + 1e-12/h^2 Hessian at 1e-3 and 1; 1e-9 forward at 1e-9, 1, 5, 1e6; 1e-6 forward cubic at 1e-3; 1e-6 symmetry; 1e-6 dprice_dy; 1e-4 d2price_dy2; 1e-9 ratios; 1e-9 at -0.99. Order checks at 1e-2 and 5e-3 with ratio 1.9-2.1 and >= 3.8. The sin ratio range 3.9999842-3.9999851 is recomputed over 100 instances in {S}/sin_ratio_r10.out (min 3.9999841904, max 3.9999850561). Richardson and complex-step accepted by alternatives (see e2-grader-alternatives).")
row("e2-project-rubric-calibration", "rubric calibration (blind scoring)", "project.html rubric table and Exemplars A and B", "PASS",
    "Blind scoring from the rubric table alone (rubric descriptors quoted): Exemplar A = C1 2, C2 1, C3 2, C4 2, C5 2 (official 2,1,2,2,2). Exemplar B = C1 4 (1/h proportionality, IEEE spacing reason, step named), C2 4 (kink and cancellation derived, rows shown), C3 2 (no AD value), C4 3 (orders derived, no bound), C5 4 (unrounded basis stated). Official 4,4,2,3,4. All within one level, and exact.")
row("e2-project-rubric-observable", "rubric levels are observable", "project.html rubric table", "PASS",
    "Each level descriptor was read for observable content. C1 level 4 names the 1/h proportionality, the IEEE spacing reason and the step below which the central error rises; C2 levels name the sweep rows; C3 levels name the AD value and tolerance; C4 level 4 names the Lagrange bound at a stated step; C5 names units per quantity. No descriptor is vague enough to fail.")
row("e2-project-adversarial-atlas-studio", "adversarial question bank / atlas / studio", "project.html", "PASS",
    "Not applicable: the project is a rung-3 autograded and rubric-graded project, not adversarial; project.html has 0 occurrences of 'adversarial'; no atlas contract or studio requirement is named (grep). Nothing to fail.")
row("e2-project-notation", "notation registry: no symbol reused with another meaning", "project.html math; cards.json; L22-L24", "PASS",
    "Symbols used on project.html (h, x, f, P, y, F, c, H, C_t, v, p_3, xi, i as \\mathrm{i}) checked against notation/notation.json: registered symbols are T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q and the macros; none is used on the page. No \\mathbb or \\gamma macro appears in project.html (grep count 0).")
row("e2-banned-phrases", "banned phrases", "project.html; cards.json; grader/*.py; labs; L22, L23, L24", "PASS",
    f"check_pages M2 banned-string scan PASS ({S}/check_pages_M2.out). Process-word grep on project.html, cards.json and grader/test_project.py (verif, ruling, round, builder, audit, TODO, agent, reviewer, previously, revised): no hits.")
row("e2-scope-words", "scope words", "project.html intro, Labs 1-3 prose; instance.py docstring; L22, L23, L24 changed text", "PASS",
    "Scope claims checked: 'every printed step' (Lab 3, twelve rows, central < forward at each), 'falls close to tenfold' (ratios 9.96-10.00), 'larger at every printed step below 1e-6' (rows 1e-7..1e-12), 'every cash flow non-negative' (F>0, c>=0), 'every instance is valid' (instance.py, 100 instances valid, see e2-grader-instances). Each has a computation or a printed row.")
row("e2-project-data-simulated", "simulated data labelled", "project.html; grader/instance.py; L22, L23, L24 labs", "PASS",
    "Lab 1 and Lab 3 hypotheses and docstrings say SIMULATED; Lab 2 is a test cubic; instance.py docstring 'All values are SIMULATED'; the project page says 'It is an illustrative input and not market data.' No dataset is read; labs use no data-files.")
row("e2-project-process-words", "no process words in learner text", "project.html; cards.json; grader/test_project.py messages", "PASS",
    "grep for verif, ruling, round, builder, fixer, audit, TODO, agent, reviewer, 'we fixed', 'previously', 'revised', 'corrected' on project.html, cards.json and test_project.py: 0 hits (run this round).")
row("e2-grader-instances", "instance validity over seeds 0-49", "course/modules/M/M2/grader/instance.py", "PASS",
    f"`{S}/instances_r10.py` (run this round): 100 instances (seeds 0-49 and 7919+seed) all valid (face 10000.00-500000.00, coupon 0-10%, maturity 1-30, yield 1-15%, price not within 1e-6 of a half cent, cubic well conditioned). Distinct prices 100, distinct yields 96, distinct x0 70: answers differ materially. Output {S}/instances_r10.out.")
row("e2-grader-instance-claims", "instance.py docstring ranges", "instance.py lines 1-20", "PASS",
    "Docstring ranges (face 10,000.00 to 500,000.00; coupon 0.00 % to 10.00 %; maturity 1 to 30 years; yield 1.00 % to 15.00 %) equal randrange bounds in make_instance (1_000_000..50_000_000 cents, 0..1000 bps, 1..30, 100..1500).")
row("e2-grader-reference", "reference solution passes the suite", "course/modules/M/M2/grader/reference.py", "PASS",
    f"run_graders 50/50 (see e2-run-graders); pytest seeds 0-3 on the reference copy: 89 passed each ({S}/pytest_M2_seed0.out..seed3.out).")
row("e2-grader-alternatives", "five alternative correct implementations pass", "ledgers/M2/scripts/M2-e-r10/alts_r10/, M2-e-r3 (alts), M2-e-r5/alts_r5, M2-e-r6/alts_r6, M2-e-r7/alts_new, M2-e-r8/alts_r8, M2-e-r9/alts_r9", "PASS",
    f"All 22 alternatives run against the CURRENT test_project.py and instance.py on seeds 0-49 by `{S}/run_alternatives_r10.sh`: round-10 five (Richardson central, complex-step AD, exact rational price, numpy sensitivities, effective-step fsum) 50/50 ({S}/alternatives_r10.out); round-3 five 50/50 after supplying the reference_core helper they import ({S}/alternatives_r3_r10.out); rounds 5-9 (2+2+2+3+3) 50/50 ({S}/alternatives_prior_r10.out). The first run of alt5 failed on a ZeroDivisionError at h=1e-300 (its own bug: dividing by (x+h)-x when it is zero); the fixed alternative passes, so no over-constraint was found.")
row("e2-grader-messages", "failure messages name a property and a hint", "course/modules/M/M2/grader/test_project.py", "PASS",
    "Every require()/pytest.fail message read this round (new messages at lines ~361-372, 501-508). Each names a property and a hint, none prints the expected value.")
row("e2-grader-valueerror-scope", "exception type demanded only for conditions the page names", "test_project.py must_raise call sites", "PASS",
    "must_raise call sites: zero, negative, -0.0, -1e-300, NaN and -inf steps (fd and hessian; page conventions (a)); unknown and non-name schemes (page (b)); yields -1, -1.0001 and -2 (page (c)); none else. must_accept is used for positive steps and yields above -1.")
row("e2-grader-no-print", "module prints nothing and warns nothing", "course/modules/M/M2/grader/test_project.py autouse fixture; purity test", "PASS",
    "Autouse fixture captures stdout/stderr and fails on any output; test_module_prints_nothing_and_warns_nothing calls each of the five named functions on both branches with warnings recorded; mutants x11 and x12 (print) are killed.")
row("e2-mutants-existing", "every existing mutant killed", "ledgers/M2/mutants/", "PASS",
    f"`tools/mutate_graders.py --unit M2` (default seeds 0-9) -> 'mutate_graders M2: PASS (171/171 killed)', exit 0 ({S}/mutate_graders_M2_r10.out). 171 = 166 existing + 5 new (w10e_01..05).")
row("e2-mutants-written", "verifier-written mutants from round 3", "ledgers/M2/mutants/", "PASS",
    "ledgers/M2/mutants/r3_01..r3_04 exist (git ls-files) and are killed in the gate run (lines 'KILLED r3_01..r3_04' in mutate_graders_M2_r10.out). The mutate tool counts every file in ledgers/M2/mutants/.")
row("e2-mut-v2-01", "round-2 survivor: dprice_dy numerical", "course/modules/M/M2/grader/test_project.py", "PASS",
    f"v2_01_dprice_dy_is_a_numerical_central_difference.py killed in {S}/mutate_graders_M2_r10.out.")
row("e2-mut-v2-02", "round-2 survivor: d2price_dy2 numerical", "course/modules/M/M2/grader/test_project.py", "PASS",
    f"v2_02_d2price_dy2_is_a_numerical_second_difference.py killed in {S}/mutate_graders_M2_r10.out.")
row("e2-mut-v2-03", "round-2 survivor: forward step floored at 1e-8", "course/modules/M/M2/grader/test_project.py", "PASS",
    f"v2_03_fd_step_floored_at_one_hundred_millionth.py killed in {S}/mutate_graders_M2_r10.out.")
row("e4-mutants-new-r4", "round-4 new mutants", "ledgers/M2/mutants/", "PASS",
    "ledgers/M2/mutants/r4_01..r4_03 exist and are killed (lines 'KILLED r4_01..r4_03' in mutate_graders_M2_r10.out).")
row("e2-cards-count", "cards: count and grades", "course/modules/M/M2/cards.json", "PASS",
    f"397 cards (was 395 at the previous pin): grade T 238, C 77, no grade 82 (`{S}/cards_mech_r10.out`). Delta vs 1e272e5a: 391 entries byte-identical, 4 changed (M2-c027, c047, c177, c352), 2 new (M2-c412, c413) (`{S}/cards_delta_r10.out`).")
row("e2-cards-dup-ids-fronts", "cards: duplicate scan (ids and fronts)", "course/modules/M/M2/cards.json", "PASS",
    f"No duplicate id and no identical front (`{S}/cards_mech_r10.out`). Pairs with front similarity >= 0.75 (52) reviewed one by one; the only semantic duplicate found is M2-c412 against M2-c065, recorded in e10-cards-c412-duplicates-c065.")
row("e2-cards-numbers", "cards: every number appears in the card's lesson", "course/modules/M/M2/cards.json", "PASS",
    f"`{S}/cards_mech_r10.py` against the lesson text extracted by `{S}/lesson_text_r10.py`: 0 numbers (excluding 0,1,2,3,10) missing from the lesson text, across all 397 cards.")
row("e2-cards-locators", "cards: lesson page exists for every card", "course/modules/M/M2/cards.json", "PASS",
    "Every card's lesson id is one of L01-L24 with a page (cards_mech_r10.py reports no 'no lesson text' problem; check_pages PASS).")
row("e2-cards-grades", "cards: grades and bases", "course/modules/M/M2/cards.json", "PASS",
    f"`{S}/cards_mech_r10.py`: no grade C card without basis; no grade T card with basis; no basis without grade. Changed grades: none. Grade T for M2-c412 is precise (proof cited to Lesson 6, Theorem 2.2, under named Assumption 1.1).")
carry("e2-cards-L01", "cards L01", "course/modules/M/M2/cards.json (L01); L01.html",
      "cards with lesson L01 and course/modules/M/M2/L01.html", "Full read of all L01 cards this round (no change): sequence and limit claims checked against the definitions; lab numbers N = 1000 and 9.990010e-04 recomputed.")
carry("e2-cards-L02", "cards L02", "course/modules/M/M2/cards.json (L02)",
      "cards with lesson L02 and L02.html", "Full read this round: sum/product/quotient laws and the counterexamples (Remark 3.1, Misconceptions) checked; Lab 1 closed-form values 6/55 and 32/110 and 54/132 recomputed from (n+2)/(n(n+1)).")
row("e2-cards-L03", "cards L03", "course/modules/M/M2/cards.json (L03)", "PASS",
    f"Changed card M2-c027 re-read against L03 section 1 Definition 1.1 (text: 'The value f(a), if it exists, plays no role in the limit at a'): match. Other L03 cards read in full; Lab 1 values 0.999800 and 2.000200 (gap 1.000400) recomputed. Evidence: card entries and L03.html text ({S}/cards_mech_r10.out).")
row("e2-cards-L04", "cards L04", "course/modules/M/M2/cards.json (L04)", "PASS",
    "Changed card M2-c047 re-read against L04 Lab 1 (predicted and printed text: error 3h + h^2; error divided by h is 3 + h, 3.000001 at h = 1e-6): match. Other L04 cards read in full, including M2-c050 (Q(0.001) = 3.003001 = 3 + 3h + h^2 at h = 0.001).")
row("e2-cards-L05", "cards L05", "course/modules/M/M2/cards.json (L05)", "PASS",
    "Full read this round: product, quotient and chain rule cards, and the central-difference expansion of x^3 ((1+h)^3-(1-h)^3)/(2h) = 3 + h^2 recomputed. Values 95.0625, 32.0625, 29/49 recomputed, and the central-difference errors at h = 1e-4 recomputed as 2.3499e-07, 3.3285e-10, 8.5501e-07 (page: 2.35e-07, 3.33e-10, 8.55e-07).")
carry("e2-cards-L06", "cards L06", "course/modules/M/M2/cards.json (L06)",
      "cards with lesson L06 and L06.html", "Full read this round: Rolle M2-c065 and MVT M2-c066 hypotheses carried (Assumption 2.1); M2-c072 x^3 on [0,1] gives c = 1/sqrt(3) (recomputed); Lab 1 grid counts 8 of 16 and 16 of 16 match L06 lines 95-96.")
carry("e2-cards-L08", "cards L08", "course/modules/M/M2/cards.json (L08)", "cards with lesson L08 and L08.html", "")  # replaced below
rows.pop()  # L08 is a FAIL row (duplicate card M2-c412); written explicitly below
row("e2-cards-L08", "cards L08", "course/modules/M/M2/cards.json (L08)", "FAIL",
    "L08 cards read in full this round. Taylor/Lagrange cards (M2-c097..c114) re-derived: xi = 1 - (1-x)^(1/(n+2)) (c102), ratio 2^(n+2)(1-x) (c104), bound x^(n+1)/(1-x)^(n+2) and its 1/2 threshold (c109, c110), R_1(0.9) = 8.1 with xi = 0.535841 (c107). New card M2-c412 restates Rolle's theorem with the content of M2-c065 (L06 Theorem 2.2): same hypotheses and same conclusion, only the assumption label differs.",
    "Delete the entry with id M2-c412 from course/modules/M/M2/cards.json (M2-c099 already covers Theorem 1.2 in L08). See e10-cards-c412-duplicates-c065.")
carry("e2-cards-L09", "cards L09", "course/modules/M/M2/cards.json (L09)", "cards with lesson L09 and L09.html", "Full read this round: U_n = (n+1)(2n+1)/(6n^2), L_n, U_n-L_n = 1/n; U_128 = 0.33724976 and L_128 = 0.32943726 (recomputed); Lab 1 part B mesh 0.19 and U-L 0.15933400 (L09 lab output); midpoint error -0.00130208 at n=8 (recomputed 680/2048 - 1/3).")
carry("e2-cards-L11", "cards L11", "course/modules/M/M2/cards.json (L11)", "cards with lesson L11 and L11.html", "Full read this round: 1/60 = 2!3!/6! and 1/30 (c151); substitution values 8/3 (c154) and 3/2 (c155) recomputed; Lab 1 part A midpoint 1/60 (c156).")
carry("e2-cards-L12", "cards L12", "course/modules/M/M2/cards.json (L12)", "cards with lesson L12 and L12.html", "Changed card M2-c177 re-read against L12 Misconception 1 (truncation error exactly 1/b, value reached only in the limit): match. Other L12 cards read in full; H_16384 - 1 = 9.28130671 recomputed as an exact float sum (matches the lesson's printed value and exceeds m/2 = 7 at m = 14).")
carry("e2-cards-L13", "cards L13", "course/modules/M/M2/cards.json (L13)", "cards with lesson L13 and L13.html", "Full read this round: Theorems 2.1/2.2 error forms, Corollary 4.1 optimal step 2 sqrt(delta/M) and value 2 sqrt(M delta), and the c187 cubic-root step recomputed; exp error intervals [0.0135914, 0.0137280] and [4.4854e-5, 4.5760e-5] recomputed from e^0.99 and e^1.01; ratio intervals 9.990-10.101 and 98.91-101.11 recomputed.")
carry("e2-cards-L14", "cards L14", "course/modules/M/M2/cards.json (L14)", "cards with lesson L14 and L14.html", "Full read this round: dual-number rules (c203, c219), adjoints x1-bar = 2 + cos 1 = 2.540302306 (c210), Example 4.1 f(2) = 15.232761 and f'(2) = 21.731771 recomputed by hand.")
carry("e2-cards-L15", "cards L15", "course/modules/M/M2/cards.json (L15)", "cards with lesson L15 and L15.html", "New card M2-c413 re-read this round against L15 section 3 (continuity = limit exists and equals f(a)): match (see e10-cards-c413-new-L15). Lab 1 values 0.500000 and 0.3849 and f(1/n,1/n) = 1/(2n) (c234) match L15 lab output lines 115-120.")
carry("e2-cards-L16", "cards L16", "course/modules/M/M2/cards.json (L16)", "cards with lesson L16 and L16.html", "Full read this round: F_x = 2xy + y e^(xy), F_y = x^2 + x e^(xy) at (1,2): 18.778112 and 8.389056 recomputed.")
carry("e2-cards-L17", "cards L17", "course/modules/M/M2/cards.json (L17)", "cards with lesson L17 and L17.html", "Full read this round: gradient (1, 1.8775826), length 2.1272791, angle 61.96 deg, and the max-norm bound 2.8775826 (c258) recomputed; Lab 1 prints 62 deg as the sampled maximum (L17 line 113).")
carry("e2-cards-L18", "cards L18", "course/modules/M/M2/cards.json (L18)", "cards with lesson L18 and L18.html", "Full read this round: Jacobian [[2,-4],[4,2]] and remainder (s1^2 - s2^2, 2 s1 s2) of length |h|^2 (c270) recomputed; f = x^2 y/(x^2+y^4) directional derivative sin theta (c276) recomputed.")
carry("e2-cards-L19", "cards L19", "course/modules/M/M2/cards.json (L19)", "cards with lesson L19 and L19.html", "Full read this round: Hessian [[6,8],[8,4]] (c281) and Lab 1 closed-form entries 0.474680, 1.898721, 0.412180, 2.148721, 1.000000 (c287) recomputed.")
carry("e2-cards-L20", "cards L20", "course/modules/M/M2/cards.json (L20)", "cards with lesson L20 and L20.html", "Full read this round: double integral 5/3 (c296), iterated integrals 2x+2x^2 and y/2+1/3 (c298), midpoint sums 3/2, 13/8, 53/32 (c301) recomputed.")
carry("e2-cards-L21", "cards L21", "course/modules/M/M2/cards.json (L21)", "cards with lesson L21 and L21.html", "Full read this round: slope -0.75 on the circle (c311), dx/dy at (1,0) (c317), Lab 1 root y = 0.6823278 of y^3+xy-1 and slope -0.2846931 (c314) recomputed.")
row("e2-cards-L07", "cards L07", "course/modules/M/M2/cards.json (L07); L07.html Lab 1 part C", "PASS",
    "Full read this round: M2-c084 (9/70, f(3/10) = 10/7), M2-c085 (x^11/(1-x) = 2.5307e-6), M2-c086 (error -2048 at x = 2, degree 10 = 2^11 with sign) recomputed; c079 f''(1/2) = 16 and f'''(1/2) = 96 recomputed.")
row("e2-cards-L10", "cards L10", "course/modules/M/M2/cards.json (L10); L10.html Theorem 1.2, Proof of Theorem 2.1, Proposition 4.1", "PASS",
    f"M2-c411 (MVT as used in L10) re-read: hypotheses (continuous on [p,q], differentiable on (p,q), Assumption 2.1) match L10 Theorem 1.2. Lab 1 values for c139/c140 match L10 lab output (lines 120-141; the lab's F is the antiderivative and sums are of f = F', as the card says). Integrals 1/2, -1 and 1/2 recomputed. Also {S}/card_numbers_r10.out: L_128 and U_128 of 3x^2-2 (-1.01168823, -0.98825073), U-L = 3/128 exact.")
row("e2-cards-L22", "cards L22: re-read against the changed lesson", "course/modules/M/M2/cards.json (L22: c323-c337, c404); L22.html", "PASS",
    f"Full read this round of L22 cards: envelope theorem statements (c325), V = a^2/4 and V' = a/2 (c330), V(a) = a ln a - (a-1) and V' = ln a (c327), max-of-ax V(0) one-sided derivatives 1 and 0 (c332), ln central differences 0.40546511, 0.69314718, 1.09861229, 1.38629436 (c328, equal to ln a) recomputed. Byte-identical L22.html since 1e272e5a, so no re-verification of the lesson text is needed.")
row("e2-cards-L23", "cards L23: re-read against the changed lesson", "course/modules/M/M2/cards.json (L23: 24 cards); L23.html", "PASS",
    f"Changed card M2-c352 re-read (see e10-cards-changed). Recomputed P(0.04) = 108110.895779, P'(0.04) = -851466.739529, P''(0.04) = 8376648.511919, P(0.03) = 117060.41 (117060), first-order error 4.037716e+02 and P(0.05) = 100000 (`{S}/card_numbers_r10.out`).")
carry("e2-cards-L24", "cards L24", "course/modules/M/M2/cards.json (L24: 18 cards); L24.html", "cards with lesson L24 and L24.html", "Full read this round: Proposition 4.2/4.3 minimisers 2 sqrt(delta/M_2) and (3 delta/M_3)^(1/3) recomputed; with delta = 2.22e-16 and M = e they give 1.8e-8 and 6.3e-6 (c370); Lab 1 part B values 1.406e-01 and 1.359e-05 consistent with (e/2)h; c196 ratio 32.6 and c197 ratio 301 recomputed.")
carry("e2-cards-L19-L21-untouched-proof", "cards L19-L21 unchanged", "course/modules/M/M2/cards.json; L19.html-L21.html", "cards M2-c280..c322 (L19-L21) and L19.html-L21.html", "No card entry of L19-L21 is among the changed or new ids (cards_delta_r10.out: changed M2-c027, c047, c177, c352; new M2-c412, c413).")
row("e3-cards-whole-set-mechanical", "cards: whole-set mechanical checks", "course/modules/M/M2/cards.json", "PASS",
    f"`{S}/cards_mech_r10.py`: 397 cards, 0 missing numbers, 52 similarity pairs listed and reviewed one by one, grade and basis rules hold. The one semantic duplicate found by the review (M2-c412 / M2-c065) is recorded in e10-cards-c412-duplicates-c065, not here.")
row("e5-alternatives", "alternative correct implementations pass", "ledgers/M2/scripts/M2-e-r10/alts_r10/*.py", "PASS",
    f"Five new alternatives in {S}/alts_r10/ (generated by make_alternatives_r10.py): Richardson central, complex-step AD, exact rational price, numpy sensitivities, effective-step fsum (with zero guard). Each 50/50 on seeds 0-49 ({S}/alternatives_r10.out).")
row("e5-mutants-new-r5", "round-5 new mutants killed", "ledgers/M2/mutants/", "PASS",
    "ledgers/M2/mutants/r5_01..r5_04 exist and are killed (lines 'KILLED r5_01..r5_04' in mutate_graders_M2_r10.out).")
row("e5-twins-alone", "lab twins alone under python -I -W error", "tests/labs/M2/*.py (27)", "PASS",
    f"27 of 27 exit 0 ({S}/twins_alone_r10.out).")
row("e5-fragment-gate-set", "gate set run this round", "repo gates for M2", "PASS",
    "Run this round, all PASS: check_pages, check_dag, check_projects, run_graders (50 seeds), run_labs (project and unit), page_smoke project, pytest collect (89) and seeds 0-3, ruff check and format, mypy labs (27 files), mypy grader strict (3 files), pytest labs -k M2, verify_refs offline and unit, mutate_graders (171/171).")
carry("e6-card-M2-c349", "cards: hypotheses carried (Proposition 3.2)", "course/modules/M/M2/cards.json, M2-c349; L23.html Proposition 3.2",
      "cards.json entry M2-c349 and L23.html", "Entry identical in cards_delta_r10.out (391 identical). Hypotheses (y0 > -1, Assumption 2.1, positive cash flows) match L23 Proposition 3.2; P''' < 0 used in the proof.")
carry("e6-card-M2-c350", "cards: hypotheses carried (Proposition 3.3)", "course/modules/M/M2/cards.json, M2-c350; L23.html Proposition 3.3",
      "cards.json entry M2-c350 and L23.html", "Entry identical (391 identical). Hypotheses match Proposition 3.3.")
carry("e6-card-M2-c363-c365", "cards: changed L24 proposition and remark cards", "course/modules/M/M2/cards.json, M2-c363, M2-c364, M2-c365; L24.html",
      "cards.json entries M2-c363, c364, c365 and L24.html", "Entries identical. Minimisers 2 sqrt(delta/M_2) and (3 delta/M_3)^(1/3) recomputed (see e2-cards-L24).")
carry("e6-card-M2-c404-c405", "cards: changed assumption cards", "course/modules/M/M2/cards.json, M2-c404, M2-c405",
      "cards.json entries M2-c404 and M2-c405", "Entries identical. Assumption statements (ln a derivative 1/a; e^x derivative e^x) match the lesson assumption paragraphs.")
carry("e6-card-M2-c408-c409", "cards: new cards", "course/modules/M/M2/cards.json, M2-c408 (L08), M2-c409 (L16)",
      "cards.json entries M2-c408 and M2-c409", "Entries identical. M2-c408 states Assumption 1.1 of L08 (extreme value theorem, assumed); M2-c409 states the exp derivative assumption of L16.")
row("e6-instances-50", "instances over seeds 0-49", "course/modules/M/M2/grader/instance.py", "PASS",
    f"See e2-grader-instances: `{S}/instances_r10.py` over 100 draws (seeds 0-49 and shifted seeds): all valid, answers distinct.")
row("e6-mutants-new-v6e", "three or more new student-error mutants killed", "ledgers/M2/mutants/v6e_01..v6e_04", "PASS",
    "v6e_01..04 are among the 171 killed in mutate_graders_M2_r10.out.")
carry("e6-L24-E3-unrounded-difference", "prose numbers vs unrounded values (lesson L24 Problem E3)", "course/modules/M/M2/L24.html E3 solution and interpretation",
      "course/modules/M/M2/L24.html", "L24.html is byte-identical since 1e272e5a (git diff --quiet over L22-L24 returned 0 this round).")
carry("e7-L22-L24-lesson-numbers", "lab numbers in changed L22-L24 prose", "course/modules/M/M2/L22.html, L23.html, L24.html",
      "course/modules/M/M2/L22.html, L23.html, L24.html", "Those files are byte-identical; numbers in the L23 and L24 cards re-checked this round (see e2-cards-L23 and e2-cards-L24).")
row("e7-round7-mutants-v7e", "new student-error mutants (at least 3)", "ledgers/M2/mutants/v7e_01..v7e_04", "PASS",
    "v7e_01..04 are among the 171 killed in mutate_graders_M2_r10.out.")
row("e7-alternatives-new", "alternatives: correct engines not over-constrained", "ledgers/M2/scripts/M2-e-r7/alts_new and M2-e-r9/alts_r9", "PASS",
    f"alt_r7_a, alt_r7_b, alt_r9_a, alt_r9_b, alt_r9_c each 50/50 on the current suite ({S}/alternatives_prior_r10.out).")
row("e7-twins-27-alone", "twins alone under python -I -W error", "tests/labs/M2/*.py (27)", "PASS",
    f"27 of 27 exit 0 ({S}/twins_alone_r10.out).")
row("e8-ad-float-return-contract", "ad_derivative returns a float (round-8 FAIL, now fixed)", "course/modules/M/M2/grader/test_project.py (float check in forward-mode tests and the zero-derivative tests)", "PASS",
    "test_forward_mode_matches_the_analytic_derivative requires isinstance float; test_constant_function_has_zero_derivative requires float 0.0; mutant v8e_05 killed (mutate_graders_M2_r10.out).")
row("e9-delta-read", "full read of the round-9 to round-10 delta in the slice", "course/modules/M/M2/cards.json, grader/test_project.py, project.html", "PASS",
    f"Every hunk of `git diff 1e272e5a..47a36d8c -- course/modules/M/M2 tests/labs/M2` read: cards.json (4 changed entries, 2 new), test_project.py (two new float tests at the origin, plus the count 87 to 89), project.html (Lab 1 and Lab 3 hypothesis wording, Grading mode 89, Richardson wording, tolerance wording). No lesson, lab twin or reference file changed.")
row("e9-ad-int-zero-at-origin", "ad_derivative returns a float (stated type) at every point, including x = 0", "course/modules/M/M2/grader/test_project.py test_ad_derivative_at_the_origin_returns_a_float",
    "PASS",
    f"Round-9 FAIL is fixed: new test test_ad_derivative_at_the_origin_returns_a_float (lines ~501-508) requires float 0.0 at x = 0. v9e_04 is killed by it in {S}/mutate_graders_M2_r10.out.")
row("e9-fd-int-zero-at-origin", "fd_derivative returns a float (stated type) at every point, including a zero forward numerator at x = 0", "course/modules/M/M2/grader/test_project.py test_forward_zero_numerator_at_the_origin_returns_a_float",
    "PASS",
    f"Round-9 FAIL is fixed: new test test_forward_zero_numerator_at_the_origin_returns_a_float (lines ~361-372) requires float 0.0. v9e_05 is killed by it in {S}/mutate_graders_M2_r10.out.")
row("e9-mutants-new-v9e", "new student-error grader mutants (at least 3)", "ledgers/M2/mutants/v9e_01..v9e_05", "PASS",
    "v9e_01..05 are killed in the 171-mutant gate run (v9e_01 by test_hessian_matches_the_analytic_hessian, v9e_02 by test_named_ratios, v9e_03 by test_second_derivative..., v9e_04 and v9e_05 by the new origin tests).")
row("e9-alternatives-r9", "new alternative correct implementations (over-constraint check)", "ledgers/M2/scripts/M2-e-r9/alts_r9/", "PASS",
    f"alt_r9_a, alt_r9_b, alt_r9_c 50/50 against the current suite ({S}/alternatives_prior_r10.out).")

# ---------- rows new in round 10 ----------
row("e10-cards-c412-duplicates-c065", "cards: no duplicate cards (semantic)", "course/modules/M/M2/cards.json, M2-c412 (L08) and M2-c065 (L06)", "FAIL",
    "M2-c065 (L06, Theorem 2.2): 'Hypotheses: f is continuous at each point of [a, b] with a < b, differentiable at each point of (a, b), f(a) = f(b), and Assumption 2.1 holds for f on [a, b]. Then there is c with a < c < b and f'(c) = 0.' M2-c412 (L08, Theorem 1.2): 'Assuming Assumption 1.1, if h is continuous on [p, q] with p < q, differentiable on (p, q), and h(p) = h(q), then there is c with p < c < q and h'(c) = 0.' Same theorem, same hypotheses and conclusion, only the assumption label and the letters differ. L08 lines 32-33 state the theorem as the special case of Lesson 6's Rolle, and M2-c099 already asks how L08 uses it, so M2-c412 is a duplicate card (rule 2.7 and verifier rule 10: no duplicate cards).",
    "Delete the entry with id M2-c412 from course/modules/M/M2/cards.json (keep M2-c065 and M2-c099). The id gap is allowed (ruling 2).")
row("e10-cards-changed-c027-c047-c177-c352", "changed cards re-read against the current lesson text", "course/modules/M/M2/cards.json M2-c027 (L03), M2-c047 (L04), M2-c177 (L12), M2-c352 (L23)", "PASS",
    "M2-c027 matches L03 Definition 1.1 and section 1 text ('The value f(a), if it exists, plays no role in the limit at a'). M2-c047 matches L04 Lab 1: Q(h) = 3 + 3h + h^2, error 3h + h^2 = 3.000001e-6 at h = 1e-6, error/h = 3.000001 = 3 + h. M2-c177 matches L12 Misconception 1 (truncation error 1/b, positive at every finite b, value reached only in the limit). M2-c352 matches L23 Misconception 1 and Lab 1 Part C ('a difference of -15 cents at +0.01'); grade C with basis 'Lab 1 (SIMULATED bond)' matches the lab. Lab numbers rechecked in {S}/card_numbers_r10.out.")
row("e10-cards-c413-new-L15", "new card: continuity definition in Section 3 of L15", "course/modules/M/M2/cards.json M2-c413 (L15)", "PASS",
    "M2-c413 (no grade, a definition card like M2-c027): 'f is continuous at a when the limit of f(x) as x tends to a exists and equals f(a): for every epsilon > 0 there is delta > 0 with |f(x) - f(a)| < epsilon whenever x is in U and 0 < |x - a| < delta.' L15.html section 3 says continuity at a in U is 'the statement that the limit as x tends to a exists and equals f(a)', with the limit defined by |f(x) - L| < epsilon for x in U with 0 < |x - a| < delta. Match; not a duplicate of M2-c226 (sequences) or M2-c020 (sequential definition, L02).")
row("e10-sin-ratio-range", "central-estimate ratio claim (3.9999842 to 3.9999851)", "course/modules/M/M2/project.html Tolerances; grader/test_project.py test_central_error_is_at_least_of_order_h_squared", "PASS",
    f"`{S}/sin_ratio_r10.py` over both instances of seeds 0-49 (100 instances): min 3.9999841904, max 3.9999850561; rounded to seven places 3.9999842 and 3.9999851, exactly the page's claim. Output {S}/sin_ratio_r10.out.")
row("e10-hours-estimate-under-ruling", "hours: verifier estimate vs declared 60 h", "course/modules/M/M2/project.html time budget", "PASS",
    "Verifier estimate of the project work for a competent student: Rung 1 about 2-4 h, Rung 2 about 2-4 h, engine and edge cases 14-24 h, note 6-10 h, self-check 2-4 h, total roughly 26-46 h, central about 35 h. That is more than 30 % below 60 h at the centre, which would fail the 2.6 hours rule, but architect ruling 'hours are design targets (fail only arithmetic inconsistencies between hub split and lesson hours)' governs, and the arithmetic is consistent (e2-hours-arithmetic). Recorded as PASS under the ruling; the estimate is a note, not a finding.")
row("e10-spec-clarifying-questions", "2.6 spec: questions a student would need to ask", "project.html Rung 3 Specification", "PASS",
    "No blocking question. Signatures, return types, instance keys, the three ValueError conditions, the test count, the browser limit (120 s, python.js TIMEOUT_MS = 120000) and the report files are all stated. The one place a student might pause is the kink line in run_report.py (backward quotient), which the page resolves explicitly as fd_derivative(f, x - h, h, 'forward').")
row("e10-links-anchors", "internal links and anchors of project.html", "course/modules/M/M2/project.html", "PASS",
    "23 distinct href targets checked by parsing: all in-page anchors and sibling files exist (L14.html, L19.html#def-hessian, L13.html#def-finite-difference-derivative, index.html#placement, L24.html, index.html). No broken link.")
row("e10-alternatives-r10", "five new alternative correct implementations of different styles pass", "ledgers/M2/scripts/M2-e-r10/alts_r10/", "PASS",
    f"alt1 Richardson central, alt2 complex-step AD (page allows it), alt3 exact rational price (page allows it), alt4 numpy sensitivities (different summation order), alt5 effective-step fsum: each 50/50 seeds 0-49 ({S}/alternatives_r10.out).")
row("e10-mutants-r10-new", "five new student-error mutants of my own, killed", "ledgers/M2/mutants/w10e_01..w10e_05", "PASS",
    f"Written by {S}/make_new_mutants_r10.py; killed in the mutate run: w10e_01 price discounts one period short (test_price_is_the_half_even...), w10e_02 scheme accepted in any case (test_unknown_scheme...[Central]), w10e_03 central forgets factor two (test_central_difference...), w10e_04 duration uses rounded price (test_named_ratios...), w10e_05 mixed Hessian over h^2 (test_hessian_matches...). Mutate tool output: {S}/mutate_graders_M2_r10.out.")

# ---------- mutants list ----------
mut_lines = pathlib.Path(root / S / "mutate_graders_M2_r10.out").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mut_lines:
    if not line.startswith("KILLED "):
        continue
    body = line[len("KILLED "):]
    name, _, rest = body.partition(": ")
    desc, _, killed = rest.rpartition(" -> ")
    killed = re.sub(r"\s*\(seed \d+\)$", "", killed).strip()
    mutants.append({"id": name, "description": desc.strip(), "killed_by": killed})

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate row ids"
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"

fragment = {
    "unit": "M2",
    "slice": "e",
    "round": 10,
    "verifier": "Haiku 5.5 independent verifier (round 10, slice e)",
    "pin": PIN,
    "base": BASE,
    "checkout": str(root),
    "scratch": "/tmp/m2e_r10_* (grader alternatives, text extraction, prior alternatives); all backing scripts are in ledgers/M2/scripts/M2-e-r10/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        f"Round 10, slice e (project.html, grader/*, project labs, all 397 M2 cards, mutants, alternatives), pin {PIN}, previous pin {BASE}. Delta: cards.json (M2-c027, c047, c177, c352 changed; M2-c412, c413 new), grader/test_project.py (two float tests at the origin, count 87 to 89), project.html (Lab 1 and Lab 3 hypothesis wording, grading-mode count and wording, Richardson wording). Lessons, lab twins, reference, starter and instance files are byte-identical to the previous pin.",
        "Round-9 FAILs e9-ad-int-zero-at-origin and e9-fd-int-zero-at-origin are fixed by the new origin tests and are PASS (v9e_04 and v9e_05 killed).",
        "One new FAIL: M2-c412 duplicates M2-c065 (Rolle's theorem stated twice, same hypotheses and conclusion). Fix: delete M2-c412.",
        "Mutants: 171 of 171 killed (166 existing, 5 new student-error mutants w10e_01..05). No survivor.",
        "Alternatives: 22 alternative correct implementations run on seeds 0-49 against the current suite, all 50/50 (round-10 five, round-3 five, rounds 5-9 twelve). The round-10 alt5 first failed on its own ZeroDivisionError (dividing by a represented step of zero at h = 1e-300) and was fixed in the alternative, not the suite.",
        f"Directory {S}/ already contained tracked files from commit f42f4329 that this verifier did not write (for example alts/altA-C.py, cards_r10.py, labels_r10.py, make_mutants_r10.py, write_fragment_r10.py, run_alts_r10.sh). They are not cited. page_smoke_project.out in that directory was overwritten by my run and then restored with git checkout; my output is in page_smoke_project_r10.out.",
        "The fragment ledgers/M2/M2-e.json replaces the previous fragment at this path. Scripts under ledgers/M2/scripts/M2-e-r10/ are the ones this verifier ran (names ending _r10 or M2-e-r10 outputs).",
    ],
    "summary": (
        f"Slice e round 10: {verdict}. {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE of {len(rows)} rows. "
        f"Mutants {len(mutants)}/{len(mutants)} killed. FAIL: M2-c412 duplicates M2-c065 (delete M2-c412). All gates re-run and PASS: check_pages, check_dag, check_projects, run_graders 50/50, run_labs 27/27 and project 3/3, page_smoke project, pytest 89 collected and passing (seeds 0-3), ruff, mypy labs and grader strict, pytest labs, verify_refs offline and live."
    ),
}
out = root / "ledgers/M2/M2-e.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), counts, "mutants", len(mutants), "verdict", verdict)
