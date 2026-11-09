"""Round 18 (E4 slice d): build ledgers/E4/E4-d.json from the round-17 fragment and this round's evidence.

Carry rule (verifier-rules, round after the first): a round-17 PASS row is carried only when its cited subject is
byte-identical since the previous pin; rows whose subject changed, or that name a gate or file re-run this round, are
restated with round-18 evidence. Every row id of round 17 is kept. New rows carry the E4d18 prefix.
"""
import json
import re
import datetime
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE18-E4-d")
O = "ledgers/E4/scripts/E4-d-r18/out"
prev = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-E4-d.round17.json").read_text(encoding="utf-8"))

CARRY_PREFIX = ("Carried from round 17 (course/modules/E/E4/project.html except line 317, tests/labs/E4/*, "
                "grader/reference.py, grader/instance.py, grader/starter.py, ledgers/E4/alternatives/, references/, "
                "notation/, tools/ and curriculum/ byte-identical since the previous pin 700bf33f): ")

R18 = {}  # id -> (status, check, location, evidence, fix)

def pas(i, check, loc, ev):
    R18[i] = ("PASS", check, loc, ev, None)

def fail(i, check, loc, ev, fix):
    R18[i] = ("FAIL", check, loc, ev, fix)

# ---- commands run this round (pin 50559266) -------------------------------------------------------------------------
pas("E4d-cmd-check-projects", "2.6-structure", "course/modules/E/E4/project.html; course/modules/E/E4/grader/",
    f"{O}/check_projects.txt: 'check_projects E4: PASS', exit 0 (tools/check_projects.py --unit E4), round 18.")
pas("E4d-cmd-check-pages", "2.9-structure", "course/modules/E/E4/project.html",
    f"{O}/check_pages.txt: 'check_pages E4: PASS', exit 0 (includes the banned-string scan), round 18.")
pas("E4d-cmd-check-dag", "2.9-dag", "course/modules/E/E4/project.html",
    f"{O}/check_dag.txt: 'check_dag E4: PASS', exit 0, round 18.")
pas("E4d-cmd-run-labs", "2.5-labs", "tests/labs/E4/lab-E4-project-1.py, -2.py, -3.py",
    f"{O}/run_labs.txt: 'run_labs E4: PASS (12/12)', exit 0, round 18; twins re-run alone by {O}/labs_check.txt.")
pas("E4d-cmd-run-graders", "2.6-autograder", "course/modules/E/E4/grader/reference.py",
    f"{O}/run_graders_0_49.txt: 'run_graders E4: PASS (reference 50/50 seeds)', exit 0, round 18 (edited suite).")
pas("E4d-cmd-page-smoke-project", "2.9-smoke", "course/modules/E/E4/project.html",
    f"{O}/page_smoke_project.txt: 'page_smoke E4: PASS', exit 0 (project page only), round 18.")
pas("E4d-cmd-ruff", "gate", "course/modules/E/E4 and tests/labs/E4",
    f"{O}/ruff_check.txt 'All checks passed!' and {O}/ruff_format.txt '16 files already formatted', exit 0, round 18.")
pas("E4d-cmd-mypy-workspace", "gate", "tests/labs/E4 and course/modules/E/E4/grader",
    f"{O}/mypy_workspace.txt: full .venv/bin/mypy --no-incremental 'Success: no issues found in 385 source files', exit 0, round 18.")
pas("E4d-cmd-mypy-plan-command", "gate", "tests/labs/E4; grader",
    f"{O}/mypy_e4.txt: mypy --no-incremental tests/labs/E4 course/modules/E/E4/grader 'Success: no issues found in 16 source files', exit 0, round 18.")
pas("E4d-cmd-pytest-relevant", "gate", "tests/test_memo_exemplars.py, test_page_checks.py, test_labs.py, test_page_smoke.py, test_run_labs.py",
    f"{O}/pytest_relevant.txt: 5 files, all dots, exit 0, round 18.")
pas("E4d-cmd-verify-refs", "2.1-citations", "references/references.json (E4 keys: muth1961rational, milgrom1982information)",
    f"{O}/verify_refs_offline.txt '560 entries, 0 problems' exit 0; {O}/verify_refs_E4_live.txt '3 of 560 entries, 0 problems' exit 0, round 18.")
pas("E4d-cmd-collect", "2.6-autograder", "course/modules/E/E4/grader/test_project.py",
    f"{O}/collect_only_reference.txt: '48 tests collected' with reference.py installed as solver.py "
    f"(ledgers/E4/scripts/E4-d-r18/collect_reference_r18.sh), round 18. The bare collect fails with ModuleNotFoundError: solver by design.")

