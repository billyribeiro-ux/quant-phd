"""Write ledgers/E4/E4-d.json for round 8 (verifier scratch script; not course content)."""
import datetime
import json
import pathlib
import re

LOG = "ledgers/E4/scripts/E4-d-r8/logs"
PIN = "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3"
BASE = "06994db16d1ab449bcf29898a7f56cfa999dce57"
CARRY = "Carried from round 7 (course/modules/E/E4/project.html lines outside the round-7-to-round-8 hunks, or the file named, byte-identical since 06994db1):"

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix or "see evidence"
    rows.append(r)


P = "PASS"
# ---- commands (run this round)
row("E4d-cmd-check-projects", "2.6-structure", "course/modules/E/E4/project.html; course/modules/E/E4/grader/", P,
    f"`tools/check_projects.py --unit E4` -> 'check_projects E4: PASS', exit 0 ({LOG}/check_projects.txt).")
row("E4d-cmd-check-pages", "2.9-structure", "course/modules/E/E4/project.html", P,
    f"`tools/check_pages.py --unit E4` -> 'check_pages E4: PASS', exit 0 ({LOG}/check_pages.txt).")
row("E4d-cmd-check-dag", "2.9-DAG", "course/modules/E/E4/project.html", P,
    f"`tools/check_dag.py --unit E4` -> 'check_dag E4: PASS', exit 0 ({LOG}/check_dag.txt).")
row("E4d-cmd-run-labs", "2.5-labs", "tests/labs/E4/lab-E4-project-1.py, -2.py, -3.py", P,
    f"`tools/run_labs.py --unit E4` -> 'run_labs E4: PASS (12/12)', exit 0 ({LOG}/run_labs.txt).")
row("E4d-cmd-run-graders", "2.6-autograder", "course/modules/E/E4/grader/reference.py", P,
    f"`tools/run_graders.py --unit E4 --seeds 0-49` -> 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0 ({LOG}/run_graders.txt).")
row("E4d-cmd-page-smoke-project", "2.9-smoke", "course/modules/E/E4/project.html", P,
    f"`tools/page_smoke.py --unit E4 --pages project` (run alone) -> 'in-browser grader: All 36 tests pass on seed 1006769816', 'page_smoke E4: PASS', exit 0 ({LOG}/page_smoke_project.txt).")
row("E4d-cmd-ruff", "conventions", "course/modules/E/E4 and tests/labs/E4 (E4 paths only)", P,
    f"`ruff check` -> 'All checks passed!'; `ruff format --check` -> '16 files already formatted' ({LOG}/ruff_check.txt, ruff_format.txt). Repository-wide ruff not run: only the E4 paths changed in this round.")
row("E4d-cmd-mypy-workspace", "conventions", "tests/labs/E4 and course/modules/E/E4/grader", P,
    f"`.venv/bin/mypy --no-incremental course/modules/E/E4/grader tests/labs/E4` -> 'Success: no issues found in 16 source files', exit 0 ({LOG}/mypy.txt).")
row("E4d-cmd-mypy-plan-command", "conventions", "tests/labs/E4; grader", P,
    f"Same mypy run as E4d-cmd-mypy-workspace ({LOG}/mypy.txt).")
row("E4d-cmd-pytest-relevant", "conventions", "tests/test_memo_exemplars.py, test_page_checks.py, test_labs.py, test_run_labs.py", P,
    f"`.venv/bin/python -m pytest -q` on the four files -> all dots, exit 0 ({LOG}/pytest_relevant.txt).")
row("E4d-cmd-verify-refs", "2.1-citations", "references/references.json (E4 keys)", P,
    f"`tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0 ({LOG}/verify_refs_offline.txt). The live run is not repeated: references/ and tools/ are byte-identical to 06994db1 (git diff empty).")
row("E4d-cmd-collect", "2.6-autograder", "course/modules/E/E4/grader/test_project.py", P,
    f"Scratch copy with reference.py as solver.py: `pytest --collect-only -q` -> '36 tests collected'; QF_SEED=0, 7, 49 with -W error --assert=plain -> '36 passed' each ({LOG}/collect.txt). Page says 36 (project.html:320).")
# ---- labs
row("E4d-lab-project-1", "2.5-labs", "course/modules/E/E4/project.html #lab-E4-project-1; tests/labs/E4/lab-E4-project-1.py", P,
    f"Twin run `python -I -W error` exit 0 ({LOG}/twin_project-1.txt); page code == twin (98 lines each; {LOG}/page_vs_twin.txt); expected block matched by run_labs.")
row("E4d-lab-project-2", "2.5-labs", "course/modules/E/E4/project.html #lab-E4-project-2; tests/labs/E4/lab-E4-project-2.py", P,
    f"Twin (completed solution) run `python -I -W error` exit 0 ({LOG}/twin_project-2.txt). Page code equals the twin except the one blank line (page 'return ___' vs twin 'return f_u - math.exp(A * COST) * f_i'; {LOG}/page_vs_twin.txt). Expected block matched by run_labs.")
row("E4d-lab-project-3", "2.5-labs", "course/modules/E/E4/project.html #lab-E4-project-3; tests/labs/E4/lab-E4-project-3.py", P,
    f"Twin run `python -I -W error` exit 0 ({LOG}/twin_project-3.txt); page code == twin (114 lines each, including the MAX_HALVINGS change); expected block matched by run_labs.")
