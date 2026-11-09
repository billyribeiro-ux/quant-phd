"""Round 19 (E4-d): assemble ledgers/E4/E4-d.json from this round's outputs (ledgers/E4/scripts/E4-d-r19/out/).

Mutant rows come from out/mutate_graders_E4_0_9_r19.txt (tools/mutate_graders.py --unit E4 --seeds 0-9). Every row id of
the round-18 fragment is kept. Run from the checkout root with the checkout's .venv python."""
import json
import re
import glob
import os
from datetime import datetime, timezone

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE19-E4-d"
OUT = f"{ROOT}/ledgers/E4/scripts/E4-d-r19/out"
MUT = open(f"{OUT}/mutate_graders_E4_0_9_r19.txt", encoding="utf-8").read().splitlines()
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-E4-d.round18.json", encoding="utf-8"))
prev_ids = [r["id"] for r in prev["rows"]]

# ---- mutants -----------------------------------------------------------------------------------------------------
mutants = []
killed_by = {}
for line in MUT:
    m = re.match(r"^(KILLED|SURVIVED) (\S+\.py): (.*) -> (.*)$", line)
    if not m:
        continue
    status, fname, desc, killer = m.groups()
    kb = None if status == "SURVIVED" else re.sub(r"\s*\(seed \d+\)$", "", killer).strip()
    if kb is not None and kb.startswith("None"):
        kb = None
    killed_by[fname] = kb
    mutants.append({"id": fname[:-3], "file": f"ledgers/E4/mutants/{fname}", "description": desc, "killed_by": kb})
assert len(mutants) == 142, len(mutants)
survivors = [m["id"] for m in mutants if not m["killed_by"]]
assert survivors == ["mutant_r19_02_price_denominator_drops_uninformed_posterior_precision"], survivors


def kills(pattern):
    names = [f for f in killed_by if re.match(pattern, f)]
    surv = [f for f in names if killed_by[f] is None]
    return names, surv


def killed_text(pattern):
    names, surv = kills(pattern)
    if not names:
        return "no matching mutant"
    if surv:
        return f"{len(names) - len(surv)}/{len(names)} killed; survivors: {', '.join(s[:-3] for s in surv)}"
    return f"{len(names)}/{len(names)} KILLED at seeds 0-9 (out/mutate_graders_E4_0_9_r19.txt)"


R = "ledgers/E4/scripts/E4-d-r19/out"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- commands and gates --------------------------------------------------------------------------------------------
row("E4d-cmd-check-projects", "2.6-structure", "course/modules/E/E4/project.html; course/modules/E/E4/grader/", "PASS",
    f"{R}/check_projects.txt: 'check_projects E4: PASS', exit 0 (tools/check_projects.py --unit E4), pin cd4dd7df.")
row("E4d-cmd-check-pages", "2.9-structure", "course/modules/E/E4/project.html", "PASS",
    f"{R}/check_pages.txt: 'check_pages E4: PASS', exit 0 (includes the banned-string scan).")
row("E4d-cmd-check-dag", "2.9-dag", "course/modules/E/E4/project.html", "PASS",
    f"{R}/check_dag.txt: 'check_dag E4: PASS', exit 0.")
row("E4d-cmd-run-labs", "2.5-labs", "tests/labs/E4/lab-E4-project-1.py, -2.py, -3.py", "PASS",
    f"{R}/run_labs.txt: 'run_labs E4: PASS (12/12)', exit 0 (gates_driver.log).")
row("E4d-cmd-run-graders", "2.6-autograder", "course/modules/E/E4/grader/reference.py", "PASS",
    f"{R}/run_graders_0_49.txt: 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0.")
row("E4d-cmd-page-smoke-project", "2.9-smoke", "course/modules/E/E4/project.html", "PASS",
    f"{R}/page_smoke_project.txt: 'page_smoke E4: PASS', exit 0 (tools/page_smoke.py --unit E4 --pages modules/E/E4/project.html).")
row("E4d-cmd-ruff", "gate", "course/modules/E/E4 and tests/labs/E4", "PASS",
    f"{R}/ruff_check.txt 'All checks passed!' (exit 0); {R}/ruff_format.txt '16 files already formatted' (exit 0).")
row("E4d-cmd-mypy-workspace", "gate", "tests/labs/E4 and course/modules/E/E4/grader (full repository)", "PASS",
    f"{R}/mypy_workspace_r19.txt: full .venv/bin/mypy --no-incremental: 'Success: no issues found in 385 source files', exit 0.")
row("E4d-cmd-mypy-plan-command", "gate", "tests/labs/E4; course/modules/E/E4/grader", "PASS",
    f"{R}/mypy_e4.txt: mypy --no-incremental tests/labs/E4 course/modules/E/E4/grader: 'Success: no issues found in 16 source files'.")
row("E4d-cmd-pytest-relevant", "gate", "tests/test_memo_exemplars.py, test_page_checks.py, test_labs.py, test_page_smoke.py, test_run_labs.py", "PASS",
    f"{R}/pytest_relevant.txt: five files, all dots, exit 0.")
row("E4d-cmd-verify-refs", "2.1-citations", "references/references.json (E4 keys)", "PASS",
    f"{R}/verify_refs_offline.txt: 'offline integrity: 560 entries, 0 problems', exit 0; {R}/verify_refs_E4_live.txt: 'live re-verification of E4: 3 of 560 entries, 0 problems', exit 0.")
row("E4d-cmd-collect", "2.6-autograder", "course/modules/E/E4/grader/test_project.py", "PASS",
    f"{R}/collect_reference_r19.txt: '49 tests collected' with reference.py installed as solver.py (scratch copy, produced by the command in the notes); the same 49 pass at QF_SEED=0 with -W error. The bare collect without solver.py fails by design (out/collect_only.txt).")
row("E4d-lab-project-1", "2.5-labs", "course/modules/E/E4/project.html #lab-E4-project-1; tests/labs/E4/lab-E4-project-1.py", "PASS",
    f"{R}/labs_check.txt: page code equals twin; twin run alone under python -I -W error exits 0 with empty stderr; expected block equals stdout (15 lines).")
row("E4d-lab-project-2", "2.5-labs", "course/modules/E/E4/project.html #lab-E4-project-2; tests/labs/E4/lab-E4-project-2.py", "PASS",
    f"{R}/labs_check.txt: page block differs from the twin only at the blanked return line (twin 'return f_u - math.exp(A * COST) * f_i' vs page 'return ___'); twin exit 0, empty stderr, expected equals stdout.")
row("E4d-lab-project-3", "2.5-labs", "course/modules/E/E4/project.html #lab-E4-project-3; tests/labs/E4/lab-E4-project-3.py", "PASS",
    f"{R}/labs_check.txt: page code equals twin; exit 0; expected block (12 lines) equals stdout.")
row("E4d-num-lab-hypotheses", "2.4-numbers", "course/modules/E/E4/project.html:57, :175, :375", "PASS",
    "Every number in the Lab 1, Lab 2 and Lab 3 hypothesis paragraphs was compared with the expected block: Lab 1 +0.053092, -0.080731, 0.57937525, -3.45199422, 0.18904110, 0.15898618 (project.html:155-169); Lab 2 +0.037435, -0.071386, 0.57052263, 0.12466375 (:238-241); Lab 3 0.5582/0.6978/0.8373, 0.1920/0.1420/0.0889, 484 points (:490-501). All match.")
row("E4d-num-exemplar-table", "2.2-numbers", "course/modules/E/E4/project.html Exemplar B table and passage (:603-650) and Exemplar A (:543-597)", "PASS",
    "Exemplar B table rows (:632-640) equal the Lab 3 expected rows; Exemplar A's 0.5567, 0.1420 and +3.55e-14 (:565) equal the Lab 3 row 0.625|0.135. Ratios 0.6978/0.5582 = 1.2501 and 0.8373/0.5582 = 1.5000 recomputed; 'every printed gap below 4e-14' holds (max 3.55e-14).")
row("E4d-num-box-bounds", "2.4-numbers", "course/modules/E/E4/project.html:313; course/modules/E/E4/grader/instance.py:11-18", "PASS",
    f"{R}/numbers_r19.txt: tau_bar(0.150)=0.0976232722, tau_bar(0.120)=0.2375667836, tau_y(1) at sd 0.75 = 0.3076923077; the printed bounds 0.097623, 0.237567, 0.30769 agree.")
row("E4d-prose-lede-directional", "2.3-grades", "course/modules/E/E4/project.html:37 (lede)", "PASS",
    "Lede (changed this round: Proposition 5 cross-reference) states: with the fraction fixed, more noise lowers the informativeness (tau_y = lam^2 tau_e^2/(lam^2 tau_e + a^2 sd^2) falls in sd, Proposition 2); on the interior at fixed cost the fraction rises with the noise and the informativeness does not depend on it (Proposition 5, verified in props_r19.txt: lambda* ratio and sigma-invariance 1.6e-13).")
row("E4d-math-lemmas", "2.4-mathematics", "course/modules/E/E4/project.html:265-272 (Lemmas 1-3)", "PASS",
    "Re-derived by hand: Lemma 1 completes the square, g'(x)=(m-p)-axV, g(xhat)=(m-p)^2/(2aV), -a g = -(m-p)^2/(2V); Lemma 2 is the Gaussian integral (2 pi S)^(-1/2) sqrt(2 pi SV/(S+V)); Lemma 3 is the variance decomposition. The lemma text is unchanged since the previous pin.")
row("E4d-math-prop1", "2.4-mathematics", "course/modules/E/E4/project.html:275-281 (Proposition 1)", "PASS",
    f"{R}/props_r19.txt: b_s, b_u from the formulas vs the suite's independent fixed point on the clearing condition: max relative difference 5.98e-15 over 300 points (sd in [0.5,2]); b_u/b_s = -a/(lam tau_e) to 2.2e-16. The clearing algebra (3) rechecked by hand.")
row("E4d-math-prop2", "2.4-mathematics", "course/modules/E/E4/project.html:284-285 (Proposition 2)", "PASS",
    f"{R}/props_r19.txt: Corr(v,p)^2 = tau_y/(tau_v+tau_y) vs the oracle's population moments: max abs difference 1.67e-16 over 300 points.")
