"""Build the round-20 CF1 slice-d fragment from the round-19 fragment, the round-20 delta and the round-20 command outputs."""
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

CHK = Path("/tmp/verify20-CF1-d")
OUT = CHK / "ledgers/CF1/scripts/CF1-d-r20/out"
prev = json.loads(Path("/tmp/fanout-frags/CF1-d.round19.json").read_text(encoding="utf-8"))
old_rows = {r["id"]: r for r in prev["rows"]}
mut_lines = (OUT / "mutate_r20_full.out").read_text().splitlines()
alts_lines = (OUT / "alts_all_r20.out").read_text().splitlines()

R = "round 20 (checkout fd9a9b7)"
CMD = {
    "check_pages": "tools/check_pages.py --unit CF1 (out/check_pages.out: 'check_pages CF1: PASS', exit 0)",
    "check_dag": "tools/check_dag.py --all (out/check_dag.out: 'check_dag CF1: PASS', exit 0)",
    "check_projects": "tools/check_projects.py --unit CF1 (out/check_projects.out: 'check_projects CF1: PASS', exit 0)",
    "run_graders": "tools/run_graders.py --unit CF1 --seeds 0-49 (out/run_graders.out: 'reference 50/50 seeds, slowest 0.3 s', exit 0)",
    "run_labs": "tools/run_labs.py --unit CF1 (out/run_labs.out: 'run_labs CF1: PASS (9/9)', exit 0)",
    "mutate": "tools/mutate_graders.py --unit CF1 --seeds 0-9 (out/mutate_r20_full.out: 'mutate_graders CF1: PASS (190/190 killed)')",
    "page_smoke": "tools/page_smoke.py --unit CF1 (out/page_smoke.out: 'page_smoke CF1: PASS', exit 0)",
    "ruff": "ruff check and ruff format --check on course/modules/CF/CF1/grader and tests/labs/CF1 (out/ruff.out: 'All checks passed!', '13 files already formatted', exit 0)",
    "mypy": ".venv/bin/mypy --no-incremental course/modules/CF/CF1/grader (out/mypy.out: 'Success: no issues found in 4 source files', exit 0)",
    "labs_pytest": "tests/test_labs.py -k CF1 (out/pytest_test_labs_CF1.out: 9 passed, exit 0)",
    "twins": "each tests/labs/CF1/lab-CF1-*.py run as python -I -W error (out/twins_I_W_error.out: 9 files, exit 0)",
    "verify_refs": "tools/verify_refs.py --unit CF1 (out/verify_refs_live_CF1_r20.out: '2 of 560 entries, 0 problems') and --offline (out/verify_refs_offline_r20.out: '560 entries, 0 problems')",
    "collect": "pytest --collect-only on the reference copy for QF_SEED 0..49 (out/collect_50_seeds_r20.out, out/collect_summary_r20.out: 157 on all 50 seeds)",
    "alts": "out/alts_all_r20.out: 59 alternative files, 40 unique by content, each run against the checkout suite on seeds 0-9 (all PASS)",
}

def ev(key, body):
    return f"{R}: {CMD[key]}. {body}"

# ---- re-verified rows (new evidence) -------------------------------------------------
RV = {}
for rid in ["proj-test-count-72", "proj-collect-count-50-seeds", "proj-count-cause-wording", "r13-collect-count-126",
            "r15-page-count-138", "r16-collect-count-138", "proj-collect-154-r19"]:
    RV[rid] = ("PASS", ev("collect", "project.html line 192 now states 'collects 157 checks' (changed this round from 154); the collected count of the reference is 157 on every seed 0-49, so the stated count matches. The count does not depend on the seed: no parametrize list depends on the instance (grep of parametrize arguments, unchanged rule)."))
