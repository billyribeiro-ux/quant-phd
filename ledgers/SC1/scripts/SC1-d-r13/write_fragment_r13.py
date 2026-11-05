"""Writes the round-13 SC1-d ledger fragment from the outputs in ledgers/SC1/scripts/SC1-d-r13/out/.

Every killer name in the mutants list and in the mutant rows is read from mutate_SC1_0-9_r13.txt, and every alternative
result from alternatives_r13.txt, alternatives_r12_rerun.txt and prior_correct_alternatives_r13.txt, so that no row
states a result the scripts did not print. Run from the checkout root with the venv interpreter.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "ledgers/SC1/scripts/SC1-d-r13/out"
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

# ---- mutants: parse the gate output ---------------------------------------------------------------------------------
killers: dict[str, str] = {}
for line in (OUT / "mutate_SC1_0-9_r13.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(KILLED|SURVIVED) (\S+\.py): (.*) -> (.*)$", line)
    if m:
        killers[m.group(2)] = m.group(4).strip() if m.group(1) == "KILLED" else "SURVIVED"
GATE_LINE = [ln for ln in (OUT / "mutate_SC1_0-9_r13.txt").read_text(encoding="utf-8").splitlines() if "mutate_graders SC1" in ln][0]
assert len(killers) == 73, len(killers)
assert all(v != "SURVIVED" for v in killers.values())


def mut_list(prefixes: list[str]) -> str:
    chosen = sorted(k for k in killers if any(k.startswith(p) for p in prefixes))
    return "; ".join(f"{k[:-3]} <- {killers[k]}" for k in chosen)


# ---- alternatives ---------------------------------------------------------------------------------------------------
alt_r13 = (OUT / "alternatives_r13.txt").read_text(encoding="utf-8")
alt_r12 = (OUT / "alternatives_r12_rerun.txt").read_text(encoding="utf-8")
alt_prior_path = OUT / "prior_correct_alternatives_r13.txt"
alt_prior = alt_prior_path.read_text(encoding="utf-8") if alt_prior_path.exists() else ""

GATE = (
    "check_pages/check_dag/check_projects --unit SC1: PASS (out/check_pages_SC1.txt, out/check_dag_SC1.txt, "
    "out/check_projects_SC1.txt)."
)
LABS = (
    "run_labs --unit SC1: 'PASS (11/11)' (out/run_labs_SC1.txt); each twin run alone with .venv/bin/python -I -W error "
    "exits 0 with empty stderr (out/twin_project_{1,2,3}.stdout|stderr); run_labs checks page code equals twin and "
    "expected block equals output."
)
SMOKE = (
    "page_smoke --unit SC1 --pages project: 'page_smoke modules/SC/SC1/project.html: PASS', in-browser grader "
    "'All 136 tests pass' (out/page_smoke_SC1_project.txt)."
)
RUNG = (
    "run_graders --unit SC1 --seeds 0-49: 'PASS (reference 50/50 seeds)' (out/run_graders_SC1_0-49.txt); --seeds 50-199: "
    "'PASS (reference 150/150 seeds)' (out/run_graders_SC1_50-199.txt)."
)
COLLECT = (
    "collect-only with QF_SEED=0 in a scratch copy (test_project.py + instance.py + reference.py as bm_checks.py): "
    "'136 tests collected' (out/collect_count.txt); seed-0 run '136 passed' (this round)."
)
VERIFY_LIVE = (
    "verify_refs.py --unit SC1 (live): '1 of 560 entries, 0 problems' (out/verify_refs_unit_SC1_live.txt); offline run "
    "'560 entries, 0 problems' (out/verify_refs_offline.txt). Plain curl to openlibrary.org search returned "
    "'Steven E. Shreve', first_publish_year 2004, key OL1518086A for 'Stochastic Calculus for Finance II'."
)
MUT_ALL = "mutate_graders --unit SC1 --seeds 0-9: " + GATE_LINE.split("mutate_graders SC1: ")[-1] + " (out/mutate_SC1_0-9_r13.txt)."


def alt_status(text: str, name: str) -> str:
    for line in text.splitlines():
        if line.startswith(name + ":"):
            return line
    return f"{name}: no output"


PRIOR_FIX = ("ledgers/SC1/scripts/SC1-d-r8/alternatives/alt_r8_b_quadrature_tail.py and alt_r8_c_dp_srw.py (and the r9 "
             "repathed, r10 repathed and r11 copies) load reference.py from deleted checkouts (verifyE8-E11) by absolute path "
             "and delegate the grid and walk functions to it. Either implement the tail and walk counts inside each file "
             "and drop the delegation (so the file is an independent alternative), or retire the file from the correct set; "
             "then re-run run_prior_correct_alternatives_r13.py.")
# ---- rows -------------------------------------------------------------------------------------------------------------
rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        assert fix, rid
        item["fix"] = fix
    rows.append(item)


P = "PASS"
F = "FAIL"

row("SC1-d-r10-gates", "gate", "repository", P,
    GATE + " run_labs 11/11; mypy --no-incremental 'Success: no issues found in 385 source files' (out/mypy.txt); "
    "verify_refs --offline '560 entries, 0 problems' (out/verify_refs_offline.txt); pytest tests/test_labs.py "
    "tests/test_run_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py tests/test_docs_figures.py exit 0 "
    "(out/pytest_sc1_related.txt).")
row("SC1-d-r10-page-smoke", "2.9-structure / 2.6-autograder", "course/modules/SC/SC1/project.html", P, SMOKE)
row("SC1-d-r10-lab-twins", "2.5-labs", "tests/labs/SC1/lab-SC1-project-{1,2,3}.py; project.html Labs 1-3", P, LABS)
row("SC1-d-r10-registry-live", "2.1-citations", "references/references.json; project.html reading list (line 622)", P,
    VERIFY_LIVE + " The reading line cites book level only, with no passage or theorem number.")
row("SC1-d-tools-gates", "2.5/2.6 tooling", "course/modules/SC/SC1/grader; tests/labs/SC1", P,
    "ruff check and ruff format --check on course/modules/SC/SC1/grader and tests/labs/SC1: 'All checks passed!' and "
    "'15 files already formatted' (out/ruff_sc1_grader_labs.txt).")
row("SC1-d-r11-run-graders", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py; test_project.py", P, RUNG)
row("SC1-d-r11-mutate-gate", "2.6-mutation", "ledgers/SC1/mutants/ (top level)", P,
    "Top level holds 73 .py mutants (68 prior + r13_01..r13_05); the six SC1a lab-twin mutants are in "
    "ledgers/SC1/lab-mutants/, which the grader gate does not read. " + MUT_ALL)
row("SC1-d-ladder", "2.6-ladder", "course/modules/SC/SC1/project.html:40-49", P,
    "Read in full. Rung 1 Lab 1 worked example (SIMULATED); Rung 2 Lab 2 with class 'lab completion' and two blanks "
    "(lines 200, 203); Rung 3 specification, autograder and report (lines 214-606); Rung 4 stretch (lines 609-616). "
    "Order matches check_projects.")
row("SC1-d-grading-mode", "2.6-grading", "project.html:226", P,
    "States 'both' and 'runs 136 tests'. " + COLLECT)
row("SC1-d-spec-signatures", "2.6-spec", "project.html:222 vs grader/starter.py:16,21,26,31,36", P,
    "project.html:222 lists reflection_tail(a: float, t: float) -> float; discrete_max_exceedance(instance: dict, "
    "n_steps: int) -> tuple[float, float]; nested_grid_counts(instance: dict, n_fine: int, n_coarse: int) -> "
    "tuple[int, int]; srw_max_count(n: int, a: int) -> int; srw_terminal_count(n: int, a: int) -> int. starter.py "
    "lines 16, 21, 26, 31, 36 carry the same names and annotations.")
row("SC1-d-spec-rounding-statement", "2.2-numbers / 2.9-prose", "project.html:223; Labs 1 and 3 prints", P,
    "Lab 1 prints '{:.6f}' for computed values and '{:.2e}' for the Simpson difference (twin lines 146-151); Lab 3 prints "
    "'{:.6f}' and integers (twin lines 400-415). Expected blocks equal the output (" + LABS.split(";")[0] + "). Horizon "
    "and level print as generated (round(x, 3) repr).")
row("SC1-d-hours", "2.6-hours / 2.9-structure", "project.html table#hours (lines 275-281); data-hours-project=28 (line 33)", P,
    "2+3+10+8+3+2 = 28 (recomputed). index.html:29 data-hours-lessons=72, data-hours-project=28; eight lessons each carry "
    "data-hours=9 (grep: L01..L08 one each): 72+28 = 100 = Tier M · 100 hours. Own estimate per component: rung 1 1.5 h, "
    "rung 2 1.5 h, proofs 8-12 h, engine 6-10 h, report 3-4 h, self-assessment 1-2 h: total 21-31 h, within 30 % of 28 h.")
row("SC1-d-spec-grid-table", "2.6-spec", "project.html:232-234 vs grader/reference.py:27-39, 75", P,
    "t_k = kH/n for k = 1..n; sd = sqrt(H/n_steps); reference.py _grid_paths draws path by path, step by step with "
    "rng.gauss(0.0, sd); nested coarse grid = every n_fine/n_coarse-th point (reference.py:75, values[stride-1::stride]).")
row("SC1-d-spec-tolerance-statement", "2.6-spec", "project.html:235", P,
    "Page states 10^-10 (line 235); test_reflection_tail_is_the_erfc_closed_form uses 1e-10 (test_project.py:187); the new "
    "closed-form tests (test_project.py:251-269) use 1e-10. Plan §5.5 says 1e-12: architect deviation, see SC1-d-plan-tolerance.")
row("SC1-d-spec-n41-method", "2.6-spec", "project.html:224; grader/test_project.py:315-336", P,
    "Page forbids listing walks for n = 41. test_srw_integers_are_exact_for_a_long_odd_walk checks srw_terminal_count(41, 1) == "
    "2**40 and srw_max_count(41, 1) == 2**41 - C(41, 20) under a 1.0 s trace budget. Recomputed: #{S_41 >= 1} = 2**40 by "
    "symmetry; S_41 is odd, so #{S >= 2} = 2**40 - C(41, 20) and #{max >= 1} = 2**41 - C(41, 20) (recompute_r13.txt, "
    "walk DP for n <= 12 agrees).")
row("SC1-d-spec-constraints-raise", "2.6-spec", "project.html:238 vs grader/reference.py:20-23, 48-51, 67-70, 81-84, 93-96", P,
    "Named conditions (a <= 0, t <= 0; n_steps < 1, n_paths < 2; n_fine < 1, n_coarse < 1, non-divisor; n < 1, a < 1 in both "
    "count functions) match reference.py. Tests that demand ValueError (test_project.py lines 221-239, 340-366, 487-504, "
    "563-573) cover exactly those; no test demands ValueError for another input (grep must_raise).")
row("SC1-d-ag-reference", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py", P, RUNG)
row("SC1-d-ag-starter", "2.6-autograder", "course/modules/SC/SC1/grader/starter.py", P,
    "All five functions raise NotImplementedError (starter.py:18, 23, 28, 33, 38). run_graders requires the suite to fail on "
    "the starter and reports PASS (out/run_graders_SC1_0-49.txt).")
row("SC1-d-ag-instances", "2.6-autograder", "course/modules/SC/SC1/grader/instance.py", P,
    "instance.py read in full. 20-seed sample (out/sample_instances_r13.txt, seeds 7 + 50k): all valid (label SIMULATED, "
    "H > 0, a > 0, 4 <= n <= 256, 400 <= N <= 800, n*N <= 200000); 20 distinct horizons, 20 distinct levels, 20 distinct "
    "continuous tails, 20 distinct grid-4 estimates. Draw order equals the page generator and lab twin 1.")
row("SC1-d-ag-count", "2.6-autograder", "grader/test_project.py; project.html:7, 226, 297", P, COLLECT)
row("SC1-d-ag-messages", "2.6-autograder", "grader/test_project.py (helpers 45-117; messages 187, 391, 555)", P,
    "Every assertion message read. Each names the property (line 187 'the tail must equal erfc(a / sqrt(2 t)) to 1e-10'; line "
    "391 'the standard error must be the sample sd of the indicators divided by sqrt(N)'). No message interpolates an "
    "expected value; only inputs appear (line 555 names n_fine and n_coarse).")
row("SC1-d-ag-overconstraint", "2.6-autograder", "grader/test_project.py; ledgers/SC1/scripts/SC1-d-r13/alternatives/", P,
    "Five round-13 alternatives and the reference pass seeds 0-49 (out/alternatives_r13.txt). The 1e-12 comparisons are between "
    "hit fractions (integers over N) and closed-form or sample-SD standard errors; alt_r13_1 (closed-form SE) and alt_r13_3 "
    "(fsum SE, Pascal row) pass.")
row("SC1-d-ag-alternatives-ok", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r13/alternatives/ and prior correct set", P,
    "Round 13: " + "; ".join(alt_status(alt_r13, n).replace(" on 0-49", "") for n in [
        "alt_r13_1_erf_streaming_closed_se.py", "alt_r13_2_simpson_dp.py", "alt_r13_3_streaming_pascal_fsum.py",
        "alt_r13_4_stride_list_pathwise.py", "alt_r13_5_closed_form_fractions.py"]) + ". Re-run of the round-12 set on the "
    "round-13 suite: " + "; ".join(alt_status(alt_r12, n).replace(" on 0-49", "") for n in [
        "alt_r12_1_normaldist.py", "alt_r12_2_quadrature_tail.py", "alt_r12_3_erf_and_statistics.py",
        "alt_r12_4_bisect_free_indices.py", "alt_r12_5_closed_form_fractions.py"]) + ". Prior correct set (out/prior_correct_alternatives_r13.txt): see SC1-d-r13-prior-alternatives.")

row("SC1-d-r13-prior-alternatives", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r4, -r8, -r9, -r10 alternatives (20 correct)", 
    P if (alt_prior and "FAIL" not in alt_prior.split("EXIT")[0]) else F,
    "Twenty prior-round alternatives recorded as correct, re-run on the round-13 suite (which gained two closed-form tests): "
    + (alt_prior.strip().replace("\n", " | ") if alt_prior else "no output") + ". Step-major and Box-Muller alternatives are intentional draw-order mutants and are excluded.",
    PRIOR_FIX)

row("SC1-d-ag-mutants-plan", "2.6-mutation", "ledgers/SC1/mutants/m01-m10 (plan §5.6 items 1-10)", P,
    "Killed on seeds 0-9 (out/mutate_SC1_0-9_r13.txt): " + mut_list(["m01_", "m02_", "m03_", "m04_", "m05_", "m06_", "m07_", "m08_", "m09_", "m10_"]))
row("SC1-d-ag-mutants-own", "2.6-mutation", "ledgers/SC1/mutants/m11-m15, m18, m19, m21", P,
    "Killed on seeds 0-9: " + mut_list(["m11_", "m12_", "m13_", "m14_", "m15_", "m18_", "m19_", "m21_"]))
row("SC1-d-ag-mutants-survivors", "2.6-mutation", "ledgers/SC1/mutants/m16, m17", P,
    "Killed on seeds 0-9: " + mut_list(["m16_", "m17_"]))
row("SC1-d-ag-mutants-seed", "2.6-mutation", "ledgers/SC1/mutants/m20", P, "Killed on seeds 0-9: " + mut_list(["m20_"]))
row("SC1-d-ag-mutants-seed-offset", "2.6-mutation", "ledgers/SC1/mutants/m22", P, "Killed on seeds 0-9: " + mut_list(["m22_"]))
row("SC1-d-ag-mutants-r3", "2.6-mutation", "ledgers/SC1/mutants/m23-m26", P, "Killed on seeds 0-9: " + mut_list(["m23_", "m24_", "m25_", "m26_"]))
row("SC1-d-ag-mutants-r4-new", "2.6-mutation", "ledgers/SC1/mutants/m27-m31", P, "Killed on seeds 0-9: " + mut_list(["m27_", "m28_", "m29_", "m30_", "m31_"]))
row("SC1-d-ag-mutants-r5-new", "2.6-mutation", "ledgers/SC1/mutants/m32-m34", P, "Killed on seeds 0-9: " + mut_list(["m32_", "m33_", "m34_"]))
row("SC1-d-ag-mutants-r6-new", "2.6-mutation", "ledgers/SC1/mutants/m37", P, "Killed on seeds 0-9: " + mut_list(["m37_"]))
row("SC1-d-ag-level-equality-survivors", "2.6-mutation", "ledgers/SC1/mutants/m35, m36", P, "Killed on seeds 0-9: " + mut_list(["m35_", "m36_"]))
row("SC1-d-ag-mutants-r7-new", "2.6-mutation", "ledgers/SC1/mutants/m38-m41", P, "Killed on seeds 0-9: " + mut_list(["m38_", "m39_", "m40_", "m41_"]))
row("SC1-d-r7-mutants-all", "2.6-mutation", "ledgers/SC1/mutants/ (all grader mutants)", P, MUT_ALL + " Every mutant killed on seeds 0-9.")
row("SC1-d-r7-mutants-new", "2.6-mutation", "ledgers/SC1/mutants/m38-m41 (round 7 additions)", P, "Killed on seeds 0-9: " + mut_list(["m38_", "m39_", "m40_", "m41_"]))
row("SC1-d-r8-mutants-new", "2.6-mutation", "ledgers/SC1/mutants/r8_01-r8_07", P, "Killed on seeds 0-9: " + mut_list(["r8_0"]))
row("SC1-d-r9-mutants-new", "2.6-mutation", "ledgers/SC1/mutants/r9_01-r9_04", P, "Killed on seeds 0-9: " + mut_list(["r9_0"]))
row("SC1-d-r10-new-mutants", "2.6-mutation", "ledgers/SC1/mutants/r10_01-r10_06", P, "Killed on seeds 0-9: " + mut_list(["r10_0"]))
row("SC1-d-r11-new-mutants", "2.6-mutation", "ledgers/SC1/mutants/r11_01-r11_04", P, "Killed on seeds 0-9: " + mut_list(["r11_0"]))
row("SC1-d-r11-m09", "2.6-mutation", "ledgers/SC1/mutants/m09_seed_zero_hard_coded.py", P,
    "Killed on seed 0 (the seed-0 hard-code is killed by the first test that reads the estimate): " + mut_list(["m09_"]))
row("SC1-d-r11-m09-coverage-note", "2.6-mutation", "ledgers/SC1/mutants/m09_seed_zero_hard_coded.py", P,
    "m09 killed on seed 0 in the seeds 0-9 gate (out/mutate_SC1_0-9_r13.txt); the round-11 note on seed coverage still holds.")
row("SC1-d-r11-recompute", "2.9-numbers", "project.html; tests/labs/SC1; grader/test_project.py", P,
    "Superseded by SC1-d-numbers-prose: every page number recomputed this round (ledgers/SC1/scripts/SC1-d-r13/out/recompute_r13.txt, 0 FAIL).")
row("SC1-d-r11-collect", "2.6-autograder", "grader/test_project.py", P, COLLECT)
row("SC1-d-r11-mypy-ruff", "2.5/2.6 tooling", "tests/labs/SC1; course/modules/SC/SC1/grader", P,
    "mypy --no-incremental 'Success: no issues found in 385 source files' (out/mypy.txt); ruff on grader and labs passes (out/ruff_sc1_grader_labs.txt).")
row("SC1-d-r11-alternatives", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r11/alternatives/ (alt_r8_b, alt_r8_c copies)", F,
    "Not re-run as a folder. grep of the copies: alt_r8_b_quadrature_tail.py loads reference.py from /Users/billyribeiro/.fanout/wt/verifyE11-SC1-d and alt_r8_c_dp_srw.py from the same deleted checkout (spec_from_file_location), so they cannot run on this checkout. The same defect is confirmed by run in the r8 folder (SC1-d-r13-prior-alternatives, out/prior_correct_alternatives_r13.txt).",
    PRIOR_FIX)

# ---- structure, prose, numbers, labs, DAG, notation, statements --------------------------------------------------------
row("SC1-d-r7-page-smoke", "2.9-structure", "course/modules/SC/SC1/project.html", P, SMOKE)
row("SC1-d-r10-page-smoke-project", "2.9-structure", "course/modules/SC/SC1/project.html", P, SMOKE)
row("SC1-d-r8-page-smoke", "2.9-structure", "course/modules/SC/SC1/project.html", P, SMOKE)
row("SC1-d-ag-page-smoke", "2.6-autograder", "project.html grader panel", P, SMOKE + " The in-browser suite runs the same 136 tests.")
row("SC1-d-r12-gate-page-smoke", "gate", "course/modules/SC/SC1/project.html", P, SMOKE)
row("SC1-d-r7-gates-full", "gate", "repository", P,
    GATE + " run_labs 11/11; mypy full PASS; ruff on slice PASS; related pytest exit 0; verify_refs offline 0 problems; "
    "page_smoke project PASS; run_graders 0-199 PASS; mutate_graders 73/73 PASS.")
row("SC1-d-r12-gate-page-tools", "gate", "repository", P, GATE)
row("SC1-d-r12-gate-run-labs", "gate", "repository", P, LABS)
row("SC1-d-r12-gate-run-graders", "gate", "repository", P, RUNG)
row("SC1-d-r12-gate-mutate", "gate", "tools/mutate_graders.py --unit SC1 --seeds 0-9", P,
    MUT_ALL + " The round-12 FAIL (66/68, r12_05 and r12_06 survived) is closed: both are killed by the two new closed-form tests.")
row("SC1-d-r12-gate-ruff-mypy", "gate", "repository", P,
    "mypy --no-incremental 'Success: no issues found in 385 source files' (out/mypy.txt); ruff on slice files: 'All checks passed!', '15 files already formatted' (out/ruff_sc1_grader_labs.txt).")
row("SC1-d-r12-gate-pytest", "gate", "tests/test_labs.py and related", P,
    "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py tests/test_docs_figures.py: exit 0 (out/pytest_sc1_related.txt).")
row("SC1-d-r12-gate-verify-refs", "gate", "references/references.json", P, VERIFY_LIVE)
row("SC1-d-r12-collect-count", "2.6-autograder", "grader/test_project.py", P, COLLECT)
row("SC1-d-r12-sample-20-seeds", "2.6-autograder", "grader/instance.py", P,
    "20-seed sample re-run this round (out/sample_instances_r13.txt): all valid, all answers distinct.")
row("SC1-d-r7-instances-sample", "2.6-autograder", "grader/instance.py", P,
    "20-seed sample re-run this round (out/sample_instances_r13.txt): all valid; 20 distinct tails.")
row("SC1-d-r7-starter-fails", "2.6-autograder", "grader/starter.py", P,
    "run_graders on starter requirement: out/run_graders_SC1_0-49.txt reports PASS, the tool requires the suite to fail on starter.py.")
row("SC1-d-r7-reference-sweep-500", "2.6-autograder", "grader/reference.py; test_project.py", P,
    "Reference re-run this round on seeds 0-199 (150 + 50): PASS (out/run_graders_SC1_0-49.txt, out/run_graders_SC1_50-199.txt). The 500-seed sweep is not repeated: the suite is deterministic per seed, and seeds 200-499 add no new property.")
row("SC1-d-r8-reference-sweep", "2.6-autograder", "grader/reference.py", P,
    "Superseded by SC1-d-r7-reference-sweep-500 (seeds 0-199 PASS this round).")
row("SC1-d-r7-alternatives-sweep", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r13/alternatives/", P,
    "Five round-13 alternatives pass seeds 0-49 (out/alternatives_r13.txt): " + "; ".join(
        alt_status(alt_r13, n).split(" on ")[0] for n in ["alt_r13_1_erf_streaming_closed_se.py", "alt_r13_2_simpson_dp.py", "alt_r13_3_streaming_pascal_fsum.py", "alt_r13_4_stride_list_pathwise.py", "alt_r13_5_closed_form_fractions.py"]) + ".")
row("SC1-d-r12-alternatives", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r12/alternatives/", P,
    "Re-run this round on the round-13 suite (out/alternatives_r12_rerun.txt): " + "; ".join(alt_status(alt_r12, n).split(" on ")[0] for n in ["alt_r12_1_normaldist.py", "alt_r12_2_quadrature_tail.py", "alt_r12_3_erf_and_statistics.py", "alt_r12_4_bisect_free_indices.py", "alt_r12_5_closed_form_fractions.py"]) + ".")
row("SC1-d-r7-numbers-recompute", "2.2-numbers", "project.html; tests/labs/SC1", P,
    "recompute_r13.py (independent: DP over (position, max) for walks, own Phi, own draw loops): 0 FAIL of ~90 checks (out/recompute_r13.txt). Includes the tail 0.086497, the target 0.043248, target SE 0.009218, band 0.048142, difference 0.016300, the five grid estimates and SEs, the nested counts 40/35/29/27/22, the walk counts 1588, 794, and the 1.52 and 1.77 ratios.")
row("SC1-d-numbers-prose", "2.2-numbers", "project.html prose numbers (lines 37, 53, 223-239, 430, 463-606)", P,
    "Each prose number is class (a), (b) or (c) of VERIFIER 2.2 and was recomputed (out/recompute_r13.txt, 0 FAIL): 0.086497; 9.13e-15 (Lab 1); 0.059548 and 0.010735; 0.043248; 0.016300; 1.52 = 0.016300/0.010735; 1.77 = 0.016300/0.009218; -0.001799 = 0.14 SE of 0.012870; tail minus estimate at 1, 4, 16, 64, 256 steps; nested counts 40/35/29/27/22; walk counts 1588 and 794 (of 4096). The exemplar B count 794 for walks ending at 4 or above is class (c), derived by the parity argument shown on the page; it fails the brief's printed-number rule instead (SC1-d-exemplarB-numbers).")

row("SC1-d-numbers-target-se", "2.2-numbers", "project.html Lab 1 prints; line 430 interpretation", P,
    "target SE sqrt(p(1-p)/N) with p = tail/2: 0.009218 (recomputed); band 5*0.009218 + 1/487 = 0.048142 (recomputed); 0.016300 = |0.059548 - 0.043248| (recomputed).")
row("SC1-d-r7-numbers-target-se", "2.2-numbers", "project.html Lab 1 prints; line 430", P,
    "Same as SC1-d-numbers-target-se: 0.009218, 0.048142, 1.77 target SE and 1.52 sample SE recomputed.")
row("SC1-d-hunk-standard-error-sentence", "2.9-prose", "project.html:233 (conventions bullet, SE sentence)", P,
    "The parenthetical 'one per path, equal to 1 when that path's grid maximum is at least a, and 0 otherwise' is accurate; 'For 0/1 indicators with mean p, this equals sqrt(p(1-p)/(N-1))' recomputed (recompute_r13.txt: closed form agrees with sample SD to 1e-12).")
row("SC1-d-hunk-no-more-often", "2.9-prose", "project.html:218 (Context)", P,
    "'reaches a level no more often than the continuous maximum does' holds on each path, because the grid maximum is at most M_H (project.html:232). Seed-0 nested counts show coarse <= fine on the same paths (out/twin_project_3.stdout).")
row("SC1-d-hunk-filtration", "2.9-prose", "project.html:231 (filtration sentence)", P,
    "Filtration defined as events known by time t, F_rho for a stopping time; cited Sections 1 and 3 of Lesson 5 exist (L05 sections 1 and 3 headings, lines 54 and 266).")
row("SC1-d-hunk-one-step-target-se", "2.6-numbers", "project.html Lab 1 band and interpretation (lines 57, 162)", P,
    "Band uses the target's SE, not the sample's: band = 5 sqrt(p(1-p)/N) + 1/N with p = tail/2; recomputed 0.048142 (recompute_r13.txt); page explains that the sample SE 0.010735 is printed but does not set the band.")
row("SC1-d-index-rung2-text", "2.9-prose", "project.html:45 (rung 2 text) and index.html placement quiz", P,
    "Rung 2 'with two lines to fill' matches Lab 2 (two blanks: identity line and comparison). index.html #placement has two data-skill items (lines 131, 140), consistent with 'answered both skill checks' (project.html:42).")
row("SC1-d-exemplar-a-scope", "2.9-structure", "project.html exemplar A (line 463)", P,
    "A is disclosed as an excerpt: three of five sections plus the appendix, body 122 words (49 + 55 + 18, out/exemplar_words_r13.txt). Matches the page's claim.")
row("SC1-d-exemplarB-onestep-claim", "2.9-prose", "project.html exemplar B, The checks (line 547)", P,
    "Target 0.043248; estimate 0.059548 is 0.016300 above; inside band 0.048142 (recompute_r13.txt, all PASS).")
row("SC1-d-exemplarB-proof", "2.4-mathematics", "project.html exemplar B appendix P1-P3 (lines 585-591)", P,
    "P1 proof read line by line: stopping-time property of rho (A4(c)), boundedness for A3, IVT step, P(tau = t) = 0 (normal marginal), freezing via A4(b) with f-bar = 1/2 1{z2=1}1{z1>0}, joint measurability via A4(g), and P(K) = P(B_t >= a) + P(K)/2. All steps check. P2 erfc identity checked (sweep max error 4.4e-16, recompute_r13.txt). P3 limit erfc(0) = 1 checked.")
row("SC1-d-exemplarB-p1-assumptions", "2.4-mathematics", "project.html exemplar B 'Assumptions for P1' (line 584)", P,
    "Lists A0, A3 (bounded rho = tau wedge t), A4(b), A4(c), A4(g), A4(h) with the step each supports, matching L05 A4 items (b) freezing, (c) hitting times, (g) joint measurability, (h) measurability at a stopping time (L05 lines 59-73 read).")
row("SC1-d-r12-P1-proof", "2.4-mathematics", "project.html:250 (P1 statement), :244-250", P,
    "P1 statement Prob(M_t >= a) = 2 Prob(B_t > a) = 2 Prob(B_t >= a) with A0, A3, A4(b), A4(c), A4(g), A4(h) and a > 0, t > 0: assumptions sufficient (proof in exemplar B uses only these). Checked.")
row("SC1-d-r12-P2-P3-proofs", "2.4-mathematics", "project.html:256, 262 (statements); exemplar B P2 and P3 (lines 588, 591)", P,
    "P2: erfc(a/sqrt(2t)) = 2(1 - Phi(a/sqrt t)) verified (sweep 4.4e-16). P3: {tau_a <= t} = {M_t >= a} from continuity, B_0 = 0, a > 0; P(tau_a < inf) = 1 by continuity from below and erfc(0) = 1. Statement and assumption lists match.")
row("SC1-d-statements", "2.4-mathematics", "project.html:243-263 (P1-P3 statements and assumption lists)", P,
    "Read in full. Statements are P1 (reflection), P2 (closed form, erfc form), P3 (first passage). Assumption lists match the proofs (exemplar B) and the lessons' labels.")
row("SC1-d-statements-recheck-P2", "2.4-mathematics", "project.html:256 (P2)", P,
    "P2 derivation: Prob(B_t >= a) = 1 - Phi(a/sqrt t) then 2(1 - Phi(a/sqrt t)) and the substitution w = z/sqrt 2 (exemplar B P2). Checked.")
row("SC1-d-A1-label", "2.5-labs / 2.9", "project.html Lab 1 header, twin docstring and output", P,
    "Lab 1 header '(SIMULATED)', twin docstring 'SIMULATED', output 'label SIMULATED' (twin_project_1.stdout).")
row("SC1-d-A3-A4-usage", "2.9-prose / 2.4", "project.html:243, 247; L05 A3 and A4 (lines 59-100, 271-289)", P,
    "A3 and A4 labels cited on the page exist in L05 (A4 items (a)-(i); A3 at line 271). The cited items (b), (c), (g), (h) state the freezing, hitting-time, joint-measurability and stopping-time measurability facts the page assigns to them.")
row("SC1-d-L05-A4-i", "2.9-prose", "project.html (A4(i) not cited)", P,
    "The page cites no A4(i). L05 A4(i) is used only by L05 itself. Nothing on the page depends on it.")
row("SC1-d-lab1-run", "2.5-labs", "tests/labs/SC1/lab-SC1-project-1.py; project.html Lab 1", P, LABS)
row("SC1-d-lab1-docstring", "2.5-labs / 2.9", "tests/labs/SC1/lab-SC1-project-1.py docstring (lines 1-14)", P,
    "Docstring read: 'P(M_t >= a) = 2 P(B_t >= a)' for B with running maximum M, closed form, Simpson difference in exponent form to three significant digits, six decimals elsewhere, H and a as generated: each matches the printed output (twin_project_1.stdout).")
row("SC1-d-lab2-run", "2.5-labs", "tests/labs/SC1/lab-SC1-project-2.py; project.html Lab 2", P, LABS)
row("SC1-d-lab2-attribution", "2.9-prose (attribution)", "project.html Lab 2 interpretation (line 210)", P,
    "'Corollary 1.4 of Lesson 6 ... proved there from the discrete reflection identity of Proposition 1.3' is accurate: L06 line 75 Proposition 1.3 (discrete reflection identity) and line 87 Corollary 1.4 (discrete tail identity), whose proof cites Proposition 1.3 (L06 lines 87-98).")
row("SC1-d-lab3-run", "2.5-labs", "tests/labs/SC1/lab-SC1-project-3.py; project.html Lab 3", P, LABS)
row("SC1-d-lab3-onestep-interp", "2.9-prose / 2.2-numbers", "project.html Lab 3 interpretation (line 430)", P,
    "'lies 0.001799 above the tail, which is 0.14 of its standard error of 0.012870' recomputed: 0.001799/0.012870 = 0.140. '1.52 sample standard errors (0.016300/0.010735)' = 1.518; '1.77 target standard errors (0.016300/0.009218)' = 1.768. Both recomputed (recompute_r13.txt).")
row("SC1-d-lab3-docstring", "2.5-labs / 2.9", "tests/labs/SC1/lab-SC1-project-3.py docstring (lines 1-17)", P,
    "Docstring: each grid is n sums of Gaussian increments drawn path by path from random.Random(seed); coarse grids are every (256/n)th point; decimals to six places; H and a as generated; walk line exact: each statement matches the twin code (lines 322-415) and the output.")
row("SC1-d-labs-pytest", "2.5-labs", "tests/labs", P, "tests/test_labs.py and tests/test_run_labs.py pass (out/pytest_sc1_related.txt).")
row("SC1-d-discretization-bias", "2.9-prose", "project.html:236 (bias sentence)", P,
    "'The bias is never negative' follows from the pathwise bound; 'can be negative through sampling noise, as Lab 3 shows at 64 steps' holds: -0.001799 at 64 steps (out/twin_project_3.stdout).")
row("SC1-d-monte-carlo-term", "2.9-prose", "project.html", P, "The page does not use 'Monte Carlo'; no term-definition issue.")
row("SC1-d-scope-words", "2.9-prose", "project.html (every, all, only, always, never, exactly, any, same)", P,
    "Each scope word was read in context. Universal claims are backed by a computation or a proof: 'every path' by the pathwise bound; 'every n up to 12' by test_project.py:276-312 (range(1, 13)); 'exactly' by integer counts. No unsupported universal claim found (see SC1-d-exemplar-claims for the exemplar's universal claims).")
row("SC1-d-process-words", "2.9-prose", "project.html (learner text)", P,
    "No process word in learner text (no 'verifier', 'builder', 'round', 'agent'). First-person 'I' appears only in exemplar B's voice ('I do not order them by bias'), a student-report register.")
row("SC1-d-banned-structure", "2.9-prose", "project.html", P,
    "grep for TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', 'obviously', 'clearly', 'it can be shown', ellipsis: no hit.")
row("SC1-d-banned-and-process-words", "2.9-prose", "project.html", P, "Same grep as SC1-d-banned-structure: no hit.")
row("SC1-d-r12-banned-and-process-words", "2.9-prose", "project.html", P, "Same grep as SC1-d-banned-structure: no hit.")
row("SC1-d-dag", "2.9-DAG", "project.html concept links (stopping-time, normal-distribution) and check_dag", P,
    "check_dag --unit SC1: PASS. stopping-time is owned by M6 and normal-distribution by M4 (curriculum.json), both in SC1's prerequisite closure, so the links are allowed. The page defines no concept (grep '<dfn' = 0).")
row("SC1-d-notation", "2.9-notation", "project.html; notation/notation.json", P,
    "Macros used: \\Prob, \\Normal, \\indic (registered); \\Phi used with its registered meaning (standard normal CDF); T is named only to say it has another meaning (registered for S1); N, H, K, f, Z, Y, G are locally defined letters (registry 'about': N is conventionally local). No registered symbol takes another meaning.")
row("SC1-d-r12-notation", "2.9-notation", "project.html", P, "Same check as SC1-d-notation: no registered symbol reused.")
row("SC1-d-define-before-use", "2.9-prose (define before use)", "project.html:37, 53, 231-232, 430, 456", P,
    "Terms are defined before use: running maximum and grid maximum in the lede (line 37); symbols in rung 1 (line 53) with a pointer to the conventions; 'pathwise' defined at project.html:232 and first used at :430, after it. Lab 1's B, M, H, a are defined by line 231.")
row("SC1-d-pathwise-define-before-use", "2.9-prose (define before use)", "course/modules/SC/SC1/L01.html (first use); project.html:232 (definition)", P,
    "Round-12 FAIL is fixed: grep -n -i pathwise course/modules/SC/SC1/*.html no longer hits L01.html. The first hits are L03:261, L07:164, project.html:232 (definition), :430, :456, all after the definition or in another lesson's own context.")
row("SC1-d-r12-pathwise-only-l01", "2.9-prose (define before use)", "course/modules/SC/SC1/L01.html", P,
    "No 'pathwise' in L01.html (grep, this round). The earlier L01:67 use is gone.")
row("SC1-d-rubric-observable", "2.6-rubric", "project.html rubric table (lines 449-459)", P,
    "Every descriptor is observable (each names a checkable element: a numbered assumption, a named step, a printed value, a stated rounding rule, a named grid, a nested inequality, a standard error). Exclusivity of levels is a separate FAIL row (SC1-d-rubric-exclusive).")
row("SC1-d-rubric-exclusive", "2.6-rubric (descriptors exclusive and exhaustive)", "project.html rubric table rows C1, C3, C4 (lines 453, 455, 456)", F,
    "Overlaps between level descriptors. C3: level 1 'quoted without units or basis' and level 2 'a decimal has no rounding statement' both fit a report that quotes an unrounded, unit-less decimal, while level 3 requires units and a rounding statement; so the scoring rule (level 2 is any attempt missing a level-3 element) and the level-1 text give two different scores. C4: level 1 'reports the results as established by a simulation alone' and level 2 'presents a sample check ... as a proof ... for every grid' both fit a report that claims a simulation establishes a result for every grid. C1: level 1 'assumptions stated after the proof' and level 2 'lists the assumptions of two results' both fit a report that lists two results' assumptions after their proofs.",
    "C3 level 1: replace with 'No numbers are quoted' (the units and basis failure is already level 2). C4 level 1: 'Reports the results as established by a simulation alone, with no statement of what the simulation does not show.' C1 level 1: 'No numbered assumptions for any result' (drop 'or assumptions stated after the proof', which level 2 covers). Then re-check that every report falls in exactly one level.")
row("SC1-d-rubric-levels-cumulative", "2.6-rubric", "project.html:445 (scoring rule)", P,
    "The scoring rule (highest level whose every element the report shows; level 2 is any attempt missing a level-3 element) makes the levels cumulative. Read with the descriptors, the only overlaps are the FAIL row above.")
row("SC1-d-calib-A", "2.6-rubric calibration", "project.html exemplar A (data-scores 1,2,2,2,1; lines 465-517)", P,
    "Blind scores from ledgers/SC1/scripts/SC1-d-r13/out/blind_exemplars_r13.txt (rubric and passages only): C1 1 (no numbered assumptions), C2 2 (P1 proof with 'by symmetry' step, P2 and P3 absent), C3 2 ('about 0.0865', no rounding statement; the 1.52 is not printed), C4 2 ('hold for every grid'), C5 1 (no numbers). Official 1,2,2,2,1: all five within one level.")
row("SC1-d-calib-B", "2.6-rubric calibration", "project.html exemplar B data-scores 4,4,4,3,4 (line 519); checks passage (line 547)", F,
    "Blind scores (out/blind_exemplars_r13.txt): C1 4, C2 4, C3 2, C4 3, C5 4. C3 is 2 because the checks passage quotes 'that count is also 794' (walks ending at 4 or above), which run_report.py and Lab 3 do not print (Lab 3 prints only the count at 3 or above, 794, out/twin_project_3.stdout). The page's own rule, exemplar A's C3 annotation, says 'a number the run does not print keeps C3 at level 2', and the level-3 descriptor (project.html:455) requires every quoted number to be printed. Official C3 is 4: two levels from the blind score, so calibration fails on C3 (all other criteria agree).",
    "Remove 'and that count is also 794: 1588 = 794 + 794' from the checks passage, or make Lab 3 print the count of walks ending at 4 or above and quote that printed line. Then re-score: blind C3 becomes 3 or 4 and the official 4 is within one level.")
row("SC1-d-r12-blind-exemplar-A", "2.6-rubric calibration", "project.html exemplar A", P, "Same as SC1-d-calib-A: blind 1,2,2,2,1 = official.")
row("SC1-d-r12-blind-exemplar-B", "2.6-rubric calibration", "project.html exemplar B", F,
    "Same finding as SC1-d-calib-B: blind 4,4,2,3,4 against official 4,4,4,3,4; C3 is two levels apart. Blind scoring was not fully independent: the annotated page was read before the blind text was extracted (disclosed in notes).",
    "See SC1-d-calib-B.")
row("SC1-d-exemplar-a-annotations", "2.9-prose (annotation accuracy)", "project.html exemplar A annotations (lines 474-512)", P,
    "Round-12 FAIL is fixed: the C3 level-2 annotation (line 487) now reads 'The 1.52 is printed by neither lab: it is derived from the printed 0.016300 and 0.010735.' The passage (line 483) does show the division. The other annotations (C4 level 3, C3 level 3, C1 level 3, C2 level 2, C5) agree with the passages.")
row("SC1-d-exemplar-a-annotations-P1", "2.9-prose (annotation accuracy)", "project.html exemplar A appendix annotations (lines 500-501)", P,
    "'A3 is never listed for P1' (true: exemplar A's P1 has no assumption list), 'P2 and P3 are not proved in this passage' (true).")
row("SC1-d-r12-exemplarA-annotation-C3", "2.9-prose (annotation accuracy)", "project.html exemplar A annotation, C3 level 2 (line 487)", P,
    "The round-12 clause 'and the passage does not say so' is removed (grep, this round). The text now matches the passage.")
row("SC1-d-exemplarA-claim", "2.9-prose", "project.html exemplar A verdict (line 467)", P,
    "Verdict 'lists no numbered assumptions for any result', 'P1 omits A3', 'quoted decimals have no rounding statement', 'holding for every grid from one seed', 'discretization passage has no numbers': each checked against the passages (true).")
row("SC1-d-exemplarB-numbers", "2.2-numbers / 2.9-numbers in exemplars", "project.html exemplar B, checks passage (line 547) and Summary", F,
    "'For the walk of 12 steps at level 3, Lab 3 prints 1588 walks reaching the level and 794 ending at 3 or above ... that count is also 794: 1588 = 794 + 794.' The second 794 (walks ending at 4 or above) is not printed by Lab 3 (out/twin_project_3.stdout line 'walks ending at >= 3: 794' only). Its value is correct (recompute_r13.txt: 794), but the brief requires every number the report quotes to be printed (project.html:444) and the verdict sentence 'the numbers are Lab 3's printed values' is then false.",
    "Print the ≥4 count in Lab 3 (add it to the twin, regenerate with embed_labs.py), or delete the second 794 and state the identity without a number.")
row("SC1-d-r12-exemplarB-numbers-values", "2.2-numbers", "project.html exemplar B (all passages)", F,
    "All other numbers in exemplar B are printed by Lab 1 or Lab 3 or are the difference of printed values (0.016300, 0.043248, 0.048142, 0.026948 ... 0.004361, nested 35/29/27/22/40, 9.13e-15, 1588, 794). Only the 794 (ending at 4 or above) is not printed; see SC1-d-exemplarB-numbers.",
    "See SC1-d-exemplarB-numbers.")
row("SC1-d-r12-annotations-B-accuracy", "2.9-prose (annotation accuracy)", "project.html exemplar B verdict (line 521) and annotations (lines 529-598)", F,
    "The verdict says 'the numbers are Lab 3's printed values with their rounding'. That is false for the walk count 794 at 4 or above (not printed). The other B annotations are accurate: C1 level 4 (A3 tied to rho <= t, lines 595), C2 level 4 (A4(b), (c), (g), (h) named), C5 level 4 (every grid, SE, nested direction), C3 level 3 for the Summary (its values printed; '10 to the minus 14' is a bound of the printed 9.13e-15).",
    "Change the verdict to 'the numbers are printed by Lab 1 and Lab 3, except one count that is derived (see the checks passage)', once the checks passage is fixed as SC1-d-calib-B requires.")
row("SC1-d-r12-exemplarB-brief", "2.9-structure-and-prose (brief conformance of the exemplar that claims to follow it)", "project.html exemplar B (passages Summary, Setup and conventions, The checks, Limitations) and brief lines 436-444", F,
    "Exemplar B says it is 'written to this brief'. Brief item 1 (Summary: 'the one number that shows each holds'): the Summary gives a number for P1 (9.13e-15 closed form vs Simpson) and P2 (0.086497), but for P3 says 'no run checks it', so no number shows P3 holds. Brief item 2 (Setup and conventions: 'the horizon, the level, the grids, the draw order, the rounding rule, and which module function computes each number'): the Setup omits the grids (t_k = kH/n) and the draw order (path by path, step by step from random.Random(seed)). Brief item 3 (The checks: 'the walk identity ... with its printed value'): the identity's second count is unprinted (see SC1-d-exemplarB-numbers). Items fixed since round 12: walk identity stated; rounding rule in Limitations (line 571). Summary is 79 words (<= 80).",
    "(1) Give P3 a printed number, or state the Summary's P3 line as a stated limit of the brief; (2) add the grid definition t_k = kH/n and the draw order to the Setup passage; (3) print the walks-ending-at-4-or-above count (see SC1-d-exemplarB-numbers).")
row("SC1-d-r12-exemplarB-brief-length", "2.9-structure", "project.html exemplar B body (602 words) and Summary (79 words)", P,
    "Body 602 words (tag-stripped count of the five sections, out/exemplar_words_r13.txt; within 400-900), Summary 79 words (within 80).")
row("SC1-d-exemplarB-proof-structure", "2.9-structure", "project.html exemplar B appendix (lines 583-591)", P,
    "Assumption lists are numbered and precede each statement (P1, P2, P3). Matches rubric C1 level 3.")
row("SC1-d-exemplarB-p1-freezing", "2.4-mathematics", "project.html exemplar B P1 (line 585)", P,
    "Freezing step applies A4(b) with Z = (t - rho, 1_K), Y = B-tilde independent of F_rho (A3), f bounded and jointly measurable (A4(g)); f-bar computed; step valid.")
row("SC1-d-r12-lab-numbers", "2.5-labs / 2.2", "tests/labs/SC1; project.html Labs 1-3", P,
    "Every printed number of Labs 1-3 recomputed independently (recompute_r13.txt, 0 FAIL). Lab 2 counts 29, 22, 7 recomputed by DP (not enumeration).")
row("SC1-d-r12-page-vs-twin", "2.5-labs", "project.html Labs 1-3 vs tests/labs/SC1 twins", P, LABS)
row("SC1-d-r12-walk-identity", "2.4-mathematics", "project.html Lab 2 identity; exemplar B checks", P,
    "Walk identity #{max >= a} = #{S_n >= a} + #{S_n >= a+1} holds for n <= 12 and 1 <= a <= n+1 (DP, recompute_r13.txt); 1588 = 794 + 794 holds arithmetically. The printed-value issue is a separate FAIL row (SC1-d-exemplarB-numbers).")
row("SC1-d-r12-hours", "2.6-hours", "project.html table#hours", P, "Same as SC1-d-hours: 28 = 2+3+10+8+3+2; 72 + 28 = 100.")
row("SC1-d-r12-spec-tolerance-and-errors", "2.6-spec", "project.html:235, 238", P, "Same as SC1-d-spec-tolerance-statement and SC1-d-spec-constraints-raise.")
row("SC1-d-spec-tolerance-plan", "2.6-spec", "plans/SC1-build-plan.md §5.5 vs project.html:235", P,
    "Architect deviation carried (not re-litigated): the plan says 1e-12; the page and tests say 1e-10. The page and tests agree with each other.")
row("SC1-d-plan-tolerance", "2.6-spec", "plans/SC1-build-plan.md §5.5 (1e-12) vs project.html:235, test_project.py:187 (1e-10)", P,
    "Carried from round 12 (plans/SC1-build-plan.md byte-identical and project.html:235 unchanged in the round delta): architect deviation kept as PASS, not re-litigated.")
row("SC1-d-r12-reading-and-registry", "2.1-citations", "project.html:619-623; references/references.json", P, VERIFY_LIVE + " Reading line is book level only.")
row("SC1-d-registry", "2.1-citations", "references/references.json (shreve2004stochastic)", P, VERIFY_LIVE)
row("SC1-d-reading-disclosure", "2.1-citations", "project.html reading list (line 622)", P,
    "'at book level, with no passage or theorem number attributed' matches the entry; no theorem or page number attributed.")
row("SC1-d-privacy-claim", "2.9-prose (claims about storage)", "project.html:289 and footer line 637; course/assets/js/store.js", P,
    "'Your code is saved in this browser' and 'kept in this browser's storage': store.js uses indexedDB (grep, this round). Claim matches.")
row("SC1-d-exemplar-naming", "2.6-rubric (plan conformance)", "plans/SC1-build-plan.md §5.4 vs project.html data-level attributes (lines 465, 519)", P,
    "Carried from round 12 (plans/SC1-build-plan.md and the data-level attributes at project.html:465 and :519 unchanged in the round delta): Architect deviation kept as PASS, not re-litigated (plan names exemplar-a data-level 4; the page has A = 2 and B = 4).")
row("SC1-d-dfn-policy", "2.9-DAG", "project.html (no dfn)", P, "No <dfn> on the project page (grep = 0).")
row("SC1-d-exemplar-claims", "2.9-prose", "project.html exemplars and Summary", P,
    "Universal claims in the exemplars checked: 'coarse counts never exceed the fine count' (on the same 256-step paths, recompute_r13.txt nested checks, all True); 'the coarse maximum is at most the fine maximum on every path' (checked on every path); 'every grid' claims in exemplar A flagged (C4 level 2).")
row("SC1-d-r12-interpretation-claim-lab3-grid-direction", "2.9-prose / 2.2", "project.html Lab 3 interpretation; exemplar A Discretization annotation (line 513)", P,
    "Exemplar A's claim 'Finer grids give estimates closer to the continuous tail' is contradicted at seed 0: tail minus estimate is 0.004361 at 256 steps and -0.001799 at 64 steps (recompute_r13.txt). The annotation says so and the lab says one seed cannot order the rows (project.html:430).")
row("SC1-d-ag-docstring", "2.6-autograder", "grader/test_project.py docstring lines 1-21 (except the sentence at lines 14-16)", P,
    "Docstring: 'Several tests check ... against another' (srw identity, one-step vs reflection_tail, nested vs discrete, coarse vs fine: all present); 'One test calls discrete_max_exceedance twice' (test_estimate_is_reproducible); 'One test pins the one-step draws' (test_one_step_draws_are_the_seeded_gaussians); 'never prints the expected value' (expect/within/must_* messages). The count sentence at lines 14-16 is a separate FAIL row.")
row("SC1-d-r10-docstring", "2.6-autograder", "grader/test_project.py docstring", P,
    "Counts of 'two tests regenerate the seeded paths' (test_discrete_estimate_matches_an_explicit_count..., test_nested_counts_match_an_explicit_subsample...) and 'one test calls twice' are correct. The level-on-maximum sentence is a separate FAIL row.")
row("SC1-d-r13-docstring-level-on-max", "2.6-autograder (docstring counts)", "grader/test_project.py:14-16", F,
    "The docstring says 'Two tests put the level exactly on a path's maximum and just above it.' Actual: three tests use a path's maximum: test_path_whose_maximum_equals_the_level_counts_as_reaching_it (line 437, exact), test_nested_counts_include_a_path_whose_maximum_equals_the_level (line 528, exact), and test_path_just_below_the_level_is_not_counted (line 445, just above). So two exact and one just above.",
    "Replace with: 'Two tests put the level exactly on a path's maximum, one for the discrete estimate and one for the nested counts, and one puts it just above.'")
row("SC1-d-r13-comment-both-zero", "2.6-autograder (comment accuracy)", "grader/test_project.py:470-472 (comment in test_draws_depend_on_the_instance_seed)", F,
    "The comment says: 'At the instance's own level the tail is so small for some seeds that no path reaches it, and both estimates are 0.' Checked (out/comment_claims_r13b.txt): seed 32 has zero own-level estimates at grids 16, 32 and 64 (tail 1.4e-3), so 'some seeds' is supported. 'Both estimates are 0' is not: no pair (seed s, seed s+7919) for s in 0..49 has both own-level estimates zero at grids 4, 8, 16, 32 or 64.",
    "Rewrite as: 'At the instance's own level the tail can be so small that no path reaches it (seed 32 at grids 16, 32 and 64), so the estimates are 0 and cannot differ.' Or drop the sentence about both estimates.")
row("SC1-d-ag-draws-depend-overconstraint", "2.6-autograder", "grader/test_project.py:470-478", P,
    "The test (level 1e-9, grids 4..64, changed-seed comparison) passes the reference and all five round-13 alternatives on seeds 0-49. Its logic is not over-constrained.")
row("SC1-d-ag-band-overconstraint", "2.6-autograder", "grader/test_project.py:121-124 (simulation_band) and uses", P,
    "Band = 5 sqrt(p(1-p)/N) + 1/N with the target p, as the page specifies (page 239). Reference and alternatives pass.")
row("SC1-d-ag-walk-listing-stall", "2.6-autograder", "grader/test_project.py:315-336", P,
    "n = 41 test under a 1.0 s trace budget; closed-form DP and binomial alternatives pass it; a listing implementation was not run this round (2**41 walks cannot be enumerated inside the budget).")
row("SC1-d-ag-print-coverage", "2.6-autograder", "grader/test_project.py:584-614", P, "test_no_function_prints_or_warns sweeps boundary inputs; the mutant set includes four leftover-print mutants (r9_01..r9_04), all killed by it.")
row("SC1-d-r10-explicit-tests", "2.6-autograder", "grader/test_project.py:624-665", P,
    "Two explicit-path tests (test_discrete_estimate_matches_an_explicit_count..., test_nested_counts_match_an_explicit_subsample...) regenerate paths by hand and compare exactly. Mutants r12_01 (step-major draw order) and r12_04 (truncated coarse grid) are killed by them.")
row("SC1-d-r10-mutant-folder-hygiene", "2.6-mutation", "ledgers/SC1/mutants/ vs ledgers/SC1/lab-mutants/", P,
    "ls: ledgers/SC1/lab-mutants/ holds SC1a-lab-mut*.py (six files); ledgers/SC1/mutants/ top level holds only grader mutants (73). The gate reads the top level only.")
row("SC1-d-r10-mutant-seed-coverage", "2.6-mutation", "ledgers/SC1/mutants/ on seeds 0-9", P, MUT_ALL)
row("SC1-d-r12-mutants-all-existing", "2.6-mutation", "ledgers/SC1/mutants/*.py (73 files, seeds 0-9)", P,
    MUT_ALL + " All 73 killed; the round-12 survivors r12_05 and r12_06 are killed by the new closed-form tests.")
row("SC1-d-r12-mutants-new-r12-01-04", "2.6-mutation", "ledgers/SC1/mutants/r12_01..r12_04", P,
    "Killed on seeds 0-9: " + mut_list(["r12_01_", "r12_02_", "r12_03_", "r12_04_"]))
row("SC1-d-r12-mutant-tiny-level", "2.6-mutation", "course/modules/SC/SC1/grader/test_project.py:251-259; ledgers/SC1/mutants/r12_05_tiny_level_guard_returns_one.py", P,
    "Round-12 FAIL closed. New test_reflection_tail_small_levels_match_the_closed_form (1e-10, a in 1e-7..1e-3, t in {H, 2}) kills r12_05 on seed 0: " + killers["r12_05_tiny_level_guard_returns_one.py"])
row("SC1-d-r12-mutant-tiny-time", "2.6-mutation", "course/modules/SC/SC1/grader/test_project.py:262-269; ledgers/SC1/mutants/r12_06_tiny_time_guard_returns_zero.py", P,
    "Round-12 FAIL closed. New test_reflection_tail_small_times_match_the_closed_form kills r12_06 on seed 0: " + killers["r12_06_tiny_time_guard_returns_zero.py"])
row("SC1-d-r7-alt4-ruling10", "2.6-mutation (architect ruling)", "plans/SC1-build-plan.md §5.7(4); ledgers/SC1/mutants/r12_01_step_major_draw_order.py", P,
    "Carried from round 12 (plans/SC1-build-plan.md unchanged; Ruling 10 treats the draw-order alternative as a mutant): r12_01 is killed on seed 0 this round (" + killers["r12_01_step_major_draw_order.py"] + ").")

# ---- new round-13 mutants (own student errors) ----------------------------------------------------------------------
row("SC1-d-r13-mutants-new", "2.6-mutation", "ledgers/SC1/mutants/r13_01..r13_05", P,
    "Five new student-error mutants, each a single-change copy of the reference (ledgers/SC1/scripts/SC1-d-r13/make_mutants_r13.py): " + mut_list(["r13_0"]))

# ---- round-13 structure rows: the grader's failure messages and the tiny-level tests -------------------------------
row("SC1-d-r13-tests-added", "2.6-autograder", "grader/test_project.py:251-269 (two added tests)", P,
    "The two added tests use the closed form erfc(a/sqrt(2t)) at 1e-10 over fixed grids; they name the property in their messages and never print the value. Reference and every runnable alternative (the five round-13 and the prior correct set) pass them on seeds 0-49.")


# ---- rows for round-12 ids not otherwise re-stated ---------------------------------------------------------------------
def alt_line(text: str, name: str) -> str:
    for ln in text.splitlines():
        if ln.startswith(name + ":") or ln.startswith(name.split("/")[-1] + ":") or (ln.split(":")[0].endswith(name)):
            return ln
    return "no line"


row("SC1-d-r7-page-vs-twin", "2.5-labs", "project.html Labs 1-3 vs tests/labs/SC1 twins", P, LABS)
row("SC1-d-r7-registry-live", "2.1-citations", "references/references.json (shreve2004stochastic)", P, VERIFY_LIVE)
row("SC1-d-r8-proofs-trace", "2.4-mathematics", "project.html P1-P3 statements and exemplar B proof", P,
    "Proof trace re-done this round line by line (exemplar B appendix, lines 585-591, and statements, 243-263); each step names its assumption; the proof of P1 uses A3 for the bounded time rho = tau wedge t and A4(b), (c), (g), (h) as listed.")
row("SC1-d-delta-r5-read", "process", "project.html; grader/test_project.py; tests/labs/SC1/lab-SC1-project-1.py", P,
    "Delta 5db69a9..e919577 for these files read hunk by hunk this round (git diff): project.html (lines 7, 58-68, 223-226, 234, 297, 462-584 hunks), test_project.py (+21 lines, 251-269), lab twin 1 (docstring only). Whole page and grader read in full.")
row("SC1-d-delta-r6-read", "process", "project.html; grader/test_project.py; tests/labs/SC1", P,
    "Same as SC1-d-delta-r5-read; in addition the twin output was re-run and compared with the expected blocks (run_labs, twin_project_*.stdout).")
row("SC1-d-r10-alternatives", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r10/alternatives/ (alt_r10_a, b, c, e correct; alt_r10_d step-major intentional)", P,
    "Re-run on the round-13 suite: " + "; ".join(alt_line(alt_prior, n).split(" on ")[0] for n in ["SC1-d-r10/alt_r10_a_normaldist_tail.py", "SC1-d-r10/alt_r10_b_quadrature_tail.py", "SC1-d-r10/alt_r10_c_dp_walk_counts.py", "SC1-d-r10/alt_r10_e_index_subsample.py"]) + " (out/prior_correct_alternatives_r13.txt). alt_r10_d (step-major) is an intentional draw-order mutant, excluded.")
row("SC1-d-r10-prior-alternatives", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r10/ (prior-round alternatives)", P,
    "Same run as SC1-d-r10-alternatives (out/prior_correct_alternatives_r13.txt): the four correct round-10 alternatives pass 50/50 on the round-13 suite; step-major alt_r10_d is an intentional mutant and is not in the correct set.")
row("SC1-d-r8-alternatives", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r8/alternatives/ (a, b, c, d; e step-major intentional)",
    F,
    "alt_r8_a: " + alt_line(alt_prior, "SC1-d-r8/alt_r8_a_normaldist_tail.py").split(" on ")[0] + "; alt_r8_d: " + alt_line(alt_prior, "SC1-d-r8/alt_r8_d_streaming.py").split(" on ")[0] + "; alt_r8_b and alt_r8_c: " + alt_line(alt_prior, "SC1-d-r8/alt_r8_b_quadrature_tail.py").split(" on ")[0] + " / " + alt_line(alt_prior, "SC1-d-r8/alt_r8_c_dp_srw.py").split(" on ")[0] + ", 1 error at import (stale reference path, out/prior_correct_alternatives_r13.txt). Repeated with the repathed copies in SC1-d-r9: " + "; ".join(ln.strip() for ln in (OUT / "repathed_alternatives_r13.txt").read_text(encoding="utf-8").splitlines() if "FAIL" in ln or "PASS" in ln) + ".",
    PRIOR_FIX)
row("SC1-d-r8-alternatives-b-c-repath", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r9/alternatives_r8_repathed/ (alt_r8_b, alt_r8_c)", F,
    "The 'repathed' copies still load reference.py from /Users/billyribeiro/.fanout/wt/verifyE9-SC1-d (deleted): 0/50 seeds, import error (out/repathed_alternatives_r13.txt). The round-12 note 'PASS (repathed)' is not reproducible on this checkout.",
    PRIOR_FIX)

NOTES = (
    "Round 13 on e919577 (round-12 pin 5db69a9). Delta read in full for this slice: project.html (lines 7, 58-68, 223-226, 234-235, 297, 462-584), "
    "grader/test_project.py (+21 lines: two closed-form tests at 251-269), tests/labs/SC1/lab-SC1-project-1.py (docstring only). "
    "reference.py, starter.py, instance.py, lab twins 2 and 3, references.json and notation.json are byte-identical to 5db69a9. "
    "Every gate was re-run on this checkout, not carried. Blind exemplar scoring: the annotated page was read in full before the blind text "
    "was extracted (out/blind_exemplars_r13.txt, which strips annotations, the verdict paragraphs and data attributes), so the blind scores "
    "are disclosed as not fully independent; C1, C2, C4, C5 of exemplar B and all of exemplar A were scored from the rubric text and passages. "
    "Rubric exclusivity is the verifier's reading of the level cells. Architect deviations (tolerance 1e-10 vs plan 1e-12; exemplar data-level "
    "attributes; plan 5.7(4) draw-order alternative treated as a mutant, Ruling 10) are carried as PASS rows, not re-litigated. "
    "Mutants: the 73 .py files in ledgers/SC1/mutants/ are all killed on seeds 0-9 (round-12 survivors r12_05, r12_06 now killed). "
    "New mutants r13_01..r13_05 (ledgers/SC1/scripts/SC1-d-r13/make_mutants_r13.py) are student errors: an erfc approximation at 1.5e-7, "
    "a per-seed generator cache, a three-path minimum, the increment variance ignoring the grid size, and a float-typed count; all killed. "
    "Alternatives: five round-13 correct alternatives pass 0-49 (alt_r13_1..5); the round-12 five pass 0-49 on the round-13 suite; the 20 prior "
    "correct alternatives were re-run on the round-13 suite (out/prior_correct_alternatives_r13.txt), 18 PASS and alt_r8_b and alt_r8_c FAIL "
    "to import (stale absolute reference paths in old checkouts, see SC1-d-r8-alternatives-b-c-repath). "
    "Could not check: (1) live verify_refs for the full registry (only the SC1 unit live; the full run is CI's); (2) the in-browser "
    "self-assessment reveal and the form (JavaScript UI not clicked; page_smoke runs the grader panel only); (3) the 50-seed sweep of "
    "the 73 mutants (the gate is seeds 0-9 as specified); (4) the 500-seed reference sweep was not repeated (seeds 0-199 PASS); "
    "(5) a live walk-enumeration timing check for n = 41 (cannot enumerate 2**41 walks; the budget test is the check); (6) rung-2 "
    "placement behaviour on the hub. Exemplar B's Setup, Summary and checks passages are judged against brief lines 436-444 as written."
)
SUMMARY = (
    "SC1 slice d round 13 on e919577: verdict FAIL. Rows 169: PASS 156, FAIL 13, UNVERIFIABLE 0. Mutants 73/73 killed on seeds 0-9 "
    "(five new round-13 mutants all killed). Round-12 FAILs closed: pathwise define-before-use (L01 no longer uses it), the r12_05 and r12_06 "
    "survivors (killed by the two added closed-form tests), exemplar A's C3 annotation, the mutate gate. Still FAIL: exemplar B quotes a "
    "walk count (794 at 4 or above) that Lab 3 does not print (blind C3 2 vs official 4; brief item 3), exemplar B's Setup lacks the grids "
    "and the draw order (brief item 2), P3 has no number in the Summary (brief item 1), the rubric's level cells overlap (C1, C3, C4), two "
    "grader comments/docstrings misstate counts or outcomes, and two old alternatives (alt_r8_b, alt_r8_c and their copies) cannot run on "
    "this checkout."
)

# ---- assemble ----------------------------------------------------------------------------------------------------------
PREV = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-SC1-d.round12.json").read_text(encoding="utf-8"))
prev_ids = [r["id"] for r in PREV["rows"]]
ids = [r["id"] for r in rows]
dupes = sorted({i for i in ids if ids.count(i) > 1})
missing = [i for i in prev_ids if i not in ids]
print("rows:", len(rows), "duplicates:", dupes, "round-12 ids missing:", len(missing))
print("missing:", missing)
assert not dupes

mutants = []
for name in sorted(killers):
    mutants.append({"name": name, "description": "", "killed_by": killers[name]})

# the mutant descriptions come from each file's first docstring line
import ast  # noqa: E402

for m in mutants:
    src = (ROOT / "ledgers/SC1/mutants" / m["name"]).read_text(encoding="utf-8")
    m["description"] = (ast.get_docstring(ast.parse(src)) or "(no description)").splitlines()[0]

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) and all(m["killed_by"] != "SURVIVED" for m in mutants) else "FAIL"
fragment = {
    "unit": "SC1",
    "slice": "d",
    "round": 13,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-d, round 13 (did not build SC1; read the whole project page, the grader, the labs, the round-12 fragment and the delta e919577 vs 5db69a9)",
    "pin": "e919577b45b431ce68e1e6533b00b8a301277937",
    "base": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0 (round-12 pin)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE13-SC1-d",
    "scratch": "/tmp/sc1d-r13/ (scratch workspace for collect-only and the seed-0 run); durable scripts and outputs under ledgers/SC1/scripts/SC1-d-r13/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": NOTES,
    "summary": SUMMARY,
}
dest = ROOT / "ledgers/SC1/SC1-d.json"
dest.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
problems = ledger.validate(fragment, "SC1-d")
print("validate:", problems)
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
print("counts:", counts, "mutants:", sum(1 for m in mutants if m["killed_by"] != "SURVIVED"), "/", len(mutants))
print("verdict:", verdict)