row("E4d-math-prop3", "2.4-mathematics", "course/modules/E/E4/project.html:287-292 (Proposition 3)", "PASS",
    f"{R}/props_r19.txt: reference indifference_gap vs the oracle's quadrature gap: max abs difference 7.8e-16; G(0+) formula equals reference gap_at_zero (derivation checked by hand, step-by-step in the Proposition's proof). Sign rule sign G = sign(tau_bar - tau_y) follows from V_U - e^(2ac) V_I.")
row("E4d-math-prop4", "2.4-mathematics", "course/modules/E/E4/project.html:294-297 (Proposition 4)", "PASS",
    f"{R}/props_r19.txt: 172 interior cases, max relative |bisection - closed form| = 4.53e-13 (page tolerance 1e-10 times root).")
row("E4d-math-prop5", "2.4-mathematics", "course/modules/E/E4/project.html:299-300 (Proposition 5, changed this round: Assuming A6)", "PASS",
    f"{R}/props_r19.txt: d lambda*/d sigma = lambda*/sigma (finite difference, max relative error 1.2e-10, roundoff of the FD step); lambda* never increases when c rises by 0.001 on the interior (max increment 0); informativeness changes by at most 1.6e-13 when sigma rises 10%.")
row("E4d-math-assumptions", "2.4-mathematics", "course/modules/E/E4/project.html:253-261 (A1-A6)", "PASS",
    "A1-A5 unchanged since the previous pin. A6 is stated as an assumption ('The page assumes this and does not prove it') and is used only in the interior case (Propositions 4 and 5, the boundary rule covers the rest), consistent with Propositions 4-5 and Lab 1 step 2.")
row("E4d-notation", "2.4-notation", "course/modules/E/E4/project.html (macros and symbols); notation/notation.json", "PASS",
    "Macros used on the page (\\\\Corr, \\\\Var, \\\\E, \\\\Normal) are registered in notation.json macros (names '\\\\Corr', '\\\\Normal', '\\\\Var', '\\\\E' present). The registry's 8 symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) do not occur on the page with another meaning; the page's own symbols (lambda, tau, sigma, Omega, V_I, V_U, b_s, b_u, G) are not registered and do not collide.")
row("E4d-banned-phrases", "2.9-banned", "course/modules/E/E4/project.html; grader/*.py; tests/labs/E4/", "PASS",
    "grep -i over project.html for TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', 'obviously', 'clearly': no hit. check_pages.txt PASS.")
row("E4d-process-words", "2.2-prose", "course/modules/E/E4/project.html (learner text)", "PASS",
    "grep -i over project.html for round, ruling, verifier, builder, architect, ledger, mutant, fanout: no learner-text hit (the 'grader' hits are the autograder's file name, not a process word).")
row("E4d-dag-links", "2.9-dag", "course/modules/E/E4/project.html (concept links, hrefs)", "PASS",
    f"{R}/check_dag.txt PASS; L06.html:66 defines 'Definition 6.2 (CARA utility)' (the citation in project.html Assumption A3 and the Rungs paragraph); L06.html:169 has the dfn of noisy-rational-expectations-equilibrium; L07.html has def-price-informativeness (cited by project.html:248).")
row("E4d-registry-muth", "2.1-citations", "course/modules/E/E4/project.html:683-685 (Reading); references/references.json", "PASS",
    f"{R}/verify_refs_E4_live.txt: live re-verification of E4 entries, 0 problems; reading section unchanged this round.")
row("E4d-registry-milgrom", "2.1-citations", "course/modules/E/E4/project.html:684-686 (Reading); references/references.json", "PASS",
    f"{R}/verify_refs_E4_live.txt: live re-verification of E4 entries, 0 problems; reading section unchanged this round.")
row("E4d-cites-only-registry", "2.1-citations", "course/modules/E/E4/project.html data-cite (:683-686)", "PASS",
    f"{R}/check_pages.txt PASS (data-cite keys must be in references.json); verify_refs offline 560/0.")
row("E4d-spec-context-sentences", "2.6-spec", "course/modules/E/E4/project.html:311-313 (Context, Inputs)", "PASS",
    "Read in full this round: Context and Inputs unchanged; each sentence matches grader/instance.py (noise_sd, info_cost ranges and rounding) and the constants a=2, tau_v=tau_e=1 of reference.py:18-20.")
row("E4d-spec-questions", "2.6-spec", "course/modules/E/E4/project.html:313-322 (Inputs, Required outputs, Constraints, Grading mode, Reading list)", "PASS",
    "Read in full this round. Questions a competent student would ask: none that the page leaves open (the constants, the tolerance, the stop rule, the exception table and the display rule are stated). Constraints sentences were checked one by one (E4d16 row).")
row("E4d-spec-ladder", "2.6-spec", "course/modules/E/E4/project.html:40-48 (ladder), :51-53 (rungs)", "PASS",
    "Rung 1 (Lab 1) is solved and annotated (six printed steps with a comment per step); Rung 2 (Lab 2) is a blanked line graded instantly; Rung 3 is the solver and report; Rung 4 is open-ended (:671-677). Changed rung-2 text matches Lab 2.")
row("E4d-prose-scope-words", "2.4-scope", "course/modules/E/E4/project.html (changed sentences :37, :53, :299-304, :313, :317, :319)", "PASS",
    f"Scope words in the changed sentences: 'every instance the generator draws has one interior root' is derived from the box bounds (E4d-num-box-bounds, {R}/numbers_r19.txt); 'the interior results also need A6' matches Propositions 4-5; 'the reported fraction within 1e-10 ... is accepted' is ruling 17 (plans/FINAL-ARCHITECT-RULINGS.md). No unproved 'all/always/only' claim found.")
row("E4d-prose-simulated-labs", "2.2-prose", "course/modules/E/E4/project.html:53, :57, :175, :313, :375", "PASS",
    "Each lab's inputs are labelled SIMULATED and stated as values; the twins read no file (run_labs and page code).")
row("E4d-prose-simulated-exemplars", "2.8-data", "course/modules/E/E4/project.html:533 (exemplar intro)", "PASS",
    "The exemplar intro says 'Two report excerpts on a SIMULATED instance'.")
row("E4d-hours-project", "2.9-hours", "course/modules/E/E4/project.html:35, :341-352; course/modules/E/E4/index.html:29", "PASS",
    "Components sum to 28 (1+1+5+8+5+5+3); data-hours-project=28 (project.html:33), eyebrow 28 h; index.html data-hours-lessons=72 + data-hours-project=28 = 100 = the module's 100 hours.")
row("E4d-hours-estimate", "2.6-hours", "course/modules/E/E4/project.html #hours (:341-352)", "PASS",
    "Verifier estimate per component: read/annotate Lab 1 ~1 h; Lab 2 ~1 h; derivation of Propositions 1-4 ~5 h; solver with the boundary rule, bisection and two exceptions plus a 50-seed local run ~7-9 h; 3x3 grid ~4-6 h; four-section write-up ~5 h; self-assessment ~3 h. Total within 30% of 28.")
row("E4d-rubric-observable", "2.6-rubric", "course/modules/E/E4/project.html:519-528 (#rubric)", "PASS",
    "Re-read this round: every descriptor cell names an observable thing (a named assumption, a formula, a sign with its grid, a stated digit rule, a named limit); C3 level 1 example 'prices become more informative' is observable as a sign with no grid.")
row("E4d-exemplar-A-calibration", "2.6-rubric-calibration", "course/modules/E/E4/project.html:535 (Exemplar A, data-scores 2,2,1,2,1)", "PASS",
    "Blind scores from the dedicated blind scorer (ruling 23): ~/.fanout/blind/E4-d.json field A = [2,2,1,2,1] for C1..C5, equal to data-scores and within one level of every annotation. Not scored by this verifier.")
row("E4d-exemplar-B-calibration", "2.6-rubric-calibration", "course/modules/E/E4/project.html:600 (Exemplar B, data-scores 4,4,4,4,4)", "PASS",
    "Blind scores from ~/.fanout/blind/E4-d.json field B = [4,4,4,4,4], equal to data-scores and within one level of every annotation. Not scored by this verifier.")
row("E4d-exemplar-annotations-hidden", "2.6-rubric", "course/modules/E/E4/project.html:537, :602 (data-reveal markup)", "PASS",
    "Each exemplar's verdict paragraph carries data-reveal (lines 537 and 602), so the official scoring is hidden until the form reveals it; the self-assessment section (:664-668) describes the reveal.")
row("E4d-grader-exceptions", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:192-234; reference.py:26-34", "PASS",
    "Read in full this round. ValueError is demanded only for the named conditions (sd zero, negative, infinite, NaN; cost negative, including -1e-12) with the table's message text; cost above 1 and sd above 1 are accepted (test_info_cost_above_one_is_accepted, test_noise_volume_far_above_one_is_accepted).")
row("E4d-grader-messages", "2.6-autograder", "course/modules/E/E4/grader/test_project.py (every expect() and pytest.fail)", "PASS",
    "Read in full this round. Each hint names the violated property and gives a concept to revisit; no message prints an expected value (pytest.fail with pytrace=False; --assert=plain).")
row("E4d-grader-oracle", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:79-172", "PASS",
    f"Read in full. The oracle does not read solver.py: it finds the price by fixed-point iteration on the regression moments and evaluates expected utility by trapezoid quadrature. Agreement with reference.py on sd in [0.5,2]: prices 5.98e-15, informativeness 1.67e-16, gap 7.8e-16 ({R}/props_r19.txt). Below sd about 0.1 the fixed point returns b_s near 0; the suite never uses the oracle there (scope note in props_r19.py).")
row("E4d-grader-instances", "2.6-autograder", "course/modules/E/E4/grader/instance.py; test_project.py:40-41", "PASS",
    f"{R}/equiv_and_instances_r19.txt: instances 0-49 all valid (noise in [0.5,0.75], cost in [0.12,0.15], three decimals); seeds 0-19 give 20 distinct informed fractions; seed 0 = (0.711, 0.143), seed 1 = (0.534, 0.145).")