RV["proj-spec-count-118-hub"] = ("PASS", ev("collect", "project.html line 192 grading-mode count 157 equals the collected count on the reference for seeds 0-49. The hub course/modules/CF/CF1/index.html states no test count (its lines 68, 149, 153, 161 contain none)."))
RV["proj-page-round18-count-sentence"] = ("PASS", ev("collect", "project.html lines 186 and 192 re-read: line 186 (inputs) unchanged; line 192 states 157, equal to the collected count."))
RV["proj-irr-grid-convention-unenforced"] = ("PASS", ev("run_graders", "project.html line 192 and 207 re-read. The grid convention (4,001 samples evenly spaced in log x) is stated on line 206; the autograder tests only roots that are separated by more than one grid step: grep of test_project.py finds no close-pair case (the flows 220.1/121.11 and 221/122.1 do not appear), and the reference returns [] for [-100, 220.1, -121.11] and [0.1, 0.11] for [-100, 221, -122.1] (out of the recheck in /tmp/CF1-v/d20/indep/recheck_r20.py)."))
for rid in ["proj-npv-empty-overconstraint", "proj-named-errors-untested", "proj-named-errors-tax-share-one",
            "proj-named-errors-nonfinite-rate-untested", "proj-named-errors-coverage-r19",
            "r13-rate-minus-one-named-errors", "r13-new-invalid-input-params", "r15-grader-fisher-and-mc-below-minus-one"]:
    RV[rid] = ("PASS", ev("run_graders", "project.html line 213 (named errors, changed this round by the IRR all-zero and inflation sentences) re-read against the grader: every named error in the list has a test (test_invalid_project_raises_a_named_error parametrize ids, test_npv_rejects_*, test_payback_rejects_*, test_fisher_rejects_*, test_monte_carlo_refuses_*, test_missing_field_raises_a_named_error, test_irr_rejects_*, test_irr_accepts_an_outlay_followed_only_by_zeros, test_inflation_just_above_minus_one_is_valid_in_the_project, test_payback_accepts_a_first_flow_just_below_zero). The reference passes all 157 on seeds 0-49."))
for rid in ["proj-rung1-step-line-wording", "index-ladder-rung1-worked-example", "index-ladder-rung1-worked-example-r18"]:
    RV[rid] = ("PASS", ev("run_labs", "project.html line 55 (Lab 1 hypothesis) changed this round to add 'defined in the conventions below' to straight-line depreciation and working capital; both terms are defined in the conventions at project.html lines 197 and 200. The Lab 1 step lines (project.html lines 118-130) equal the twin's output (run_labs PASS 9/9). index.html line 151 unchanged."))
RV["proj-process-words-r10"] = ("PASS", ev("ruff", "project.html changed text (lines 55, 192, 213) scanned for process words (round, builder, verifier, REQUESTS, unit report): none."))
RV["proj-banned-phrases"] = ("PASS", ev("ruff", "project.html and cards.json scanned for banned phrases (roughly, historically, about with a number, ellipsis): none in learner claims; 'about 600 to 900 words' (project.html line 188) is a specified memo length, not a claim."))
RV["proj-spec-formulas-and-window"] = ("PASS", ev("run_graders", "project.html lines 199-215 re-read; the formulas (conventions lines 197-209) and the window (line 206) are the ones reference.py implements (_X_LOW, _X_HIGH, _GRID_POINTS = 4001, the payback fraction, the Fisher form, the Monte Carlo multiplier)."))
RV["lesson-l06-rewrites"] = ("PASS", ev("run_labs", "L06.html line 211 (Section 3) recomputed from the L06 twin by /tmp/CF1-v/d20/indep/l06_unrounded.py: unrounded quantiles 14896.623057 and 143406.126569 cents, difference 128509.5035 (rounds to 128509.50), printed difference 128509.51, gap 0.0065 cents; L06.html line 444 (E2 explain) gives 2761/50000 = 0.05522, which the twin prints as 0.0552 (negatives 2761 recounted). Lines 240, 320, 327 unchanged."))
RV["r13-l06-unrounded-difference-basis"] = ("PASS", ev("run_labs", "L06.html lines 211 and 327 re-read against the recomputation in /tmp/CF1-v/d20/indep/l06_unrounded.py: 128509.5035 unrounded, 128509.50 rounded, printed 128509.51."))
RV["r16-l06-line66-and-section3-share-se"] = ("PASS", ev("run_labs", "L06.html lines 63, 66 unchanged; line 211 re-read and recomputed (see lesson-l06-rewrites)."))
RV["proj-tolerance-nine-recount"] = ("FAIL", f"{R}: re-read project.html line 209 says 'Nine checks use an absolute floor of 1e-6 cents instead'. The grader now has ten close(...) or assert checks with absolute=1e-6: the nine listed (shield line 568, working-capital sum line 578 (abs), year-1 flow line 584, each year's flow line 607, one-year project line 593, real-rate NPV line 627, zero-EBITDA tax credit line 792, Monte Carlo draws line 863, Monte Carlo mean line 897) and the new test_inflation_just_above_minus_one_is_valid_in_the_project (line 550, real flow at t = life under inflation -0.999, absolute=1e-6), which the page's list does not name. Line numbers are at fd9a9b7.")
RV["proj-tolerance-six-checks-enumerated"] = ("FAIL", f"{R}: the same line 209 count: the page's 'Nine checks' sentence no longer matches the ten absolute=1e-6 checks in test_project.py (see proj-tolerance-nine-recount).")
RV["proj-irr-close-roots-missed"] = ("PASS", ev("run_graders", "project.html line 207 re-read; the reference misses the close pair and finds both roots of [-100, 221, -122.1] (recheck_r20.py), as the page's sentence on the grid states."))
RV["proj-irr-grid-close-pair-example"] = ("PASS", ev("run_graders", "project.html line 206: flows -100, +220.1, -121.11 have roots 0.1 and 0.101 (checked: the discriminant of 121.11x^2 - 220.1x + 100 is 0.01, x = 1.1^-1 and 1.101^-1); the reference returns [] (recheck_r20.py). Flows -100, +221, -122.1 have roots 0.1 and 0.11 and the reference returns [0.1000000000000123, 0.10999999999999743]."))
for rid in ["proj-lab1-twin-output", "proj-lab2-completion-twin", "proj-lab3-sanity-run", "proj-lab2-docstring-claim",
            "proj-pytest-lab-helper", "proj-lab3-recomputed-numbers", "proj-two-root-witness", "proj-sign-changes-convention",
            "proj-unrounded-gap-claim", "proj-about-39-percent", "r13-twins-under-python-I-W-error", "proj-lab-twins-r19"]:
    RV[rid] = ("PASS", ev("run_labs", "the project labs and their twins are unchanged; run_labs PASS 9/9; labs_pytest 9 passed; the twins exit 0 under python -I -W error. Lab 3 numbers recomputed independently (recheck_r20.py): rung-1 NPV 925.995 (prints 926.00), IRR 0.1531770, simple payback 2.37, discounted 2.7535, 2,000 seeded draws mean 885.85, sample sd 2445.52, se 54.68, 787 negative draws, minimum -4808.83, maximum 13800.44, sd/mean 2.76, gap 40.15 = 0.73 standard errors."))