# ---- labs, numbers, docstrings re-derived this round ----------------------------------------------------------------
pas("E4d-lab-project-1", "2.5-labs", "course/modules/E/E4/project.html #lab-E4-project-1; tests/labs/E4/lab-E4-project-1.py",
    f"{O}/labs_check.txt: page code equals twin (after trailing newline), twin exit 0 and stderr 0 bytes under python -I -W error, "
    "expected block equals twin stdout (15 lines), round 18.")
pas("E4d-lab-project-2", "2.5-labs", "course/modules/E/E4/project.html #lab-E4-project-2; tests/labs/E4/lab-E4-project-2.py",
    f"{O}/labs_check.txt: page block differs from the twin only at the blanked return line (by design, diff shown); twin exit 0, "
    "stderr 0; expected block equals twin stdout (4 lines), round 18.")
pas("E4d-lab-project-3", "2.5-labs", "course/modules/E/E4/project.html #lab-E4-project-3; tests/labs/E4/lab-E4-project-3.py",
    f"{O}/labs_check.txt: page code equals twin, twin exit 0 and stderr 0, expected block equals twin stdout (12 lines), round 18.")
pas("E4d-num-lab-hypotheses", "2.4-numbers", "course/modules/E/E4/project.html:57, :175, :375",
    "Every number in the Lab 1, Lab 2 and Lab 3 hypothesis paragraphs equals the expected block printed by the twin "
    f"({O}/labs_check.txt): Lab 1 +0.053092, -0.080731, 0.57937525, -3.45199422, 0.18904110, 0.15898618; Lab 2 +0.037435, "
    "-0.071386, 0.57052263, 0.12466375; Lab 3 fractions 0.5582/0.6978/0.8373, informativeness 0.1920/0.1420/0.0889, gaps < 1e-13 "
    "(max 3.55e-14), closed-form agreement 2.1e-13 < 1e-12, 484 of 484. Closed-form check of 0.5582 etc. re-derived with "
    "ledgers/E4/scripts/E4-d-r18/numbers_r18.py (out/numbers_r18.txt)-style decimal arithmetic.")
pas("E4d18-lab1-halving-claim", "2.4-numbers", "course/modules/E/E4/project.html:170 (Lab 1 interpretation)",
    f"ledgers/E4/scripts/E4-d-r18/numbers_r18.py section C (out/numbers_r18.txt): bracket width after halving 53 is 1.110223e-16 = 2^-53 and stays there to halving 60, "
    "as the interpretation states.")
pas("E4d18-docstring-numbers", "2.4-numbers", "grader/test_project.py:386-390 (docstring), :568-571 (corner docstring); :243-244",
    "ledgers/E4/scripts/E4-d-r18/numbers_r18.py (out/numbers_r18.txt) section A (ledgers/E4/scripts/E4-d-r18/ holds the gate scripts; the probe is in the scratch dir): gap at fraction 1e-12 differs from the limit by 1.02e-13 to 3.54e-13 at the six "
    "inputs (docstring says 1e-13 to 4e-13); oracle agrees with the limit to at most 1.110e-16 (docstring: at most 1.1e-16); "
    "section B: corner root 2.022385e-51, 1e-10*root 2.022e-61, 2^-200 = 6.223e-61 (wider, as the docstring says); tau-bar at c=0.1707691121 is 0.0101216 (>= 1e-2).")
pas("E4d18-spec-box-bounds", "2.4-numbers", "course/modules/E/E4/project.html:313 (Inputs box)",
    "tau-bar(0.150) = 2e^-0.6 - 1 = 0.09762327 and tau-bar(0.120) = 2e^-0.48 - 1 = 0.23756678 (computed); tau_y(1) = 1/(1+4 sd^2) >= "
    "1/3.25 = 0.30769 on sd <= 0.75; so 0 < tau-bar < tau_y(1) on the box, as stated. Box: grader/instance.py:7-8, :28-29 draw sd in [0.500, 0.750] "
    "and c in [0.120, 0.150], each rounded to three decimals (read in full this round; unchanged since 700bf33f).")
pas("E4d18-math-derivations", "2.2-math",
    "course/modules/E/E4/project.html:257-301 (A1-A6, Lemmas 1-3, Propositions 1-5)",
    "Re-derived this round by hand from the page text: Lemma 1 (completion of the square, g(xhat)=(m-p)^2/(2aV)); Lemma 2 (Gaussian integral "
    "gives (V/(V+S))^(1/2)); Lemma 3; Prop 1 steps (1)-(4) (coefficient of s and of u, kappa = -a/(lam tau_e)); Prop 2 (Corr^2 = tau_y/(tau_v+tau_y)) "
    "and the lam=0 case; Prop 3 (sign rule, G(0+) closed form matches reference.py gap_at_zero, V_I/Omega identity); Prop 4 closed form "
    "(lam^2 = tau-bar a^2 sigma^2/(tau_e(tau_e-tau-bar))) and informativeness identity; Prop 5 (lam* proportional to sigma, decreasing in c). "
    "No error found.")