row("E4d-num-lab-hypotheses", "2.2-numbers", "course/modules/E/E4/project.html:57, :176, :376", P,
    "Lab 1 hypothesis (+0.053092, -0.080731, 0.57937525, -3.45199422, 0.18904110, 0.15898618) equals the expected block lines 157-170. Lab 2 (+0.037435, -0.071386, 0.57052263, 0.12466375) equals lines 240-243. Lab 3 (0.5582/0.6978/0.8373; 0.1920/0.1420/0.0889; gap < 1e-13; 484 of 484) equals lines 492-502.")
row("E4d-num-exemplar-table", "2.2-numbers", "course/modules/E/E4/project.html Exemplar B table and passage (:629-641)", P,
    "Every table row equals the Lab 3 expected row. Ratios from the displayed values: 0.6978/0.5582 = 1.25009 (page: 1.2501); 0.8373/0.5582 = 1.50000 (page: 1.5000). Largest printed |gap| 3.55e-14 < 4e-14 as stated.")
row("E4d-num-box-bounds", "2.2-numbers", "course/modules/E/E4/project.html:314; course/modules/E/E4/grader/instance.py:14-17", P,
    "Recomputed: tau_bar(0.150) = 2e^-0.6 - 1 = 0.0976233; tau_bar(0.120) = 2e^-0.48 - 1 = 0.2375668; 1/(1+4*0.75^2) = 0.3076923. Page quotes 0.097623, 0.237567, 0.30769: consistent with the rounding shown.")
row("E4d-prose-lede-directional", "2.4-prose", "course/modules/E/E4/project.html:37", P,
    "Lede: the fraction rises with the noise on the interior and informativeness does not depend on the noise there (Props 4, 5: lambda* = a sigma k(tau_bar), informativeness tau_bar/(tau_v+tau_bar)); more noise at fixed lambda lowers tau_y, hence informativeness (Prop 1 formula). Consistent.")
# ---- math
row("E4d-math-lemmas", "2.3-math", "course/modules/E/E4/project.html:265-273 (Lemmas 1-3)", P,
    "Re-derived by hand: Lemma 1 (g(x*) = (m-p)^2/(2aV), -a g = -(m-p)^2/(2V)); Lemma 2 (integral gives (V/(V+S))^(1/2)); Lemma 3 (law of total variance). Hypotheses stated in each lemma match their proofs.")
row("E4d-math-prop1", "2.3-math", "course/modules/E/E4/project.html:276-283", P,
    "Re-derived: kappa = -a/(lambda tau_e) from step (3); tau_y formula from step (4); b_s formula reproduces Lab 1 printed b_s = 0.39718750 and tau_y = 0.18904110 (run_labs output).")
row("E4d-math-prop2", "2.3-math", "course/modules/E/E4/project.html:285-287", P,
    "Re-derived Corr(v,p)^2 = tau_y/(tau_v+tau_y) from Cov(v,p)=b_s/tau_v and Var(p)=b_s^2(1/tau_v+1/tau_y); lambda=0 case: b_s=0, p=-a u/tau_v, Corr=0 (step text consistent).")
row("E4d-math-prop3", "2.3-math", "course/modules/E/E4/project.html:288-293", P,
    "Sign rule: sign G = sign(V_U - e^{2ac} V_I); multiplying by (tau_v+tau_y)(tau_v+tau_e)e^{-2ac} gives tau_bar - tau_y. G(0+) formula equals Omega^(-1/2)(V_U^(1/2) - e^{ac} V_I^(1/2)) at the limits; numerically equal to reference gap_at_zero (grader oracle and reference agree within 1e-8 on 50 seeds).")
row("E4d-math-prop4", "2.3-math", "course/modules/E/E4/project.html:295-298", P,
    "lambda* = a sigma sqrt(tau_bar/(tau_e(tau_e - tau_bar))) re-derived from tau_y(lambda*)=tau_bar. Bisection vs closed form on the 3x3 grid: largest difference 2.1e-13 (lab output). Informativeness identity 1 - e^{2ac} tau_v/(tau_v+tau_e) re-derived.")
row("E4d-math-prop5", "2.3-math", "course/modules/E/E4/project.html:300-301", P,
    "d lambda*/d sigma = lambda*/sigma (lambda* linear in sigma); tau_bar strictly decreasing in c, k strictly increasing, so lambda* decreasing in c; informativeness independent of sigma. Re-derived.")
row("E4d-math-assumptions", "2.3-math", "course/modules/E/E4/project.html:257-262 (A1-A5), :604-606 (Exemplar B use list)", P,
    "Read in full this round. A3 positive-factor argument and A4 b_s != 0 for lambda > 0 consistent with Prop 1 denominators. No contradiction with Props 1-5.")
row("E4d-notation", "2.7-notation", "course/modules/E/E4/project.html (math spans); notation/notation.json", P,
    "Read every math span in the round-8 changed text (:315-326, :396-398 of the lab code). No symbol outside the existing notation. notation/notation.json is byte-identical to 06994db1 (git diff empty).")
row("E4d-banned-phrases", "2.8-prose", "course/modules/E/E4/project.html; grader/*.py; tests/labs/E4/lab-E4-project-*.py", P,
    "Read in full; no banned phrase found in the changed text.")