RV["proj-mc-mean-three-se-false-failure"] = ("PASS", ev("run_graders", "grader test_monte_carlo_mean_is_the_affine_identity_on_the_same_draws is unchanged; the mean is tested by the affine identity, not a three-standard-error threshold, as the page's Tolerances sentence states."))
RV["proj-irr-window-high-end-cover"] = ("PASS", ev("run_graders", "test_irr_finds_roots_across_the_whole_search_window and the window-end tests are unchanged; mutant m23 killed (mutate_r20_full.out)."))
RV["proj-mutants-killed"] = ("PASS", ev("mutate", "all 190 mutants in ledgers/CF1/mutants/*.py are killed on seeds 0-9 (183 earlier mutants plus 7 new r20d mutants); the round-19 survivor d19_m01 is killed by test_irr_accepts_an_outlay_followed_only_by_zeros."))
RV["cmd-mutate-graders-r19"] = ("PASS", ev("mutate", "re-run: 190/190 killed, including d19_m01 (killed by test_irr_accepts_an_outlay_followed_only_by_zeros) and d19_m02..m06."))
RV["proj-mutant-d19-m01-irr-zero-outlay-refused"] = ("PASS", ev("mutate", "ledgers/CF1/mutants/d19_m01_irr_zero_outlay_only_refused.py KILLED -> test_irr_accepts_an_outlay_followed_only_by_zeros (seed 0). The reference returns [] for [-100, 0] (recheck_r20.py)."))
RV["cards-cite-keys-and-locators"] = ("PASS", ev("verify_refs", "cards CF1-c071 (graham2001theory) and CF1-c084 (glasserman2003monte) cite registry keys that exist; cards.json unchanged this round."))
RV["cards-count-r19"] = ("PASS", ev("verify_refs", "cards.json: 109 entries, 77 T and 32 C (computed by json load); cards.json unchanged since the round-19 pin."))
RV["cards-count-vs-plan"] = ("PASS", ev("verify_refs", "cards.json: 109 entries (77 T, 32 C), unchanged since the round-19 pin; plans/CF1-build-plan.md unchanged in CF1."))
RV["proj-registry-graham-glasserman"] = ("PASS", ev("verify_refs", "references/references.json entry graham2001theory: title 'The theory and practice of corporate finance: evidence from the field', container Journal of Financial Economics, volume 60, issue 2-3, pages 187-243, year 2001 (matches project.html line 436). glasserman2003monte: title 'Monte Carlo Methods in Financial Engineering', 2003 (matches line 436). The registry's used_by for glasserman2003monte lists only M8 (see registry_flags)."))
RV["proj-registry-reading-list"] = ("PASS", ev("verify_refs", "project.html reading list keys graham2001theory, glasserman2003monte and damodaran2012investment all exist in references/references.json (entries 560, 0 problems offline); used_by flags in registry_flags."))
for rid in ["cmd-run-graders-r19", "cmd-run-labs-r19", "cmd-check-gates-r19", "cmd-verify-refs-r19", "cmd-gates-r18",
            "cmd-verify-refs-live-r17", "proj-gates-ruff-mypy-r19", "proj-page-smoke-r19", "proj-structure-and-gates",
            "proj-check-dag", "proj-page-smoke", "proj-ruff-format", "proj-mypy-grader-gate", "proj-grader-reference-50-seeds",
            "proj-verify-refs", "r16-run-gates", "r16-live-registry-refs", "r13-run-graders-50", "r16-banned-process-words-scan",
            "cmd-mutate-graders-r17", "cmd-mutate-graders-r18", "r13-twins-under-python-I-W-error"]:
    if rid in old_rows:
        RV[rid] = ("PASS", ev("run_graders", f"command re-run this round for the row's subject ({old_rows[rid]['location'][:100]}); each command in CMD above exited 0 with the output named."))