pas("E4d18-prose-scope-words", "2.2-prose", "course/modules/E/E4/project.html:317 and the rest of the page",
    "The changed sentence 'Any reported fraction within 1e-10 times the root that the grader's independent oracle computes ... is accepted' is "
    "true of the suite: test_fraction_is_the_oracle_root accepts |lam - oracle root| <= TOL_ROOT = 1e-10 absolute, which contains every "
    "fraction within 1e-10 times a root <= 1. The accuracy claim at tiny roots is tested against the closed form, not the oracle "
    "(test_project.py:544-591).")
pas("E4d-spec-questions", "2.6-spec", "course/modules/E/E4/project.html:314-322 (Inputs, Required outputs, Constraints, Grading mode, Reading)",
    "Read in full this round. The Constraints sentences at :317 were checked one by one against reference.py and test_project.py "
    "(see E4d16-constraints-any-sentence).")
pas("E4d3-spec-stop-rule-and-constraints", "2.6-spec", "course/modules/E/E4/project.html:317 (Constraints); grader/test_project.py:251-254, :312-317, :377-383",
    "Stop rule: reference.py:21-22 (BISECTION_TOLERANCE 1e-12, MAX_BISECTION_STEPS 240) and :138 (while high - low > tolerance*high and steps < cap). "
    "Gap clauses now tested at 1e-14 relative to max(1,|limit|) at test_project.py:251-254 (gap at 0, cost 2.0), :312-317 (gap at the "
    "reported fraction, both instances) and :377-383 (gap at 0, cost 0.30). Suite and reference pass 50/50 (run_graders). Round-17 FAIL resolved.")
pas("E4d10-delta-constraints-gap-at-zero", "2.6-spec", "course/modules/E/E4/project.html:317; grader/test_project.py:251-254, :377-383",
    "Round-17 FAIL resolved: both gap-at-zero comparisons use 1e-14 * max(1, |limit|) (test_project.py:251-254, :377-383); "
    "reference passes (run_graders_0_49.txt, 50/50); oracle-vs-limit at the six inputs of :386-402 is at most 1.110e-16 (ledgers/E4/scripts/E4-d-r18/numbers_r18.py section A).")
pas("E4d16-constraints-any-sentence", "spec-vs-suite", "course/modules/E/E4/project.html:317 (Constraints)",
    "Every sentence of :317 checked against reference.py and the suite: stop rule, bracket, boundary rule, tolerance, accuracy for "
    "noise >= 1e-50 and tau-bar >= 1e-2 (closed-form tests :544-591), exception names and messages, display rule. The gap-precision "
    "clauses are now tested at 1e-14 at fraction 0, fraction 1 and at the reported fraction of the two instances (:251, :312, :377, :308-317, "
    ":406-421, :424-463). The domain-wide interior clause is met by reference.py (exact formula within 2e-16 of 80-digit Decimal "
    "values: ledgers/E4/scripts/E4-d-r18/exact_v17_02.py (out/exact_v17_02.txt)) but the suite samples it only on the autograder box; that gap is what lets mutant_v17_02 survive "
    "(row E4d17-mutant-v17-02).")
pas("E4d17-gap-tolerance-constraint", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:44, :251-254, :312-317, :377-383",
    "Round-17 fix applied as requested: TOL_GAP stays 1e-8 at the root and boundary tests (:301, :325, :329) and the three named "
    "comparisons use 1e-14 * max(1,|limit|). Reference and alt_1..alt_8 pass 50/50 with this suite (E4d18-alt-eq-edited-suite).")
pas("E4d18-test-edit-review", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:44, :247-254, :309-317, :373-383",
    "Full re-read of the suite at 50559266: the only changes since 700bf33f are the TOL_GAP comment (:44) and the three comparisons "
    "(:251-254, :312-317, :377-383), each of which now reads limit=..., abs(out - limit) <= 1e-14 * max(1.0, abs(limit)). No test "
    "was weakened; messages unchanged in meaning.")
pas("E4d-grader-exceptions", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:191-234, :242-280; reference.py:26-34",
    "Re-read in full this round: the exception tests demand ValueError only for the named conditions (noise volume zero, negative, "
    "infinite, nan; cost negative, just below zero); the two far-above-one tests are accepted as the table states. Messages match the table.")
