"""Write ledgers/E4/E4-d.json for round 7 (slice d). Rows are re-verified or carried from round 6 as the verifier rules say."""
import json, re, sys
from datetime import datetime, UTC
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyE7-E4-d/tools")
import ledger  # noqa: E402  (validator from the checkout)

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE7-E4-d"
S = f"{ROOT}/ledgers/E4/scripts/E4-d-r7"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-E4-d.round6.json", encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}
PIN_OLD = "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07"
PIN = "06994db16d1ab449bcf29898a7f56cfa999dce57"

def carry(rid, files):
    r = prev_rows[rid]
    assert r["status"] == "PASS", rid
    return {"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
            "evidence": f"Carried from round 6 ({files} byte-identical since the previous pin {PIN_OLD[:8]}): " + r["evidence"]}

def fresh(rid, status, evidence, fix=None):
    old = prev_rows[rid]
    row = {"id": rid, "check": old["check"], "location": old["location"], "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    return row

def new(rid, check, location, status, evidence, fix=None):
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    return row

PAGE = "course/modules/E/E4/project.html"
TEST = "course/modules/E/E4/grader/test_project.py"
RUN = {
    "check_pages": f"{S}/logs/check_pages.txt", "check_dag": f"{S}/logs/check_dag.txt",
    "check_projects": f"{S}/logs/check_projects.txt", "run_labs": f"{S}/logs/run_labs.txt",
    "run_graders": f"{S}/logs/run_graders.txt", "page_smoke": f"{S}/logs/page_smoke_project.txt",
}
L = "ledgers/E4/scripts/E4-d-r7/logs"

fresh_rows = [
    fresh("E4d-cmd-check-projects", "PASS", f"`.venv/bin/python tools/check_projects.py --unit E4` -> 'check_projects E4: PASS', exit 0 ({L}/check_projects.txt)."),
    fresh("E4d-cmd-check-pages", "PASS", f"`.venv/bin/python tools/check_pages.py --unit E4` -> 'check_pages E4: PASS', exit 0 ({L}/check_pages.txt)."),
    fresh("E4d-cmd-check-dag", "PASS", f"`.venv/bin/python tools/check_dag.py --unit E4` -> 'check_dag E4: PASS', exit 0 ({L}/check_dag.txt)."),
    fresh("E4d-cmd-run-labs", "PASS", f"`tools/run_labs.py --unit E4` -> 'run_labs E4: PASS (12/12)', exit 0 ({L}/run_labs.txt)."),
    fresh("E4d-cmd-run-graders", "PASS", f"`tools/run_graders.py --unit E4` -> 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0 ({L}/run_graders.txt)."),
    fresh("E4d-cmd-page-smoke-project", "PASS", f"`tools/page_smoke.py --unit E4 --pages project` -> 'in-browser grader: All 35 tests pass on seed 1249566998', 'page_smoke E4: PASS', exit 0 ({L}/page_smoke_project.txt)."),
    fresh("E4d-cmd-ruff", "PASS", f"`.venv/bin/python -m ruff check` and `ruff format --check` on course/modules/E/E4 and tests/labs/E4 -> 'All checks passed!' and '16 files already formatted', exit 0 each ({L}/ruff_check.txt, {L}/ruff_format.txt). Repository-wide ruff was not re-run this round; the slice's files are the only changed Python."),
    fresh("E4d-cmd-mypy-workspace", "PASS", f"`.venv/bin/mypy --no-incremental course/modules/E/E4/grader tests/labs/E4` -> 'Success: no issues found in 16 source files', exit 0 ({L}/mypy.txt)."),
    fresh("E4d-cmd-mypy-plan-command", "PASS", f"Same mypy run as E4d-cmd-mypy-workspace, which covers tests/labs/E4 and the grader ({L}/mypy.txt)."),
    fresh("E4d-cmd-pytest-relevant", "PASS", f"`.venv/bin/python -m pytest -q tests/test_memo_exemplars.py tests/test_page_checks.py tests/test_labs.py tests/test_run_labs.py` -> all dots, exit 0 ({L}/pytest_relevant.txt)."),
    fresh("E4d-cmd-verify-refs", "PASS", f"Offline re-run: `tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0 ({L}/verify_refs_offline.txt). The live E4-key run of round 6 is carried: references/references.json is byte-identical since {PIN_OLD[:8]} (git diff empty), and its E4 keys are present (muth1961rational, milgrom1982information)."),
    fresh("E4d-cmd-collect", "PASS", f"`pytest --collect-only -q` on a scratch copy with reference.py as solver.py -> '35 tests collected', and the same copy passes 35 of 35 with QF_SEED=0, -W error, --assert=plain. The page says 35 checks ({PAGE}:320)."),
    fresh("E4d-lab-project-1", "PASS", f"Page code vs twin: identical (python, {L}/lab_page_vs_twin_r7.txt); twin under `python -I -W error` exits 0 ({L}/twin_project-1.txt); expected block equals twin output (same log). Re-checked the step-3 width claim in {L}/lab1_width_r7.txt."),
    fresh("E4d-lab-project-2", "PASS", f"Page code vs twin: identical except the blank line (`return ___` vs `return f_u - math.exp(A * COST) * f_i`, the expected completion), so the page shows the twin with that one line blanked ({L}/lab_page_vs_twin_r7.txt). Twin exits 0 under -I -W error; its output equals the expected block ({L}/twin_project-2.txt)."),
    fresh("E4d-lab-project-3", "PASS", f"Page code vs twin: identical (docstring change at :383-386 mirrored in the twin); twin under -I -W error exits 0 ({L}/twin_project-3.txt); expected block equals output ({L}/lab_page_vs_twin_r7.txt)."),
    fresh("E4d-num-lab-hypotheses", "PASS", f"Every number in the Lab 1, 2 and 3 hypothesis paragraphs (:57, :176, :375-376) equals the expected block of its lab (twin outputs in {L}/): gaps +0.053092/-0.080731, lambda* 0.57937525, b_u/b_s -3.45199422, tau_bar 0.18904110, informativeness 0.15898618; gaps +0.037435/-0.071386, lambda* 0.57052263, informativeness 0.12466375; grid 0.5582/0.6978/0.8373, 0.1920/0.1420/0.0889, |gap| < 1e-13 (max 3.55e-14), agreement 2.1e-13 < 1e-12, 484 of 484."),
    fresh("E4d-num-exemplar-table", "PASS", f"Exemplar B Results passage and table (:626-639) equal the Lab 3 output rows (twin output, {L}/twin_project-3.txt); the ratios 1.25 and 1.50 of the unrounded fractions are 1.25009 and 1.50000 (displayed 1.2501, 1.5000); max |gap| 3.55e-14 < 4e-14 (:626)."),
    fresh("E4d-num-box-bounds", "PASS", f"tau_bar(0.150) = 2e^-0.6 - 1 = 0.09762327, tau_bar(0.120) = 0.23756678, 1/(1+4*0.75^2) = 0.30769 (page :314); instance.py ranges re-run over seeds 0-49: noise 0.503-0.741, cost 0.120-0.149, inside the box ({TEST} instance.py)."),
    fresh("E4d-math-assumptions", "PASS", f"A3 (:259) and A4 (:260) changed this round; re-derived. A3: exp(-a(w0+w)) = exp(-a w0) exp(-a w), a positive factor, so no comparison changes. A4: b_s = (lambda tau_e + (1-lambda) tau_y)/D > 0 for lambda > 0, so 'b_s != 0 whenever lambda > 0' holds (Prop 1 denominators positive). A1, A2, A5 unchanged (:257, :258, :261)."),
    fresh("E4d-math-prop2", "PASS", f"Proof changed (:286). Re-derived: E[v|p] = beta p, Var(v|p) = V (linear by joint normality of (v,p)); Lemma 1 gives x_U = (beta-1)p/(aV); clearing x_U = u gives p = aVu/(beta-1), a multiple of u, so Cov(v,p) = 0, beta = 0, V = 1/tau_v, p = -a u/tau_v, Corr = 0; A4 allows b_s = 0 at lambda = 0. Statement lambda in (0,1] formula re-derived (Cov(v,p)^2 / (Var v Var p) = tau_y/(tau_v+tau_y)). Also checked at lambda = 0: reference price_informativeness(0) = 0 ({ROOT}/course/modules/E/E4/grader/reference.py:price_informativeness)."),
    fresh("E4d-notation", "PASS", f"LaTeX macros on {PAGE} (\\tau, \\lambda, \\varepsilon, \\bar, \\sigma, \\E, \\Var, \\mathcal, \\kappa, \\Omega, \\Corr, \\beta, \\Normal, \\Cov and standard ones) vs notation/notation.json macros (\\E, \\Var, \\Corr, \\Cov, \\Normal, ...): every custom macro used is registered. Registered symbols (\\gamma_3, \\gamma_4, R^\\ast) do not occur on the page (grep count 0). beta, kappa, V and V_I/V_U are introduced inline with their meaning (:281-286)."),
    fresh("E4d-banned-phrases", "PASS", f"Re-read the whole page (:1-699). No banned phrase found; the changed sentences (:168, :259-260, :286, :318, :383-386, :604) contain none."),
    fresh("E4d-process-words", "PASS", f"grep on {PAGE} for round, verifier, builder, slice, audit, agent, plan, TODO, FIXME, we, our, previous, revised: no process-word hits; 'fixed' hits are the mathematical sense (fixed cost, fixed decimals)."),
    fresh("E4d-dag-links", "PASS", f"`tools/check_dag.py --unit E4` PASS ({L}/check_dag.txt). Concept links on the page resolve in the concept index (check_pages PASS, {L}/check_pages.txt)."),
    fresh("E4d-spec-questions", "PASS", f"The question the round-6 row raised (which point of the final bracket is reported) is now answered at {PAGE}:318 ('The reported lambda* is the midpoint of the final bracket'). Whether the sentence is testable is a separate row (E4d7-midpoint-untested). No other open question about the outputs, constants, exceptions or the gap at 0 and at 1 (:316-318)."),
    fresh("E4d-spec-ladder", "PASS", f"Ladder (:40-49) unchanged; rung statements checked against the page (Lab 1 one instance, six steps; Lab 2 one blank, graded instantly by run; Lab 3 nine points). Lines :168, :256-260, :283-286, :315-320 changed and were re-read."),
    fresh("E4d-prose-scope-words", "PASS", f"47 scope-word hits on {PAGE} re-read. Changed claims with scope words are computed: 'every point of that bracket is within the stated tolerance' (:318, conditional on the stop rule, width <= 1e-12 x upper end); 'at all three' (:626, computed); 'every printed gap' (:626, max 3.55e-14); 'every instance has one interior root' (:314, bound computed, instance.py). No unsupported 'always'."),
    fresh("E4d-prose-simulated-labs", "PASS", f"Labs 1-3 and the Inputs paragraph (:57, :176, :314, :375) state SIMULATED stated inputs; instance.py and the labs read no file (checked in the lab code)."),
    fresh("E4d-hours-project", "PASS", f"Eyebrow (:35) '28 hours' and data-hours-project=\"28\" (:33) equal the #hours total (:351) and the hub (course/modules/E/E4/index.html:29-43: 72 h lessons + 28 h project = 100). Re-checked."),
    fresh("E4d-hours-estimate", "PASS", f"Hours column (:344-350) sums to 1+1+5+8+5+5+3 = 28 (:351)."),
    fresh("E4d-grader-messages", "PASS", f"New test at {TEST}:359-374 has three expect() messages that name the property and carry no values; the existing messages (:49-68 and every expect call) unchanged, re-read in full."),
    fresh("E4d-grader-test-docstring", "PASS", f"Docstrings re-read in full at {TEST}:1-16, :384, :409, :446, :457-458, :468-469 (line numbers after the +18 insertion at :356). Each claim matches the code: browser and local runs use the same flags, the exact-keys and float checks, the relative stop rule, and the closed form of Proposition 4."),
    fresh("E4d-grader-stdlib", "PASS", f"test_solver_imports_only_the_standard_library ({TEST}:422-431) passes on reference, all five alternatives and the damped candidate (50 of 50 seeds each, {L}/alternatives_seeds0-49.txt)."),
    fresh("E4d-starter", "PASS", f"starter.py raises NotImplementedError for all 50 seeds ({L}/alternatives_seeds0-49.txt, the starter row: 0 pass / 50 fail), as expected for an unwritten solver; its docstring matches the spec (ValueError, three keys, no print)."),
    fresh("E4d-browser-local-parity", "PASS", f"page_smoke in-browser grader: 35 of 35 on seed 1249566998 ({L}/page_smoke_project.txt); the local run with -W error and --assert=plain: 35 passed (seed 0, scratch copy)."),
    fresh("E4d-runtime", "PASS", f"Runtime: slowest reference seed 0.2 s (run_graders); in-browser suite 0.8 s (page_smoke)."),
    fresh("E4d-alternatives", "PASS", f"alt_1..alt_5 each pass 50 of 50 seeds 0-49 against the 35 checks under -W error ({L}/alternatives_seeds0-49.txt). Their docstrings are checked in E4d7-alt5-docstring."),
    fresh("E4d2-exemplar-B-C1-annotation", "PASS", f"Exemplar B Model passage (:604) rewritten this round (A4 'when lambda > 0', use-lists per assumption). Each use claim checked against the proofs: A1 in Props 1-3; A2 clearing in Props 1 and 2 (lambda = 0 case), noise normal in Prop 3 (Lemma 2), sigma in Prop 4; A3 in Lemma 1 for Props 1-3 and the cost in Prop 3; A4 in Props 1-3 (b_s >= 0 at lambda = 0 in Prop 2); A5 in Props 1-3; Props 4-5 state A1-A5 as a block (:295, :300). Annotation (:607-608) matches."),
    fresh("E4d3-cara-defined-twice", "PASS", f"A3 (:259) cites 'Definition 6.2 of Lesson 6' (course/modules/E/E4/L06.html:66 'Definition 6.2 (CARA utility)'); L06.html:57 also cites Definition 6.2. A3 gives the utility as a reference, not a second definition; the Exemplar B model passage gives the utility as a formula, not a definition."),
    fresh("E4d3-anchors-links", "PASS", f"Same-page anchors: 12 targets, none missing; relative hrefs: 15, none missing; fragment targets exist (links_r7.py, {L}/links_r7.txt)."),
    fresh("E4d3-no-figures-no-data", "PASS", f"grep for img, svg, canvas, figure, data-file, iframe on {PAGE}: 0 matches. No figures or data files."),
    fresh("E4d3-spec-stop-rule-and-constraints", "PASS", f"Constraints (:318) state the stop rule (1e-12 times the upper end; 200 halvings), the evaluation at 0 by the limit, and the midpoint; reference.py:138-148 implements the same loop, the boundary rule and lam = 0.5*(low+high). The midpoint sentence is not testable at the suite tolerance: see E4d7-midpoint-untested."),
    fresh("E4d4-proposed-test-validated", "PASS", f"The round-4 small-noise test is in {TEST} (test_small_noise_root_is_relatively_accurate, :455-463). It passes on reference and on all five alternatives (seeds 0-49, {L}/alternatives_seeds0-49.txt), and mutant_r4_absolute_bracket_tolerance is killed by it (seed 0, {L}/mutate_graders_seeds0-9_with_r7.txt)."),
    fresh("E4d4-mutants-killed-r4", "PASS", f"All mutant_r4_* and mutant_r4f_* files are KILLED in the round-7 run of tools/mutate_graders.py --unit E4 --seeds 0-9 (log {L}/mutate_graders_seeds0-9_with_r7.txt)."),
    fresh("E4d4-exemplar-B-results-numbers", "PASS", f"Exemplar B Results (:626-639) numbers re-checked against the Lab 3 output (see E4d-num-exemplar-table)."),
    fresh("E4d4-alt4-wrong-on-small-noise", "PASS", f"alt_4 (secant with a sign-change bracket and relative stop) passes all 50 seeds ({L}/alternatives_seeds0-49.txt). The small-noise tests pass for alt_4 on every seed in this round's run."),
    fresh("E4d4-alt1-docstring", "PASS", f"alt_1.py docstring 'bisection with a fixed 120 halvings and no tolerance check' matches its code (`for _ in range(120)`, no tolerance test, ledgers/E4/alternatives/alt_1.py:76-85)."),
    fresh("E4d5-mutant-bracket-floor", "PASS", f"mutant_r5_bracket_floor_1e-12 KILLED by test_tiny_noise_root_is_relatively_accurate[1e-12] (seed 0), {L}/mutate_graders_seeds0-9_with_r7.txt."),
    fresh("E4d5-mutant-sixty-halvings", "PASS", f"mutant_r5_sixty_halvings_no_tolerance KILLED by test_tiny_noise_root_is_relatively_accurate[1e-11] (seed 0), same log."),
    fresh("E4d5-mutant-uninformed-precision", "PASS", f"mutant_r5_uninformed_posterior_precision_informed KILLED by test_indifference_holds_at_an_interior_fraction[first] (seed 0), same log."),
    fresh("E4d6-mutant-06", "PASS", f"mutant_r6_06_cost_scales_whole_gap was SURVIVING in round 6 and is now KILLED by the new test_unit_fraction_is_reported_with_a_positive_cost (seed 0), {L}/mutate_graders_seeds0-9_with_r7.txt. The test is at {TEST}:359-374."),
    fresh("E4d6-mutant-07", "PASS", f"mutant_r6_07_unit_informativeness_discounted_by_cost was SURVIVING in round 6 and is now KILLED by test_unit_fraction_is_reported_with_a_positive_cost (seed 0), same log."),
    fresh("E4d6-rung1-why", "PASS", f"Lab 1 interpretation (:171) now gives a reason for each of the six steps: step 1 (inputs fix the model), step 2 (the bisection needs a sign change), step 3 (halving; width 2^-53 from the 53rd halving on, verified by {L}/lab1_width_r7.txt: width 1.110223e-16 at halvings 53-60, and 2^-53 = 1.110223e-16), step 4 (the zero of the gap is the indifference condition of Proposition 3), step 5 (ratio of Proposition 1), step 6 (precision equals tau_bar; informativeness is the squared correlation of Proposition 2)."),
    fresh("E4d-mutants-existing", "PASS", f"ledgers/E4/mutants/mutant_01..mutant_10: all KILLED in {L}/mutate_graders_seeds0-9_with_r7.txt."),
    fresh("E4d-mutants-new", "PASS", f"mutant_d11..d18 and mutant_d6_01..d6_10: all KILLED in {L}/mutate_graders_seeds0-9_with_r7.txt."),
    fresh("E4d2-mutants-r2", "PASS", f"mutant_r2_*: all KILLED in {L}/mutate_graders_seeds0-9_with_r7.txt."),
    fresh("E4d3-mutants-r3", "PASS", f"mutant_r3_*: all KILLED in {L}/mutate_graders_seeds0-9_with_r7.txt."),
    fresh("E4d3-mutant-tolerance-survives", "PASS", f"mutant_r3_tolerance_1e-9 is KILLED in the round-7 run ({L}/mutate_graders_seeds0-9_with_r7.txt); the tolerance constants at {TEST}:44-46 are unchanged (TOL_GAP, TOL_ROOT, TOL_MOMENT)."),
    fresh("E4d6-mutants-new-killed", "PASS", f"mutant_r6_01..r6_05: all KILLED in {L}/mutate_graders_seeds0-9_with_r7.txt."),
    fresh("E4d-equivalent", "PASS", f"ledgers/E4/equivalent/literal_price_sign.py (b_u sign flipped; outputs unchanged, proof in equivalent/README.md) passes 50 of 50 seeds ({L}/alternatives_seeds0-49.txt). It is kept outside mutants/, as the README records."),
    fresh("E4d6-alt-extra-damped", "PASS", f"ledgers/E4/scripts/E4-d-r6/candidates/damped_fixed_point_log_r6.py passes 50 of 50 seeds against the round-7 suite ({L}/candidate_damped_r6_seeds0-49.txt)."),
    fresh("E4d6-stop-rule-measured", "PASS", f"Measured in round 6 (logs alt5_error_vs_closed_form_r6.txt): reference and alt_5 at 7.4e-13 relative error to the closed form; the grader's reference (reference.py:22-23, :138) and alt_5 unchanged. Carried."),
]
fresh_rows.append(fresh("E4d4-mutant-absolute-tolerance-survives", "PASS",
    f"mutant_r4_absolute_bracket_tolerance (absolute 1e-12 stop) is KILLED by test_small_noise_root_is_relatively_accurate[1e-06] (seed 0) in the round-7 run ({L}/mutate_graders_seeds0-9_with_r7.txt); the test is at {TEST}:455-463."))
fresh_rows.append(carry("E4d4-equivalent-price-slope", "ledgers/E4/scripts/E4-d-r4/check_equivalence_r4.py (candidate b_s = lambda tau_e / D)"))
carried_ids = [
    ("E4d-prose-lede-directional", "course/modules/E/E4/project.html:37 (lede)"),
    ("E4d-math-lemmas", "course/modules/E/E4/project.html:265-273"),
    ("E4d-math-prop1", "course/modules/E/E4/project.html:276-283 (line 283 is context in the diff only)"),
    ("E4d-math-prop3", "course/modules/E/E4/project.html:288-294"),
    ("E4d-math-prop4", "course/modules/E/E4/project.html:295-299"),
    ("E4d-math-prop5", "course/modules/E/E4/project.html:300-302"),
    ("E4d-spec-context-sentences", "course/modules/E/E4/project.html:312"),
    ("E4d-prose-simulated-exemplars", "course/modules/E/E4/project.html:530"),
    ("E4d-rubric-observable", "course/modules/E/E4/project.html:517-527 and the rubric.js source"),
    ("E4d-exemplar-annotations-hidden", "course/assets/js/rubric.js:147-150 and project.html data-reveal/.annotation markup"),
    ("E4d-grader-exceptions", f"{TEST}:191-234"),
    ("E4d-grader-oracle", f"{TEST}:79-170"),
    ("E4d-grader-instances", "course/modules/E/E4/grader/instance.py and test_project.py:37-40"),
    ("E4d-grader-instance-docstring", "course/modules/E/E4/grader/instance.py:1-21"),
    ("E4d-grader-reference-docstring", "course/modules/E/E4/grader/reference.py:3-10, :22-23, :92-93, :105-107"),
    ("E4d-registry-muth", "course/modules/E/E4/project.html:681 and references/references.json"),
    ("E4d-registry-milgrom", "course/modules/E/E4/project.html:682 and references/references.json"),
    ("E4d-cites-only-registry", "course/modules/E/E4/project.html data-cite (:681-682)"),
    ("E4d-hours-project-hub", None),
    ("E4d3-atlas-studios-na", "curriculum/curriculum.json (atlas array, E4 entry)"),
]
for rid, files in carried_ids:
    if files is None:
        continue
    fresh_rows.append(carry(rid, files))

fresh_rows.append(fresh("E4d-exemplar-A-calibration", "UNVERIFIABLE",
    f"Not scored blind. This session's reads of {PAGE} displayed Exemplar A's official scoring line (:535) and annotations (:541-595) before any scoring, so a blind score cannot be claimed. No rubric-only score is recorded here, because a score taken after reading the official line is not independent.",
    "A fresh verifier (or a stripped copy of the passages with data-scores, .exemplar-verdict and .annotation removed, read before the official line) scores Exemplar A and records the result."))
fresh_rows.append(fresh("E4d-exemplar-B-calibration", "UNVERIFIABLE",
    f"Not scored blind. This session displayed Exemplar B's official scoring line (:600) and its Model passage and annotation (:603-608) before scoring. No rubric-only score is recorded here, because a score taken after reading the official line is not independent.",
    "A fresh verifier scores Exemplar B from a stripped copy (no data-scores, verdict or annotation) before reading the official line, and records the score."))
fresh_rows.append(fresh("E4d4-calibration-blind", "UNVERIFIABLE",
    "Same as E4d-exemplar-A-calibration: Exemplar A (:533-596) was read with its official scoring before scoring in this session.",
    "Same as E4d-exemplar-A-calibration."))
fresh_rows.append(fresh("E4d5-calibration-B-blind", "UNVERIFIABLE",
    "Same as E4d-exemplar-B-calibration: Exemplar B (:598-660) was read with its official scoring before scoring in this session.",
    "Same as E4d-exemplar-B-calibration."))

fresh_rows.append(fresh("E4d-mutants-total", "FAIL",
    f"`tools/mutate_graders.py --unit E4 --seeds 0-9` -> 'mutate_graders E4: FAIL (62/64 killed)' ({L}/mutate_graders_seeds0-9_with_r7.txt). Survivors: mutant_r7_01_reports_bracket_lower_end.py (E4d7-midpoint-untested) and mutant_r7_03_rejects_cost_above_one.py (E4d7-cost-above-one-rejected). Round-6 survivors 06 and 07 are now killed.",
    "Fix the two rows E4d7-midpoint-untested and E4d7-cost-above-one-rejected; re-run tools/mutate_graders.py --unit E4."))
fresh_rows.append(fresh("E4d6-spec-variants-08-09", "FAIL",
    f"Round 6 classed variant 08 (reports the lower end of the final bracket) and variant 09 (always 200 halvings) as spec-compliant and not counted. That is no longer true for variant 08: {PAGE}:318 now states 'The reported lambda* is the midpoint of the final bracket'. Variant 08 differs from the reference in the last bits (exact_equal 11,939 of 20,030 inputs; worst relative 5.0e-13 in the round-6 log, logs/equivalence_within_tolerance_r6.txt) and no test separates it. Also the two files the round-6 row cites (ledgers/E4/equivalent/mutant_r6_08_*.py and mutant_r6_09_*.py) do not exist in the checkout: `find ledgers/E4 -name '*r6_08*'` is empty. Variant 09 (no relative stop) stays documented as an interpretation: the stop-rule sentence says 'stops when ... or after 200 halvings'.",
    "Remove the word 'midpoint' from :318 (state that the reported point lies in the final bracket, within the stated tolerance of the root), or add a test that fails the lower end; store variant 08 and 09 under ledgers/E4/equivalent/ or delete the citation."))
fresh_rows.append(new("E4d7-midpoint-untested", "2.6-spec / 2.6-mutation",
    f"{PAGE}:318; ledgers/E4/mutants/mutant_r7_01_reports_bracket_lower_end.py",
    "FAIL",
    f"Constraints (:318) states 'The reported lambda* is the midpoint of the final bracket'. mutant_r7_01 reports low instead of 0.5*(low+high) and SURVIVES seeds 0-9 ({L}/mutate_graders_seeds0-9_with_r7.txt: 'SURVIVED mutant_r7_01_reports_bracket_lower_end.py ... -> None'). The difference is at most half the final bracket width, below 1e-12 relative; the suite's tolerances (TOL_ROOT 1e-10, the 1e-8 relative checks at {TEST}:44-46 and :455-474) cannot see it. So the stated midpoint rule is untested, and by the ruling a surviving mutant that violates a stated sentence is a FAIL.",
    "Either delete 'midpoint' from :318 and state only that the reported point lies in the final bracket (the lower end then complies), or add a test that replays the stated stop rule (1e-12 times the upper end, 200 halvings) and requires the midpoint to 1e-15. The second option rejects alt_4 (secant), which ruling 10 requires to pass, so the first is preferred."))
fresh_rows.append(new("E4d7-cost-above-one-rejected", "2.6-spec / 2.6-mutation",
    f"{PAGE}:326-332 (exception table); {TEST} (no test with info_cost > 0.15); ledgers/E4/mutants/mutant_r7_03_rejects_cost_above_one.py",
    "FAIL",
    f"The exception table names only 'info_cost is negative' as a ValueError condition (:332). mutant_r7_03 raises ValueError for any finite cost above 1 and SURVIVES seeds 0-9 ({L}/mutate_graders_seeds0-9_with_r7.txt). No test in {TEST} uses a cost above 0.3, so the valid input range above 1 is untested. The reference accepts (0.6, 2.0): informed_fraction 0.0, gap -24.075236829295875 (proposed-test log {L}/proposed_large_cost_test_r7.txt).",
    f"Add the test in {L}/proposed_large_cost_test_r7.txt (test_large_information_cost_is_accepted: run(0.6, 2.0) gives informed_fraction 0.0 and the gap at 0 of the oracle). Validated in a scratch copy: reference and alt_1..alt_5 pass 50 of 50 seeds, mutant_r7_03 fails 50 of 50 ({L}/proposed_large_cost_test_r7_seeds0-49.txt)."))
fresh_rows.append(new("E4d7-noise-above-one-rejected", "2.6-spec / 2.6-mutation",
    f"{PAGE}:331; ledgers/E4/mutants/mutant_r7_02_rejects_noise_above_one.py",
    "PASS",
    f"mutant_r7_02 (rejects finite noise volume above 1) is KILLED by test_unit_fraction_is_reported_at_zero_cost (seed 0; it uses noise 2.0), {L}/mutate_graders_seeds0-9_with_r7.txt. The kill is incidental, but the stated behaviour (only non-positive or non-finite noise volumes are named invalid, :331) is enforced."))
fresh_rows.append(new("E4d7-alt5-docstring", "2.6-alternatives (docstring vs code)",
    "ledgers/E4/alternatives/alt_5.py:1-2 and :100",
    "FAIL",
    "The docstring says 'the same model parameterised by the noise precision, with a different bracket'. The code uses the same bracket as the reference: `lo, hi = 0.0, 1.0` (alt_5.py:100). Only the parameterisation (nu = 1/sd^2) differs. The solver's answers pass 50 of 50 seeds, so the defect is in the prose only.",
    "Change the docstring to 'the same model parameterised by the noise precision, with the same bracket [0, 1]'. (ledgers/E4/alternatives is not in this verifier's write scope, so it is not edited here.)"))
fresh_rows.append(new("E4d7-lab1-bracket-width", "2.5-labs (prose vs output)",
    f"{PAGE}:171 (Lab 1 interpretation); {L}/lab1_width_r7.txt",
    "PASS",
    "The claim 'the width is 2^-53 = 1.110e-16 from the 53rd halving on, and the remaining halvings do not shrink it' is computed: width 1.110223e-16 at halvings 53 through 60 (equal from 53 on), 2^-53 = 1.110223e-16, first k with width 2^-53 is 53. Step 3's printed bracket and width are the same numbers as the twin output."))
fresh_rows.append(new("E4d7-lab2-blank", "2.5-labs (prose vs code)",
    f"{PAGE}:176-181, :240-244",
    "PASS",
    "The page code equals the twin except the blank (`return ___`, page line 217). The interpretation (:244) 'the blank is the only line that changes' holds, and 'a gap at 1 other than -0.071386 means the sign or a term is wrong' holds because the same function computes the gap at 1 (the twin's gap at 1 is -0.071386, expected block :240)."))
fresh_rows.append(new("E4d7-instance-bound", "2.2-numbers",
    f"{TEST}; course/modules/E/E4/grader/instance.py:1-21; {PAGE}:314",
    "PASS",
    "tau_bar(0.150) = 2e^-0.6 - 1 = 0.097623; tau_bar(0.120) = 0.237567; 1/(1+4*0.75^2) = 0.307692. The bound 0 < tau_bar < 0.237567 < 0.30769 <= tau_y(1) holds on the box; instance.py ranges over seeds 0-49 are 0.503-0.741 and 0.120-0.149, inside [0.5, 0.75] and [0.12, 0.15]."))
fresh_rows.append(new("E4d7-lab3-closed-form-sentence", "2.9-prose (what a lab prints)",
    f"{PAGE}:303 (model section sentence on Lab 3); {L}/twin_project-3.txt",
    "PASS",
    "'Lab 3 prints these values on its grid, and its last column checks lambda* against the closed form of Proposition 4 at each point.' The last printed column is the closed form (0.5582 ... 0.4934), next to the bisection value; the comparison is printed as one maximum on the line below ('largest difference ... 2.1e-13'), not per row. The reader can compare each row, so the sentence is read as a per-row display, and the twin's printed closed form equals the page's expected block."))
fresh_rows.append(new("E4d7-test-count", "2.6-autograder (count)",
    f"{PAGE}:320; {TEST}",
    "PASS",
    "The page says '35 checks' (:320) and the collect-only count is 35 (scratch copy with reference.py as solver.py): equal."))

rows = [carry_row for carry_row in []]
ids_now = {r["id"] for r in fresh_rows}
MISSING = []
for rid in prev_rows:
    if rid in ids_now:
        continue
    MISSING.append(rid)
print("MISSING", MISSING)
# keep the round-6 row order, then the round-7 additions
ordered = []
seen = set()
by_id = {r["id"]: r for r in fresh_rows}
for rid in prev_rows:
    ordered.append(by_id[rid]); seen.add(rid)
for r in fresh_rows:
    if r["id"] not in seen:
        ordered.append(r)
print("rows:", len(ordered), "ids unique:", len({r['id'] for r in ordered}) == len(ordered))

# ---- mutants from the round-7 run (all 64 files under ledgers/E4/mutants/) ----
mutants = []
for line in open(f"{S}/logs/mutate_graders_seeds0-9_with_r7.txt", encoding="utf-8"):
    m = re.match(r"^(KILLED|SURVIVED) (\S+?\.py): (.*) -> (.*)$", line.rstrip("\n"))
    if not m:
        continue
    status, fname, desc, killed = m.groups()
    killed_by = "" if killed.strip() == "None" else f"{killed} (seeds 0-9 run; {L}/mutate_graders_seeds0-9_with_r7.txt)"
    mutants.append({"id": fname[:-3], "description": desc.strip().rstrip("."),
                    "file": f"ledgers/E4/mutants/{fname}", "killed_by": killed_by})
assert len(mutants) == 64, len(mutants)

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in ordered:
    counts[r["status"]] += 1
non_pass = [r["id"] for r in ordered if r["status"] != "PASS"]
killed = sum(1 for m in mutants if m["killed_by"])
fragment = {
    "unit": "E4",
    "slice": "d",
    "round": 7,
    "verifier": "Haiku independent verifier, E4 slice d, round 7 (did not build E4)",
    "pin": PIN,
    "base": f"{PIN_OLD} (round-6 pin). Delta in this slice: course/modules/E/E4/project.html (Lab 1 interpretation at :168-171; A3 :259 and A4 :260; Proposition 2 proof :286; Constraints :318 and Grading mode :320; Lab 3 lead-in :383-386; Exemplar B Model passage :604), course/modules/E/E4/grader/test_project.py (new test at :359-374 and the docstring of closed-form checks; +18 lines), tests/labs/E4/lab-E4-project-3.py (docstrings only), ledgers/E4/mutants/mutant_r6_01..07 (new since round 6 pin, listed as in the round-6 mutant set) and ledgers/E4/mutants/mutant_r7_01..03 (new this round). Lab twins project-1/2, instance.py, starter.py, reference.py, rubric.js, references.json, notation.json, the alternatives and the course/assets are byte-identical to the round-6 pin.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE7-E4-d",
    "scratch": "/tmp/e4r7-prop-* and /tmp/e4r7-alt-* (created and removed by the scripts); /tmp/e4r7-collect-* (removed). No scratch copy of the repo kept.",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": ordered,
    "mutants": mutants,
    "registry_flags": [
        "muth1961rational: present in references/references.json (entries 4 total); live E4-key verify carried from round 6 (references byte-identical).",
        "milgrom1982information: present in references/references.json; the page attributes no statement to it.",
    ],
    "freshness_flags": [
        "Exemplar A and Exemplar B calibration rows are UNVERIFIABLE: both official scoring lines were read in this session before scoring. A fresh verifier must score from stripped passages.",
    ],
    "notes": [
        f"Round 7 re-ran every command row on the pin: check_pages, check_dag, check_projects, run_labs, run_graders, page_smoke (project), ruff (E4 paths), mypy --no-incremental (grader and labs), the four relevant pytest files, verify_refs --offline, collect-only (35), the five alternatives and the damped candidate and the literal-sign variant over seeds 0-49, and tools/mutate_graders.py --unit E4 --seeds 0-9 (64 mutants).",
        "Mutation testing: 64 mutants, 62 killed. Survivors are mutant_r7_01 (lower end of the final bracket, E4d7-midpoint-untested) and mutant_r7_03 (cost above 1 rejected, E4d7-cost-above-one-rejected). Both are FAIL by the ruling because project.html states the behaviour (:318 midpoint; :332 negative cost only). Proposed fixes are given in each row; the cost fix was validated in a scratch copy.",
        "Round-6 variant 08 (lower end) is no longer spec-compliant because :318 now states the midpoint; round 6 classed it as compliant. Variant 09 (always 200 halvings) is kept as documented in round 6 (stop-rule sentence reads 'stops when ... or after 200 halvings'); it is a judgement, not a finding.",
        "ledgers/E4/equivalent/literal_price_sign.py (b_u sign flipped) is output-equivalent (README proof) and is not counted; it passes all 50 seeds. The architect item in its README is unchanged.",
        "Alternatives: alt_1..alt_5 pass 50/50 seeds. alt_5's docstring says 'a different bracket' but uses [0, 1] (E4d7-alt5-docstring, FAIL, minor).",
        "Lab 1 step-3 width claims were computed (2^-53 from the 53rd halving; equal thereafter). The Lab 1 why-note for each of the six steps is now present (E4d6-rung1-why PASS).",
        "Not checked: a fresh blind calibration of the two exemplars (UNVERIFIABLE, by design of this session); a live verify_refs run this round (carried from round 6, references unchanged); the in-browser Pyodide run beyond page_smoke; the proof of the Assumption-1 normalization beyond the page's argument; the other units' changed files (L07 lab twin and page are another slice).",
    ],
    "summary": {
        "rows": len(ordered),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants": len(mutants),
        "mutants_killed": killed,
        "non_pass_ids": non_pass,
        "alternatives_seeds_0_49": "alt_1..alt_5 50/50 each; starter 0/50 (expected); damped candidate 50/50; literal_price_sign 50/50",
        "round7_new_mutants": ["mutant_r7_01_reports_bracket_lower_end (SURVIVED)", "mutant_r7_02_rejects_noise_above_one (KILLED incidentally)", "mutant_r7_03_rejects_cost_above_one (SURVIVED)"],
    },
}
for r in ordered:
    if r["id"] == "E4d-mutants-total":
        r["location"] = "ledgers/E4/mutants/ (64 mutants)"
out = "/Users/billyribeiro/.fanout/wt/verifyE7-E4-d/ledgers/E4/E4-d.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
problems = ledger.validate(fragment, "E4-d")
print("validate:", problems)
print("counts:", counts, "mutants:", len(mutants), "killed:", killed)
print("non-pass:", non_pass)