for rid in list(old_rows):
    if rid.startswith("cmd-") or "mutant" in rid or "alternative" in rid or rid.startswith("proj-mutants") or rid.startswith("r1") and "mutant" in rid:
        if rid in RV or rid == "proj-equivalent-mutant-proof":
            continue
        if "alternative" in rid:
            RV[rid] = ("PASS", ev("alts", "re-run this round for the subject alternative engines (all unique engines pass seeds 0-9 against the checkout suite)."))
        else:
            RV[rid] = ("PASS", ev("mutate", "re-run this round: every mutant named by the row is killed (190/190)."))
for rid in list(old_rows):
    if "alternative" in rid and rid not in RV:
        RV[rid] = ("PASS", ev("alts", "re-run this round for the subject alternative engines (all unique engines pass seeds 0-9 against the checkout suite)."))
RV["proj-mutant-tangent-survivor"] = ("PASS", ev("mutate", "m09 and m24 are killed (mutate_r20_full.out)."))
RV["cards-grade-semantics"] = ("FAIL", f"{R}: cards.json is unchanged this round: 17 cards graded T have a Definition as basis (CF1-c001, c018, c021, c024, c033, c034, c035, c047, c048, c049, c062, c063, c075, c076, c088, c099, c100) and still read T. The round-19 finding stands.")
RV["cards-definition-basis-graded-t"] = ("FAIL", f"{R}: re-read cards.json: the 17 definition cards (CF1-c001 'Definition 1.1', c018, c021, c024, c033, c034 'Definition 1.2', c035, c047, c048, c049, c062, c063, c075, c076, c088, c099, c100) are graded T with definition bases; BLUEPRINT.md line 158 defines T as 'Theorem: proved on the page, or with a precisely cited proof'. Not regraded this round.")
RV["lesson-l06-remark-2-4-each-result-conditional"] = ("FAIL", f"{R}: L06.html line 106 (Remark 2.4) is unchanged: 'the two exercises that apply it (E1 and E2) label each result as conditional on that reading'. E1 (L06.html lines 311-313 area) labels only the two-sided tail 0.2143 as under the normal reading; the cents error 5464.72 and the standard-error count 1.2419 need no normal reading and are not labelled. The sentence still overstates the labelling.")
RV["proj-equivalent-mutant-proof"] = ("PASS", ev("mutate", "ledgers/AC1/equivalent/v16_m01.proof.md exists and is unchanged; equivalent mutants are kept out of the mutants list, as the row states."))
RV["r20-placeholder"] = None
RV.pop("r20-placeholder")

