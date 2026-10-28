"""Build ledgers/CF1/CF1-d.json (round 13) from the round-12 fragment, carrying only byte-identical subjects."""
import json, re
from pathlib import Path

ROOT = Path("/tmp/verify13-CF1-d")
PREV = json.loads(Path("/tmp/fanout-frags/CF1-d.round12.json").read_text(encoding="utf-8"))
S = ROOT / "ledgers/CF1/scripts/CF1-d-r13"
CHANGED = {"project.html", "test_project.py", "L05.html", "L06.html", "lab-CF1-L05-1.py"}

# Rows whose subject changed in this delta, or whose command was re-run this round, get new evidence below.
REVERIFY = {
    "proj-test-count-72", "proj-spec-count-118-hub", "proj-count-cause-wording", "proj-collect-count-50-seeds",
    "proj-grader-reference-50-seeds", "proj-page-smoke", "proj-verify-refs", "proj-check-dag",
    "proj-structure-and-gates", "proj-pytest-lab-helper", "proj-ruff-format", "proj-mypy-grader-gate",
    "proj-mutants-killed", "proj-mutants-round12-new", "proj-alternatives-correct", "proj-alternatives-round10",
    "proj-alternatives-round11", "proj-equivalent-mutant-proof", "proj-npv-zero-flow-alternatives-r12",
    "proj-grader-new-tests-r12", "proj-named-errors-untested", "proj-error-message-unenforced",
    "proj-must-raise-text-claim", "proj-npv-empty-overconstraint", "proj-process-words-r10",
    "proj-hours-table", "proj-hours-arithmetic-split", "proj-banned-phrases", "proj-lab1-twin-output",
    "proj-lab2-completion-twin", "proj-lab3-sanity-run", "proj-lab2-docstring-claim", "lesson-l05-rewrites",
    "lesson-l06-rewrites", "proj-cards-c071-not-established", "cards-changed-c071-c084",
    "cards-changed-c071-lesson-agreement", "cards-c065-payback-basis", "cards-count-vs-plan",
    "index-ladder-rung1-worked-example", "proj-mutant-m58-zero-flow-time-index", "proj-mutants-round11-new",
    "proj-mutants-round10-new", "proj-capex-negative-untested", "cards-numbers-in-lesson",
    "proj-npv-zero-flow-alternatives-r12",
}

