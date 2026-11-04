"""Writes the round-7 E3-d fragment (ledgers/E3/E3-d.json) from the verifier's recorded outputs in this directory."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

CK = Path("/Users/billyribeiro/.fanout/wt/verifyD7-E3-d")
SCR = CK / "ledgers/E3/scripts/E3-d-r7"


def mutants_from(path: Path) -> list[dict]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^KILLED (\S+)\.py: (.*) -> (.*)$", line)
        if m:
            out.append({"id": m.group(1), "description": m.group(2), "killed_by": m.group(3)})
    return out


def alt_result(name: str) -> tuple[str, str]:
    if name == "alt4":
        parts = []
        for seed in range(10):
            text = (SCR / f"verifier_alt_alt4_seed_{seed}.out").read_text(encoding="utf-8")
            ok = bool(re.search(r"^alt4: PASS \(1/1 seeds\)$", text, re.M)) and "EXIT 0" in text
            parts.append(ok)
        if all(parts):
            return "PASS", "10/10 seeds, one process per seed"
        return "FAIL", "failing seeds " + str([i for i, p in enumerate(parts) if not p])
    text = (SCR / f"verifier_alt_{name}_seeds_0_9_r7.out").read_text(encoding="utf-8")
    m = re.search(rf"^{name}: (PASS|FAIL) \((.*?)\)$", text, re.M)
    if m:
        return m.group(1), m.group(2)
    return "UNVERIFIABLE", "no summary line in " + f"verifier_alt_{name}_seeds_0_9_r7.out"


PASS, FAIL, UNV = "PASS", "FAIL", "UNVERIFIABLE"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != PASS:
        r["fix"] = fix
    rows.append(r)


row("gate-check-pages", "tools/check_pages.py --unit E3", "course/modules/E/E3/project.html", PASS,
    "verifier_check_pages.out: 'check_pages E3: PASS'")
row("gate-check-dag", "tools/check_dag.py --unit E3", "course/modules/E/E3/project.html", PASS,
    "verifier_check_dag.out: 'check_dag E3: PASS'")
row("gate-check-projects", "tools/check_projects.py --unit E3", "course/modules/E/E3/project.html", PASS,
    "verifier_check_projects.out: 'check_projects E3: PASS'")
row("gate-run-labs-project", "tools/run_labs.py --unit E3 --page project", "project.html Labs 1-3", PASS,
    "verifier_run_labs_project.out: 'run_labs E3: PASS (3/3)'")
row("gate-run-graders-seeds-0-49", "tools/run_graders.py --unit E3 --seeds 0-49", "course/modules/E/E3/grader/", PASS,
    "verifier_run_graders_0_49.out: 'run_graders E3: PASS (reference 50/50 seeds, slowest 14.3 s)', EXIT 0")
row("gate-collect-45", "pytest --collect-only in a grader workspace (reference as elicit.py); id kept from round 6, "
    "where the count was 45", "course/modules/E/E3/grader/test_project.py; project.html:213", PASS,
    "46 tests collected (grep '^def test_' = 46; the page says 46 checks, project.html:213)")
row("gate-reference-seed0-46-pass", "pytest -q --assert=plain -W error, reference as elicit.py, QF_SEED=0",
    "course/modules/E/E3/grader/test_project.py", PASS, "46 passed in 13.71s (scratch pyt/)")
row("gate-starter-fails", "pytest on starter.py as elicit.py (must fail)", "course/modules/E/E3/grader/starter.py", PASS,
    "44 failed, 2 passed. The 2 passing tests accept any exception on their input by design "
    "(test_wrong_types_never_return_money_as_a_float, test_estimate_counts_a_mixed_lottery_whether_or_not_it_was_chosen)")
row("gate-page-smoke-project", "tools/page_smoke.py --unit E3 --pages project", "course/modules/E/E3/project.html", PASS,
    "verifier_page_smoke_project.out: labs 1-3 run in browser; 'in-browser grader: All 46 tests pass'; 'PASS'")
row("gate-ruff-check-grader-labs", "ruff check course/modules/E/E3/grader tests/labs/E3",
    "course/modules/E/E3/grader; tests/labs/E3", PASS, "'All checks passed!'")
row("gate-ruff-format-E3", "ruff format --check course/modules/E/E3/grader tests/labs/E3",
    "course/modules/E/E3/grader; tests/labs/E3", PASS, "'15 files already formatted'")
row("gate-ruff-format-repo", "ruff format --check . (repo; round-6 FAIL re-verified)", "repo", PASS,
    "'551 files already formatted' at 9373ef3 (round-6 failure was ledgers/M3/retired, now clean)")
row("gate-mypy-strict", "mypy --no-incremental (repo strict configuration)", "repo", PASS,
    "verifier_mypy.out: 'Success: no issues found in 385 source files', EXIT 0")
row("gate-verify-refs-offline", "tools/verify_refs.py --offline", "references/references.json", PASS,
    "verifier_verify_refs.out: 'offline integrity: 560 entries, 0 problems'")
row("gate-pytest-labs", "pytest tests/test_labs.py tests/test_run_labs.py", "tests/", PASS,
    "verifier_pytest_labs.out: all dots, rc=0 (the round-6 wider file list is not rerun here)")
row("gate-mutate-E3-existing-105", "tools/mutate_graders.py --unit E3 --seeds 0-9 (all 105 mutants at the pin)",
    "ledgers/E3/mutants/", PASS, "verifier_mutate_E3_0_9.out: 'mutate_graders E3: PASS (105/105 killed)', EXIT 0")
row("gate-mutants-new-4", "round-7 mutants e3d7_01..04 (run with verifier_run_mutants.py, seeds 0-9)",
    "ledgers/E3/mutants/e3d7_0*.py", PASS, "verifier_new_mutants_r7.out: 4 of 4 KILLED")
row("gate-mutants-count", "at least 10 student-error mutants; the page/plan asks ten, the tool enforces three",
    "ledgers/E3/mutants/", PASS, "109 mutant files at the pin plus this round's 4; all 109 killed (see mutants list)")
for rid, mid in [("mut-e3d5-01-zero-prize-mixed-test-fixed", "e3d5_01_zero_prize_counts_as_a_gain_in_the_mixed_test"),
                 ("mut-e3d6-01-zero-prize-counts-as-loss", "e3d6_01_zero_prize_counts_as_a_loss_in_the_mixed_test"),
                 ("mut-e3d6-02-mixed-check-reads-chosen-lottery", "e3d6_02_mixed_check_reads_only_the_chosen_lottery"),
                 ("mut-e3d6-03-loss-inverse-divides-after-power", "e3d6_03_loss_inverse_divides_after_the_power")]:
    row(rid, "round-6 mutant re-run at 9373ef3 (round-6 FAIL for -01 and -02 is now killed)",
        "ledgers/E3/mutants/" + mid + ".py", PASS, "verifier_mutate_E3_0_9.out line for " + mid + ": KILLED")
row("mut-e3d7-01-crra-gamma-zero-float", "new student-error mutant: CRRA gamma = 0 expectation summed in float",
    "ledgers/E3/mutants/e3d7_01_crra_gamma_zero_expectation_summed_in_float.py", PASS,
    "verifier_new_mutants_r7.out: KILLED by test_crra_gamma_zero_is_expected_final_wealth_exactly (seed 1)")
row("mut-e3d7-02-loss-power-lambda-inside-root", "new student-error mutant: lambda inside the loss power",
    "ledgers/E3/mutants/e3d7_02_loss_power_applies_lambda_inside_the_root.py", PASS,
    "verifier_new_mutants_r7.out: KILLED by test_prospect_matches_oracle_for_instance_lotteries (seed 0)")
row("mut-e3d7-03-prospect-refuses-nonpositive-wealth", "new student-error mutant: prospect model applies wealth rule",
    "ledgers/E3/mutants/e3d7_03_prospect_model_refuses_nonpositive_final_wealth.py", PASS,
    "verifier_new_mutants_r7.out: KILLED by test_crra_requires_wealth_plus_every_prize_to_stay_positive (seed 0)")
row("mut-e3d7-04-estimate-grid-start-only", "new student-error mutant: estimate returns the grid start",
    "ledgers/E3/mutants/e3d7_04_estimate_returns_the_grid_start_without_refinement.py", PASS,
    "verifier_new_mutants_r7.out: KILLED by test_score_is_zero_at_the_estimate (seed 0)")
for i, name in enumerate(["alt1", "alt2", "alt3", "alt4", "alt5"], 1):
    status, detail = alt_result(name)
    fix = None
    if status != PASS:
        fix = "investigate the failing seeds in verifier_alt_%s_seeds_0_9_r7.out" % name
    row(f"alt-{i}", f"alternative correct implementation {name} (ledgers/E3/scripts/run_alternatives.py)",
        "ledgers/E3/scripts/run_alternatives.py", status,
        f"verifier_alt_{name}_seeds_0_9_r7.out: {name}: {status} ({detail})", fix)
row("lab-twin-1", "python -I -W error on tests/labs/E3/lab-E3-project-1.py", "tests/labs/E3/lab-E3-project-1.py", PASS,
    "verifier_labs_check.py: exit 0, stderr '', output equals expected block")
row("lab-twin-2", "python -I -W error on tests/labs/E3/lab-E3-project-2.py", "tests/labs/E3/lab-E3-project-2.py", PASS,
    "verifier_labs_check.py: exit 0; output equals expected block (completed solution)")
row("lab-twin-3", "python -I -W error on tests/labs/E3/lab-E3-project-3.py", "tests/labs/E3/lab-E3-project-3.py", PASS,
    "verifier_labs_check.py: exit 0, stderr '', output equals expected block")
row("lab-page-code-equals-twin", "page code of Labs 1-3 equals the twin (Lab 2: line by line, blanks allowed)",
    "project.html Labs 1-3", PASS,
    "verifier_labs_check.py: Labs 1 and 3 identical; verifier_lab2_lines.py: 38 = 38 lines, only lines 14-15 differ, "
    "each a '___' blank")
row("lab-expected-equals-output", "expected block equals twin output", "project.html Labs 1-3", PASS,
    "verifier_labs_check.py: expected==output True for Labs 1-3")
row("lab1-prose-numbers", "Lab 1 prose and printed numbers (496/500, -30/500, 3000/-762/-513, P(A), -2.302315)",
    "project.html Lab 1 hypothesis and interpretation", PASS,
    "verifier_labs_check.py output of lab-E3-project-1; prose 'pair 2 ... prints as -762' matches; "
    "constants 0.40/2.00/1.50 match the code")
row("lab2-prose-numbers", "Lab 2 prose: z = -0.14, 0.465057055, -0.765595182, -0.625595182",
    "project.html Lab 2 hypothesis and interpretation", PASS,
    "verifier_labs_check.py output of lab-E3-project-2; z = 2*(1500-2200)/10000 = -0.14 (computed)")
row("lab3-prose-numbers", "Lab 3 prose: 0.6352, 6.1503, 2.0201, SEs 0.32/9.59/1.86, 3.55e-10, -7.1445, 11 of 12 mixed, "
    "se_lambda > lambda_hat", "project.html Lab 3 and interpretation",
    PASS, "verifier_labs_check.py output of lab-E3-project-3; verifier_lab3_answers.py: 11 mixed pairs")
row("exemplar-word-count-A", "exemplar A memo text word count = 117", "project.html exemplar-a memo blocks (around line 621)", PASS,
    "verifier_exemplar_words.py: 117 (headings included, tags removed, whitespace split)")
row("exemplar-word-count-B", "exemplar B memo text word count = 435 (round-6 FAIL: page said 582)",
    "project.html exemplar-b memo blocks", PASS,
    "verifier_exemplar_words.py: 435 (five memo blocks); page claims 435 at project.html:621")
row("exemplar-scores-annotations", "data-scores and annotation levels agree with the official scoring; data-level is the median score",
    "project.html exemplar-a and exemplar-b articles", PASS,
    "A: scores 2,2,1,2,1, data-level 2 (median); B: 3,3,4,3,3, data-level 3 (median); every 'Meets/Misses' line agrees")
row("seed49-se-docstring-numbers", "seed-49 standard errors and step/order sensitivity in test_project.py docstring",
    "course/modules/E/E3/grader/test_project.py:966-983", PASS,
    "verifier_seed49_se.py: lambda 135.05 (1e-5) and 97.67 (1e-6); gamma 0.09474 and 0.07983; reversed order 136.78 and "
    "98.09; percentages -27.7, -15.7, +1.3, +0.4 recomputed")
row("allA-docstring-numbers", "test_estimate_counts docstring: all-A set gives kappa near 925 and SE above 1e5",
    "course/modules/E/E3/grader/test_project.py:806-830", PASS,
    "verifier_allA_estimate.py: kappa_hat 924.73, se_lambda 6.9e5, se_kappa 1.98e6 (reference)")
row("seed30-kappa-below-one", "LOW_KAPPA participant (generator seed 30) has kappa below 1", "project.html:213; test_project.py:36",
    PASS, "verifier_seed49_se.py output: seed30 kappa 0.635")
row("grader-recovery-seeds", "recovery: estimate within 4 SE on at least 47 of seeds 0-49 (page threshold)",
    "course/modules/E/E3/grader/test_project.py:585-600", PASS,
    "verifier_run_graders_0_49.out: reference passes the suite on 50/50 seeds, which includes this test")
row("grader-message-never-prints-answer", "failure messages never print the expected value (test_project.py:11 "
    "docstring; plan section 6.7)", "course/modules/E/E3/grader/test_project.py:254,258,265,267,269,271", FAIL,
    "The module docstring says 'It never prints the expected value', but the failure messages for exact cases state "
    "the answer: line 254 '...the sure amount of this lottery is -25 cents'; line 258 '...is +25 cents'; line 265 "
    "'...must round half up to 3'; line 267 '...to 1'; line 269 '...to 0'; line 271 '...to 3'.",
    "reword those six messages without the numeric answer (for example, 'an exact half cent must go toward plus "
    "infinity'), or change the docstring to say that the messages name the rule, not the value")
row("grader-gamma0-exact-over-constraint", "a float-computed expectation at gamma = 0 (the page's stated method, "
    "'computed in floating point') fails test_crra_gamma_zero_is_expected_final_wealth_exactly; the exact-half rule "
    "is not guarded at gamma = 0", "course/modules/E/E3/grader/test_project.py:143-148; project.html:"
    "'Whole cents' convention and Constraints", FAIL,
    "verifier_gamma0_float_all.py (scratch): on seeds 0-49, PARSED[:40] has a float-vs-exact rounding divergence on "
    "12 of 50 seeds (seed 1 pair 25 A: exact 58581/2, float 29290.499999999996). The instance guard (instance.py) "
    "checks half-cent clearance only at the true gamma, not at gamma = 0. No alternative tests a float gamma = 0 path.",
    "either state on the page that the rounding rule applies to the exact value, so an exact-half expectation is computed "
    "with Fraction arithmetic, or restrict test_crra_gamma_zero to lotteries whose exact expectation is not a half cent "
    "(test_half_cent_goes_up_on_exact_halves already tests the half rule on exact cases)")
row("spec-probability-text-fixed", "spec probability text and questionnaire contract", "project.html:207, 273", PASS,
    "node verifier_questionnaire_regex.js: '1','0','1/2','10/20','0/1','1/01' accepted; '1/0','0.5','-1/4','' rejected")
row("questionnaire-fraction-contract", "questionnaire regex accepts exactly the forms the spec names (round-6 FAIL fixed)",
    "project.html:273", PASS,
    "node verifier_questionnaire_regex.js (regex of project.html isProbability); '1/0' is refused, '1/2' accepted")
row("questionnaire-no-egress", "questionnaire and page scripts send nothing", "project.html:249-353", PASS,
    "grep: no fetch, XMLHttpRequest or sendBeacon in project.html; export is a Blob download (project.html:342-344)")
row("questionnaire-export-only-when-complete", "export only when every pair has a choice", "project.html:324-344", PASS,
    "missing.length > 0 returns before the Blob is built (project.html:338-341)")
row("grader-autosave-and-reveal", "autograder code autosave and exemplar reveal behave as the page says",
    "course/assets/js/grader.js:59-61; rubric.js:147-150", PASS,
    "code read: editor input is saved after 400 ms (grader.js:59-61); annotations hidden until revealed (rubric.js:147-150)")
row("grader-imports-stdlib-no-print", "grader imports and output checks", "test_project.py:1166-1191", PASS,
    "test_engine_imports_only_the_standard_library_with_no_network_and_prints_nothing passes on the reference")
row("instance-validity", "instance guards match the instance docstring: 200 pairs, >=100 mixed, Hessian PD, "
    "boundary margin 0.5, half-cent guard at 1e-6", "course/modules/E/E3/grader/instance.py:210-261", PASS,
    "code read (instance.py:210-261: mixed count, Hessian, boundary margin, half-cent guard); run_graders passes 50/50 seeds")
row("instance-docstring-ranges", "instance docstring ranges: gamma [0.10,0.80], lambda [1,3], kappa [0.5,5], wealth "
    "$50k-$200k, prizes $5-$500, 2-3 prizes", "course/modules/E/E3/grader/instance.py:1-30", PASS,
    "code read: uniform draws and randrange(500, 50001) and randrange(5_000_000, 20_000_001, 100)")
row("hours-arithmetic", "project hours sum and hub split", "project.html:357-368; index.html", PASS,
    "1+1+3+4+3+2 = 14 = data-hours-project; hub 70 = 56 + 14 (index.html:31, data-hours-lessons=56)")
row("tolerance-disclosure", "every tolerance in the suite is disclosed on the page", "project.html:213; test_project.py", PASS,
    "CE exact, half cent and 1e-6 cent slack, 1e-9 value slack, one-cent dominance, 1e-9 and 1e-7 likelihood, 2e-5 "
    "score, 0.1 percent move, 10 percent SE: each matches test_project.py (lines cited in the check code)")
row("notation", "every symbol vs notation/notation.json", "project.html math (129 spans)", PASS,
    "registered Phi (standard normal CDF, project.html:750) used with the registered meaning; gamma, lambda, kappa, "
    "alpha, delta, xi, zeta local; none of T, R*, R^e*, R_f, Q, gamma_3, gamma_4 used")
row("citations-reading", "reading section and citations vs the lessons and the registry", "project.html:757-763", FAIL,
    "Reading says 'Lesson 2 ... attaches no key'. L02.html:References lists 'Registry keys cited on this page: "
    "pratt1964risk'. The key is attached to no claim (no data-cite in L02), so 'attaches no key' is not accurate.",
    "write 'Lesson 2 cites pratt1964risk in its references list and attaches it to no claim'")
row("lesson-definitions-cited", "Definitions 1.2 and 1.3 of L06, Proposition 2.7 of L03 and the CRRA form",
    "project.html:53, 220; L06.html:61-68; L03.html:173", PASS,
    "L06 Def 1.2 is the power value with alpha, delta, lambda > 0; Def 1.3 is the prospect value, probabilities used as "
    "they are; L03 Prop 2.7 is the affine invariance (a > 0, b real); the subtracted-1 identity is arithmetic")
row("concept-links", "concept links resolve to defined anchors", "project.html:53, 205, 207, 213", PASS,
    "all in-page href anchors resolve; L02/L03/L04/L06 def-ids exist; check_dag E3 PASS")
row("conventions-vs-grader", "conventions and identification sentences vs grader and reference",
    "project.html:220-225; grader/reference.py", PASS,
    "reference: floor(c+1/2) on rounded value; crra gamma 0 exact; prospect inverse on each side; identification: "
    "derivation: all-gain and all-loss CEs do not depend on lambda (v = x^a on gains, -lambda(-x)^a on losses, inverse divides it out); reference._prospect_ce follows it")
row("exception-table-vs-reference", "exception table rows vs reference.py and grader tests", "project.html:228-240", PASS,
    "reference raises ValueError with the quoted text for each row; tests use must_raise on the same four conditions")
row("scope-words", "scope words (only, all, every, any, same, exactly, never) in learner prose", "project.html", PASS,
    "each occurrence checked: 'only a mixed lottery can identify' (necessary, computed); 'every pair' (export check, "
    "code); 'every certainty equivalent' (Lab 1 prints all); 'exactly 1' (exact Fraction check); none unsupported")
row("process-words", "no process words in learner-visible text", "project.html visible text", PASS,
    "scan for verif, round, builder, gate, fragment, campaign, audit, planner, TODO: only mathematical 'round' and 'pinned down'")
row("dag-unlinked-names", "concepts used by name outside the prerequisite closure", "project.html", PASS,
    "maximum likelihood, logit, observed information used as plain prose (architect decision); no undefined link")
row("reading-and-report-claims", "claims about what the report and the lab print", "project.html:589, 682, 706, 716, 729", PASS,
    "each cited number matches Lab 3 output; 'Eleven of the twelve' and 'se_lambda 9.59 > 6.15' checked")
row("not-checked-browser-questionnaire", "browser behaviour of the questionnaire file load and download, and the "
    "footer claim, beyond the regex and the code read", "project.html:249-353; assets/js/site.js (outside slice)", UNV,
    "the regex, the no-egress grep and the export guard were checked; no browser session drove the file input, "
    "radio buttons or the download", "run the questionnaire in a browser with an instrument.json and a responses export")

mutants = mutants_from(SCR / "verifier_mutate_E3_0_9.out") + mutants_from(SCR / "verifier_new_mutants_r7.out")

frag = {
    "unit": "E3",
    "slice": "d",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-d, round 7 (did not build E3)",
    "pin": "9373ef398589097500ea849e30ff9da423b98943",
    "base": "142ecfc2bd27061de18bd67e83df81e69f5c249d (round-6 pin). Delta in slice d: project.html (lines 44, 207, 273, 357-368, "
            "398, 621), grader/test_project.py (lines 696-717, 806-830, 894-895), grader/instance.py (lines 11-16, 25-26), "
            "tests/labs/E3/lab-E3-project-3.py (lines 4-5), and four new mutants e3d6_* (round 6) already in the round-6 base. "
            "Every row of slice d is re-verified this round; no row is carried.",
    "checkout": str(CK),
    "scratch": "/Users/billyribeiro/.fanout/scratch-E3-d-r7",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Scripts and outputs: ledgers/E3/scripts/E3-d-r7/verifier_*.py and verifier_*.out (labs, lab2 line check, "
        "seed-49 SE recomputation, all-A set, gamma-0 float divergence, questionnaire regex in node, new mutants, "
        "mutation run, alternatives split per alternative). Mutation run: verifier_mutate_E3_0_9.out (105/105 at the pin). "
        "New mutants: ledgers/E3/mutants/e3d7_01..04 (4/4 killed). "
        "Alternatives: the five in ledgers/E3/scripts/run_alternatives.py (numerical-method variants of the reference) were run "
        "per alternative with unbuffered output; none exercises a float gamma = 0 path, which is why row "
        "grader-gamma0-exact-over-constraint is FAIL. Observation, not a row: project.html gives exemplar-b data-level 3 "
        "(its scores 3,3,4,3,3 have median 3, and the page's own verdict says it falls short of level 4), while plan "
        "section 6.6 says data-level 4; the page is internally consistent and the plan line is not an open question, so "
        "no row. Could not check: a real browser session of the questionnaire file input and download (only the regex, "
        "the no-egress grep and the export guard were read); the rubric's calibration beyond the stated scores (cards "
        "excluded from this slice); the full repo pytest suite (only tests/test_labs.py and tests/test_run_labs.py were run "
        "here); live verify_refs (no reference changed); hours beyond arithmetic. Carried rows: none; every row was "
        "re-verified this round because project.html, the grader and the twin changed since round 6."
    ),
    "summary": "",
}
counts = {s: sum(1 for r in rows if r["status"] == s) for s in (PASS, FAIL, UNV)}
frag["summary"] = (f"E3-d round 7 at 9373ef3: verdict FAIL. Rows {len(rows)} (pass {counts[PASS]}, fail {counts[FAIL]}, "
                   f"unverifiable {counts[UNV]}). Mutants {len(mutants)}/{len(mutants)} killed.")
out = CK / "ledgers/E3/E3-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, counts, "mutants", len(mutants))
