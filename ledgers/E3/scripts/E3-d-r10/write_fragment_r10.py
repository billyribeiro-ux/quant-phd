import json
import sys
from datetime import datetime, timezone

R = sys.argv[1]
S = "ledgers/E3/scripts/E3-d-r10/"
P = "PASS"
U = "UNVERIFIABLE"


def row(rid, check, location, status, evidence, fix=""):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    return r


rows = [
    row("proj-gate-check-projects", "tools/check_projects.py --all", "project.html", P, S + "check_projects.out: 'check_projects E3: PASS', rc=0"),
    row("proj-gate-check-pages", "tools/check_pages.py --all", "project.html", P, S + "check_pages.out rc=0"),
    row("proj-gate-check-dag", "tools/check_dag.py --all", "project.html", P, S + "check_dag.out rc=0"),
    row("proj-gate-run-labs", "tools/run_labs.py --unit E3 --page project", "project.html Labs 1-3", P, S + "run_labs_project.out: 'run_labs E3: PASS (3/3)', rc=0"),
    row("proj-labs-twins-isolated", "python -I -W error on each twin", "tests/labs/E3/lab-E3-project-1..3.py", P, "twin_project_{1,2,3}.out rc=0 and .err 0 bytes; outputs in twin_project_*.out"),
    row("proj-page-smoke", "tools/page_smoke.py --unit E3 --pages project", "project.html", P, S + "page_smoke.out: 'page_smoke E3: PASS'; in-browser grader 'All 38 tests pass'"),
    row("proj-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental on grader and labs", "grader/, tests/labs/E3/lab-E3-project-*.py", P, S + "ruff_check.out 'All checks passed!'; ruff_format.out '7 files already formatted'; mypy.out 'Success: no issues found in 3 source files'"),
    row("proj-grader-reference-50", "tools/run_graders.py --unit E3 --seeds 0-49", "grader/", P, S + "run_graders_0_49.out: 'PASS (reference 50/50 seeds, slowest 13.8 s)'"),
    row("proj-grader-collect", "pytest --collect-only on test_project.py in a grader workspace", "grader/test_project.py", P, S + "collect_only.out: '38 tests collected'; page says 38 checks (project.html line 203)"),
    row("proj-grader-instances", "run_graders instance checks, seeds 0-49", "grader/instance.py", P, S + "run_graders_0_49.out PASS (determinism and seed variation checked by the tool)"),
    row("proj-grader-oracles", "Oracle functions and hand-checked exact cases", "grader/test_project.py lines 87-120, 247-249, 697-709, 716-728", P, "Exact cases recomputed by hand: gamma=0 risk-neutral; lambda=2 lottery -> -25 cents (line 253); sqrt case 225 cents and -225 / -900 (lines 703, 713); Lab 2 probabilities -0.765595182 and -0.625595182 recomputed in python -I"),
    row("proj-grader-no-network", "Import check of elicit.py and no-print check", "grader/test_project.py lines 941-992", P, "Read in full. Module list (lines 941-964) includes asyncio, webbrowser and others. The page states only 'no network, checked by reading the imports' (line 201) and names no module list, so the list is not a page claim. Informational: asyncio is in the list although it is not itself a socket module."),
    row("proj-grader-second-participant", "Second participant (seed + 7919) is a maximum in gamma and kappa", "grader/test_project.py lines 520-542", P, "Read in full; reference passes on seeds 0-49 (run_graders_0_49.out). Docstring matches the code: lambda excluded, reason stated."),
    row("proj-grader-mutants-existing", "All 53 pre-existing mutants killed on seeds 0-9", "ledgers/E3/mutants/ (53 files)", U, "tools/mutate_graders.py --unit E3 --seeds 0-9 started in background (" + S + "mutate_E3_0_9.out) and was still running at the end of the time budget", "Wait for " + S + "mutate_E3_0_9.out and record its rc and count"),
    row("proj-grader-mutant-score-tolerance", "Tolerances of the suite match the page", "grader/test_project.py lines 396, 456, 483, 512, 791, 895", P, "Score 2e-5 (line 483) matches page line 203; recovery 4 SE on 47 of 50 (line 512-515) matches page line 203; SE 10% window (line 791) is stated in its docstring; likelihood 1e-9 and 1e-7 are float tolerances"),
    row("proj-grader-mutants-new", "New student-error mutants r10n04-r10n07 on seed 0", "ledgers/E3/mutants/r10n04..r10n07 (scripts/make_mutants_r10.py)", P, "r10n04 (probabilities normalised): killed by test_probabilities_must_be_nonnegative_and_sum_to_exactly_one; r10n05 (prospect gain exponent): RuntimeError, no convergence, killed; r10n07 (kappa SE without delta factor): killed by test_standard_errors_match_the_delta_method_oracle. r10n06 (naive log1p(exp) overflow): survives, 38 passed; the page states no numerical-stability requirement, so this is informational, not a finding"),
    row("proj-grader-alt-correct", "Five alternative correct implementations on seeds 0-9", "ledgers/E3/scripts/run_alternatives.py", U, "run_alternatives.py --seeds 0-9 started at 09:37 and had not printed at the end of the time budget (" + S + "alternatives_0_9.out is empty)", "Re-run and record alt1 to alt5 lines"),
    row("proj-grader-estimate-domain", "Estimates lie in their domains", "grader/test_project.py lines 439-443", P, "Read; reference passes 50/50"),
    row("proj-grader-identification-margin", "Identification tests", "grader/test_project.py lines 550-644", P, "Read in full. Pure-lottery refusal, zero-probability loss refusal, and B-side-only mixed lottery accepted, matching page item Identification (line 213) and the exception table row (line 227)"),
    row("proj-grader-recovery-threshold", "Recovery: 4 SE on at least 47 of seeds 0-49", "grader/test_project.py lines 502-517", P, "Read; reference passes 50/50 (run_graders_0_49.out)"),
    row("proj-grader-plan-mutant-list", "Plan 6.5 mutant list vs ledgers/E3/mutants", "plans/E3-build-plan.md lines 359-369; plans/E3-open-items.md (Architect ruling, batch 3 round 9)", P, "Items 1 to 5, 8 and 10 map to m01_crra_no_log_limit_at_gamma_one, m02_crra_risk_neutral_ignores_curvature, m03_crra_inverse_of_utility_of_expected_wealth, m04_loss_aversion_applied_to_gains, m05_prizes_sorted_but_probabilities_listed, r3_half_cent_truncated_toward_zero, m07_loglikelihood_omits_unchosen_alternative. Items 6, 7, 9 are ruled not applicable by the Architect (no dominance or Epstein-Zin interface)"),
    row("proj-grader-plan-fosd-tests", "FOSD and SOSD tests", "grader/test_project.py lines 849-938", P, "Read in full. Tests use the specified certainty_equivalent_cents ordering with witness pairs FOSD_WITNESS and SOSD_WITNESS (lines 865-867); reference passes 50/50. Covered by the Architect ruling, not a dominance interface"),
    row("proj-grader-seed49-docstring", "Seed-49 SE figures quoted in test docstring", "grader/test_project.py lines 770-780", P, "seed49_se_r10.out reproduces 135.05 and 97.67 (lambda, -27.7%), 0.09474 and 0.07983 (gamma, -15.7%), order effect 1.28% at step 1e-5"),
    row("proj-grader-se-step-overconstraint", "Score and SE checks accept either step", "grader/test_project.py lines 460-485, 770-796", P, "Read; seed 49 deltas (27.7% and 15.7%) exceed 10%, so the either-step rule is required and is stated in the docstring"),
    row("proj-grader-estimate-domain-note", "Estimation convention and test domains", "project.html Conventions 'Estimation' (line 214)", P, "Matches test_estimates_lie_in_their_domains and the standard error formula; delta-method factors checked algebraically"),
    row("proj-spec-math", "Spec formulas (CRRA, prospect, inverse, choice probability)", "project.html lines 209-214", P, "Prospect inverse for V<0 checked algebraically: v(c) = -lambda(-c)^(1-gamma) gives c = -(-V/lambda)^(1/(1-gamma)); reference.py lines 85-97 agree; test oracles agree"),
    row("proj-spec-rounding", "Whole cents rule", "project.html line 211; reference.py lines 71-73; test_project.py lines 260-270", P, "floor(c + 1/2): 2.5 -> 3, -0.5 -> 0 (tests lines 264-268)"),
    row("proj-spec-exception-table", "Exception table", "project.html lines 218-230", P, "Each row has a test: model names (286-297), probabilities sum (300-343), wealth positive (346-367), responses empty and mixed (545-595); message texts match"),
    row("proj-spec-params-keys", "Required outputs: signatures and keys", "project.html line 199; grader/starter.py lines 13-35; test_project.py line 434", P, "Signatures identical to starter.py; the seven estimate keys match the test"),
    row("proj-spec-instrument-schema", "Inputs (a) and (b) schema", "project.html line 197; questionnaire script lines 263-285", P, "Keys match. Informational: the questionnaire accepts a probability written without a denominator (regex line 263), which the engine's Fraction reads; the spec text says numerator/denominator. Not a grader defect"),
    row("proj-spec-questions", "Questionnaire section", "project.html lines 233-344", P, "Read in full: export refused until every pair has a choice (lines 328-331); no network call in the script"),
    row("proj-spec-curriculum-scope", "Reading list and lessons referenced", "project.html lines 742-752; L02.html line 616; L05.html line 609; L06.html line 531; L07.html line 80; L08.html lines 133, 620", P, "Four keys carry a claim in Lessons 5 to 8 (kahneman via L06 and L07, epstein L05, ellsberg and gilboa L08); pratt named for name only in L02 line 616; all five keys exist in references/references.json"),
    row("proj-spec-ladder", "Ladder and rung references", "project.html lines 40-49", P, "tools/check_projects.py PASS"),
    row("proj-hours", "Time budget arithmetic", "project.html lines 346-362 and data-hours-project line 33", P, "1+1+3+4+3+2 = 14 equals the total row and data-hours-project=14. Hub figure 70 was checked in round 9 and not re-read"),
    row("proj-rubric-observable", "Rubric observable levels", "project.html rubric table", U, "Outside slice d (slice e owns the rubric). Not assessed here", "Slice e to assess"),
    row("proj-rubric-calibration", "Exemplars A and B calibration", "project.html lines 609-725", U, "Outside slice d (slice e). Exemplar B numbers were checked here (proj-exemplar-numbers), the descriptors were not", "Slice e to assess"),
    row("proj-rubric-checks", "Rubric checks tool", "tools/check_projects.py rubric_problems", P, S + "check_projects.out rc=0"),
    row("proj-rubric-question-bank", "Rubric question bank", "project.html", U, "Outside slice d (slice e)", "Slice e to assess"),
    row("proj-exemplar-numbers", "Exemplar B and Lab 3 numbers", "project.html lines 665-725 vs Lab 3 output lines 571-577", P, "0.6352, 6.1503, 2.0201, SEs 0.32, 9.59, 1.86, score 3.55e-10, log-likelihood -7.1445, 11 of 12 mixed, prize range -18700 to 19000 (pair 10 B, pair 1 A) all match the printed output and the data"),
    row("proj-prose-lab1", "Lab 1 prose vs output", "project.html lines 57-138", P, "Expected block equals twin output (checked by script); prose values 496/500, -30/500, 0.480149, -0.733658, -2.302315, 3000/-762 match; wealth 1000.00 matches WEALTH=100000"),
    row("proj-prose-lab2", "Lab 2 prose and blanks vs twin", "project.html lines 141-188; tests/labs/E3/lab-E3-project-2.py", P, "Round-9 FAIL resolved: page and twin now both say 'Rung 2' (no 'completed solution'). Page block differs from twin only at the two ___ blanks; expected block equals twin output; -0.765595182 and -0.625595182 recomputed"),
    row("proj-prose-lab3", "Lab 3 prose vs output", "project.html lines 381-579", P, "Expected block equals twin output; 'eleven of twelve' and SE larger than estimate (9.59 > 6.15) match; largest score 3.55e-10 < 1e-6 matches"),
    row("proj-prose-banned", "Banned words in learner text", "project.html", U, "No banned-word list was given in the verifier rules, so this cannot be checked honestly here", "Name the banned-word list, then grep"),
    row("proj-prose-process-words", "No process words in learner text", "project.html", P, "grep for verifier, builder, round, ledger, batch, fanout, architect, plan returned no matches"),
    row("proj-notation", "Symbols vs notation/notation.json", "project.html", P, "\\Phi is registered (standard normal CDF, M4) and used with that meaning in Rung 4 (line 737); gamma, lambda, kappa, eta are local symbols"),
    row("proj-reading-keys", "Reading keys exist", "project.html lines 746-750; references/references.json", P, "pratt1964risk, kahneman1979prospect, epstein1989substitution, ellsberg1961risk, gilboa1989maxmin each appear once in references.json"),
    row("proj-attribution", "No locator or statement attributed to a source", "project.html lines 744 and 717 (exemplar B evidence, out of slice)", P, "Reading section states no passage locator; the sources' claims are graded in the lessons, read above"),
    row("proj-figures", "Figures", "project.html", P, "No svg, figure or canvas elements in project.html (grep count 0)"),
    row("proj-cards-sample", "Cards sample", "course/modules/E/E3/cards.json", U, "Outside slice d (slice e owns cards)", "Slice e to assess"),
    row("proj-cards-numbers", "Card numbers vs own lesson", "course/modules/E/E3/cards.json", U, "Outside slice d (slice e owns cards); cards.json changed since round 9 (c144, c150, c164-c166)", "Slice e to assess"),
    row("proj-cards-duplicates", "Duplicate cards", "course/modules/E/E3/cards.json", U, "Outside slice d (slice e)", "Slice e to assess"),
    row("proj-cards-xref", "Card lesson field", "course/modules/E/E3/cards.json", U, "Outside slice d (slice e)", "Slice e to assess"),
    row("proj-cards-grade-cite", "Card grade and cite fields", "course/modules/E/E3/cards.json", U, "Outside slice d (slice e)", "Slice e to assess"),
    row("proj-cards-hypotheses", "Changed cards agree with current lesson text", "course/modules/E/E3/cards.json c144 c150 c164 c165 c166", U, "Outside slice d (slice e)", "Slice e to assess"),
    row("proj-cards-coverage", "Card coverage script", "ledgers/E3/scripts", U, "Outside slice d (slice e); not re-run here", "Slice e to re-run"),
    row("proj-structure", "Section order and build outputs", "project.html", P, "check_pages and check_projects rc=0; section order read in full (ladder, rungs, spec, questionnaire, budget, autograder, local, report, stretch, reading)"),
    row("proj-links", "Hrefs resolve", "project.html (31 distinct hrefs)", P, "Every relative file target exists under course/modules/E/E3/; anchors are covered by check_pages"),
    row("proj-grader-crra-half-cent-margin", "Half-cent margin of exact-rounding oracle values, seeds 0-49", "grader/test_project.py lines 150-159; " + S + "margins_r10.out", P, "Smallest distance to a half-cent boundary: CRRA 6.6e-6 cents (seed 41, response 36, inside the first 40 that the test uses); prospect 5.1e-6 cents (seed 7, response 149, outside that window). Float noise is about 1e-8 cents, so the exact-rounding tests are not over-constrained"),
    row("proj-delta-lab2-docstring", "Delta: lab-E3-project-2 docstring change (fa61d6e)", "tests/labs/E3/lab-E3-project-2.py line 1; project.html line 144", P, "Page and twin both now read 'Rung 2:'; checked by the page-vs-twin comparison"),
]