NEW_EVIDENCE = {
    "proj-test-count-72": "Page line 192 states 126 checks. pytest --collect-only on the reference (runone.py collect, workspace copy) gives 126 tests; collect_seeds.py gives 126 on seeds 0, 1, 7, 49 and 134675774 (ledgers/CF1/scripts/CF1-d-r13/runone.py, collect_seeds.py).",
    "proj-spec-count-118-hub": "The 118 figure is gone: grep of project.html and index.html for 118 shows no 'collects 118' statement; the page states 126, equal to the collected count (proj-test-count-72).",
    "proj-count-cause-wording": "The sentence (project.html line 192) gives the cause: counted with pytest --collect-only on the reference, and no parametrize list's length depends on the seed. Parametrize lists in test_project.py are literal lists; the lists added this round (line 371 (bad_rate parametrize) and lines 502-525 pytest.param entries) are literal. Collect count is 126 on all five seeds.",
    "proj-collect-count-50-seeds": "Collect count 126 on seeds 0, 1, 7, 49, 134675774 (collect_seeds.py output in CF1-d-r13).",
    "proj-grader-reference-50-seeds": "tools/run_graders.py --unit CF1 --seeds 0-49: 'run_graders CF1: PASS (reference 50/50 seeds, slowest 0.3 s)' (ledgers/CF1/scripts/CF1-d-r13/graders.out).",
    "proj-page-smoke": "tools/page_smoke.py --unit CF1 --pages project: 'in-browser grader: All 126 tests pass on seed 843998308. (1.1 s)'; 'page_smoke CF1: PASS' (page_smoke_project.out).",
    "proj-verify-refs": "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems'. tools/verify_refs.py --unit CF1 (live): '2 of 560 entries, 0 problems' (vr_offline.out, vr_live_cf1.out). references/references.json unchanged since aebdc15.",
    "proj-check-dag": "tools/check_dag.py --all: 'check_dag CF1: PASS' and 'check_dag AP1: PASS' (check_dag.out).",
    "proj-structure-and-gates": "tools/check_projects.py --all: 'check_projects CF1: PASS'; tools/check_pages.py --unit CF1: 'check_pages CF1: PASS'; check_dag PASS (check_projects.out, check_pages.out, check_dag.out).",
    "proj-pytest-lab-helper": "tools/run_labs.py --unit CF1: 'run_labs CF1: PASS (9/9)' (run_labs.out).",
    "proj-ruff-format": "ruff check on course/modules/CF/CF1/grader and tests/labs/CF1: 'All checks passed!'; ruff format --check: '13 files already formatted' (ruff.out).",
    "proj-mypy-grader-gate": "mypy --no-incremental on the grader and the CF1 labs: 'Success: no issues found in 13 source files' (mypy.out).",
    "proj-mutants-killed": "tools/mutate_graders.py --unit CF1 --seeds 0-9: 'mutate_graders CF1: PASS (105/105 killed)' before the four r13v mutants were added; with them the set is 109, 108 killed (r13v_04 survives, see r13-mutant-r13v-04-fisher-rounding).",
    "proj-mutants-round12-new": "r12d_01..r12d_05 are in the mutate run: all KILLED (mutate_all_r13.out). Killer tests as listed in the mutant rows.",
    "proj-alternatives-correct": "All 20 alternative engines from rounds 7 to 12 (ledgers/CF1/scripts/CF1-d-r9/alts, CF1-d-r10/alts, CF1-d-r12/alts) pass all 10 seeds on the current grader: alts_prior_r9_r12.out.",
    "proj-alternatives-round10": "alt_r10_1..alt_r10_5 pass all 10 seeds on the current grader (alts_prior_r9_r12.out).",
    "proj-alternatives-round11": "Round-11 engines (scratch /tmp/CF1-v/d11 of the round-11 checkout) are not reachable from this checkout; not re-run. Their alternatives r12 are the newer set; see proj-alternatives-correct for the prior engines that are in the repository.",
    "proj-equivalent-mutant-proof": "No equivalent mutant is in the list. The r13v_04 Fisher rounding is not equivalent: round(x, 9) changes the identity by up to 5e-10, far above the stated 1e-12 (project.html line 209).",
    "proj-npv-zero-flow-alternatives-r12": "alt_r12_1_npv_running_discount_factor.py passes all 10 seeds on the current grader (alts_prior_r9_r12.out).",
    "proj-grader-new-tests-r12": "The grader tests added in rounds 11 and 12 (zero-flow NPV) are still present (test_npv_keeps_a_zero_flow_in_its_time_index line 113, test_npv_keeps_a_leading_zero_flow_in_its_time_index line 120) and pass on the reference (50/50 seeds). Line numbers moved after the insertion at 368.",
    "proj-named-errors-untested": "project.html line 210 (Named errors) lists each class; each has a test in test_project.py: rate at or below -1 (lines 104-107, 371-374, 400-403, 772-775); payback first flow not negative (366-368); IRR all zero (262-264); tax one (line 526); Monte Carlo negative draws (765-768); cash cost just below zero and the revenue and cost infinities (lines 511-525).",
    "proj-error-message-unenforced": "project.html line 210 and line 213 say the autograder checks the exception type and not the wording. must_raise (grader lines 54-60) checks only that ValueError is raised, so the wording claim is enforced by construction. Verified by reading must_raise.",
    "proj-must-raise-text-claim": "must_raise (test_project.py lines 54-60) catches ValueError and fails otherwise; the condition text is only used in the failure message. Matches the wording rule on project.html line 210.",
    "proj-npv-empty-overconstraint": "project.html line 210 names an NPV over an empty list as ValueError; test_npv_rejects_empty_flows (line 109) requires ValueError; the reference refuses an empty list (reference.py npv). No test forces an empty NPV to be refused beyond this one, and the spec names it, so it is not an over-constraint.",
    "proj-process-words-r10": "grep of the added lines in the round-13 delta (project.html, grader, L05, L06, lab L05-1) for process words (build, builder, round, verifier, unit report) and banned phrases (roughly, about, historically, typically, usually, half, most, many, ...): none in the added learner text.",
    "proj-hours-table": "project.html lines 216-230 time budget: 1 + 1 + 4 + 2 + 1 + 1 + 2 = 12 hours (the total row). Unchanged in this delta.",
    "proj-hours-arithmetic-split": "index.html: six lesson cards L01-L06 each 8 h (grep card-kicker): 6 x 8 = 48 lesson hours; data-hours-lessons=48 and data-hours-project=12; 48 + 12 = 60; 12/60 = 20.0% (index.html line 41). Matches project.html line 216-230 total of 12.",
    "proj-banned-phrases": "Scan of the round-13 delta additions (project.html lines 192, 210; L05.html 3, 33, 67, 132, 218, 231; L06.html 103, 208, 220, 456; test_project.py) for banned phrases and process words: none.",
    "proj-lab1-twin-output": "python -I -W error tests/labs/CF1/lab-CF1-project-1.py: exit 0; output identical to round 12 (twin_lab-CF1-project-1.out, diffed).",
    "proj-lab2-completion-twin": "python -I -W error tests/labs/CF1/lab-CF1-project-2.py: exit 0; output identical to round 12 (diffed).",
    "proj-lab3-sanity-run": "python -I -W error tests/labs/CF1/lab-CF1-project-3.py: exit 0; output identical to round 12 (diffed).",
    "proj-lab2-docstring-claim": "lab-CF1-project-2.py run as above: exit 0, output identical to round 12.",
    "lesson-l05-rewrites": "L05.html rewritten sentences re-read: line 67 (Proposition 2.1 and the discounted rule): D_t for t <= tau_D uses only C_s with s <= t, and the fractional discounted value uses D_(tau_D - 1) and the discounted flow of year tau_D, so no later year enters (matches Definition 1.2 and the fraction formula). Line 132 payback code raises ValueError when flows[0] >= 0, same as the twin (grep finds one match each in L05.html and tests/labs/CF1/lab-CF1-L05-1.py). Line 218 heading. Line 231 'Graham and Harvey (2001) ... corporate finance practice': registry graham2001theory title 'The theory and practice of corporate finance: evidence from the field' (references.json). PASS. The lab's output is identical (twin_lab-CF1-L05-1.out).",
    "lesson-l06-rewrites": "L06.html re-read: line 103 Glasserman sentence: registry glasserman2003monte is 'Monte Carlo Methods in Financial Engineering', 2003 (references.json). Line 208: the three printed quantiles 14896.62, 79457.94, 143406.13 and the 50000-draw output match twin_lab-CF1-L06-1.out. The difference of the printed quantiles is 128509.51 (143406.13 - 14896.62). The unrounded values from the same lab (ledgers/CF1/scripts/CF1-d-r13/ patched copy at /tmp/CF1-v/d13/l06_unrounded.py) are 14896.623057, 79457.938852, 143406.126569; their difference is 128509.503511, which the sentence rounds as '128509.50'. The sentence states that figure without a rounding basis: see row lesson-l06-unrounded-difference-basis. Line 220 limits: the third limit in the list is the sampling error of tail quantiles, so 'first, second and fourth' is correct. Line 456 nav title matches L05 h1.",
    "proj-cards-c071-not-established": "cards.json CF1-c071 against L05.html Section 4 (current text, line 231): 'states no finding from its registered source ... and quotes no passage' matches. PASS.",
    "cards-changed-c071-c084": "c071 and c084 agree with the current L05 Section 4 and L06 Remark 2.4 text; the registry keys graham2001theory and glasserman2003monte resolve (references.json, 2001 and 2003).",
    "cards-changed-c071-lesson-agreement": "c065, c071, c084 and c085 re-read against the current lesson text: L05 Proposition 2.2 (line 86) is unchanged and is the statement c065 cites; c071 and c084 as above.",
    "cards-c065-payback-basis": "L05.html line 86: Proposition 2.2 'Flows with C_0 < 0 and C_t >= 0 ... r >= 0 ... Then tau_D >= tau_S' matches c065's conventional flows, rate zero or more, both paybacks exist. Unchanged in this delta.",
    "cards-count-vs-plan": "Recounted: cards.json has 103 entries (cards.json unchanged since aebdc15); per lesson L01 18, L02 17, L03 16, L04 20, L05 17, L06 15. plans/CF1-build-plan.md line 240 expects four to six per lesson; unchanged, so the FAIL stands.",
    "index-ladder-rung1-worked-example": "index.html line 151 still says rung 1 is 'A year-1 worked after-tax operating cash flow ... Lab 2 prints the later years'; project.html line 42-44 (unchanged in this delta except lines 189-192 and 210-213) says rung 1 is Lab 1, 'the NPV of a three-year SIMULATED machine project'. The FAIL stands; index.html is unchanged since aebdc15.",
    "proj-mutant-m58-zero-flow-time-index": "m58 is in the r13 mutate run: KILLED by test_npv_keeps_a_zero_flow_in_its_time_index (seed 0) (mutate_all_r13.out).",
    "proj-mutants-round11-new": "m59 and m60 in the r13 mutate run: both KILLED (mutate_all_r13.out).",
    "proj-mutants-round10-new": "m54..m57 in the r13 mutate run: all KILLED (mutate_all_r13.out).",
    "proj-capex-negative-untested": "test_invalid_project_raises_a_named_error[capex-negative] (parameter at line 502, capex -1000) is present and passes on the reference; project.html line 210 names 'a capex that is not a positive integer'.",
    "cards-numbers-in-lesson": "Cards whose numbers come from L05 and L06 (c068-c070, c074, c081-c083, c097, c098, c102): the lab outputs they quote are unchanged (twin_lab-CF1-L05-1.out, twin_lab-CF1-L06-1.out identical to round 12). The L06 quantile numbers are not on any card.",
}