row("E4d-process-words", "2.8-prose", "course/modules/E/E4/project.html; grader/*.py; labs", P,
    "grep -i 'round|verifier|builder|ruling|architect|audit|previous|fixed in' over the slice: only 'round(' calls in instance.py and test_project.py (code), and 'fixed in your module/solver.py' (constants, :314, instance.py:10). No process words in learner text.")
row("E4d-dag-links", "2.9-DAG", "course/modules/E/E4/project.html", P,
    f"check_dag and check_pages PASS this round ({LOG}/check_dag.txt, check_pages.txt).")
row("E4d-registry-muth", "2.1-citations", "course/modules/E/E4/project.html:684; references/references.json", P,
    "muth1961rational present in references/references.json (offline integrity 0 problems, verify_refs). The page attributes no statement to it (:682).")
row("E4d-registry-milgrom", "2.1-citations", "course/modules/E/E4/project.html:685; references/references.json", P,
    "milgrom1982information present in references/references.json; the page attributes no statement to it (:682).")
row("E4d-cites-only-registry", "2.1-citations", "course/modules/E/E4/project.html data-cite (:684-685)", P,
    CARRY + " exactly two data-cite values, both registry keys (grep in this round's read of the full page).")
row("E4d-spec-context-sentences", "2.4-spec", "course/modules/E/E4/project.html:312 (Context)", P,
    CARRY + " the Context dd has four sentences (2-4 required); line 312 unchanged.")
row("E4d-spec-questions", "2.4-spec", "course/modules/E/E4/project.html:314-322 (Inputs, Required outputs, Constraints, Grading mode)", P,
    "Read this round. Outputs, constants, exceptions and the gap at 0 and at 1 are all specified; the reported point of the final bracket is now specified as 'lies in the final bracket' (:318), which the grader tests within tolerance.")
row("E4d-spec-ladder", "2.4-spec", "course/modules/E/E4/project.html:40-49, :51-305, :308, :669-675", P,
    "Read this round. Ladder rungs match the page: Lab 1 one instance with six printed steps; Lab 2 one blank; Lab 3 nine points. Changed lines :318, :326, :320 re-read.")
row("E4d-prose-scope-words", "2.4-prose", "course/modules/E/E4/project.html:326 ('The table names no upper bound: ... valid inputs, and return the three keys')", "FAIL",
    "Scope claim 'no upper bound ... valid inputs, and return the three keys' is false for finite inputs in the reference's floating-point range. Reference (course/modules/E/E4/grader/reference.py, solve_model) on scratch copies: solve_model(0.6, 355.0) -> OverflowError (math range error); solve_model(0.6, 1000.0) -> OverflowError; solve_model(1e154, 0.13) -> ZeroDivisionError; solve_model(1e200, 0.13) -> ZeroDivisionError; solve_model(1e153, 0.13) -> ok. Log: " + LOG + "/probe_reference_r8.txt.",
    "Either narrow :326 to the range where the arithmetic is finite (costs up to 354 (cost 355 overflows exp(2c)), noise volumes up to 1e153) or make solve_model return finite keys for those inputs and add a test. Cross-ref E4d8-no-upper-bound.")
row("E4d-prose-simulated-labs", "2.4-prose", "course/modules/E/E4/project.html:57, :176, :314, :375", P,
    "Read this round: each lab and the Inputs paragraph state the SIMULATED stated inputs; the labs read no file (twin source inspected).")
row("E4d-prose-simulated-exemplars", "2.4-prose", "course/modules/E/E4/project.html:530 (exemplar intro)", P,
    CARRY + " the exemplar intro says SIMULATED and names the Lab 3 grid point; line 530 unchanged.")
row("E4d-hours-project", "2.4-hours", "course/modules/E/E4/project.html:33, :35, :341-352; course/modules/E/E4/index.html:29, :31", P,
    "Eyebrow 28 h, data-hours-project 28, #hours total 28. Hub: data-hours-lessons 72 + data-hours-project 28 = 100 (index.html:29, :31); the hub hunks this round changed only the lede and the Data text, not the hours.")
row("E4d-hours-estimate", "2.4-hours", "course/modules/E/E4/project.html #hours (:344-351)", P,
    "1+1+5+8+5+5+3 = 28 (recomputed).")
row("E4d-rubric-observable", "2.4-rubric", "course/modules/E/E4/project.html:517-527 (#rubric); course/assets/js/rubric.js", P,
    CARRY + " the rubric table and the rubric.js source are unchanged (round-7 delta hunks are at :315-326 and the lab code only).")
row("E4d-exemplar-A-calibration", "2.4-rubric-calibration", "course/modules/E/E4/project.html:533-597 (Exemplar A, data-scores 2,2,1,2,1)", "UNVERIFIABLE",
    "Not scored blind. This round's full read of course/modules/E/E4/project.html displayed the official scoring line (:538) and annotations before any scoring, so an independent score cannot be claimed.",
    "A fresh verifier scores Exemplar A from a stripped copy of the passages (no data-scores, no data-reveal, no annotation) and compares.")