row("E4d-grader-instance-docstring", "2.6-autograder", "course/modules/E/E4/grader/instance.py:1-21", "PASS",
    "Re-read: tau_bar(0.150)=0.09762327..., tau_bar(0.120)=0.23756678..., tau_y(1) >= 1/(1+4*0.75^2)=0.30769...; the bound 0 < tau_bar < 0.237567 < 0.30769 <= tau_y(1) holds (numbers_r19.txt). The docstring says the suite does not re-check it, which is true.")
row("E4d-grader-test-docstring", "2.4-docstrings", "course/modules/E/E4/grader/test_project.py docstrings (:243-245, :271-273, :388-391, :408-411, :446-449, :483-484, :584-585, :596-597, :607-609, :621-623)", "PASS",
    f"{R}/numbers_r19.txt and props: gap at 1e-12 minus limit for the six inputs is 1.02e-13 to 3.54e-13 (docstring: '1e-13 to 4e-13'); oracle minus limit at most 1.11e-16 (docstring: 'at most 1.1e-16'); domain point root 7.79e-22 (docstring 'about 7.8e-22') with |reported - exact| 1.17e-16 against tolerance 1e-14; 200 halvings give width 6.2e-61 vs 1e-10 root 2.0e-61 (docstring holds); sd-tiny claims hold.")
row("E4d-grader-reference-docstring", "2.6-autograder", "course/modules/E/E4/grader/reference.py:21-23", "PASS",
    "2^-240 = 5.66e-73 (docstring '5.7e-73'); 240 halvings reach the relative tolerance above about 6e-61 (5.66e-73/1e-12 = 5.7e-61); 200 halvings do not reach it near 2e-51 (6.2e-61 > 2e-61). Verified by numbers_r19.txt.")
row("E4d-grader-stdlib", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:549-558; reference.py:14-16; instance.py:24-26", "PASS",
    "reference.py imports math; instance.py imports random; test_solver_imports_only_the_standard_library passes for the reference (49/49 local run).")
row("E4d-runtime", "2.6-autograder", "course/modules/E/E4/grader/test_project.py", "PASS",
    f"{R}/run_graders_0_49.txt: slowest seed 0.2 s over 50 seeds; local pytest of the 49 tests: 0.04 s (collect-and-run in the scratch copy).")
row("E4d-browser-local-parity", "2.6-autograder", "course/modules/E/E4/grader/test_project.py; tools/page_smoke.py", "PASS",
    f"{R}/page_smoke_project.txt PASS and the local pytest run with the browser flags (--assert=plain -W error, QF_SEED) pass 49/49.")
row("E4d2-exemplar-B-C1-annotation", "2.3-grades", "course/modules/E/E4/project.html:604-611 (Exemplar B Model passage)", "PASS",
    "Blind C1 score for Exemplar B = 4 (ruling 23 file); the annotation 'Meets C1 level 4' names the assumptions and the results that use them, which the passage does (A1-A6 with their propositions).")
row("E4d3-cara-defined-twice", "2.9-prose", "course/modules/E/E4/project.html:259 (A3); course/modules/E/E4/L06.html:66", "PASS",
    "The CARA utility is defined once in L06 (Definition 6.2) and cited in A3 and the Rungs paragraph; project.html does not redefine it as a dfn (grep).")
row("E4d3-anchors-links", "2.9-structure", "course/modules/E/E4/project.html (href targets)", "PASS",
    f"{R}/check_pages.txt and check_dag.txt PASS; every internal href (#spec, #grader-section, #report, #stretch, #placement in index.html, #lab-E4-project-3, #self-assessment, #model, #brief) resolves to an id in the page or index.")
row("E4d3-no-figures-no-data", "2.8-data", "course/modules/E/E4/project.html", "PASS",
    "project.html has no figure, chart or dataset; grep for data-files and data-chart: none. The labs read no file.")
row("E4d3-spec-stop-rule-and-constraints", "2.6-spec", "course/modules/E/E4/project.html:317 (Constraints); grader/test_project.py; reference.py:21-22, :138", "PASS",
    "Read sentence by sentence this round against reference.py and the suite: the stop rule (1e-12 times the upper end, at most 240 halvings) is reference.py:21-22 and :138-145; the 1e-14 gap agreement is the three comparisons at test_project.py:253, :315, :400 (1e-14 * max(1,|expected|)); the 1e-10 root agreement is measured in props_r19.txt and the accuracy sweep (13,614 points, max 4.9e-13).")
row("E4d3-atlas-studios-na", "2.6-atlas", "course/modules/E/E4/project.html; curriculum entry E4", "PASS",
    "E4 has no Atlas milestone and no studio requirement in its entry (the page's reading and rung structure do not reference an Atlas contract); nothing to compare.")