pas("E4d-grader-messages", "2.6-autograder", "course/modules/E/E4/grader/test_project.py (every expect() and pytest.fail call)",
    "Re-read in full this round. Hints name the property and carry no values; the edited hints at :252-254, :315-316, :379-382 "
    "name the precision and the point, consistent with the test.")
pas("E4d-grader-oracle", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:79-170",
    "Re-read in full this round: oracle_regressions/oracle_price/oracle_gap follow the moments of the model and do not import the reference. "
    "Accuracy of the oracle at the 1e-14 level is limited: at sd=0.1, cost=0.0598 the oracle differs from the exact gap by about 8e-15 "
    "(ledgers/E4/scripts/E4-d-r18/oracle_at_violations.py (out/oracle_at_violations.txt)), so 1e-14 checks rely on the oracle only where it is accurate (the box).")
pas("E4d-grader-instances", "2.6-autograder", "course/modules/E/E4/grader/instance.py; test_project.py:37-40",
    "Re-read in full this round: INST and INST2 from make_instance(SEED) and make_instance(SEED+7919); instance.py unchanged; 50 seeds run.")
pas("E4d-grader-test-docstring", "2.4-docstrings", "course/modules/E/E4/grader/test_project.py (test docstrings)",
    "Re-read in full this round; the numbers in the docstrings at :386-390, :546-547, :558-559, :569-571, :583-585 were re-derived (E4d18-docstring-numbers).")
pas("E4d-grader-stdlib", "2.6-autograder", "course/modules/E/E4/grader/test_project.py (test_solver_imports_only_the_standard_library)",
    "Re-read in full this round; reference.py imports only math (and __future__); suite passes 50/50.")
pas("E4d-runtime", "2.6-autograder", "course/modules/E/E4/grader/test_project.py",
    "Suite run 50/50 seeds in the verifier's local runner (run_graders_0_49.txt, slowest seed 0.2 s), round 18.")
pas("E4d-browser-local-parity", "2.6-autograder", "course/modules/E/E4/grader/test_project.py; tools/page_smoke.py",
    "Same flags as the browser (--assert=plain -W error, QF_SEED) used in the candidate runner (run_candidate_r17.py); page_smoke PASS (round 18).")
pas("E4d-num-box-bounds", "2.4-numbers", "course/modules/E/E4/project.html:314; course/modules/E/E4/grader/instance.py:14-17",
    "Box values re-derived this round (E4d18-spec-box-bounds); instance.py unchanged since 700bf33f.")
pas("E4d-prose-simulated-labs", "2.2-prose", "course/modules/E/E4/project.html:57, :176, :314, :375",
    "Labs state their inputs as stated values and the page calls them SIMULATED; lab twins read no file (checked by labs_check.txt).")

# ---- check_pages / check_dag / verify_refs re-run this round --------------------------------------------------------
pas("E4d-banned-phrases", "2.9-banned", "course/modules/E/E4/project.html; grader/*.py; tests/labs/E4/lab-E4-project-*.py",
    f"{O}/check_pages.txt PASS (banned-string scan), round 18; the new sentence at :317 contains no banned string.")
pas("E4d-process-words", "2.2-prose", "course/modules/E/E4/project.html; grader/*.py; tests/labs/E4/lab-E4-project-*.py",
    "Re-read in full this round; no process word in learner text. The line-317 change contains no process word.")
pas("E4d-dag-links", "2.9-dag", "course/modules/E/E4/project.html (concept links and hrefs)",
    f"{O}/check_dag.txt PASS, round 18; the one changed line (:317) adds no link.")

# ---- mutants: all 137 mutant files killed by the round-18 gate ------------------------------------------------------
mut_gate = "tools/mutate_graders.py --unit E4 --seeds 0-9: 137/137 KILLED (out/mutate_graders_E4_0_9_r18.txt), round 18"
for i in list(prev_row_ids := [r["id"] for r in prev["rows"]]):
    if "mutant" in i or i in ("E4d-mutants-existing", "E4d-mutants-new", "E4d-mutants-total", "E4d15-cmd-mutate"):
        pass
pas("E4d-mutants-total", "2.6-mutation", "ledgers/E4/mutants/ (137 files)",
    mut_gate + ". v17_02 is no longer in mutants/ (moved to equivalent/, see E4d18-equiv-readme-v17-02-proof, which is FAIL).")
pas("E4d15-cmd-mutate", "2.6-mutation", "tools/mutate_graders.py --unit E4 --seeds 0-9", mut_gate + ".")
pas("E4d-mutants-existing", "2.6-mutation", "ledgers/E4/mutants/ (133 pre-existing files)",
    mut_gate + ": every pre-existing file KILLED.")