row("E4d-exemplar-B-calibration", "2.4-rubric-calibration", "course/modules/E/E4/project.html:598-661 (Exemplar B, data-scores 4,4,4,4,4)", "UNVERIFIABLE",
    "Not scored blind. This round's full read displayed the official scoring line (:603) and the Model passage and annotation before scoring.",
    "A fresh verifier scores Exemplar B from a stripped copy of the passages and compares.")
row("E4d-exemplar-annotations-hidden", "2.4-rubric", "course/assets/js/rubric.js:147-150; project.html data-reveal and .annotation", P,
    CARRY + " rubric.js is byte-identical to the round-5 pin (git diff 7376a5e..4bd8cb9 empty for course/assets/js).")
# ---- grader
row("E4d-grader-exceptions", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:191-234; reference.py:26-34; project.html:326-332", P,
    "Named conditions tested in both directions (sd 0, -SD, inf, nan rejected; 1e-12 accepted; cost -0.01, -1e-12 rejected; cost 0 accepted). Re-run: 36/36 on seeds 0, 7, 49. Unnamed-but-valid inputs that raise (E4d-prose-scope-words) are a page/reference mismatch recorded there.")
row("E4d-grader-messages", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:49-68 and every expect() call", P,
    "Read in full this round. Every hint names the property and carries no value; the new test's three hints (:245-253) follow the same form.")
row("E4d-grader-oracle", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:79-170", P,
    CARRY + " the oracle lines are unchanged; the suite passes 36/36 for the reference on seeds 0, 7, 49 and 50/50 on seeds 0-49 (run_graders).")
row("E4d-grader-instances", "2.6-autograder", "course/modules/E/E4/grader/instance.py; test_project.py:37-40", P,
    CARRY + " instance.py unchanged; read this round: uniform draws rounded to three decimals on [0.5,0.75] and [0.12,0.15] match the page's box (:314).")
row("E4d-grader-instance-docstring", "2.2-numbers", "course/modules/E/E4/grader/instance.py:1-21", P,
    "Read this round. Numbers 0.09762327..., 0.23756678..., 1/(1+4*0.75^2) = 0.30769... recomputed (E4d-num-box-bounds). The claim that the suite does not re-check the bound is consistent with the file.")
row("E4d-grader-test-docstring", "2.2-numbers", "course/modules/E/E4/grader/test_project.py:481-484 (new docstring, 6e-49)", P,
    "2^-200 = 6.22e-61; 6.22e-61 / 1e-12 = 6.2e-49, so 200 halvings reach the relative tolerance for every root above about 6e-49 (computed). Other docstrings (:9-16, :455-456, :471) read this round and consistent with the code.")
row("E4d-grader-reference-docstring", "2.2-numbers", "course/modules/E/E4/grader/reference.py:21-23", P,
    "Same 6e-49 check (computed). The reference's docstrings for each proposition read this round.")