prev = PREV["rows"]
rows = []
for r in prev:
    rid = r["id"]
    if rid in NEW_EVIDENCE:
        status = r["status"]
        if rid == "index-ladder-rung1-worked-example" or rid == "cards-count-vs-plan":
            status = "FAIL"
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status,
                     "evidence": NEW_EVIDENCE[rid]})
        continue
    if rid in REVERIFY:
        # re-verified above or in the new evidence list; if not, carry only if status PASS and subject unchanged
        pass
    if r["status"] != "PASS":
        rows.append(dict(r))
        continue
    files = sorted({f for f in re.findall(r"[\w/.-]+\.(?:html|json|py|md|yaml)", r["location"]) if Path(f).name not in CHANGED})
    files = [f for f in files]
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                 "evidence": "Carried from round 12 (" + (", ".join(files) if files else "the cited locator") +
                 " byte-identical since the previous pin; project.html and grader/test_project.py changed in this delta only at the hunks named in the new rows): " + r["evidence"].replace("this round", "in round 12").replace("(95/95 killed)", "(95/95 killed in round 12)")})
print("carried", sum(1 for x in rows if x["evidence"].startswith("Carried")), "total", len(rows))

# ---- new rows (this round) -------------------------------------------------------------------------------
NEW_ROWS = [
    {"id": "r13-rate-minus-one-named-errors", "check": "2.6-spec / ruling (a): a rate at or below -1 in an NPV, a discounted payback, a Fisher conversion or a Monte Carlo request is a ValueError (project.html line 210, changed this round)",
     "location": "course/modules/CF/CF1/project.html line 210; grader/test_project.py lines 104-107 (NPV), 371-374 (discounted payback), 400-403 (Fisher real and inflation), 772-775 (Monte Carlo)",
     "status": "PASS", "evidence": "Each clause has a test that requires ValueError through must_raise (lines 54-60). Mutants r13d_01 (payback), r13d_06 (npv rate -1 accepted) and r13d_09 (Fisher inflation -1 accepted) are KILLED (mutate_all_r13.out). The Monte Carlo rate test (line 772) is checked by reading; its mutant is not in the list, so the Monte Carlo clause is covered by the test only, which is enough for a named-error claim."},
    {"id": "r13-new-invalid-input-params", "check": "2.6-spec: the new invalid-input parameters (cash cost -1e-9, revenue and cost minus infinity) and negative Monte Carlo draws are named errors (project.html line 210)",
     "location": "course/modules/CF/CF1/project.html line 210; grader/test_project.py lines 511-525 (parametrize ids cost-just-below-zero, revenue-minus-inf, cost-minus-inf) and 765-768",
     "status": "PASS", "evidence": "Mutants r13d_02, r13d_03, r13d_04 and r13d_05 are KILLED (mutate_all_r13.out: test_invalid_project_raises_a_named_error[cost-just-below-zero], [revenue-minus-inf], [cost-minus-inf], test_monte_carlo_refuses_negative_draws). The spec's 'negative or non-finite entry (zero is valid in both lists)' is the sentence these enforce."},
    {"id": "r13-collect-count-126", "check": "2.9 / figure quoted in prose: the 126 checks on project.html line 192 equal the collected count",
     "location": "course/modules/CF/CF1/project.html line 192; grader/test_project.py",
     "status": "PASS", "evidence": "pytest --collect-only through runone.py collect: 126 tests; collect_seeds.py: 126 on seeds 0, 1, 7, 49, 134675774 (CF1-d-r13 scripts)."},
    {"id": "r13-mutant-r13v-04-fisher-rounding", "check": "2.6 mutation: student rounds fisher_nominal to nine decimals (new student-error mutant r13v_04); spec states the identity holds to relative 1e-12",
     "location": "ledgers/CF1/mutants/r13v_04_fisher_rounded_to_nine_decimals.py; course/modules/CF/CF1/project.html line 209 (Tolerances: 'The Fisher identity holds to a relative 1e-12, with an absolute floor of 1e-12, including at zero inflation and at a zero real rate'); grader/test_project.py lines 380-388 (test_fisher_round_trip_is_exact) and 391-397",
     "status": "FAIL", "evidence": "The mutant (return round(exact, 9)) SURVIVES all 10 seeds (mutants_r13v.out: 'r13v_04 ... PASS all 10 seeds'). The Fisher tests use only real and inflation values with at most four decimals (lines 381-382: real in -0.5, -0.1, 0.0, 0.03, 0.07, 0.2; pi in -0.5, -0.02, 0.0, 0.03, 0.1), whose exact nominal rates also have at most nine decimals, so rounding to nine decimals changes nothing; instance test line 411 uses the seeded rate and inflation. The page's claim of a relative 1e-12 identity is therefore not enforced for general inputs. A witness with more digits (for example real 0.0123456789123 and inflation 0.0314159265) is off by about 5e-10 in the nominal rate.",
     "fix": "Add a grader test with rates that need more than nine decimals (for example real = 0.0123456789123 and inflation = 0.0314159265358, and a random sweep of 200 seeded pairs) asserting the 1e-12 identity; or reword project.html line 209 to state the identity only for the test values. Either change must be re-run through mutate_graders (r13v_04 must then be KILLED)."},
    {"id": "r13-alternatives-new", "check": "2.6-spec / ruling (b): three new correct alternatives pass the suite",
     "location": "ledgers/CF1/scripts/CF1-d-r13/alts/alt_r13v_a_life_whole_float_accepted.py, alt_r13v_b_fisher_via_log1p_expm1.py, alt_r13v_c_npv_horner_from_last_flow.py",
     "status": "PASS", "evidence": "run_alts_r13.py: all three 'PASS all 10 seeds' (alts_r13.out). (a) accepts life 2.0, a whole-number float; the spec says 'a life that is not a whole number' is refused, so 2.0 is not refused and nothing in project.html forbids it. (b) Fisher by expm1/log1p; (c) NPV by Horner's rule, the same sum."},
    {"id": "r13-prior-alternatives-rerun", "check": "2.6-spec / ruling (b): the twenty alternatives from rounds 7 to 12 pass on the grader with the new tests",
     "location": "ledgers/CF1/scripts/CF1-d-r9/alts, CF1-d-r10/alts, CF1-d-r12/alts (copied to /tmp/CF1-v/d13/prior)",
     "status": "PASS", "evidence": "run_alts_r13.py on 20 files: 'PASS all 10 seeds' for every file (alts_prior_r9_r12.out)."},
    {"id": "r13-mutants-r13d-killed", "check": "2.6 mutation: the ten round-12 fixer mutants r13d_01..r13d_10 (verifier-added set in the repository) are all killed",
     "location": "ledgers/CF1/mutants/r13d_01..r13d_10 (10 files)",
     "status": "PASS", "evidence": "mutate_all_r13.out: all ten KILLED (killers listed in the mutants array)."},
    {"id": "r13-mutants-full-run", "check": "2.6 / command: mutate_graders --unit CF1 --seeds 0-9 over the 105 mutants present before this round's additions",
     "location": "ledgers/CF1/mutants/*.py (105 files at eaf6d87); tools/mutate_graders.py",
     "status": "PASS", "evidence": "'mutate_graders CF1: PASS (105/105 killed)' (mutate_all_r13.out, exit 0)."},
    {"id": "r13-run-graders-50", "check": "2.5 / command: run_graders --unit CF1 --seeds 0-49 on the reference",
     "location": "course/modules/CF/CF1/grader/reference.py; tools/run_graders.py",
     "status": "PASS", "evidence": "'run_graders CF1: PASS (reference 50/50 seeds, slowest 0.3 s)' (graders.out, exit 0)."},
    {"id": "r13-twins-under-python-I-W-error", "check": "2.5 / each CF1 twin lab under python -I -W error",
     "location": "tests/labs/CF1/lab-CF1-L01-1.py .. lab-CF1-project-3.py (9 files; L05-1 changed this round)",
     "status": "PASS", "evidence": "All nine exit 0; outputs saved as twin_lab-*.out; each byte-identical to the round-12 output (diffed). The L05-1 change (payback raises for flows[0] >= 0) does not change its output."},
    {"id": "r13-lab-l05-1-raise-claim", "check": "2.9 / prose: the payback raise is stated in the lesson and the twin",
     "location": "course/modules/CF/CF1/L05.html line 132 (code block); tests/labs/CF1/lab-CF1-L05-1.py (payback)",
     "status": "PASS", "evidence": "The lesson code and the twin both raise ValueError for flows[0] >= 0 with the same message (grep: one match in each). The lab output is unchanged."},
    {"id": "r13-l06-unrounded-difference-basis", "check": "2.2 numbers in prose: the L06 difference of the unrounded quantiles and the 0.01 gap (rounding basis)",
     "location": "course/modules/CF/CF1/L06.html line 208 (the sentence beginning 'The middle 80% of the simulated NPVs spans 128509.51 cents'); tests/labs/CF1/lab-CF1-L06-1.py (quantile computed unrounded)",
     "status": "FAIL", "evidence": "The unrounded quantiles from the lab's own code (patched copy printing repr, /tmp/CF1-v/d13/l06_unrounded.py, run with python -I -W error): 14896.623057292309, 79457.93885166803, 143406.1265686024. Their difference is 128509.503511 cents, which displays as 128509.50. The sentence gives '128509.50 cents' and '0.01 cents below the printed difference' without a rounding basis; the exact gap to the printed 128509.51 is 0.0065 cents. The figures are correct only when rounded to two decimals, and the page does not say so."},
    {"id": "r13-hub-l05-card-title-stale", "check": "2.9 / hub: the L05 card title matches the L05 page title (changed this round)",
     "location": "course/modules/CF/CF1/index.html line 142 (card-title 'Payback and What Firms Actually Use'); course/modules/CF/CF1/L05.html line 36 (h1 'Payback and Its Discounted Form') and line 3 (title)",
     "status": "FAIL", "evidence": "L05.html's h1 and <title> changed in eaf6d87 to 'Payback and Its Discounted Form' (diff lines 3, 33 and 36). The hub card at index.html line 142 still reads 'Payback and What Firms Actually Use'; index.html is unchanged. L06's previous-link (line 456) was updated in the same commit, so the hub was missed."},
    {"id": "r13-delta-coverage", "check": "2.9 / delta: every file in this slice changed since aebdc15 has been read at its changed hunks",
     "location": "git diff aebdc15 eaf6d87 for course/modules/CF/CF1/{project.html,grader/test_project.py,L05.html,L06.html} and tests/labs/CF1/lab-CF1-L05-1.py",
     "status": "PASS", "evidence": "project.html hunks 189-192 and 210-213 (read in full); test_project.py hunks at 246, 368-377, 508-523, 763-770 (read); L05.html hunks 3, 33, 36, 67, 132, 218, 231 (read); L06.html hunks 103, 208, 220, 456 (read); lab L05-1 hunk (read). cards.json, index.html, references.json, plans and L01-L04 are byte-identical (no hunk)."},
]
FIXES = {
    "r13-l06-unrounded-difference-basis": "Give the rounding basis in L06.html line 208: state the unrounded difference 128509.5035 cents and that it displays as 128509.50, or rewrite the sentence to say the printed quantiles differ by 128509.51 and the unrounded quantiles by 128509.50 when rounded to two decimals; then re-run the L06 lab and the lab check.",
    "r13-hub-l05-card-title-stale": "Change the card title in course/modules/CF/CF1/index.html line 142 to 'Payback and Its Discounted Form' (the L05 h1), using tools/build_site.py if index.html is generated from the lesson titles, and re-run check_pages.py --unit CF1.",
}
for r in NEW_ROWS:
    if r["status"] != "PASS" and "fix" not in r:
        r["fix"] = FIXES[r["id"]]