row("E4d-mutants-existing", "2.6-mutation", "ledgers/E4/mutants/ (all files except the four r19 additions)", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_(?!r19_)") + " (tools/mutate_graders.py --unit E4 --seeds 0-9).")
row("E4d-mutants-new", "2.6-mutation", "ledgers/E4/mutants/mutant_r7_02_*.py, mutant_r7_03_*.py", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r7_") + ".")
row("E4d2-mutants-r2", "2.6-mutation", "ledgers/E4/mutants/mutant_r2_*.py", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r2_") + ".")
row("E4d3-mutants-r3", "2.6-mutation", "ledgers/E4/mutants/mutant_r3_*.py", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r3_") + ".")
row("E4d3-mutant-tolerance-survives", "2.6-mutation", "ledgers/E4/mutants/mutant_r3_tolerance_1e-9.py", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r3_tolerance") + ".")
row("E4d-mutants-total", "2.6-mutation", "ledgers/E4/mutants/ (142 files, including the four r19 additions)", "FAIL",
    f"{R}/mutate_graders_E4_0_9_r19.txt: 'mutate_graders E4: FAIL (141/142 killed)', exit 1. The survivor is mutant_r19_02 (E4d19-mutant-r19-02).",
    "Kill mutant_r19_02 with a grader test, or rule it equivalent under ruling 22 and move it to ledgers/E4/equivalent/ with a proof (see the E4d19-mutant-r19-02 fix).")
row("E4d-equivalent", "2.6-equivalent", "ledgers/E4/equivalent/*.py (four files) and README.md", "PASS",
    f"{R}/eq_stop_rule_r19.txt (ruling 17): r6_08 and r7_01 differ from the reference on 3000/3000 inputs but by at most 5.0e-13 relative to the root; v9_02 agrees bitwise on 3000/3000. {R}/equiv_and_instances_r19.txt: literal_price_sign agrees bitwise on 3000 inputs. alts_driver.log: all four equivalents pass 50/50.")
row("E4d-alternatives", "2.6-alternatives", "ledgers/E4/alternatives/alt_1.py .. alt_8.py", "PASS",
    "ledgers/E4/scripts/E4-d-r19/out/alts_driver.log: alt_1 .. alt_8 each '50/50 seeds pass' with the current suite (49 tests, pin cd4dd7df).")
row("E4d-starter", "2.6-autograder", "course/modules/E/E4/grader/starter.py", "PASS",
    "Read this round: signature solve_model(noise_sd: float, info_cost: float) -> dict[str, float] matches the page; raises NotImplementedError until written; no print. Byte-identical since the previous pin.")
row("E4d4-alt4-wrong-on-small-noise", "2.6-alternatives", "ledgers/E4/alternatives/alt_4.py", "PASS",
    f"{R}/alts_driver.log: alt_4 50/50 with the current suite (the suite accepts the secant alternative at small noise).")
row("E4d4-alt1-docstring", "2.6-alternatives", "ledgers/E4/alternatives/alt_1.py:1-3", "PASS",
    "Header read this round: 'bisection with a relative bracket width of 1e-12, or at most 240 halvings' matches alt_1's loop; alt_1 passes 50/50.")
row("E4d4-equivalent-price-slope", "2.6-equivalent", "ledgers/E4/equivalent/literal_price_sign.py", "PASS",
    f"{R}/equiv_and_instances_r19.txt: literal_price_sign and reference differ only in the b_u line (diff printed) and give 0 differing outputs on 3000 random inputs; the sign of b_u enters only as b_u*b_u (reference.py:101).")
row("E4d4-calibration-blind", "2.6-rubric-calibration", "course/modules/E/E4/project.html:535 (Exemplar A)", "PASS",
    "Same record as E4d-exemplar-A-calibration: ~/.fanout/blind/E4-d.json (dedicated blind scorer, ruling 23) field A = [2,2,1,2,1].")
row("E4d4-proposed-test-validated", "2.6-autograder", "course/modules/E/E4/grader/test_project.py (small-noise, corner and domain-point tests)", "PASS",
    "The small-noise, corner and domain-point tests pass for reference.py (49/49 local run) and kill the surviving-candidate mutants they target (mutate output: r6_09, f11_01, v17_02 KILLED).")
row("E4d4-mutants-killed-r4", "2.6-mutation", "ledgers/E4/mutants/mutant_r4*.py", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r4") + ".")
row("E4d4-exemplar-B-results-numbers", "2.2-numbers", "course/modules/E/E4/project.html:628-641 (Exemplar B results)", "PASS",
    "Exemplar B's 0.5582, 0.6978, 0.8373, 0.1920, 0.1420, 0.0889 and the nine gaps equal the Lab 3 expected block; 'every printed gap below 4e-14' holds (max 3.55e-14).")
row("E4d5-mutant-bracket-floor", "2.6-mutation", "ledgers/E4/mutants/mutant_r5_bracket_floor_1e-12.py", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r5_bracket_floor") + ".")
row("E4d5-mutant-sixty-halvings", "2.6-mutation", "ledgers/E4/mutants/mutant_r5_sixty_halvings_no_tolerance.py", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r5_sixty") + ".")
row("E4d5-mutant-uninformed-precision", "2.6-mutation", "ledgers/E4/mutants/mutant_r5_uninformed_posterior_precision_informed.py", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r5_uninformed") + ".")
row("E4d5-calibration-B-blind", "2.6-rubric-calibration", "course/modules/E/E4/project.html:600 (Exemplar B)", "PASS",
    "Same record: ~/.fanout/blind/E4-d.json (dedicated blind scorer, ruling 23) field B = [4,4,4,4,4], equal to data-scores.")
row("E4d6-mutant-06", "2.6-mutation", "ledgers/E4/mutants/mutant_r6_06_cost_scales_whole_gap.py", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r6_06") + ".")
row("E4d6-mutant-07", "2.6-mutation", "ledgers/E4/mutants/mutant_r6_07_unit_informativeness_discounted_by_cost.py", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r6_07") + ".")
row("E4d6-mutants-new-killed", "2.6-mutation", "ledgers/E4/mutants/mutant_r6_0*.py", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r6_") + ".")
row("E4d6-spec-variants-08-09", "2.6-mutation", "ledgers/E4/equivalent/mutant_r6_08_reports_lower_end.py; ledgers/E4/mutants/mutant_r6_09_always_200_halvings.py", "PASS",
    f"r6_08 is in equivalent/ under ruling 17 (eq_stop_rule_r19.txt: max 5.0e-13 relative). r6_09 is in mutants/: {killed_by.get('mutant_r6_09_always_200_halvings.py')} (mutate output).")
row("E4d6-stop-rule-measured", "2.6-autograder", "course/modules/E/E4/grader/reference.py:21-23, :138-145", "PASS",
    "Measured this round: at the corner root 2.02e-51 the 240-halving reference agrees with the closed form to 4.9e-13 (eq_stop_rule and sweep); 200 halvings leave a bracket of 6.2e-61 > 2e-61 (numbers_r19.txt).")
row("E4d6-alt-extra-damped", "2.6-alternatives", "ledgers/E4/scripts/E4-d-r6/candidates/damped_fixed_point_log_r6.py", "PASS",
    f"{R}/cand_damped_fixed_point_log_r6.txt: 'damped_fixed_point_log_r6.py: 0/50 seeds pass' (it fails test_tiny_noise_root_is_relatively_accurate and test_corner_root_meets_the_relative_accuracy_at_the_domain_edge). A deliberately inaccurate candidate is rejected by the suite as intended.")
row("E4d6-rung1-why", "2.9-prose", "course/modules/E/E4/project.html:170-171 (Lab 1 interpretation)", "PASS",
    "Interpretation explains each step with its quantity; 'step 6 checks the precision at the root against the target and the informativeness against the closed form of Proposition 4' matches the printed step 6 lines.")
row("E4d7-midpoint-untested", "2.6-autograder", "course/modules/E/E4/project.html:317-318; ledgers/E4/equivalent/mutant_r7_01_reports_bracket_lower_end.py", "PASS",
    "The reported midpoint is covered by ruling 17 (the page's 1e-10 agreement and the stop rule are the reference's convention); the variant reporting the bracket low differs by at most 5.0e-13 relative (eq_stop_rule_r19.txt).")
row("E4d7-cost-above-one-rejected", "2.6-autograder", "course/modules/E/E4/grader/test_project.py (test_info_cost_above_one_is_accepted, test_info_cost_far_above_one_is_accepted)", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r8_03|^mutant_r7_03") + "; the suite accepts cost 2.0, 10 and 50 (reference).")
row("E4d7-noise-above-one-rejected", "2.6-autograder", "course/modules/E/E4/grader/test_project.py (test_noise_volume_far_above_one_is_accepted)", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r7_02|^mutant_r4f_rejects_noise") + ".")
row("E4d7-alt5-docstring", "2.6-alternatives", "ledgers/E4/alternatives/alt_5.py:1-2", "PASS",
    "Header read this round ('the same model parameterised by the noise precision, with the same bracket [0, 1]'); alt_5 passes 50/50.")
row("E4d7-lab1-bracket-width", "2.5-labs", "course/modules/E/E4/project.html:170 (Lab 1 interpretation)", "PASS",
    f"{R}/numbers_r19.txt: width after 53 halvings = 1.110223e-16 = 2^-53 (is_2^-k True) and stays there after 54 (is_2^-k False, same width); the page's '53rd halving' claim holds.")
row("E4d7-lab2-blank", "2.5-labs", "course/modules/E/E4/project.html:215, :242 (Lab 2 blank)", "PASS",
    "The page code differs from the twin only at the blanked return (labs_check.txt).")
row("E4d7-instance-bound", "2.8-data", "course/modules/E/E4/grader/instance.py:1-21; project.html:313", "PASS",
    "The box bound is re-derived in numbers_r19.txt; instance draws are valid for seeds 0-49 (equiv_and_instances_r19.txt).")
row("E4d7-lab3-closed-form-sentence", "2.5-labs", "course/modules/E/E4/project.html:376-378, :490-501", "PASS",
    "Lab 3 prints the closed-form column and the largest difference (2.1e-13, expected block) and the page sentence says the difference is printed below the grid: true.")
row("E4d7-test-count", "2.6-autograder", "course/modules/E/E4/project.html:319 (Grading mode); grader/test_project.py", "PASS",
    f"The page says '49 checks'; {R}/collect_reference_r19.txt collects 49 tests with reference.py as solver.py. Round 18's count of 48 is superseded by the added domain-point test.")
row("E4d8-no-upper-bound", "2.4-scope", "course/modules/E/E4/project.html:325-327; grader/reference.py:122-151; grader/test_project.py:257-280", "PASS",
    f"numbers_r19.txt: sd 1e150 with cost 350 and sd 1e150 with cost 0.13 return the three keys with finite values; the page's range (sd up to 1e150, cost up to 350) is accepted by reference.py.")
row("E4d8-cap-100-survives", "2.6-mutation", "ledgers/E4/mutants/mutant_r8_01_cap_100_halvings.py; project.html:318", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r8_01") + ".")
row("E4d8-noise-cap-10-survives", "2.6-mutation", "ledgers/E4/mutants/mutant_r8_02_noise_above_ten_rejected.py", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r8_02") + ".")
row("E4d8-cost-cap-5-survives", "2.6-mutation", "ledgers/E4/mutants/mutant_r8_03_cost_above_five_rejected.py", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r8_03") + ".")
row("E4d8-mutants-r8-killed", "2.6-mutation", "ledgers/E4/mutants/mutant_r8_04_*.py, mutant_r8_05_*.py", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r8_0[45]") + ".")
row("E4d8-alternatives-r8", "2.6-alternatives", "ledgers/E4/alternatives/ (alt_r8_a.py, alt_r8_b.py)", "PASS",
    "Retired under ruling 18: alt_r8_* are absent from the checkout (ls ledgers/E4/alternatives/ shows alt_1..alt_8 only); the current set alt_1..alt_8 passes 50/50.")
row("E4d8-tiny-root-reference", "2.6-autograder", "course/modules/E/E4/grader/reference.py", "PASS",
    "The reference's 240-halving cap reaches the relative tolerance for roots above about 6e-61 (numbers_r19.txt: 2^-240 = 5.66e-73); the corner test at 2.0e-51 passes for the reference.")
row("E4d8-lab3-twin-page", "2.5-labs", "course/modules/E/E4/project.html:377-503; tests/labs/E4/lab-E4-project-3.py", "PASS",
    "labs_check.txt: page code equals the twin for lab 3; the twin run alone exits 0 with empty stderr; expected equals stdout.")
row("E4d9-mutant-v9-02", "2.6-mutation", "ledgers/E4/equivalent/mutant_v9_02_stop_rule_relative_to_lower_end.py", "PASS",
    f"{R}/eq_stop_rule_r19.txt: 0/3000 differing fractions; {R}/alts_driver.log: 50/50. Ruling 17 applies (differs only inside the 1e-12 stop tolerance).")
row("E4d9-mutant-v9-06", "2.6-mutation", "ledgers/E4/mutants/mutant_v9_06_gap_at_zero_from_tiny_fraction.py", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_v9_06") + ".")
row("E4d9-equivalent-r6-08-09-docstrings", "2.6-equivalent", "ledgers/E4/equivalent/mutant_r6_08_reports_lower_end.py (docstring)", "PASS",
    "The file's docstring describes the reported point (the lower end of the bracket); the code reports low, as the README says.")
row("E4d9-mutants-v9-killed", "2.6-mutation", "ledgers/E4/mutants/mutant_v9_01_*, _03_*, _05_*, _07_*", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_v9_0[1357]") + ".")
row("E4d9-mutant-docstrings", "2.6-mutation", "ledgers/E4/mutants/*.py (first docstring line of each)", "PASS",
    "Each mutant's first docstring line names the error (listed in mutate_graders output for all 142 files); the four r19 mutants' first lines name their errors.")
row("E4d9-alternatives-v9", "2.6-alternatives", "ledgers/E4/alternatives/ (alt_v9_*)", "PASS",
    "Retired under ruling 18: alt_v9_* absent from the checkout; alt_1..alt_8 pass 50/50.")
row("E4d10-delta-A1-prior-mean", "2.4-mathematics", "course/modules/E/E4/project.html:255 (A1)", "PASS",
    "A1 unchanged since the previous pin. The prior-mean normalisation is algebraically right: a common mean mu shifts v, s, the conditional means and p by mu, and the utility depends on v-p only.")
row("E4d10-delta-inputs-interior-root", "2.6-spec", "course/modules/E/E4/project.html:313 (Inputs)", "PASS",
    "The interior-root sentence is derived from the box bounds (numbers_r19.txt) and checked over 484 grid points by Lab 3.")
row("E4d10-delta-constraints-gap-at-zero", "2.6-spec", "course/modules/E/E4/project.html:317; grader/test_project.py:253, :382, :400", "PASS",
    "Gap-at-zero agreement is 1e-14 * max(1,|limit|) in all three comparisons; reference passes (49/49 local, 50/50 gate).")
row("E4d10-delta-grading-mode-43", "2.6-spec", "course/modules/E/E4/project.html:319 (Grading mode)", "PASS",
    "Now '49 checks' (changed this round from 48); collect count 49 (collect_reference_r19.txt).")
row("E4d10-delta-results-ratio", "2.4-numbers", "course/modules/E/E4/project.html:628 (ratios)", "PASS",
    "1.25 = 0.625/0.500 and 1.50 = 0.750/0.500 for the unrounded fractions (Proposition 5: lambda* proportional to sigma at fixed cost); displayed 0.6978/0.5582 = 1.2501 and 0.8373/0.5582 = 1.5000.")
row("E4d10-new-test-numbers", "2.4-docstrings", "course/modules/E/E4/grader/test_project.py (docstrings with numbers)", "PASS",
    "Numbers in the test docstrings re-derived (numbers_r19.txt): 1.02e-13..3.54e-13, 1.11e-16, 7.79e-22, 6.2e-61, 2.0e-61.")
row("E4d10-mutants-new-r10", "2.6-mutation", "ledgers/E4/mutants/mutant_r10_01..04 (seven files)", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r10_") + ".")
row("E4d10-alternatives-r10", "2.6-alternatives", "ledgers/E4/alternatives/alt_1..alt_5.py", "PASS",
    "alts_driver.log: alt_1..alt_5 each 50/50 with the current suite.")
row("E4d10-l06-dependency", "2.10-dag", "course/modules/E/E4/L06.html:57, :66, :169; course/modules/E/E4/project.html:53, :248", "PASS",
    "L06.html:66 'Definition 6.2 (CARA utility)'; L06.html:169 dfn of the noisy-rational-expectations equilibrium; the page's citations match; check_dag PASS.")
row("E4d10-lab3-numbers", "2.5-labs", "course/modules/E/E4/project.html:376-503", "PASS",
    "Every number in the Lab 3 hypothesis matches the expected block (labs_check.txt; numbers in E4d-num-lab-hypotheses).")
row("E4d11-delta-hunks", "2.9-delta", "project.html:37, :45, :53, :299-302, :316-319; grader/test_project.py:+38 lines; ledgers/E4/equivalent; ledgers/E4/mutants", "PASS",
    "Every hunk of the delta 50559266..cd4dd7df in slice d was read this round: project.html lede, rung 2, rungs paragraph, Proposition 5 and its paragraph, limits paragraph, Grading mode '49 checks'; test_project.py new domain-point test and its import of Decimal; README (retraction of v17_02, ruling 24); mutants r18_01..04 added and v17_02 moved back.")
row("E4d11-constraints-accuracy", "2.4-numbers", "course/modules/E/E4/project.html:317 (Constraints accuracy sentences)", "PASS",
    "Accuracy sweep over 13,614 interior points with sd in [1e-50, 1e2] and tau_bar >= 1e-2: max relative error 4.94e-13 against the 1e-10 requirement (props_r19.txt).")
row("E4d11-constraints-wording", "2.9-prose", "course/modules/E/E4/project.html:317", "PASS",
    "Read this round: the wording matches the implementation and the suite (no sentence claims a check the suite does not run; the 'suite does not test accuracy' sentence for small tau_bar and sd below 1e-50 is true of test_project.py).")
row("E4d11-oracle-precision", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:79-172", "PASS",
    "Oracle vs limit at the six gap-at-zero inputs: at most 1.11e-16 (numbers_r19.txt); oracle vs reference interior gap 7.8e-16 on sd in [0.5,2] (props_r19.txt).")
row("E4d11-mutants-new-r11", "2.6-mutation", "ledgers/E4/mutants/mutant_r11_01..04", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r11_") + ".")
row("E4d11-alt-closed-form", "2.6-alternatives", "ledgers/E4/scripts/E4-d-r11/alts/alt_r11_a.py", "PASS",
    f"{R}/cand_alt_r11_a.txt: 'alt_r11_a.py: 50/50 seeds pass' (run this round with run_candidate_r17.py on the current suite).")
row("E4d11-literal-price-sign-open", "2.4-mathematics", "course/modules/E/E4/project.html:275-281 (Proposition 1 sign); ledgers/E4/equivalent/literal_price_sign.py", "PASS",
    "The open item of round 11 is settled by ruling 24: the sign of b_u/b_s is unobservable (b_u enters only as b_u*b_u, reference.py:101), verified bitwise on 3000 inputs (equiv_and_instances_r19.txt). Ruling 9 provides the equivalent/ path.")
row("E4d11-lab-page-twin", "2.5-labs", "course/modules/E/E4/project.html lab blocks vs tests/labs/E4/lab-E4-project-{1,2,3}.py", "PASS",
    "labs_check.txt: lab 1 and lab 3 page code equals twin; lab 2 differs only at the blank.")
row("E4d11-plan-tolerance-documented", "2.6-spec", "course/modules/E/E4/project.html:317 (stop rule as a documented constant)", "PASS",
    "The constants 1e-12 and 240 halvings are documented on the page and in reference.py:21-23; the report must state them (brief).")
row("E4d11-mutant-r10-02", "2.6-mutation", "ledgers/E4/mutants/mutant_r10_02_cost_factor_relative_error.py", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r10_02") + ".")
row("E4d12-alt-variants-new", "2.6-alternatives", "ledgers/E4/alternatives/alt_6.py, alt_7.py, alt_8.py", "PASS",
    "alts_driver.log: alt_6 (closed form), alt_7 (sign of tau_bar minus tau_y), alt_8 (Illinois on the gap) each 50/50 with the current suite.")
row("E4d12-bisection-assumption", "2.4-mathematics", "course/modules/E/E4/project.html:318 ('the sign-change assumption'), :261 (A6)", "PASS",
    "A6 is stated and used only where the bisection needs a sign change; the boundary rule covers the rest (Proposition 4).")
row("E4d12-corner-test-docstring", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:606-616 (test_corner_root...)", "PASS",
    "Docstring: root about 2e-51 (2.02e-51 measured); 200 halvings leave a bracket of 6.2e-61 > 1e-10 * root (2.0e-61). Measured in numbers_r19.txt.")
row("E4d12-exemplar-B-sigma", "2.4-numbers", "course/modules/E/E4/project.html:607 (Exemplar B Model passage) and :628", "PASS",
    "Exemplar B's 'Proposition 5 gives this' for the proportionality is correct (lambda* = a sigma k(tau_bar)).")
row("E4d12-mutant-gap-stop", "2.6-mutation", "ledgers/E4/mutants/mutant_r12_04_stops_when_midpoint_gap_is_tiny.py", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r12_04") + ".")
row("E4d12-prose-2pow240", "2.4-numbers", "course/modules/E/E4/grader/reference.py:23; ledgers/E4/equivalent/README.md; project.html:325", "PASS",
    "2^-240 = 5.66e-73; 240 halvings suffice above about 6e-61 (5.66e-73 / 1e-12 = 5.7e-61); the page's 5.7e-73 is right.")
row("E4d12-tiny-noise-informativeness", "2.4-scope", "course/modules/E/E4/project.html:325-327 (exception table range)", "PASS",
    "numbers_r19.txt: sd 1e-300, cost 0.13 returns informativeness 0.5 and fraction 2.8e-73, while the closed form gives about 0.159 and 9.6e-301; the page says a noise volume below 1e-50 has no accuracy requirement and the solver may return an inaccurate value there (exception table). Disclosed, so PASS.")
row("E4d12-equivalent-readme-numbers", "2.6-equivalent", "ledgers/E4/equivalent/README.md (stop-rule numbers)", "PASS",
    "The README's round-11 corner numbers (cap 200: 11598 of 90000 cases above 1e-10, largest 1.5322e-10; cap 240: largest 5.1e-13; 2^-240 = 5.7e-73) are backed by ledgers/E4/scripts/E4-d-fix-r11/logs/check_corner_cap200_fix11.txt and check_corner_accuracy_fix11.txt (present in the checkout); the current reference's corner sweep gives 4.9e-13 (props_r19.txt). Historical logs, not re-run.")
row("E4d13-endpoint-gap-precision", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:387-459; project.html:317", "PASS",
    "Endpoint gap checks (fraction 0, 1 and the domain point) use 1e-14 * max(1,|expected|); reference passes; the domain-point test kills v17_02 (mutate output).")
row("E4d13-alternatives-plan-list", "2.6-alternatives", "ledgers/E4/alternatives/alt_4.py (docstring line 1); alt_5.py", "PASS",
    "Docstrings name each alternative's method (secant safeguarded by the bracket; parameterised by noise precision); all pass 50/50 (alts_driver.log).")
row("E4d13-readme-corner-domain", "2.6-equivalent", "ledgers/E4/equivalent/README.md ('Stop-rule variants', paragraph 2)", "PASS",
    "The README's corner numbers (cap 200: 1.5322e-10 relative error, 11598 cases; cap 240: 5.1e-13) are backed by ledgers/E4/scripts/E4-d-fix-r11/logs/check_corner_cap200_fix11.txt and check_corner_accuracy_fix11.txt; the current reference's sweep max is 4.9e-13 (props_r19.txt).")
row("E4d13-independent-rederivation", "2.4-mathematics", "course/modules/E/E4/project.html:257-301", "PASS",
    f"{R}/props_r19.txt: Propositions 1-5 re-derived numerically against the suite's independent oracle and the Proposition 4 closed form.")
row("E4d13-accuracy-sweep", "2.6-autograder", "course/modules/E/E4/grader/reference.py; project.html:317", "PASS",
    "props_r19.txt: 13,614 interior points, max relative error 4.94e-13 (requirement 1e-10).")
row("E4d13-extreme-inputs", "2.6-autograder", "course/modules/E/E4/project.html:316-318, :325-327; grader/reference.py", "PASS",
    f"{R}/numbers_r19.txt: sd 1e150 cost 350 -> (0, 0, -3.6e153); sd 1e-50 cost 350 -> (0, 0, -7.2e303); sd 1e-50 cost 0 -> (1, 0.5, 0). All finite; the solver returns the three keys inside the stated range.")
row("E4d13-instances-seeds-0-49", "2.6-autograder", "course/modules/E/E4/grader/instance.py; test_project.py", "PASS",
    f"{R}/equiv_and_instances_r19.txt: 0 invalid instances in seeds 0-49; 20 distinct informed fractions in seeds 0-19.")
row("E4d13-candidates-accepted", "2.6-alternatives", "ledgers/E4/alternatives/alt_1..alt_8.py; ledgers/E4/equivalent/*.py", "PASS",
    "alts_driver.log: alt_1..alt_8 and the four equivalents each 50/50; reference 50/50.")
row("E4d13-new-mutants", "2.6-mutation", "ledgers/E4/mutants/mutant_r13_01..04_*.py", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r13_") + ".")
row("E4d13-mutant-gate-final", "2.6-mutation", "ledgers/E4/mutants/ (142 files); tools/mutate_graders.py --unit E4 --seeds 0-9", "FAIL",
    f"{R}/mutate_graders_E4_0_9_r19.txt: 'mutate_graders E4: FAIL (141/142 killed)'. Survivor: mutant_r19_02.",
    "See E4d19-mutant-r19-02.")
row("E4d13-notation", "2.4-notation", "course/modules/E/E4/project.html:251 (notation paragraph)", "PASS",
    "Re-read: notation paragraph defines lambda, sigma, c, a, x, tau, tau_v, tau_e, tau_y, Omega, V_I, V_U and tau_bar; no registered notation.json symbol is redefined (see E4d-notation).")
row("E4d13-links", "2.9-dag", "course/modules/E/E4/project.html (href targets)", "PASS",
    "check_dag.txt and check_pages.txt PASS; the hrefs (#lab-E4-project-3, #brief, #rubric, #self-assessment, index.html#placement) resolve.")
row("E4d13-hours-arithmetic", "2.9-hours", "course/modules/E/E4/project.html:33, :35, :341-352; course/modules/E/E4/index.html:29, :40", "PASS",
    "28 = 1+1+5+8+5+5+3; 72 + 28 = 100; the hub's hours-split aria-label says 72 lesson and 28 project hours.")
row("E4d13-lab-twins-direct", "2.5-labs", "tests/labs/E4/lab-E4-project-1.py, -2.py, -3.py", "PASS",
    f"{R}/labs_check.txt: ALL_LABS_OK 3 labs; each twin run alone under python -I -W error exits 0 with empty stderr.")
row("E4d13-exemplar-numbers-arith", "2.4-numbers", "course/modules/E/E4/project.html Exemplar B Results passage (:628)", "PASS",
    "Arithmetic re-derived: 0.6978/0.5582 = 1.2501, 0.8373/0.5582 = 1.5000, 2 sigma sqrt(tau_bar/(1-tau_bar)) at cost 0.120 gives 0.5582, 0.6978, 0.8373.")
row("E4d14-mutants-r14-new", "2.6-mutation", "ledgers/E4/mutants/mutant_r14_01..05", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r14_") + ".")
row("E4d14-corner-scan", "2.6-autograder", "ledgers/E4/scripts/E4-d-r14 corner scan", "PASS",
    "Corner scan re-run through the accuracy sweep this round (props_r19.txt: 13,614 points, max 4.94e-13).")
row("E4d14-accuracy-sweep", "2.6-autograder", "ledgers/E4/scripts/E4-d-r14 accuracy sweep", "PASS",
    "Same sweep as E4d13-accuracy-sweep this round (props_r19.txt): max relative error 4.94e-13.")
row("E4d14-equivalent-literal-3000", "2.6-equivalent", "ledgers/E4/equivalent/literal_price_sign.py", "PASS",
    f"{R}/equiv_and_instances_r19.txt: 3000 random inputs, 0 differing outputs (any key), max abs difference 0.")
row("E4d14-delta-read", "2.9-delta", "delta 50559266..cd4dd7df for slice d", "PASS",
    "The delta since the round-18 pin was read this round (see E4d11-delta-hunks for the hunks and E4d19-delta-read for the file list).")
row("E4d15-grader-docstring-scale", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:387-404", "PASS",
    "Docstring at :388-391 and the message at :401-402 state 1e-14 relative to the larger of 1 and the limit; the code (:400) uses 1e-14 * max(1, abs(limit)).")
row("E4d15-mutants-single-change", "2.6-mutation", "ledgers/E4/mutants/*.py (142 files)", "PASS",
    f"{R}/mutant_profile_r19.txt (mutant_profile_r19.py, code-only AST comparison with docstrings stripped): 139 mutants change exactly one top-level unit; r11_01 changes gap_at_zero and indifference_gap by design (the cost factor in both); r3_closed_form changes _closed_fraction; r6_01 adds the seed table by design.")
row("E4d15-mutants-new-r15", "2.6-mutation", "ledgers/E4/mutants/mutant_r15_01..04_*.py", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r15_") + ".")
row("E4d15-cmd-mutate", "2.6-mutation", "tools/mutate_graders.py --unit E4 --seeds 0-9", "FAIL",
    f"{R}/mutate_graders_E4_0_9_r19.txt: 'mutate_graders E4: FAIL (141/142 killed)', exit 1.",
    "Kill mutant_r19_02 (E4d19-mutant-r19-02) and re-run to 142/142.")
row("E4d15-alternatives-sweep", "2.6-alternatives", "ledgers/E4/alternatives/alt_1..alt_8.py; ledgers/E4/equivalent/*.py", "PASS",
    "alts_driver.log (current suite, pin cd4dd7df): all eight alternatives 50/50, the four equivalents 50/50, reference 50/50.")
row("E4d15-exemplar-verdicts", "2.6-rubric-calibration", "course/modules/E/E4/project.html:537, :539, :602, :604 (data-reveal verdict text and passages)", "PASS",
    "Official verdict text of Exemplar A (C1 2, C2 2, C3 1, C4 2, C5 1) and B (all 4) equals the blind file; the verdict prose and the annotations agree with those scores.")
row("E4d15-stop-rule-variants-architect", "2.6-equivalent", "ledgers/E4/equivalent/README.md ('Stop-rule variants'); plans/FINAL-ARCHITECT-RULINGS.md ruling 17", "PASS",
    f"{R}/eq_stop_rule_r19.txt: r6_08 and r7_01 max 5.0e-13 relative to the root, v9_02 0 differing fractions, all against the 1e-10 page requirement. Ruling 17 applies.")
row("E4d15-literal-price-sign", "2.6-equivalent", "ledgers/E4/equivalent/literal_price_sign.py", "PASS",
    "Same as E4d4-equivalent-price-slope and E4d14-equivalent-literal-3000: 0 differing outputs on 3000 inputs; ruling 24 keeps it equivalent.")
row("E4d15-range-extremes", "2.4-scope", "course/modules/E/E4/project.html:325-327", "PASS",
    "numbers_r19.txt extremes: sd 1e150 and cost 350 return finite outputs; the 240-halving cap bound 5.7e-73 is stated and the small-sd inaccuracy (1e-300) is disclosed in the exception table.")
row("E4d15-plan-and-rulings", "2.9-plan", "plans/E4-build-plan.md; plans/FINAL-ARCHITECT-RULINGS.md (rulings 9, 17, 18, 22, 23, 24)", "PASS",
    "Rulings read in full: 9 (surviving mutant must be killed by a new test, or moved to equivalent/ if it differs only where the page states nothing), 17 (stop-rule variants), 18 (retired alternatives), 22 (tolerance binding; differences inside a stated tolerance are equivalent with a proof), 23 (blind scorer), 24 (v17_02 not equivalent; literal_price_sign stays equivalent). Rulings 9 and 22 bear on the one FAIL in this round.")
row("E4d15-reading-and-citations", "2.1-citations", "course/modules/E/E4/project.html:683-687 (Reading)", "PASS",
    f"{R}/verify_refs_E4_live.txt: 0 problems; the reading section names the two registry keys only, with no statement attributed.")
row("E4d16-mutants-v16-new", "2.6-mutation", "ledgers/E4/mutants/mutant_v16_01..04", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_v16_") + ".")
row("E4d16-mutants-ast-profile", "2.6-mutation", "ledgers/E4/mutants/*.py (AST profile)", "PASS",
    f"{R}/mutant_profile_r19.txt: code-only AST profile of all 142 files against reference.py; 139 change one top-level unit, and the three others are the designed cases named in E4d15-mutants-single-change. The v17 files each change one line (profile output).")
row("E4d16-alt-sweep", "2.6-alternatives", "ledgers/E4/alternatives/alt_1..alt_8.py", "PASS",
    "alts_driver.log: 8/8 alternatives 50/50 with the current suite.")
row("E4d16-equiv-bitwise", "2.6-equivalent", "ledgers/E4/equivalent/literal_price_sign.py", "PASS",
    f"{R}/equiv_and_instances_r19.txt: 0 differing outputs on 3000 random inputs (bitwise equality on every key).")
row("E4d16-equiv-ruling17-numeric", "2.6-equivalent", "ledgers/E4/equivalent/mutant_r6_08_reports_lower_end.py; mutant_r7_01_reports_bracket_lower_end.py; mutant_v9_02_stop_rule_relative_to_lower_end.py", "PASS",
    f"{R}/eq_stop_rule_r19.txt: relative differences to the reference at most 5.0e-13 (1e-10 requirement), over 3000 inputs in the accuracy domain.")
row("E4d16-constraints-any-sentence", "2.9-prose", "course/modules/E/E4/project.html:317 (Constraints)", "PASS",
    "Each sentence checked: no function prints (test_solver_prints_nothing); stop rule and bracket (reference.py:138-145); 1e-14 agreements (three comparisons); 1e-10 accuracy (props_r19.txt); boundary rule (test_boundary_rule_holds); invalid input exceptions (table); the display rule (Lab 3 format strings).")
row("E4d16-instances-20", "2.6-autograder", "course/modules/E/E4/grader/instance.py", "PASS",
    f"{R}/equiv_and_instances_r19.txt: 20 sampled seeds (0-19) valid and giving 20 distinct informed fractions.")
row("E4d16-exemplar-B-claims", "2.4-numbers", "course/modules/E/E4/project.html:604-662 (Exemplar B passages)", "PASS",
    "Exemplar B's claims: the six numbers of the table (Lab 3), the proportionality (Proposition 5), the sign statements on the grid (Lab 3), the gap bound 4e-14 (max 3.55e-14) and the display rule are all supported by the lab output and the propositions.")
row("E4d16-hours-band", "2.6-hours", "course/modules/E/E4/project.html:33; course/modules/E/E4/index.html:29", "PASS",
    "28 of 100 hours = 28%, inside the 10-40% band of BUILDER_RULES 4.3.")
row("E4d16-tier-M-ladder-sister", "2.6-spec", "course/modules/E/E4/project.html:40-53", "PASS",
    "Tier M: rungs 1 and 2 are short (one lab each); rung 3 is the graded deliverable; rung 4 is open.")
row("E4d17-mutant-v17-02", "2.6-mutation", "ledgers/E4/mutants/mutant_v17_02_price_slope_drops_uninformed_term.py; grader/test_project.py:445-459", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_v17_02") + " by test_gap_at_the_domain_point_matches_proposition_3_exactly. probe (equiv_and_instances_r19.txt): the mutant's gap at its own fraction differs from the exact Proposition 3 gap by 1.55e-14 against the 1e-14 tolerance.")
row("E4d17-mutants-new-killed", "2.6-mutation", "ledgers/E4/mutants/mutant_v17_01, _03, _04", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_v17_0[134]") + ".")
row("E4d17-gap-tolerance-constraint", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:45, :253, :315, :400", "PASS",
    "TOL_GAP stays 1e-8 for the root and boundary tests; the three gap comparisons use 1e-14 * max(1,|expected|) as ruling 22 requires.")
row("E4d17-oracle-agreement", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:79-172", "PASS",
    f"{R}/props_r19.txt: oracle vs reference, 7.8e-16 (gap), 6.0e-15 (prices), 1.7e-16 (informativeness) on sd in [0.5,2].")
row("E4d17-independent-rederivation", "2.4-mathematics", "course/modules/E/E4/project.html:257-301", "PASS",
    f"{R}/props_r19.txt: fixed-point and quadrature oracle reproduce Propositions 1-3; Proposition 4 closed form matches the bisection (4.5e-13).")
row("E4d18-lab1-halving-claim", "2.5-labs", "course/modules/E/E4/project.html:170 (Lab 1 interpretation)", "PASS",
    f"{R}/numbers_r19.txt: 53rd halving gives width 2^-53 = 1.110223e-16 exactly; the 54th leaves the width unchanged.")
row("E4d18-docstring-numbers", "2.4-docstrings", "grader/test_project.py:386-391 and :606-609 (docstrings)", "PASS",
    f"{R}/numbers_r19.txt: 1.02e-13..3.54e-13 (six inputs), 1.11e-16 (oracle), 2.0e-51 root, 6.2e-61 vs 2.0e-61.")
row("E4d18-spec-box-bounds", "2.4-numbers", "course/modules/E/E4/project.html:313 (Inputs box)", "PASS",
    f"{R}/numbers_r19.txt: tau_bar(0.150)=0.0976232722 (page 0.097623 lower bound), tau_bar(0.120)=0.2375667836 (page 0.237567 upper bound), tau_y(1) >= 0.3076923077 (page 0.30769).")
row("E4d18-math-derivations", "2.4-mathematics", "course/modules/E/E4/project.html:257-301", "PASS",
    f"Propositions 1-5 derived by hand this round and checked numerically ({R}/props_r19.txt).")
row("E4d18-prose-scope-words", "2.4-scope", "course/modules/E/E4/project.html:317 and the rest of the page", "PASS",
    "The changed Constraints sentence ('Any reported fraction within 1e-10 times the root ... is accepted') is ruling 17's binding text and is true (eq_stop_rule_r19.txt). No new unproved scope word in the changed prose.")
row("E4d18-test-edit-review", "2.6-autograder", "course/modules/E/E4/grader/test_project.py (full re-read this round)", "PASS",
    "Re-read in full this round (629 lines). Edits since 50559266: the domain-point test (:445-459) and the import of Decimal/localcontext (:26); the test's oracle and failure messages are unchanged in meaning.")
row("E4d18-mutants-r18-new", "2.6-mutation", "ledgers/E4/mutants/mutant_r18_01..04", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r18_") + ".")
row("E4d18-alt-eq-edited-suite", "2.6-alternatives", "ledgers/E4/alternatives/alt_1..alt_8.py; ledgers/E4/equivalent/*.py", "PASS",
    f"{R}/alts_driver.log: alt_1..alt_8 50/50; the four equivalents 50/50; reference 50/50 (pin cd4dd7df).")
row("E4d18-equiv-readme-v17-02-proof", "2.6-equivalent", "ledgers/E4/equivalent/README.md (section on mutant_v17_02, retracted under ruling 24)", "PASS",
    f"The v17_02 section is now a retraction: the equivalence claim is withdrawn and the file is back in mutants/. Its numbers reproduce: {R}/sweep_v17_02_r19.txt (BOX max 3.66e-15; DOMAIN 1513 of 43582 points over 1e-14, max 1.57e-14 at sd 3.3245979322709314e-22); the round-17 grid figure 4.219e-15 is in ledgers/E4/scripts/E4-d-fix-r17/equiv_v17_02_probe.out.")
row("E4d18-literal-price-sign-proof", "2.6-equivalent", "ledgers/E4/equivalent/literal_price_sign.py vs course/modules/E/E4/grader/reference.py", "PASS",
    "The file differs from reference.py only at the b_u line (diff printed in equiv_and_instances_r19.txt) and in the header; b_u enters only as b_u*b_u (reference.py:101); 0 differing outputs on 3000 inputs.")

# ---- new rows of this round ---------------------------------------------------------------------------------------
row("E4d19-delta-read", "2.9-delta", "delta 50559266..cd4dd7df for slice d", "PASS",
    "git diff --name-status 50559266 cd4dd7df read for slice d: course/modules/E/E4/project.html (5 hunks), grader/test_project.py (+38), ledgers/E4/equivalent/README.md and mutant_v17_02 moved to mutants/, four r18 mutants added, plans/FINAL-ARCHITECT-RULINGS.md ruling 24. Byte-identical since the previous pin: reference.py, instance.py, starter.py, tests/labs/E4/*, ledgers/E4/alternatives/*, notation/, references/, tools/, ledgers/E4/scripts/E4-d-r17/. Out of slice: cards.json (course/modules/E/E4/cards.json, not read) and the E1/LX1 test files.")
row("E4d19-project-hunks", "2.4-prose", "course/modules/E/E4/project.html:37, :45, :53, :299-304, :317, :319", "PASS",
    "Each changed hunk was read and checked: lede parenthesis (Proposition 5 assumes A6, true); rung-2 '(Proposition 3)' (Lab 2 blanks the gap return, true); rungs paragraph 'an interval on which the indifference gap changes sign' and the definitions of b_s, b_u, tau_y in Proposition 1 (true); Proposition 5 'Assuming A6' (true; Proposition 4 proof uses A6); limits paragraph 'the interior results also need A6' (true); Grading mode '49 checks' (true, collect count 49).")
row("E4d19-prop5-a6", "2.4-mathematics", "course/modules/E/E4/project.html:299-302 (Proposition 5, its proof, the closed-form paragraph)", "PASS",
    f"{R}/props_r19.txt: Proposition 5's three claims verified numerically on the interior; the closed-form paragraph (tau_bar = 2e^(-4c)-1, lambda* = 2 sigma sqrt(tau_bar/(1-tau_bar)), informativeness 1-e^(4c)/2) checked against the formulas with tau_v=tau_e=1, a=2.")
row("E4d19-test-domain-point", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:425-459 (prop3_gap_exact and test_gap_at_the_domain_point_matches_proposition_3_exactly)", "PASS",
    f"{R}/equiv_and_instances_r19.txt: the reference passes the new test (its reported gap 7.571721e-14 vs exact 7.560031e-14, difference 1.17e-16 < 1e-14); mutant_v17_02 fails it (difference 1.55e-14 > 1e-14). prop3_gap_exact's formula for Omega (1/tv + b_s^2 (1/tv+1/te) + b_u^2 sd^2 - 2 b_s/tv) equals Lemma 3's Var(v-p) for the linear price (hand derivation).")
row("E4d19-mutants-new-killed", "2.6-mutation", "ledgers/E4/mutants/mutant_r19_01, _03, _04 (written this round by the verifier)", "PASS",
    f"{R}/mutate_graders_E4_0_9_r19.txt: " + killed_text(r"^mutant_r19_0[134]") + ". The three are student errors: a precision divided rather than multiplied in F_I (r19_01), Var(y) from the signal precision (r19_03), and the limit at 0 with the informed prior-only precision (r19_04). No NameError or other spurious error in their logs (checked per mutant).")
row("E4d19-mutant-r19-02", "2.6-mutation", "ledgers/E4/mutants/mutant_r19_02_price_denominator_drops_uninformed_posterior_precision.py; course/modules/E/E4/grader/reference.py:56; project.html:276 (Proposition 1, b_s)", "FAIL",
    f"A student error the suite does not kill. mutant_r19_02 uses (1-lam)*tau_v in place of (1-lam)*(tau_v+tau_y) in the denominator of b_s (Proposition 1). It survives all 49 tests at seeds 0-9 ({R}/mutate_graders_E4_0_9_r19.txt). Its informed fraction and informativeness agree with the reference to the printed digits, because the sign of the gap depends only on tau_y (Proposition 3). Its gap differs: at a common fraction the mutant's gap is a positive multiple of the reference's (ratios 0.9553 to 0.9730 at the four points checked in omega_check.py, scratch; the factor is not derived here). On the sampled interior points (17,194 in scan_r19_02 and 60,000 in scan2_r19_02, scratch; sd 1e-8..0.3 and 1e-6.5..1e-2.5, cost 0..0.2 and 0.03..0.12) the gap differs from the exact Proposition 3 gap at the reported fraction by at most 8.5e-15 (tolerance 1e-14); no sampled point exceeds 1e-14; boundary fractions are unchanged (b_s does not depend on the uninformed term at lam = 1). So the mutant is equivalent within the stated tolerance on every sample, but no proof covers the whole domain and no test separates it at 1e-14.",
    "The architect must rule (ruling 9 / ruling 22). Either (a) kill it: add a grader test at an interior point where the mutant's gap error exceeds 1e-14, which the search did not find (worst 8.5e-15), or (b) rule it equivalent under ruling 22, move it to ledgers/E4/equivalent/ with a proof that bounds the gap difference below 1e-14 on the page's whole domain, and remove it from mutants/. Until one of these holds, the verdict is FAIL.")
row("E4d19-equiv-stop-rule-relative", "2.6-equivalent", "ledgers/E4/equivalent/mutant_r6_08_reports_lower_end.py, mutant_r7_01_reports_bracket_lower_end.py, mutant_v9_02_stop_rule_relative_to_lower_end.py", "PASS",
    f"{R}/eq_stop_rule_r19.txt (3000 inputs, tau_bar >= 1e-2, sd from 1e-50 to 1e2): r6_08 and r7_01 differ from the reference on 3000/3000 inputs by at most 5.0e-13 relative to the root; v9_02 on 0/3000; each within the 1e-10 requirement. Consistent with ruling 17.")
row("E4d19-equiv-literal-sign", "2.6-equivalent", "ledgers/E4/equivalent/literal_price_sign.py", "PASS",
    f"{R}/equiv_and_instances_r19.txt: literal_price_sign.py differs from the reference only at the b_u line; 0 differing outputs (any key) on 3000 random inputs (sd 0.05..3, c 0..0.4). Ruling 24 keeps it equivalent.")
row("E4d19-accuracy-sweep", "2.6-autograder", "course/modules/E/E4/project.html:317 (Constraints accuracy); grader/reference.py", "PASS",
    f"{R}/props_r19.txt: 13,614 interior points with sd in [1e-50, 1e2] and tau_bar >= 1e-2; max relative error of the reference's root vs the closed form 4.94e-13 against the 1e-10 requirement.")
row("E4d19-corner-200-halvings", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:606-616; reference.py:21-23", "PASS",
    f"{R}/numbers_r19.txt: at sd 1e-50 and cost 0.1707691121 the root is 2.022385e-51 (tau_bar 0.01012161); 200 halvings give width 6.2e-61 against 1e-10 root 2.0e-61 (fails); the 240-halving reference passes.")
row("E4d19-hub-hours", "2.9-hours", "course/modules/E/E4/index.html:29, :31, :40, :139", "PASS",
    "data-hours-lessons=72 and data-hours-project=28 sum to the module's 100 (index.html:31 eyebrow); project.html:33 data-hours-project=28 agrees.")
row("E4d19-calibration-blind-file", "2.6-rubric-calibration", "~/.fanout/blind/E4-d.json", "PASS",
    "The blind scoring file exists and its notes say blind scores A (2,2,1,2,1) and B (4,4,4,4,4) equal the official data-scores; this verifier did not score exemplars (ruling 23). Calibration rows PASS on that record.")

# keep every round-18 row id
new_ids = [r["id"] for r in rows]
missing = [i for i in prev_ids if i not in new_ids]
extra_prev = [i for i in new_ids if i not in prev_ids and not i.startswith("E4d19-")]
print("missing previous ids:", missing)
print("extra (not previous, not E4d19):", extra_prev)

# ---- assemble -------------------------------------------------------------------------------------------------------
from collections import Counter  # noqa: E402

counts = Counter(r["status"] for r in rows)
killed = sum(1 for m in mutants if m["killed_by"])
verdict = "PASS" if counts["PASS"] == len(rows) and killed == len(mutants) else "FAIL"
notes = [
    "Pin cd4dd7dfc2bbe0fc16b672329daa408d1d8a268b (detached); base 50559266 (round-18 pin). Delta read for slice d: project.html (5 hunks), grader/test_project.py (+38), ledgers/E4/equivalent/README.md, mutant_v17_02 moved back to mutants/, four r18 mutants added, rulings 24. Slice files byte-identical since the base: reference.py, instance.py, starter.py, tests/labs/E4/*, alternatives/*, notation/, references/, tools/.",
    "Gates (out/gates_driver.log, run_gates_r19.sh): check_pages PASS; check_dag PASS; check_projects PASS; run_labs 12/12 PASS; run_graders 0-49 reference 50/50 PASS; page_smoke project PASS; mutate_graders --unit E4 --seeds 0-9: 141/142 killed (FAIL, survivor mutant_r19_02); ruff check and format PASS; mypy --no-incremental on tests/labs/E4 and grader PASS (16 files); full mypy PASS (385 files); verify_refs --offline 560/0; verify_refs --unit E4 3/0; pytest on the five relevant files PASS.",
    "Collect: the bare collect (out/collect_only.txt) fails by design (solver module missing). With reference.py installed as solver.py in a scratch copy: 49 tests collected (out/collect_reference_r19.txt); 49 passed at QF_SEED=0 with --assert=plain -W error.",
    "Labs: labs_check.py (out/labs_check.txt): page code equals twin for labs 1 and 3; lab 2 differs only at the blanked return; each twin run alone under python -I -W error exits 0 with empty stderr; expected blocks equal stdout.",
    "Propositions and numbers: props_r19.py (out/props_r19.txt) compares the reference with the suite's independent fixed-point and quadrature oracle on sd in [0.5, 2] (the oracle's fixed point is not used below about sd 0.1); numbers_r19.py (out/numbers_r19.txt) re-derives the box bounds, the Lab 1 halving claim, the test docstring numbers, the corner and extreme inputs.",
    "Alternatives and equivalents: run_alts_r19.sh (out/alts_driver.log): alt_1..alt_8 50/50; the four equivalents 50/50; reference 50/50; historical candidates alt_r11_a 50/50 and damped_fixed_point_log_r6 0/50 (expected: it is inaccurate at small roots).",
    "Equivalence checks: equiv_and_instances_r19.py (out/equiv_and_instances_r19.txt): literal_price_sign 0 differing outputs on 3000 inputs; v9_02 0; r6_08 and r7_01 differ on 941 inputs by 4.5e-13 absolute; eq_stop_rule_r19.py (out/eq_stop_rule_r19.txt): relative differences to the root at most 5.0e-13 on 3000 accuracy-domain inputs. sweep_v17_02_r19.py reproduces the round-18 sweep (BOX max 3.66e-15; DOMAIN 1513 of 43582 over 1e-14, max 1.57e-14).",
    "Surviving mutant analysis (E4d19-mutant-r19-02): scan_r19_02.py and scan2_r19_02.py (scratch, 77,194 interior points) found no point where the gap error exceeds 1e-14 (worst 8.5e-15). No decisive input was found; the mutant is equivalent within the stated tolerance on the sample, which is not a proof. Ruling 9 / 22 decides the route; this verifier fails closed.",
    "Calibration: this verifier did not score exemplars (ruling 23). The blind file ~/.fanout/blind/E4-d.json (A 2,2,1,2,1; B 4,4,4,4,4) equals data-scores at project.html:535 and :600.",
    "Read in full this round: project.html (701 lines), grader/test_project.py (629 lines), grader/reference.py (151), grader/instance.py (37), grader/starter.py (17), ledgers/E4/equivalent/README.md, the headers of alt_1..alt_8, plans/FINAL-ARCHITECT-RULINGS.md rulings 9, 17, 18, 22, 23, 24. Mutants: all 142 first docstring lines listed by mutate_graders; AST profile of all 142 (out/mutant_profile_r19.txt).",
    "Fixed in this verifier's own work: mutant_r19_03 first draft referenced an undefined tau_e (NameError, a spurious kill); it was corrected before the final gate run and the other new mutants were checked for NameError/TypeError (none).",
    "Out of slice, not checked: cards.json (course/modules/E/E4/cards.json; the task excluded cards); index.html beyond hours and the placement anchor; L06/L07 beyond the cited lines; the E1 and LX1 test files in the delta; references/references.json attributions beyond verify_refs (the reading section names keys without attributing statements).",
    "Could not check: browser rendering of the self-assessment form and the exemplar reveal (no browser run this round; page_smoke PASS is the evidence); Pyodide timing beyond page_smoke PASS; the 1e-50 domain edge of the 240-halving cap below about 6e-61 (the page states no requirement there).",
    "Mutant count: 142 files in ledgers/E4/mutants (138 existing incl. v17_02 and r18 additions, plus r19_01..04). The four equivalents are in ledgers/E4/equivalent/ with proofs, not counted as mutants.",
]
fragment = {
    "unit": "E4",
    "slice": "d",
    "round": 19,
    "verifier": "Haiku independent verifier, E4 slice d, round 19 (did not build E4; checkout pinned at cd4dd7df, detached)",
    "pin": "cd4dd7dfc2bbe0fc16b672329daa408d1d8a268b",
    "base": "50559266 (round-18 pin); delta for slice d: project.html (lede, rung 2, rungs paragraph, Proposition 5 and its paragraph, limits, Grading mode 49), grader/test_project.py (+38, domain-point test), ledgers/E4/equivalent/README.md (v17_02 retracted), ledgers/E4/mutants (r18_01..04 added; v17_02 moved back), plans/FINAL-ARCHITECT-RULINGS.md ruling 24",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE19-E4-d",
    "scratch": "/Users/billyribeiro/.fanout/scratch-E4-d-r19 (probe copies only; every evidence script and output is under ledgers/E4/scripts/E4-d-r19/)",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": (f"E4 slice d round 19 (pin cd4dd7df): verdict {verdict}. Rows {len(rows)}: PASS {counts['PASS']}, "
                f"FAIL {counts['FAIL']}, UNVERIFIABLE {counts['UNVERIFIABLE']}. Mutants {len(mutants)}, killed {killed}. "
                "The only defect is mutant_r19_02 (b_s denominator slip) which survives every test; its gap differs from "
                "Proposition 3 by at most 8.5e-15 on 77,194 sampled interior points, so it is equivalent within tolerance "
                "on the sample but not proved equivalent; the architect must kill it or rule it equivalent (rulings 9, 22). "
                "Round-18 FAILs resolved: v17_02 is killed by the new domain-point test; the README retraction is accurate."),
}
out_path = f"{ROOT}/ledgers/E4/E4-d.json"
with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("wrote", out_path, "rows", len(rows), "status", dict(counts), "mutants", len(mutants), "killed", killed, "verdict", verdict)