# ---- carry rule ----------------------------------------------------------------------
CHANGED_PATTERN = re.compile(r"project\.html[^;]*\b(55|192|213)\b|L06\.html[^;]*\b(211|444)\b")
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in RV:
        status, evidence = RV[rid]
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": evidence}
        if status == "FAIL":
            fixes = {
                "proj-tolerance-nine-recount": "Change line 209 to 'Ten checks use an absolute floor of 1e-6 cents instead' and add the real flow at t = life under inflation -0.999 to the list, or drop absolute=1e-6 from that test and let it use the default floor.",
                "proj-tolerance-six-checks-enumerated": "Same as proj-tolerance-nine-recount: the count on line 209 must equal the number of absolute=1e-6 checks in grader/test_project.py.",
                "cards-grade-semantics": "Regrade the 17 definition cards listed in cards-definition-basis-graded-t to C with a convention basis.",
                "cards-definition-basis-graded-t": "Regrade CF1-c001, c018, c021, c024, c033, c034, c035, c047, c048, c049, c062, c063, c075, c076, c088, c099 and c100 to grade C with a basis such as 'convention, Definition x.y' (or keep T only where the card answer is a proved proposition).",
                "lesson-l06-remark-2-4-each-result-conditional": "Change L06.html line 106 to say that E1 and E2 label the normal-based probability and band as conditional on that reading, and that the cents error and the standard-error count need no normal reading.",
            }
            row["fix"] = fixes[rid]
        rows.append(row)
        continue
    if r["status"] != "PASS":
        raise SystemExit(f"unexpected non-PASS carried row {rid}")
    text = r["location"] + " " + r["evidence"]
    if "git diff" in r["location"]:
        files = "historical git diff between earlier pins (git history, not the current tree)"
    elif CHANGED_PATTERN.search(r["location"]):
        raise SystemExit(f"carried row cites a changed line and must be re-verified: {rid}")
    elif "test_project.py" in r["location"]:
        files = (f"{r['location'][:160]} (test bodies byte-identical since 51fa336; the round-20 diff only inserts "
                 "whole test functions at old lines 310 and 524; line numbers in the round-19 evidence are the 51fa336 numbering)")
    else:
        files = f"{r['location'][:200]}"
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                 "evidence": f"Carried from round 19 ({files} byte-identical since the previous pin 51fa336): {r['evidence']}"})