pas("E4d-mutants-new", "2.6-mutation", "ledgers/E4/mutants/mutant_r7_02_*.py, mutant_r7_03_*.py", mut_gate + ".")
pas("E4d18-mutants-r18-new", "2.6-mutation",
    "ledgers/E4/mutants/mutant_r18_01..04 (student-error mutants written this round, one changed line each from reference.py)",
    "mutant_r18_01 (uninformed posterior ignores price precision) KILLED by test_gap_is_the_oracle_gap_at_the_reported_fraction[first]; "
    "r18_02 (informed term drops b_u^2 sd^2) KILLED by test_indifference_holds_at_an_interior_fraction[first]; r18_03 (gap at 1 omits "
    "exp(ac)) KILLED by test_unit_fraction_is_reported_with_a_positive_cost; r18_04 (interior gap read at bracket low) KILLED by "
    "test_gap_is_the_oracle_gap_at_the_reported_fraction[first] (out/mutate_graders_E4_0_9_r18.txt).")
pas("E4d17-mutants-new-killed", "2.6-mutation", "ledgers/E4/mutants/mutant_v17_01, _03, _04",
    "Killed in the round-18 gate (out/mutate_graders_E4_0_9_r18.txt).")
pas("E4d-equivalent", "2.6-equivalent", "ledgers/E4/equivalent/*.py (five files)",
    f"{O}/cand/eq_*.txt: each equivalent 50/50 on seeds 0-49 with the edited suite (round 18); not counted in mutants/.")
pas("E4d4-equivalent-price-slope", "2.6-equivalent", "ledgers/E4/equivalent/literal_price_sign.py",
    "Equivalence of the literal price sign re-proved this round (E4d18-literal-price-sign-proof); carried check script unchanged.")

# ---- alternatives and equivalents on the edited suite ---------------------------------------------------------------
pas("E4d-alternatives", "2.6-alternatives", "ledgers/E4/alternatives/alt_1.py .. alt_8.py",
    f"{O}/cand/alt_*.txt: alt_1..alt_8 each 50/50 seeds 0-49 with the edited suite (run_alts_r18.sh; run_candidate_r17.py with E4_ROOT set).")
pas("E4d18-alt-eq-edited-suite", "2.6-alternatives",
    "ledgers/E4/alternatives/alt_1..alt_8.py; ledgers/E4/equivalent/*.py; grader/reference.py",
    f"{O}/alts_driver.log: alt_1..alt_8 50/50, eq_* (five files) 50/50, reference 50/50, all with the edited suite, round 18. "
    "Alternatives use bisection with 240 halvings (alt_1), Illinois (alt_2, alt_8), grid+bisection (alt_3), secant (alt_4), "
    "closed-form-style (alt_5..alt_7) — distinct styles.")
pas("E4d13-candidates-accepted", "2.6-alternatives", "ledgers/E4/alternatives/alt_1..alt_8.py; ledgers/E4/equivalent/*.py",
    "Round-18 run (E4d18-alt-eq-edited-suite): all accepted 50/50.")
pas("E4d15-alternatives-sweep", "2.6-alternatives", "ledgers/E4/alternatives/alt_1..alt_8.py; ledgers/E4/equivalent/*.py",
    "Round-18 run (E4d18-alt-eq-edited-suite): all 50/50.")
pas("E4d8-alternatives-r8", "2.6-alternatives", "ledgers/E4/alternatives/alt_r8_a.py, alt_r8_b.py (retired)",
    "Retired under ruling 18 (absent from the checkout, checked this round); the stand-in set alt_1..alt_8 passes 50/50 (round 18).")
pas("E4d9-alternatives-v9", "2.6-alternatives", "ledgers/E4/alternatives/alt_v9_* (retired)",
    "Retired under ruling 18 (absent from the checkout, checked this round); the stand-in set alt_1..alt_8 passes 50/50 (round 18).")

# ---- calibration: blind scoring by the dedicated scorer (ruling 23) -------------------------------------------------
BLIND = "~/.fanout/blind/E4-d.json (dedicated blind scorer, ruling 23)"
pas("E4d-exemplar-A-calibration", "2.6-rubric-calibration", "course/modules/E/E4/project.html:535 (Exemplar A, data-scores 2,2,1,2,1)",
    f"Blind scores of Exemplar A from {BLIND}: C1 2, C2 2, C3 1, C4 2, C5 1 (field A). Equal to the page's data-scores 2,2,1,2,1 "
    "(project.html:535). Not scored by this verifier.")