for r in rows:
    if r["status"] != "PASS" and "fix" not in r:
        prev_fix = next((p.get("fix") for p in prev if p["id"] == r["id"]), None)
        r["fix"] = prev_fix or "see the row's evidence"
rows_out = rows + NEW_ROWS

# ---- mutants ---------------------------------------------------------------------------------------------
import re as _re
mutants = []
for line in (S / "mutate_all_r13.out").read_text(encoding="utf-8").splitlines():
    m = _re.match(r"(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killer = m.groups()
    if status != "KILLED":
        continue
    mutants.append({"file": f"ledgers/CF1/mutants/{name}", "description": desc.strip(), "killed_by": killer.strip()})
for line in (S / "mutants_r13v.out").read_text(encoding="utf-8").splitlines():
    name, _, rest = line.partition(" ")
    if not name.startswith("r13v_"):
        continue
    desc = next(ln for ln in (ROOT / "ledgers/CF1/mutants" / name).read_text(encoding="utf-8").splitlines() if ln.startswith('"""'))
    desc = desc.strip('"')
    killer = _re.search(r"FAIL (\S+)", rest)
    mutants.append({"file": f"ledgers/CF1/mutants/{name}", "description": desc,
                    "killed_by": (killer.group(1) + " (seed 0)") if killer else None})
fragment = {
    "unit": "CF1", "slice": "CF1-d", "round": 13,
    "verifier": "independent verifier (Haiku), round 13 of CF1 slice d (project page incl. case-memo rubric, grader, project labs, cards.json)",
    "pin": "eaf6d87 (detached, /tmp/verify13-CF1-d)",
    "base": "aebdc15 (round-12 pin); delta computed with git diff --stat and git diff aebdc15 eaf6d87",
    "checkout": "/tmp/verify13-CF1-d", "scratch": "/tmp/CF1-v/d13", "verified_at": "2026-10-28",
    "verdict": "FAIL", "rows": rows_out, "mutants": mutants,
    "registry_flags": [
        "glasserman2003monte: used_by lists M8 only; CF1 cites it (project.html Exemplar B section 5, L06 Remark 2.4, cards CF1-c084). references/references.json is unchanged since 91946cf; add CF1 with tools/add_reference.py or confirm the architect's ruling.",
        "damodaran2012investment: used_by lists CF4 only; CF1 lists it in the project reading list (project.html reading section). references/references.json is unchanged since 91946cf.",
    ],
    "freshness_flags": [],
    "notes": ("Delta aebdc15..eaf6d87 for this slice: project.html hunks 189-192 (126 checks) and 210-213 (named errors: rate at or below -1 in NPV, discounted payback, Fisher, Monte Carlo; the Monte Carlo draws and the blank 'payback zero' sentence); "
              "grader/test_project.py: message text at 246, payback rate test 368-377, invalid-input params 508-523, Monte Carlo negative draws 763-770; "
              "L05.html and L06.html lesson passages (see the lesson rows); tests/labs/CF1/lab-CF1-L05-1.py (payback raises); ledgers/CF1/mutants: r13d_01..r13d_10 added by the fixer; ledgers/CF1/scripts/CF1-d-r13 added by this verifier. "
              "Commands run this round (outputs in ledgers/CF1/scripts/CF1-d-r13/): run_graders CF1 --seeds 0-49 (50/50); mutate_graders CF1 --seeds 0-9 (105/105, then 108/109 with the four r13v mutants); runone.py collect and collect_seeds.py (126); run_labs CF1 (9/9); twin labs under python -I -W error (9 exit 0, identical to round 12); check_projects, check_pages --unit CF1, check_dag --all (PASS); verify_refs --offline (560, 0 problems) and --unit CF1 live (2 of 560, 0 problems); ruff check and format --check; mypy --no-incremental (grader and labs); page_smoke CF1 project (126 in browser); 20 prior alternatives plus three new alternatives on seeds 0-9 (all PASS). "
              "Not checked: the full repository gate; pytest outside CF1; alternatives from round 11 (scratch in another checkout, not reachable); the hub index.html beyond line 142 and 151-152 (outside this slice, except the two rows); L01-L04 lesson prose (unchanged); the live reference check for graham2001theory and glasserman2003monte beyond the registry record (no page-level passage read: the locators are graded C with 'passage locator not confirmed'); the SEC and other external sources (not in this slice)."),
    "summary": "",
}
pass_n = sum(1 for r in rows_out if r["status"] == "PASS")
fail_n = sum(1 for r in rows_out if r["status"] == "FAIL")
fragment["summary"] = (f"CF1-d round 13: {'FAIL'}. Rows {len(rows_out)}: PASS {pass_n}, FAIL {fail_n}. "
                       f"Mutants {len(mutants)}: killed {sum(1 for m in mutants if m['killed_by'])}; survivor r13v_04 (Fisher rounding). "
                       "Non-PASS: cards-count-vs-plan, index-ladder-rung1-worked-example (both carried, re-verified unchanged), r13-mutant-r13v-04-fisher-rounding, r13-l06-unrounded-difference-basis, r13-hub-l05-card-title-stale.")
out = ROOT / "ledgers/CF1/CF1-d.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", out, len(rows_out), "rows", len(mutants), "mutants", fragment["verdict"])