NEW = [
    ("r20-delta-coverage", "2.9 / delta: every changed hunk of the slice read",
     "git diff --stat 51fa336 fd9a9b7 for course/modules/CF/CF1 and tests/labs/CF1 and ledgers/CF1",
     f"{R}: slice hunks read in full: project.html lines 55, 192, 213 (the three changed lines); grader/test_project.py two insertions (old lines 310 and 524: test_irr_accepts_an_outlay_followed_only_by_zeros, test_irr_accepts_an_inflow_before_an_outlay, test_inflation_just_above_minus_one_is_valid_in_the_project); reference.py, instance.py, starter.py unchanged; tests/labs/CF1 unchanged; cards.json unchanged; the lesson L06.html lines 211 and 444 changed (non-slice lesson, checked because cards and rows cite it); seven new mutants in ledgers/CF1/mutants/ (r20d_01..07) and the d19 and fx19 files of round 19 committed with fd9a9b7."),
    ("r20-line55-defined-terms", "2.9 / scope: the terms in the rewritten Lab 1 hypothesis are defined before use",
     "course/modules/CF/CF1/project.html line 55 (Lab 1 hypothesis)",
     f"{R}: the hypothesis now says 'straight-line depreciation (defined in the conventions below)' and 'working capital (defined in the conventions below)'. Conventions line 197 define straight-line depreciation (capex / life, no salvage) and line 200 defines working capital (share of revenue at the end of years 1 to life - 1, zero at the start and at the end). The lab's invested-then-recovered pattern (step 3: -600.00, -50.00, +650.00) matches line 200."),
    ("r20-line213-irr-all-zero-example", "2.4 / scope: the named error 'every flow zero' and its example [-100, 0]",
     "course/modules/CF/CF1/project.html line 213; grader/test_project.py test_irr_accepts_an_outlay_followed_only_by_zeros",
     f"{R}: the reference returns irr_roots([-100, 0]) == [] and irr_roots([-100, 0, 0]) == [] (NPV is -100 at every rate; recheck_r20.py); the test asserts both; the sentence says the outlay followed by zeros is valid and has no root, which the reference and the test agree with. Only all-zero flows are refused (reference line 104). Verified; the alternatives (40 unique engines) all accept it."),
    ("r20-line213-irr-first-flow-positive", "2.4 / scope: 'an IRR request whose first flow is positive, such as 100 and -110, is valid: its one root is 0.1'",
     "course/modules/CF/CF1/project.html line 213; grader/test_project.py test_irr_accepts_an_inflow_before_an_outlay",
     f"{R}: irr_roots([100, -110]) = [0.09999999999999987] (recheck_r20.py); the root of 100 - 110/(1+r) is r = 0.1. The sentence and the test agree; the payback rule (first flow must be negative) is not applied to IRR requests, as the reference shows (irr_roots has no first-flow check)."),
    ("r20-line213-inflation-minus-0.999-project", "2.4 / scope: 'an inflation of −0.999 ... in a project' is valid",
     "course/modules/CF/CF1/project.html line 213; grader/test_project.py test_inflation_just_above_minus_one_is_valid_in_the_project",
     f"{R}: the reference accepts the project with inflation -0.999 (_check_project requires inflation > -1); the test asserts real[LIFE] = nominal[LIFE] / 0.001 ** LIFE with rel 1e-9 and absolute 1e-6 (this test is the tenth absolute=1e-6 check; see proj-tolerance-nine-recount). All alternative engines accept it."),
    ("r20-collect-157-seeds", "2.5 command: collected count equals the page's count on every seed",
     "course/modules/CF/CF1/grader/test_project.py; course/modules/CF/CF1/project.html line 192",
     f"{R}: {CMD['collect']}. No duplicate test function name in test_project.py (102 def test_ lines, 0 duplicates); the parametrize expansion gives 157."),
    ("r20-mutants-new-seven", "2.6 mutation: at least three new student-error mutants, each killed",
     "ledgers/CF1/mutants/r20d_01..r20d_07 (generator ledgers/CF1/scripts/CF1-d-r20/make_mutants20.py)",
     f"{R}: seven new student errors: r20d_01 discounted payback fraction over the undiscounted flow (killed by test_discounted_payback_uses_discounted_flows); r20d_02 IRR grid evenly spaced in x (killed by test_irr_finds_both_roots_of_a_two_sign_change_flow); r20d_03 IRR refuses flows that sum to zero (killed by test_irr_does_not_report_a_tangent_root, whose flows [-1, 2, -1] also sum to zero; the kill is by a test about a different property, so the message is misleading but the mutant is not a survivor); r20d_04 one normal per year not per draw (killed by test_monte_carlo_draws_follow_the_seeded_gauss_stream); r20d_05 working-capital balance from next year's revenue (killed by test_working_capital_investment_and_recovery_sum_to_zero); r20d_06 Monte Carlo scales cash costs (killed by the stream test); r20d_07 multiplier without the mean-one correction (killed by the stream test). All in out/mutate_r20_full.out."),
    ("r20-mutants-full-run", "2.6 mutation: all 190 mutants killed on seeds 0-9",
     "ledgers/CF1/mutants/*.py (183 .py files plus the seven new r20d files; 190 in total)",
     f"{R}: {CMD['mutate']}; no survivor. Only top-level .py files are run by the tool; the eight subdirectories of ledgers/CF1/mutants hold earlier scripts and are not mutants."),
    ("r20-alternatives-three-new", "2.6 over-constraint: three new genuinely different correct engines pass",
     "ledgers/CF1/scripts/CF1-d-r20/alts/alt_r20_a_irr_fine_grid_and_horner_npv.py, alt_r20_b_payback_tolerance_and_accumulated_npv.py, alt_r20_c_running_factor_and_affine_monte_carlo.py (generator make_alts20.py)",
     f"{R}: a: IRR grid of 20001 samples, Horner polynomial, longer bisection; b: payback recovery tested with a 1e-12 tolerance, NPV by backward accumulation; c: real flows by a running discount factor, Fisher by log1p/expm1, Monte Carlo by the affine identity in the multiplier. All pass the suite on seeds 0-9 (out/alts_all_r20.out)."),
    ("r20-alternatives-all-unique", "2.6 over-constraint: every earlier alternative still passes",
     "ledgers/CF1/scripts/CF1-d-r*/alts/*.py and */e/alts/*.py (run_alts20.py)",
     f"{R}: {CMD['alts']}."),
    ("r20-hub-hours-arithmetic", "2.9 hours: hub split and lesson hours agree",
     "course/modules/CF/CF1/index.html lines 29-41; L01-L06 data-hours; project.html data-hours-project and the time-budget table (lines 216-231)",
     f"{R}: index.html states '48 h lessons · 12 h project (20.0% of the 60 module hours)'; the six lessons carry data-hours=8 each (48); data-hours-project=12; the time-budget rows sum to 1+1+4+2+1+1+2 = 12. No arithmetic inconsistency. Hours are design targets (architect ruling), not re-estimated."),
    ("r20-l06-line211-recomputed", "2.2 numbers in prose: L06 Section 3 values",
     "course/modules/CF/CF1/L06.html line 211 and line 444",
     f"{R}: the twin tests/labs/CF1/lab-CF1-L06-1.py prints quantile_10 14896.62, quantile_50 79457.94, quantile_90 143406.13, share 0.0552 se 0.0010 (run under python -I -W error, exit 0). Recomputation (/tmp/CF1-v/d20/indep/l06_unrounded.py) without printing: 14896.623057292309, 143406.1265686024 (page: 143406.126569), difference 128509.50351131009 (page: 128509.5035), rounded 128509.50, printed difference 128509.51, gap 0.0065. Negatives 2761 of 50000 = 0.05522 (page: 2761/50000 = 0.05522; prints 0.0552); se sqrt(p(1-p)/n) = 0.0010215 (prints 0.0010)."),
    ("r20-cards-unchanged-agreement", "2.7 cards: cards whose lesson text changed this round",
     "course/modules/CF/CF1/cards.json CF1-c081, c082, c083 (cite L06 Lab 1 numbers); L06.html lines 211 and 444",
     f"{R}: cards.json is byte-identical to 51fa336. Cards c081 (0.625 standard errors above the closed form: 79216.82 vs 79078.68), c082 (49419.62 and ratio 1.0008) and c083 (0.0552, se 0.0010) match the twin output and the changed L06 lines 211 and 444 (no card number is changed by the lesson edits)."),
    ("r20-registry-and-verify", "2.1 citations: registry keys and live/offline verifier",
     "references/references.json; tools/verify_refs.py --unit CF1 and --offline",
     f"{R}: {CMD['verify_refs']}. The registry's used_by lists for glasserman2003monte (M8 only) and damodaran2012investment (CF4 only) do not list CF1 (flagged, see registry_flags); the CF1 citations resolve by key."),
    ("r20-labs-pytest-and-twins", "2.5 labs: the project and lesson twins run",
     "tests/test_labs.py -k CF1; tests/labs/CF1/lab-CF1-*.py",
     f"{R}: {CMD['labs_pytest']}; {CMD['twins']}."),
    ("r20-gate-set", "2.5 command: the project gates",
     "tools/check_pages.py, check_dag.py --all, check_projects.py, run_graders.py, run_labs.py, mutate_graders.py, page_smoke.py, ruff, mypy",
     "; ".join(CMD[k] for k in ["check_pages", "check_dag", "check_projects", "run_graders", "run_labs", "page_smoke", "ruff", "mypy"]) + "."),
    ("r20-sum-zero-irr-refusal-not-pinned", "2.6 spec: a refusal the page does not state is not pinned by the suite",
     "course/modules/CF/CF1/project.html line 213; grader/test_project.py test_irr_does_not_report_a_tangent_root",
     f"{R}: the page refuses IRR requests only for every flow zero. No test asserts that a request whose flows sum to zero but are not all zero (for example [-100, 100], root 0) is accepted; the suite kills the refusal mutant r20d_03 only through the tangent-root test. Survivor count is zero, so this is an observation (PASS), not a finding."),
    ("r20-no-process-words-and-banned", "2.9 prose: process words and banned phrases in the changed text",
     "course/modules/CF/CF1/project.html lines 55, 192, 213; L06.html lines 211, 444",
     f"{R}: scanned for round, builder, verifier, REQUESTS, roughly, historically, about with a number and ellipses: none in the changed sentences."),
]
for rid, check, loc, evidence in NEW:
    rows.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": evidence})