pas("E4d4-calibration-blind", "2.6-rubric-calibration", "course/modules/E/E4/project.html:535 (Exemplar A)",
    f"Same record as E4d-exemplar-A-calibration: {BLIND}, field A = 2,2,1,2,1 equals project.html:535.")
pas("E4d-exemplar-B-calibration", "2.6-rubric-calibration", "course/modules/E/E4/project.html:600 (Exemplar B, data-scores 4,4,4,4,4)",
    f"Blind scores of Exemplar B from {BLIND}: C1..C5 = 4,4,4,4,4 (field B). Equal to project.html:600 data-scores.")
pas("E4d5-calibration-B-blind", "2.6-rubric-calibration", "course/modules/E/E4/project.html:600 (Exemplar B)",
    f"Same record: {BLIND}, field B = 4,4,4,4,4.")

# ---- equivalent proof: mutant_v17_02 ---------------------------------------------------------------------------------
fail("E4d17-mutant-v17-02", "2.6-mutation",
     "ledgers/E4/equivalent/mutant_v17_02_price_slope_drops_uninformed_term.py:57 (b_s = lam tau_e / denominator); course/modules/E/E4/project.html:276 (Proposition 1, b_s formula); project.html:317 (interior gap at 1e-14)",
     "Not equivalent under the page's stated tolerance. The mutant's reported gap at its own fraction differs from the exact Proposition 3 gap "
     "by more than 1e-14 at domain points: 1513 of 43582 interior points on the page domain (sd 1e-50 to 1e2, cost 0 to 0.34, "
     "300 x 300; ledgers/E4/scripts/E4-d-r18/sweep_v17_02.py (out/sweep_v17_02.txt)), maximum 1.57e-14 at (sd 3.3245979322709314e-22, cost 0.059130434782608696). Measured in "
     "80-digit decimal (ledgers/E4/scripts/E4-d-r18/exact_v17_02.py (out/exact_v17_02.txt)): the reference's double gap is within 1.2e-16 of the exact gap at all five points, "
     "the mutant's is off by -1.55e-14 at (3.3245979322709314e-22, 0.059130434782608696) and -1.13e-14 at (1e-50, 0.0598). "
     "On the autograder box (sd 0.5-0.75, cost 0.12-0.15, 200 x 200) the maximum is 3.66e-15, so the suite cannot see it. "
     "Survives seeds 0-49 (round 17 and round 18 runs). Ruling 22 applies only to a difference inside the stated tolerance, and ruling 9 "
     "requires a surviving mutant that violates a page-stated behaviour to be killed by a new grader test.",
     "Keep the mutant in ledgers/E4/mutants/ (move it back) and add a grader test at a domain point where the exact Proposition 3 gap is "
     "computed in the test file from the Proposition 1 coefficients (not the quadrature oracle, which is 8e-15 off at sd 0.1): e.g. "
     "sd=3.3245979322709314e-22, cost=0.059130434782608696, require |reported gap - exact gap| <= 1e-14 * max(1, |exact|). Verified "
     "numerically: the reference is within 1.2e-16 there, the mutant is off by 1.55e-14. Alternatively an architect ruling that the "
     "interior gap clause holds only on the box must be written into project.html:317 and then the mutant is still a page-stated "
     "violation to be recorded as a known limit.")
fail("E4d18-equiv-readme-v17-02-proof", "2.6-equivalent",
     "ledgers/E4/equivalent/README.md, section 'mutant_v17_02 ... equivalent within the stated tolerances (round 17, ruling 22)', Proof steps 5-6 and 'Measured'",
     "Steps 1-4 of the proof (common variance Omega(beta); Omega_I and Omega_U equal Omega(beta)) re-derived and correct; the gap is "
     "Omega(beta)^(-1/2) H(lam) with H depending only on tau_y(lam). Step 6 (reported gap versus the Proposition 3 gap at the reported fraction) "
     "is stated to be 'measured, not bounded in closed form', and its measurements (14400-point grid with sd 0.30-2.70 and cost 0.10-0.20, "
     "maximum 4.219e-15) do not cover the page domain. Over the page domain the same quantity reaches 1.57e-14 (E4d17-mutant-v17-02). "
     "The 'Measured' bullet 'Largest ... 4.219e-15 for the variant (page: 1e-14)' is true only on that grid, and the README's conclusion "
     "that the variant is equivalent is false.",
     "Retract the equivalence: remove the file from ledgers/E4/equivalent/ and this README section, or replace step 6 with a bound valid "
     "on the whole page domain. A bound is not available in closed form from the stated proof; the file must return to mutants/ "
     "with a new grader test (see E4d17-mutant-v17-02).")