mutants = [
    {"id": "r10n04_probabilities_normalised_instead_of_refused", "description": "Probabilities rescaled to sum to 1 instead of raising ValueError when they do not sum to 1.", "killed_by": "test_probabilities_must_be_nonnegative_and_sum_to_exactly_one (seed 0)"},
    {"id": "r10n05_prospect_gain_inverse_exponent_one_minus_gamma", "description": "The prospect inverse for a non-negative lottery value uses exponent 1 - gamma instead of 1/(1 - gamma).", "killed_by": "RuntimeError in estimate (seed 0); the suite fails"},
    {"id": "r10n06_logit_log_term_naive_exp_overflow", "description": "Logit terms use log(1 + exp(t)) directly, with no stable form for large |z|. Survivor: informational, since the page states no numerical-stability requirement.", "killed_by": ""},
    {"id": "r10n07_kappa_standard_error_without_delta_factor", "description": "The standard error of kappa omits the delta-method factor kappa.", "killed_by": "test_standard_errors_match_the_delta_method_oracle (seed 0)"},
]

now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
counts = {s: sum(1 for r in rows if r["status"] == s) for s in (P, "FAIL", U)}
verdict = "PASS" if counts[P] == len(rows) and all(m["killed_by"] for m in mutants) else "FAIL"
frag = {
    "unit": "E3",
    "slice": "d",
    "round": 10,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-d, round 10 (did not build E3)",
    "pin": "fa61d6ec625658133891eb34667cb51101a73bff",
    "base": "33744e5a (round-9 pin); delta 33744e5a..fa61d6e: 78ae5611 and fa61d6e only touch test_project.py (lines 518-541, 849-938, 941-964), project.html (lines 144, 205, 379, 744), tests/labs/E3/lab-E3-project-2.py line 1, plans/E3-open-items.md, and cards.json (out of slice)",
    "checkout": R,
    "scratch": "/tmp/e3d-r10-ExgW",
    "verified_at": now,
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Time budget (40 min) exceeded under machine load. Not run: the full tools/mutate_graders.py --seeds 0-9 over 57 mutants (still running at the end; partial output in " + S + "mutate_E3_0_9.out) and run_alternatives.py --seeds 0-9 (still running). Cards and rubric rows are outside slice d and are left UNVERIFIABLE for slice e.",
    "summary": f"E3-d round 10: {len(rows)} rows: {counts[P]} PASS, {counts['FAIL']} FAIL, {counts[U]} UNVERIFIABLE. Gates re-run and PASS (check_projects, check_pages, check_dag, run_labs, twins isolated, page_smoke, ruff, mypy, run_graders 50/50, collect 38). Round-9 FAIL rows (plan-mutant-list, plan-fosd-tests, prose-lab2) now PASS. 4 new student-error mutants written: 3 killed, 1 survivor (informational). Verdict FAIL because the mutation run, the alternatives run and out-of-slice rows are UNVERIFIABLE.",
}
p = R + "/ledgers/E3/E3-d.json"
open(p, "w", encoding="utf-8").write(json.dumps(frag, indent=1, ensure_ascii=False) + "\n")
print("wrote", p, counts, verdict)