row("E4d-grader-stdlib", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:436-445; reference.py; ledgers/E4/alternatives/*.py", P,
    "The stdlib test passes on the reference and on every alternative and variant run this round (50/50 seeds each; ledgers/E4/scripts/E4-d-r8/logs/alternatives_seeds0-49.txt).")
row("E4d-runtime", "2.6-autograder", "course/modules/E/E4/grader/test_project.py", P,
    "run_graders slowest reference seed 0.2 s (run_graders.txt); in-browser suite 0.8 s (page_smoke_project.txt).")
row("E4d-browser-local-parity", "2.6-autograder", "course/modules/E/E4/grader/test_project.py; tools/page_smoke.py", P,
    "In-browser (page_smoke): 36 of 36 on seed 1006769816. Local pytest with -I -W error --assert=plain on seeds 0, 7, 49: 36 passed each (collect.txt).")
row("E4d2-exemplar-B-C1-annotation", "2.4-rubric", "course/modules/E/E4/project.html:604-607 (Exemplar B Model passage and annotation)", P,
    CARRY + " lines 604-607 unchanged.")
row("E4d3-cara-defined-twice", "2.4-prose", "course/modules/E/E4/project.html:259 (A3); course/modules/E/E4/L06.html:57, :66", P,
    CARRY + " A3 cites Definition 6.2 of Lesson 6 as a reference; L06.html is not in the round-7-to-round-8 delta.")
row("E4d3-anchors-links", "2.9-structure", "course/modules/E/E4/project.html (href targets)", P,
    f"check_pages PASS this round ({LOG}/check_pages.txt); no new link targets in the round-8 delta.")
row("E4d3-no-figures-no-data", "2.4-prose", "course/modules/E/E4/project.html", P,
    "Full read this round: no img, svg, canvas, figure, data-file or iframe in the page; no data file cited.")
row("E4d3-spec-stop-rule-and-constraints", "2.4-spec", "course/modules/E/E4/project.html:318 (Constraints); grader/test_project.py:469-490", "FAIL",
    "Constraints state the stop rule as 'stops when the bracket is narrower than 1e-12 times its upper end, or after 200 halvings'. The 200-halving limb is not tested: a solver with a 100-halving cap survives the suite (mutant_r8_01_cap_100_halvings.py, SURVIVED seeds 0-9, " + LOG + "/mutate_graders_seeds0-9_r8.txt). At sigma = 1e-30 it returns 1.1832913578e-30 against the closed form 9.656254e-31 (23% high, gap -0.0291 instead of +3.8e-14; " + LOG + "/probe_cap100_r8.txt) (E4d8-cap-100-survives).",
    "Add a test at sigma = 1e-30 (and 1e-40) that compares with the closed form at relative 1e-8 (proposed_tests_r8.py in ledgers/E4/scripts/E4-d-r8/); the reference passes it, the 100-halving mutant fails it.")
row("E4d3-atlas-studios-na", "2.9-structure", "atlas/, studios", P,
    "Not applicable to this slice: no atlas or studio file is in the slice (carried as not applicable).")
# ---- mutants
row("E4d-mutants-existing", "2.6-mutants", "ledgers/E4/mutants/ (the 63 pre-round-8 files)", P,
    f"All 63 pre-existing mutants are KILLED in {LOG}/mutate_graders_seeds0-9_r8.txt (mutate_graders E4 KILLED lines; 3 SURVIVED lines are the round-8 files only).")
row("E4d-mutants-new", "2.6-mutants", "ledgers/E4/mutants/mutant_r7_02_*.py, mutant_r7_03_*.py", P,
    "mutant_r7_02_rejects_noise_above_one and mutant_r7_03_rejects_cost_above_one: KILLED in the round-8 run (r7_03 by test_info_cost_above_one_is_accepted, the new test at test_project.py:242-253). mutant_r7_01 is now spec-compliant (see E4d7-midpoint-untested) and lives in ledgers/E4/equivalent/.")
row("E4d2-mutants-r2", "2.6-mutants", "ledgers/E4/mutants/mutant_r2_*.py", P,
    "All four r2 mutants KILLED in the round-8 log.")
row("E4d3-mutants-r3", "2.6-mutants", "ledgers/E4/mutants/mutant_r3_*.py", P,
    "All r3 mutants KILLED in the round-8 log.")
row("E4d3-mutant-tolerance-survives", "2.6-mutants", "ledgers/E4/mutants/mutant_r3_tolerance_1e-9.py", P,
    "KILLED in the round-8 log (test_fraction_is_the_oracle_root[first]).")
row("E4d-mutants-total", "2.6-mutants", "ledgers/E4/mutants/ (68 files)", "FAIL",
    f"`tools/mutate_graders.py --unit E4 --seeds 0-9` exit 1: 'mutate_graders E4: FAIL (65/68 killed)' ({LOG}/mutate_graders_seeds0-9_r8.txt). Survivors: mutant_r8_01_cap_100_halvings.py, mutant_r8_02_noise_above_ten_rejected.py, mutant_r8_03_cost_above_five_rejected.py. (Before the round-8 mutants were added the same command gave 63/63, {LOG}/mutate_graders_seeds0-9.txt.)",
    "Add the three tests proposed in proposed_tests_r8.py (sigma = 1e-30 with the closed form; sigma = 10 and 1000 accepted; cost = 5 and 50 accepted) to course/modules/E/E4/grader/test_project.py. Each proposed test passes on reference.py and kills the matching mutant (checked this round).")
row("E4d-equivalent", "2.6-mutants", "ledgers/E4/equivalent/literal_price_sign.py; ledgers/E4/equivalent/mutant_r7_01_reports_bracket_lower_end.py; README.md", P,
    "literal_price_sign passes 50/50 (alternatives log) and is output-equivalent by the README proof; it is an open architect item, not a grader survivor (the sign of b_u is not an output). mutant_r7_01 (lower end of the bracket) passes 50/50 as variant_r8_08_lower_end.py: the page now says the reported point 'lies in the final bracket' (:318), so it is spec-compliant.")
row("E4d-alternatives", "2.6-alternatives", "ledgers/E4/alternatives/alt_1..alt_5.py, alt_r8_a.py, alt_r8_b.py", P,
    f"Seeds 0-49, each as solver.py under the suite with -I -W error: alt_1..alt_5 50/50 each; alt_r8_a 50/50; alt_r8_b 50/50 ({LOG}/alternatives_seeds0-49.txt).")
row("E4d-starter", "2.6-autograder", "course/modules/E/E4/grader/starter.py", P,
    "starter.py unchanged since 4bd8cb94 (not in the round-7-to-round-8 delta); raises NotImplementedError by design, so 0/50 seeds pass, as the round-6 log records (ledgers/E4/scripts/E4-d-r6/logs/starter_seeds0-49.txt). Carried from round 6.")
row("E4d4-alt4-wrong-on-small-noise", "2.6-alternatives", "ledgers/E4/alternatives/alt_4.py", P,
    f"alt_4 passes 50/50 seeds this round ({LOG}/alternatives_seeds0-49.txt).")
row("E4d4-alt1-docstring", "2.6-alternatives", "ledgers/E4/alternatives/alt_1.py:1", P,
    "alt_1 unchanged since its docstring was checked; its docstring ('bisection with a fixed 120 halvings and no tolerance check') describes the code. Passes 50/50 this round.")
row("E4d4-equivalent-price-slope", "2.6-mutants", "ledgers/E4/scripts/E4-d-r4/check_equivalence_r4.py", P,
    CARRY + " the candidate's outputs agree with the reference within the root tolerance; not counted as a mutant.")
row("E4d4-calibration-blind", "2.4-rubric-calibration", "course/modules/E/E4/project.html:533-597 (Exemplar A)", "UNVERIFIABLE",
    "Same as E4d-exemplar-A-calibration: the official scoring line was displayed in this round's read before any score.",
    "Fresh blind score of Exemplar A from a stripped copy.")
row("E4d4-proposed-test-validated", "2.6-mutants", "course/modules/E/E4/grader/test_project.py (small-noise tests, now :469-478)", P,
    "The round-4 proposed small-noise test is in the grader; the reference passes it (run_graders 50/50).")
row("E4d4-mutants-killed-r4", "2.6-mutants", "ledgers/E4/mutants/mutant_r4*.py", P,
    "All r4 mutants KILLED in the round-8 log (mutate_graders_seeds0-9_r8.txt).")
row("E4d4-exemplar-B-results-numbers", "2.2-numbers", "course/modules/E/E4/project.html:629-641", P,
    "Same check as E4d-num-exemplar-table: values equal Lab 3 printed values.")
row("E4d5-mutant-bracket-floor", "2.6-mutants", "ledgers/E4/mutants/mutant_r5_bracket_floor_1e-12.py", P,
    "KILLED in the round-8 log.")
row("E4d5-mutant-sixty-halvings", "2.6-mutants", "ledgers/E4/mutants/mutant_r5_sixty_halvings_no_tolerance.py", P,
    "KILLED in the round-8 log (sixty halvings fail the 1e-11 root check).")
row("E4d5-mutant-uninformed-precision", "2.6-mutants", "ledgers/E4/mutants/mutant_r5_uninformed_posterior_precision_informed.py", P,
    "KILLED in the round-8 log.")
row("E4d5-calibration-B-blind", "2.4-rubric-calibration", "course/modules/E/E4/project.html:598-661 (Exemplar B)", "UNVERIFIABLE",
    "Same as E4d-exemplar-B-calibration.", "Fresh blind score of Exemplar B from a stripped copy.")
row("E4d6-mutant-06", "2.6-mutants", "ledgers/E4/mutants/mutant_r6_06_cost_scales_whole_gap.py", P,
    "KILLED in the round-8 log (test_unit_fraction_is_reported_with_a_positive_cost).")
row("E4d6-mutant-07", "2.6-mutants", "ledgers/E4/mutants/mutant_r6_07_unit_informativeness_discounted_by_cost.py", P,
    "KILLED in the round-8 log (test_unit_fraction_is_reported_with_a_positive_cost).")
row("E4d6-mutants-new-killed", "2.6-mutants", "ledgers/E4/mutants/mutant_r6_0*.py", P,
    "All r6 mutants (01-07) KILLED in the round-8 log.")
row("E4d6-spec-variants-08-09", "2.6-mutants", "ledgers/E4/equivalent/ (cited files mutant_r6_08_*.py, mutant_r6_09_*.py)", "FAIL",
    "Round-7 FAIL on variant 08 is resolved by the page text (:318 'lies in the final bracket'). Both variants re-created this round (ledgers/E4/scripts/E4-d-r8/variant_r8_08_lower_end.py, variant_r8_09_always_200.py) pass 50/50 seeds (alternatives_seeds0-49.txt). But the files the row cites do not exist in the checkout (ledgers/E4/equivalent/ holds only literal_price_sign.py, mutant_r7_01_reports_bracket_lower_end.py and README.md).",
    "Copy the two variant files into ledgers/E4/equivalent/ under the names the README cites, or correct the citation; variant 09 stays a documented interpretation (its loop never stops early, but its output is within tolerance, so no output test can separate it).")
row("E4d6-stop-rule-measured", "2.3-numerics", "grader/reference.py:22-23, :138; ledgers/E4/alternatives/alt_5.py", P,
    CARRY + " reference.py and alt_5.py measured in round 6 (ledgers/E4/scripts/E4-d-r6/logs/alt5_error_vs_closed_form_r6.txt); reference.py unchanged since 06994db1.")
row("E4d6-alt-extra-damped", "2.6-alternatives", "ledgers/E4/scripts/E4-d-r6/candidates/damped_fixed_point_log_r6.py", P,
    f"Re-run this round as solver.py over seeds 0-49: 50/50 pass ({LOG}/alternatives_seeds0-49.txt).")
row("E4d6-rung1-why", "2.4-prose", "course/modules/E/E4/project.html:171 (Lab 1 interpretation)", P,
    "Read this round: the interpretation gives a reason for each of the six steps and the 2^-53 width claim (computed: floating-point bracket stops shrinking at 53 halvings in [0.5,1)).")
row("E4d7-midpoint-untested", "2.6-mutants", "course/modules/E/E4/project.html:318; ledgers/E4/equivalent/mutant_r7_01_reports_bracket_lower_end.py", P,
    "Round-7 FAIL cited ':318 midpoint'. The round-8 page says 'The reported lambda* lies in the final bracket' (:318), which the lower end satisfies; the variant passes 50/50 (alternatives log). No stated sentence is violated, so the survivor is not a finding.")
row("E4d7-cost-above-one-rejected", "2.6-mutants", "course/modules/E/E4/grader/test_project.py:242-253; project.html:326", P,
    f"New test test_info_cost_above_one_is_accepted (run(0.6, 2.0): fraction 0, gap -24.075236829295875 matches the oracle within 1e-8). mutant_r7_03 (rejects cost above one) is KILLED ({LOG}/mutate_graders_seeds0-9_r8.txt). Cost above 5 is a separate survivor: E4d8-cost-cap-5-survives.")
row("E4d7-noise-above-one-rejected", "2.6-mutants", "course/modules/E/E4/grader/test_project.py:357-370", P,
    "mutant_r7_02 (rejects a finite noise volume above 1) is KILLED by test_unit_fraction_is_reported_at_zero_cost, which runs sd = 2.0. Noise above 10 is a separate survivor: E4d8-noise-cap-10-survives.")
row("E4d7-alt5-docstring", "2.6-alternatives", "ledgers/E4/alternatives/alt_5.py:1-2", P,
    "Docstring now reads 'with the same bracket [0, 1]', matching the code (lo, hi = 0.0, 1.0). alt_5 passes 50/50 (alternatives log).")
row("E4d7-lab1-bracket-width", "2.5-labs", "course/modules/E/E4/project.html:171", P,
    "Lab 1 prints the width after 60 halvings as 1.110e-16 (run_labs output), matching the interpretation's 2^-53 claim.")
row("E4d7-lab2-blank", "2.5-labs", "course/modules/E/E4/project.html:244", P,
    "The only changed line of Lab 2 against its twin is the blank; the interpretation text matches.")
row("E4d7-instance-bound", "2.2-numbers", "course/modules/E/E4/grader/test_project.py; grader/instance.py:1-21; project.html:314", P,
    "tau_bar(0.150) 0.097623; tau_bar(0.120) 0.237567; 1/(1+4*0.75^2) 0.307692; over seeds 0-49 the draws lie in [0.503,0.741] x [0.120,0.150] (computed).")
row("E4d7-lab3-closed-form-sentence", "2.5-labs", "course/modules/E/E4/project.html:376 (Lab 3 hypothesis)", P,
    "Hypothesis: bisection agrees with the closed form to within 1e-12. Printed largest difference 2.1e-13 (run_labs / twin output).")
row("E4d7-test-count", "2.6-autograder", "course/modules/E/E4/project.html:320; grader/test_project.py", P,
    "Page says 36 checks (:320). collect-only count is 36 (collect.txt). Equal.")
# ---- round-8 new rows
row("E4d8-no-upper-bound", "2.4-spec / 2.6-autograder", "course/modules/E/E4/project.html:326; grader/reference.py:122-151; grader/test_project.py", "FAIL",
    "The page says a noise volume above 1 and a cost above 1 are valid and return the three keys, and that the table names no upper bound. Counterexamples (reference solve_model; " + LOG + "/probe_reference_r8.txt): (a) info_cost 355.0 and 1000.0 at noise 0.6 raise OverflowError from math.exp(a c) (math range error; first failure between 354.0 ok and 355.0); (b) noise_sd 1e154 and 1e200 at cost 0.13 raise ZeroDivisionError (sd*sd overflows, tau_y = 0, then 1/tau_y); noise_sd 1e153 returns the keys. Each is a finite, positive input the page calls valid.",
    "Either restrict :326 to the finite range (cost up to 354 and noise volume up to 1e153, stated explicitly), or make reference.py return finite keys for these inputs (for example exp(a c) clamped via logs, tau_y computed without sd*sd overflow) and add tests at cost 1000 and noise 1e200.")
row("E4d8-cap-100-survives", "2.6-mutants", "ledgers/E4/mutants/mutant_r8_01_cap_100_halvings.py; project.html:318", "FAIL",
    f"Mutant (MAX_BISECTION_STEPS = 100) SURVIVED seeds 0-9 ({LOG}/mutate_graders_seeds0-9_r8.txt). It stops after 100 halvings, which violates the page's 'or after 200 halvings' (:318). Observable (" + LOG + "/probe_cap100_r8.txt): at sigma = 1e-30 it returns 1.1832913578e-30 against 9.656254e-31 (23% high; gap -0.0291 against +3.8e-14); at sigma = 1e-40 it returns 3.944e-31 against 9.66e-41. The reference is within 3e-13 relative of the closed form at both (" + LOG + "/probe_reference_r8.txt).",
    "Add the proposed tiny-noise probe to the suite (sigma = 1e-30 and 1e-40, closed form at relative 1e-8, proposed_tests_r8.py): reference passes; the mutant fails (checked this round).")
row("E4d8-noise-cap-10-survives", "2.6-mutants", "ledgers/E4/mutants/mutant_r8_02_noise_above_ten_rejected.py; project.html:326", "FAIL",
    "Mutant rejects finite noise volumes above 10 with the noise-volume ValueError and SURVIVED seeds 0-9. The page says no upper bound (:326). Probe: sd = 1000 is rejected by this mutant and accepted by the reference (" + LOG + "/probe_reference_r8.txt; the proposed test fails only for the mutant, checked this round).",
    "Add test_noise_volume_large_is_accepted: run(1000.0, COST) returns the three keys (the reference passes).")
row("E4d8-cost-cap-5-survives", "2.6-mutants", "ledgers/E4/mutants/mutant_r8_03_cost_above_five_rejected.py; project.html:326", "FAIL",
    "Mutant rejects a finite information cost above 5 with the cost ValueError and SURVIVED seeds 0-9. The page says a cost above 1 is valid (:326). The suite's only cost above 1 is 2.0 (test_info_cost_above_one_is_accepted), which this mutant accepts. Probe: cost 50 is rejected by the mutant and accepted by the reference (" + LOG + "/probe_reference_r8.txt).",
    "Add a test that run(0.6, 50.0) returns the three keys with informed_fraction 0.0 (reference passes; mutant raises ValueError).")
row("E4d8-mutants-r8-killed", "2.6-mutants", "ledgers/E4/mutants/mutant_r8_04_integer_zero_fraction.py; mutant_r8_05_informativeness_at_unit_precision.py", P,
    "Both KILLED: r8_04 by test_info_cost_above_one_is_accepted (seed 0); r8_05 by test_informativeness_is_the_squared_correlation[first] (seed 0).")
row("E4d8-alternatives-r8", "2.6-alternatives", "ledgers/E4/alternatives/alt_r8_a.py, alt_r8_b.py", P,
    f"Two new correct solvers written this round: alt_r8_a (Omega-form terms, bisection to relative 1e-13 with 400 steps) and alt_r8_b (bisection on the sign of tau_bar - tau_y, gap evaluated at the root). Both 50/50 on seeds 0-49 ({LOG}/alternatives_seeds0-49.txt).")
row("E4d8-tiny-root-reference", "2.3-numerics", "course/modules/E/E4/grader/reference.py; scratch probe", P,
    "reference solve_model(1e-30, 0.13): informed_fraction 9.656254101544045e-31 vs closed form 9.656254101546876e-31 (relative 2.9e-13); sigma 1e-40 likewise 2.9e-13 relative. Matches the page's 200-halving claim (the reference passes the proposed tests).")
row("E4d8-lab3-twin-page", "2.5-labs", "course/modules/E/E4/project.html:377-503; tests/labs/E4/lab-E4-project-3.py", P,
    "Page code equals the twin after the MAX_HALVINGS change (diff empty, 114 lines), and the twin runs under -I -W error with the expected output (run_labs).")

PASS_FILE = "course/modules/E/E4/project.html"
for r in rows:
    if r["status"] == "PASS" and r["evidence"].startswith(CARRY):
        pass

ids = [r["id"] for r in rows]
print("rows", len(rows), "unique", len(set(ids)))

mutants = []
for line in pathlib.Path(LOG, "mutate_graders_seeds0-9_r8.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(KILLED|SURVIVED) (\S+): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    killed_by = None if killed.strip() == "None" else killed.strip()
    mutants.append({
        "name": name,
        "description": desc.strip(),
        "killed_by": killed_by if killed_by else None,
        "status": status,
    })

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "FAIL"
fragment = {
    "unit": "E4",
    "slice": "d",
    "round": 8,
    "verifier": "Haiku independent verifier, E4 slice d, round 8 (did not build E4)",
    "pin": PIN,
    "base": BASE + " (round-7 pin; delta in this slice: project.html :315-326, :396-398 (MAX_HALVINGS), :443-457 (solve loop) and the lab-3 twin; grader test_project.py +15 lines at :239-258 and a docstring at :481-484; ledgers/E4/alternatives/alt_5.py docstring; new mutants r7_01..03 and r8 files)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE8-E4-d",
    "scratch": "/tmp/e4r8-collect-*, /tmp/e4r8-alt-*, /tmp/e4r8-probe*, /tmp/e4r8-probe2-*, /tmp/e4r8-probe3-*, /tmp/e4r8-probe4-* (all created and removed; no scratch copy of the repo kept)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [
        "Exemplar A and Exemplar B calibration rows are UNVERIFIABLE: the official scoring lines were read in this round before scoring. A fresh verifier must score from stripped passages."
    ],
    "notes": [
        "Round 8 re-ran every command row on the pin: check_pages, check_dag, check_projects, run_labs, run_graders (seeds 0-49), page_smoke (project, alone), ruff (E4 paths), mypy --no-incremental (grader and labs), the four relevant pytest files, verify_refs --offline, collect-only (36), the twins under python -I -W error, and tools/mutate_graders.py --unit E4 --seeds 0-9 (68 mutants).",
        "Mutation gate: exit 1, 65/68 killed. The three survivors are round-8 student-error mutants (cap 100, noise above 10 rejected, cost above 5 rejected); the 63 pre-existing mutants are all killed.",
        "Found in this round: the page's no-upper-bound claim (project.html:326) is false for finite inputs: cost >= about 355 raises OverflowError and noise volume >= about 1e154 raises ZeroDivisionError in reference.py.",
        "Resolved since round 7: E4d7-midpoint-untested (page no longer states the midpoint), E4d7-alt5-docstring (alt_5 docstring fixed), E4d7-cost-above-one-rejected (new test; mutant r7_03 killed).",
        "Not checked: a blind calibration of the two exemplars (UNVERIFIABLE by design of this round); a live verify_refs run (references unchanged); cards.json and the other E4 slices (not in this slice); the repository-wide ruff run; the Pyodide run beyond page_smoke.",
        "The literal_price_sign variant is an open architect item (its sign is not observable through solve_model); it is not counted as a surviving mutant.",
    ],
    "summary": {
        "rows": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants": len(mutants),
        "mutants_killed": sum(1 for m in mutants if m["status"] == "KILLED"),
    },
}
pathlib.Path("ledgers/E4/E4-d.json").write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("counts", counts, "mutants", len(mutants))