# ---- literal price sign: proof re-checked ---------------------------------------------------------------------------
pas("E4d18-literal-price-sign-proof", "2.6-equivalent", "ledgers/E4/equivalent/literal_price_sign.py vs course/modules/E/E4/grader/reference.py:58, :69, :73",
    "b_u is used only in informed_term (reference.py:73, b_u * b_u) and returned from price_coefficients; b_u*b_u is bitwise equal for b_u and -b_u "
    "(IEEE negation is exact). So the literal sign changes no output (the README proof steps 1-3 are correct). It violates the sign "
    "stated in Proposition 1 (project.html:276), which no output can observe. This remains the architect's open item (ruling 9 path, "
    "as in round 17); it is not counted as a verifier FAIL here, to keep the decision with the architect.")
pas("E4d11-literal-price-sign-open", "2.6-equivalent", "course/modules/E/E4/project.html:257-301; ledgers/E4/equivalent/literal_price_sign.py",
    "Carried: Proposition 1 sign and the literal variant as in E4d18-literal-price-sign-proof; open architect item (not re-decided).")

# ---- prose/format rows re-verified (touched lines) ------------------------------------------------------------------
pas("E4d-rubric-observable", "2.6-rubric", "course/modules/E/E4/project.html:520-527 (#rubric)",
    "Re-read: each descriptor cell is observable (names an assumption, a sign with a grid, a significant-digit rule, a named limit).")