mutants = []
for line in mut_lines:
    if not line.startswith("KILLED "):
        continue
    body = line[len("KILLED "):]
    fname, rest = body.split(": ", 1)
    desc, killer = rest.rsplit(" -> ", 1)
    killer = killer.rsplit(" (seed", 1)[0]
    mutants.append({"file": f"ledgers/CF1/mutants/{fname}", "description": desc.strip(), "killed_by": killer.strip()})
on_disk = sorted(p.name for p in (CHK / "ledgers/CF1/mutants").glob("*.py"))
assert len(mutants) == len(on_disk) == 190, (len(mutants), len(on_disk))
assert {Path(m["file"]).name for m in mutants} == set(on_disk)

counts = {"PASS": 0, "FAIL": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["FAIL"] == 0 and all(m["killed_by"] for m in mutants) else "FAIL"
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
assert set(old_rows) <= set(ids), set(old_rows) - set(ids)
fragment = {
    "unit": "CF1",
    "slice": "CF1-d",
    "round": 20,
    "verifier": "independent verifier (Haiku), round 20 of CF1 slice d (project page incl. case-memo rubric, grader, project labs, cards.json; project slice needs mutants)",
    "pin": "fd9a9b7 (detached, /tmp/verify20-CF1-d)",
    "base": "51fa336 (round-19 pin; delta computed with git diff --stat 51fa336 fd9a9b7 and every slice hunk read)",
    "checkout": "/tmp/verify20-CF1-d",
    "scratch": "/tmp/CF1-v/d20",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "glasserman2003monte: used_by lists M8 only; CF1 cites it (project.html line 436, L06.html line 106, cards CF1-c084). references/references.json unchanged since the round-19 pin; add CF1 with tools/add_reference.py or confirm the architect's ruling.",
        "damodaran2012investment: used_by lists CF4 only; CF1 lists it in the project reading list (project.html line 460). references/references.json unchanged.",
    ],
    "freshness_flags": [],
    "notes": (
        "Round-20 delta (51fa336..fd9a9b7) for this slice: project.html lines 55, 192, 213 changed (all other lines unchanged, so project.html line numbers are the same as in round 19); grader/test_project.py: three tests inserted (old lines 310 and 524, +15 and +14 lines), no existing test body changed; reference.py, instance.py, starter.py, tests/labs/CF1, cards.json unchanged; L06.html lines 211 and 444 changed (non-slice lesson, read because cards and rows cite it); the mutants and alternatives of round 19 are unchanged apart from the fx19 and d19 files added at fd9a9b7. "
        "Line numbers of test_project.py in round-19 evidence are the 51fa336 numbering: add 15 for old lines 311-524 and 29 for old lines 525 and up. Carried rows keep the round-19 evidence with the prefix 'Carried from round 19'. "
        "Re-run this round: check_pages, check_dag --all, check_projects, run_graders 0-49, run_labs, mutate_graders 0-9 (190/190), page_smoke CF1, ruff check and format, mypy strict on the grader, tests/test_labs.py -k CF1 (9 passed), the nine labs twins under python -I -W error, verify_refs live (CF1) and offline, collect-only 157 on seeds 0-49, 59 alternative files (40 unique) on seeds 0-9. "
        "Not checked: the full BLUEPRINT re-grade of every card against lesson text (cards.json and L01-L05 unchanged, so the round-19 grades are carried except the five rows that remain FAIL); the Pyodide browser grader beyond page_smoke; hours are design targets and were not re-estimated; live Crossref or SEC access not used; the L06 lesson beyond the changed lines 211 and 444 and the cited Remark 2.4 and E1. "
        "Two new FAILs (proj-tolerance-nine-recount, proj-tolerance-six-checks-enumerated) come from the round-20 grader insertion of test_inflation_just_above_minus_one_is_valid_in_the_project, which adds a tenth absolute=1e-6 check that line 209 does not list."
    ),
    "summary": (
        f"CF1-d round 20 (pin fd9a9b7): {len(rows)} rows, {counts['PASS']} PASS, {counts['FAIL']} FAIL. "
        "FAIL: proj-tolerance-nine-recount and proj-tolerance-six-checks-enumerated (line 209 says nine absolute=1e-6 checks; the grader now has ten, after the round-20 test insertion), "
        "cards-grade-semantics and cards-definition-basis-graded-t (17 definition cards still graded T), lesson-l06-remark-2-4-each-result-conditional (Remark 2.4 overstates the labelling of E1; L06 line 106 unchanged). "
        "Fixed since round 19: proj-mutant-d19-m01-irr-zero-outlay-refused, proj-mutants-killed, cmd-mutate-graders-r19 (190/190 killed). "
        "Mutants: 190 run, 190 killed, 7 new this round. Alternatives: 3 new and 40 unique engines pass seeds 0-9."
    ),
}
out_path = CHK / "ledgers/CF1/CF1-d.json"
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(rows), counts, "mutants", len(mutants), "verdict", verdict)