# ---- carry rule: remaining round-17 PASS rows ----------------------------------------------------------------------
rows = []
ids_new = set(R18)
for r in prev["rows"]:
    i = r["id"]
    if i in R18:
        st, chk, loc, ev, fix = R18[i]
        row = {"id": i, "check": chk, "location": loc, "status": st, "evidence": ev}
        if fix:
            row["fix"] = fix
        rows.append(row)
        continue
    if r["status"] == "PASS":
        rows.append({"id": i, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": CARRY_PREFIX + r["evidence"]})
    else:
        rows.append({"id": i, "check": r["check"], "location": r["location"], "status": "FAIL",
                     "evidence": "Round-17 non-PASS row not restated this round: " + r["evidence"],
                     "fix": r.get("fix", "see the round-17 fragment")})
# new rows of round 18 that are not in round 17
for i, (st, chk, loc, ev, fix) in R18.items():
    if i not in {r["id"] for r in prev["rows"]}:
        row = {"id": i, "check": chk, "location": loc, "status": st, "evidence": ev}
        if fix:
            row["fix"] = fix
        rows.append(row)

# ---- mutants list from the round-18 gate ----------------------------------------------------------------------------
mutants = []
for line in (ROOT / O / "mutate_graders_E4_0_9_r18.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    if status != "KILLED":
        mutants.append({"id": name[:-3], "file": f"ledgers/E4/mutants/{name}", "description": desc, "killed_by": None})
        continue
    mutants.append({"id": name[:-3], "file": f"ledgers/E4/mutants/{name}", "description": desc, "killed_by": killed})

verdict = "FAIL"
frag = {
    "unit": "E4",
    "slice": "d",
    "round": 18,
    "verifier": "Haiku independent verifier, E4 slice d, round 18 (did not build E4; checkout pinned at 50559266, detached)",
    "pin": "505592668894eff518befad086df192000dc86c0",
    "base": "700bf33f334486d7b5b4f22d4f82f3e25d4b39b6 (round-17 pin); delta for slice d: project.html:317, grader/test_project.py (:44, :251-254, :312-317, :377-383), ledgers/E4/equivalent (README + mutant_v17_02 moved in), ledgers/E4/mutants (v17_01, v17_03, v17_04 added; v17_02 removed), plans/FINAL-ARCHITECT-RULINGS.md (rulings 21-23)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE18-E4-d",
    "scratch": "/Users/billyribeiro/.fanout/scratch-E4-d-r18 (probe copies only; the evidence scripts and outputs are under ledgers/E4/scripts/E4-d-r18/ and its out/)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [
        "ledgers/E4/equivalent/README.md: section 'mutant_v17_02 ... equivalent within the stated tolerances' claims a 1e-14 agreement that holds only on the 14400-point grid; the domain sweep contradicts it (E4d18-equiv-readme-v17-02-proof)."
    ],
    "notes": [
        "Blind exemplar scoring: done by the dedicated scorer (ruling 23), record ~/.fanout/blind/E4-d.json (A 2,2,1,2,1; B 4,4,4,4,4), equal to project.html data-scores at :535 and :600. This verifier did not score exemplars. For structural reading this verifier read the exemplar blocks at :535-662 (not scored); this is disclosed.",
        "Delta since 700bf33f read in full: project.html line 317 only; grader/test_project.py TOL_GAP comment and three comparisons; ledgers/E4/equivalent/README.md (appended section) and mutant_v17_02 file moved in; mutants v17_01, v17_03, v17_04 present; plans/FINAL-ARCHITECT-RULINGS.md rulings 21-23 (read). Everything else in the slice is byte-identical: reference.py, instance.py, starter.py, tests/labs/E4/*, ledgers/E4/alternatives/*, notation, references, tools. cards.json (course/modules/E/E4/cards.json) is out of this slice.",
        "Gates on 50559266 (out/): check_pages PASS; check_dag PASS; check_projects PASS; run_labs 12/12 PASS; run_graders 0-49 reference 50/50 PASS; page_smoke project PASS; mutate_graders --unit E4 --seeds 0-9 137/137 KILLED (exit 0); ruff check and format PASS; mypy --no-incremental slice PASS (16 files) and full mypy PASS (385 files); pytest on five relevant files PASS; verify_refs offline 560/0 and live E4 3/0. Collect with reference.py as solver.py: 48 tests (the bare collect fails by design, ModuleNotFoundError: solver).",
        "Labs: labs_check.py (out/labs_check.txt): page code equals twin for project-1 and project-3 (trailing newline normalised); project-2 differs only at the blanked return line; each twin run alone under python -I -W error exits 0 with empty stderr; each expected block equals the twin stdout.",
        "Alternatives and equivalents on the edited suite (out/cand/, alts_driver.log): alt_1..alt_8 50/50, the five equivalents 50/50, reference 50/50.",
        "Exact-arithmetic check (ledgers/E4/scripts/E4-d-r18/exact_v17_02.py (out/exact_v17_02.txt), 80-digit Decimal): the reference's reported gap is within 2e-16 of the Proposition 3 gap at the points tested, including sd 3.3e-22 and 1e-50. The quadrature oracle in test_project.py is off by about 8e-15 at sd 0.1 (ledgers/E4/scripts/E4-d-r18/oracle_at_violations.py (out/oracle_at_violations.txt)), so 1e-14 tests need an exact Prop 3 evaluation to be decisive (see E4d17-mutant-v17-02 fix).",
        "Rulings applied: 17 (stop-rule variants: the three variants stay in equivalent/ with their proof), 18 (alt_r8_*/alt_v9_* retired; alt_1..alt_8 stand), 22 (tolerance binding: applied to the three comparisons; does NOT make mutant_v17_02 equivalent because its difference exceeds 1e-14 on the page domain). Ruling 9: a surviving mutant that violates a page-stated behaviour must be killed by a new grader test; mutant_v17_02 is not killed, so it goes back to mutants/ (see its fix).",
        "Hours: 28 h table sums to 28 (1+1+5+8+5+5+3); data-hours and eyebrow say 28; the hub split (index.html) is outside this slice and was not re-read this round.",
        "Not checked by this verifier: L01..L09 and cards.json (other slices; cards excluded by the task); tools/render_curriculum.py, build_site.py --check, fetch_data.py --check (not in slice d); the hub index.html hours split; the browser rendering of the page and of the self-assessment form (no browser run this round); exemplar prose claims beyond those re-derived above were not scored; the lab-twin and page figure for lab 2 blank line is by design.",
        "Carried rows: round-17 PASS rows whose cited subject is outside the delta are carried with the byte-identical prefix; round-17 PASS rows whose subject changed or whose gate was re-run this round are restated above. No round-17 row id is dropped.",
    ],
    "summary": "",
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
frag["verdict"] = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 and all(m["killed_by"] for m in mutants) else "FAIL"
frag["summary"] = (
    f"E4 slice d round 18 (pin 50559266): verdict {frag['verdict']}. Rows {len(rows)}: PASS {counts['PASS']}, FAIL {counts['FAIL']}, "
    f"UNVERIFIABLE {counts['UNVERIFIABLE']}. Mutants {len(mutants)}, killed {sum(1 for m in mutants if m['killed_by'])}. "
    "Resolved from round 17: the gap-tolerance FAIL (three comparisons now 1e-14), the exemplar calibration rows (blind file), and the mutants gate. "
    "Remaining FAIL: mutant_v17_02 is not equivalent under the page's stated 1e-14 (1.57e-14 at 1513 of 43582 domain points), so the README's equivalence proof is retracted and the mutant needs a new grader test."
)
out = ROOT / "ledgers/E4/E4-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), counts, "mutants", len(mutants), "killed", sum(1 for m in mutants if m['killed_by']))
