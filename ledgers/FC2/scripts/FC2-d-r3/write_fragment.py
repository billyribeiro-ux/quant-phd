"""Round-3 verifier fragment for FC2-d (project.html rubric, grader, project labs, cards.json, project mutants)."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(sys.argv[1])
S = "ledgers/FC2/scripts/FC2-d-r3/"
M = "course/modules/FC/FC2/"
G = M + "grader/"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        assert fix, rid
        r["fix"] = fix
    rows.append(r)


# ---- gates and commands (run by this verifier on pin ccfdf4c)
row("fc2d-gate-check-projects", "2.6-gate", "tools/check_projects.py --unit FC2", "PASS",
    "Observed: 'check_projects FC2: PASS'; --all shows PASS for every unit (no non-PASS line).")
row("fc2d-gate-check-pages", "2.9-gate", "tools/check_pages.py --unit FC2", "PASS",
    "Observed: 'check_pages FC2: PASS'.")
row("fc2d-gate-check-dag", "2.9-DAG", "tools/check_dag.py --unit FC2", "PASS",
    "Observed: 'check_dag FC2: PASS'. Concept links on project.html (arbitrage-opportunity, put-call-parity, "
    "option-arbitrage-bounds) are all introduced by FC2 lessons L01/L05 (project.html lede and conventions).")
row("fc2d-gate-run-labs", "2.5-labs", "tests/labs/FC2/lab-FC2-project-{1,2,3}.py", "PASS",
    "Observed: 'run_labs FC2: PASS (11/11)'. Each project twin exits 0 under python -I -W error with empty stderr "
    "(" + S + "check_labs.py).")
row("fc2d-gate-page-smoke", "2.9-page_smoke", "project.html via tools/page_smoke.py --unit FC2", "PASS",
    "Observed: 'page_smoke modules/FC/FC2/project.html: PASS'; in-browser grader line 'All 84 tests pass on seed "
    "917703293. (0.8 s)'; 'page_smoke FC2: PASS'.")
row("fc2d-gate-run-graders", "2.6-autograder-1", "grader/reference.py, tools/run_graders.py --unit FC2 --seeds 0-49",
    "PASS", "Observed: 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.2 s)'. Independently: "
    + S + "run_suite.sh reference.py 0-49 gives '84 passed' on every seed 0 to 49 (0 lines differ).")
row("fc2d-gate-ruff-mypy", "2.6-gate", "repository", "PASS",
    "Observed: 'ruff check .' -> 'All checks passed!'; 'ruff format --check .' -> '340 files already formatted'; "
    "'mypy --no-incremental' -> 'Success: no issues found in 229 source files'.")
row("fc2d-gate-pytest", "2.5-pytest", "tests/test_labs.py, tests/test_page_checks.py, tests/test_memo_exemplars.py",
    "PASS", "Observed: 3 files, 'pytest -q' all dots, exit 0 (no failures). Note: test_memo_exemplars.py pins only "
    "S7 exemplars; no automated test pins FC2's exemplar numbers (see fc2d-exemplar-numbers).")
row("fc2d-gate-verify-refs", "2.1-citations", "tools/verify_refs.py --unit FC2 (live)", "PASS",
    "Observed: 'live re-verification of FC2: 3 of 560 entries, 0 problems', exit 0 (keys hull2021options, "
    "stoll1969relationship, cox1979option cited in project.html reading list).")
row("fc2d-collect-count", "2.6-autograder", "grader/test_project.py vs project.html 'collects 84 checks'", "PASS",
    "Observed: 'pytest --collect-only' on reference.py -> '84 tests collected'; project.html Grading paragraph says 84.")
row("fc2d-seeds-84", "2.6-autograder-1", "grader/test_project.py on reference.py, seeds 0-49", "PASS",
    "Observed: run_suite.sh reference.py 0-49 -> 50 lines, each '84 passed'.")
row("fc2d-starter-fails", "2.6-autograder", "grader/starter.py", "PASS",
    "Observed: QF_SEED=0 pytest on starter.py -> '75 failed, 9 passed'. The suite fails on the starter as the "
    "spec states; the 9 passing checks are structural (function presence, stdlib-only imports, purity, instance label).")
row("fc2d-alternatives", "2.6-autograder-5", "ledgers/FC2/scripts/FC2-d-r3/alts/alt1..alt5 (five correct implementations)",
    "PASS", "Each of the five alternatives passes 84/84 on every seed 0-49 (run_suite.sh; 0 non-84 lines). alt1 Fraction "
    "independent, alt2 integer-only with half-up helper, alt3 float with half-up on float result, alt4 adjacent-slope "
    "convexity (valid on unequal grid, test_unequal_grid_violation_is_found passes), alt5 parity via forward S/df. "
    "Early versions of alt1-alt5 failed one test each because of my own sign and rounding slips; they were corrected "
    "to the spec (gross is half-up in magnitude of the exact gap), not the suite changed.")

# ---- mutants (verifier's own student-error mutants plus the builder's)
row("fc2d-mutate-builder", "2.6-mutation", "ledgers/FC2/mutants/m01..m46 (30 builder mutants)", "PASS",
    "Observed: 'python tools/mutate_graders.py --unit FC2 --seeds 0-9' -> every builder mutant KILLED (30/30); "
    "the tool's run on all 36 files shows 35/36 killed, the sole survivor is v02 below.")
row("fc2d-mut-v03", "2.6-mutation", "ledgers/FC2/mutants/v03_parity_gross_bankers_round.py", "PASS",
    "Parity gross via Python round() (half-even). KILLED by test_half_cent_gross_rounds_once_up (seed 0).")
row("fc2d-mut-v04", "2.6-mutation", "ledgers/FC2/mutants/v04_convexity_returns_one_based_index.py", "PASS",
    "Convexity indices one-based. KILLED by test_unequal_grid_violation_is_found (seed 0).")
row("fc2d-mut-v05", "2.6-mutation", "ledgers/FC2/mutants/v05_convexity_findings_before_parity.py", "PASS",
    "Convexity records before parity. KILLED by test_findings_are_in_parity_then_convexity_order (seed 0).")
row("fc2d-mut-v06", "2.6-mutation", "ledgers/FC2/mutants/v06_gross_rounds_signed_gap_then_abs.py", "PASS",
    "Gross = abs(half-up of signed gap), which breaks half-up-in-magnitude. KILLED by "
    "test_negative_half_cent_gross_rounds_once_up_in_magnitude (seed 0).")
row("fc2d-mut-v01-boundary", "2.6-mutation", G + "test_project.py (convexity net-of-cost boundary)", "FAIL",
    "Mutant v01 (convexity kept when net == 0, i.e. '>= 0' for convexity only) passes seed 0 entirely. It is killed "
    "only on seed 1 (mutate_graders.py output 'KILLED ... (seed 1)') by the random oracle test "
    "test_scan_matches_exhaustive_oracle_second_chain. No hand-built convexity case has gross == fee + spread: the "
    "only net-zero boundary tests are parity (test_finding_with_net_exactly_zero_is_not_returned line 651, "
    "test_negative_parity_gap_is_reported_with_positive_gross line 664). project.html Constraints says a finding is "
    "kept only if net is strictly greater than zero, and Grading says the suite checks 'the net-of-cost rule at its "
    "boundary in both directions'.",
    "Add a hand-built convexity test to test_project.py: a chain whose one convexity violation has gross == fee + "
    "half-spread times 3 (e.g. the chord less call of -45 cents with fee 10 and half-spread 5), asserting scan returns "
    "no convexity record; add the kept-at-net-1 counterpart.")
row("fc2d-mut-v02-labels", "2.6-mutation", G + "test_project.py line 584 (ASSUMPTION_LABEL = 'P1')", "FAIL",
    "Mutant v02 (parity explanation names only P1, omitting P2, P3, P4 and P6) SURVIVES seeds 0-9 (mutate output "
    "'SURVIVED v02_parity_explanation_names_P1_only.py: ... -> None'). project.html Required outputs: the explanation "
    "'names the rule and the assumptions the finding depends on, by the labels in the conventions'; Conventions P4 says "
    "'The parity gap uses it', and P6 says a parity finding trades the call, put and underlying at 3 x (fee + "
    "half-spread). test_scan_explanations_are_nonempty_and_name_the_rule only asserts 'P1' in text.",
    "Replace the single-label check with per-kind label sets: parity explanations must contain P1, P2, P4 and P6; "
    "convexity explanations must contain P1, P2, P5 and P6 (the labels the rubric C4 and the reference use).")

# ---- grader
row("fc2d-grader-stdlib", "2.6-autograder", G + "instance.py, reference.py, test_project.py", "PASS",
    "Only math, random, fractions, typing, itertools, ast, copy, os, sys, pathlib, pytest imported; "
    "test_module_imports_standard_library_only enforces it for scanner.py.")
row("fc2d-grader-messages", "2.6-autograder-4", G + "test_project.py (assert messages)", "PASS",
    "Read every assert message (lines 136-759). They name the property (e.g. 'the parity gap must be the exact "
    "C - P - (S - K df), rounded once'); none prints an expected value. ValueError matches name the condition "
    "(strictly increasing, df_ppm, non-negative, the two lengths).")
row("fc2d-grader-instance-validity", "2.8-instances / 2.6-autograder-2", G + "instance.py lines 60-72", "FAIL",
    "Generated 'clean' and planted chains break L05 Theorem 2.2 (course/modules/FC/FC2/L05.html: 0 <= P, "
    "C >= max(S - DK, 0)). Over seeds 0-49 (" + S + "bounds_check.py): clean ('none') chains 6 of 20 violate a bound; "
    "examples seed 9: K=2500 put -3462 (P < 0) and call 2805 < S - DK = 6343; seed 10: K=10000 put -1154; seed 17: "
    "K=7500 put -1057; seed 21: K=7500 put -2230; seed 43: K=5000 put -1357; seed 48: K=2500 put -3173. In all 50 "
    "seeds, 11 chains have a negative put quote (" + S + "instance_diversity.py). Project Inputs call the quotes "
    "'mid prices', and the instance docstring says every chain is valid under the contract. Honest-data rule: a "
    "SIMULATED chain must not contain quotes that the lessons define as model-free violations.",
    "In instance._draw reject a draw when any put < 0, any call < max(S - K df, 0), any put > K df, or any put < "
    "max(K df - S, 0), allowing the half-cent rounding slack; then add a test asserting each generated chain satisfies "
    "Theorem 2.2 for seeds 0-49. Seeds change, so the planted-amount tests will still hold by construction.")
row("fc2d-grader-instance-diversity", "2.8-instances", G + "instance.py", "PASS",
    "Seeds 0-49: 50 distinct chains; planted kinds none 20, convexity 16, parity 14; 26 distinct non-empty findings "
    "lists; findings counts 0 (24 seeds) or 1 (26 seeds); clean instances give 0 findings "
    "(" + S + "instance_diversity.py). Answers change with the seed, not only the labels.")
row("fc2d-lab1", "2.5-labs", M + "project.html lab-FC2-project-1", "PASS",
    "Expected block equals twin stdout (check_labs.py: 'expected == stdout: True'). Hypothesis prediction (two kept) "
    "matches the output. Numbers recomputed in " + S + "prose_numbers.py: parity gap 120 at 9500, -20 at 11000, "
    "chord-call 50/100/-75/75; gross 75 net 30 at 10500; cost 45.")
row("fc2d-lab2", "2.5-labs", M + "project.html lab-FC2-project-2", "PASS",
    "Three blanks (gap, net, net). Page code equals the twin except the three blank lines (diff_labs.py); completion "
    "rule holds (0 non-blank differing lines). Expected output equals twin stdout. Interpretation numbers (120, 30) "
    "match the output.")
row("fc2d-lab3", "2.5-labs", M + "project.html lab-FC2-project-3", "PASS",
    "Expected equals stdout. Recomputed (prose_numbers.py): gap -60 at 4500 (gross 60 = cost, net 0, dropped), 226 at "
    "6500, 540 at 7000; chord-call 35, 470/3, -188/3 (gross 63, net 3), 59. Hypothesis and interpretation match.")
row("fc2d-lab-twins-pure", "2.5-labs", "tests/labs/FC2/lab-FC2-project-{1,2,3}.py", "PASS",
    "No random, network, file or __name__ guard; each ends with an unconditional main() call; run under "
    "python -I -W error exit 0.")
row("fc2d-rubric-observable", "2.6-rubric-1", M + "project.html rubric table (C1 to C5, levels 1 to 4)", "PASS",
    "Each level descriptor was read. Each names something a grader can see (strike, cents, legs, labels P1 to P6, "
    "a named check, a named direction). None is vague by the rule's standard.")
row("fc2d-rubric-calib-A", "2.6-rubric-2", M + "project.html article#exemplar-a (data-scores 2,1,1,2,1)", "PASS",
    "Blind scoring of Exemplar A by the rubric alone: C1 2 (amounts 'about', no legs), C2 1 (no cost model), C3 1 or 2 "
    "(discount factor named for parity, no label), C4 2, C5 1. Each within one level of the official scores.")
row("fc2d-rubric-calib-B", "2.6-rubric-2", M + "project.html article#exemplar-b, C2 (data-scores 4,4,3,3,3)", "FAIL",
    "Blind scoring of Exemplar B C2: the level-3 descriptor requires 'three legs at fee plus half-spread'. The passage "
    "text states only 'a cost of 60 cents per finding' (the fee of 8 is never stated in the passage). The annotation "
    "'the cost of 60 cents comes from three legs at 8 plus 12' describes content that is not in the passage. Level 4's "
    "'gap between the net and zero' is not stated either. Blind C2 = 2, official = 4: a two-level gap.",
    "Add to the Summary or the Findings passage the sentence 'Each finding trades three legs, each paying a fee of 8 and "
    "a half-spread of 12 cents, so 3 x (8 + 12) = 60 cents, and the net is the gross less 60', or lower the official C2 "
    "score to 2 and remove the annotation's 'three legs at 8 plus 12' claim.")
row("fc2d-exemplar-numbers", "2.2-numbers", M + "project.html exemplar-a and exemplar-b passages", "PASS",
    "Every number in the exemplars recomputed in prose_numbers.py: 6175 and 6650 (6500 and 7000 times 0.95), gaps 226 "
    "and 540, nets 166 and 480, chord 802/3, chord-call -188/3, gross 63, net 3, cost 60. Exemplar A's 'about 226/540/63' "
    "are the same values, stated approximately as a level-2 example.")
row("fc2d-exemplar-annotations", "2.6-rubric-2", M + "project.html annotations", "PASS",
    "All other annotations (B: C1 4, C3 3, C4 3, C5 3; A: C1 2, C2 1, C4 2, C5 1) are consistent with the passage text. "
    "Only the B C2 annotation fails (row fc2d-rubric-calib-B).")
row("fc2d-spec-explanation-labels", "2.6-spec", M + "project.html 'Required outputs' bullet 3", "FAIL",
    "The spec requires explanations to name 'the assumptions the finding depends on, by the labels in the conventions' "
    "but never says which labels each kind depends on; a competent student would have to ask. The conventions say P4 is "
    "used by the parity gap and P6 by every cost. The test only checks 'P1' (see fc2d-mut-v02-labels).",
    "State in the spec: parity findings name P1, P2, P4 and P6; convexity findings name P1, P2, P5 and P6.")
row("fc2d-spec-errors-scope", "2.6-spec", M + "project.html 'Constraints' exception list", "PASS",
    "The exception table says 'Invalid input raises the exception types'; the tests require df and strike errors from "
    "parity_gap_cents and convexity_violations as well as scan. This reading is the natural one; noted, not a finding.")
row("fc2d-hours", "2.6-hours", M + "project.html #hours table", "PASS",
    "Rows sum to 30 (2+3+5+9+3+5+3). Verifier estimate (judgment): rung 1 1.5 h, rung 2 1 h, derivations 3 h, "
    "scanner.py 4 h, edge cases 2 h, note 4 h, self-assessment 2 h = 17.5 to 22 h; central 22 h is 27 percent below "
    "30 and inside the 30 percent band (21 to 39 h). Margin is thin: the lower bound sits outside the band. Judgment.")
row("fc2d-cards-sample", "2.7-cards-sample", M + "cards.json (sampled every 10th card: c001, c011, c021, c032, "
    "c042, c052, c062, c072, c082, c092, c102, c112, c122)", "PASS",
    "Each sampled card read against its lesson: c001 and c011 vs L01 Definition 1.1; c021 vs L02 Example 2.4 and "
    "'Lab 2, Part A prints 5126.58' (50 e^0.025 = 51.2658); c042 vs L03 Proposition 3.3 (R_par formula); c052 vs L04 "
    "Lemma 1.2 and Remark 1.3; c062 vs L04 Example 2.5 and Remark 2.6; c072 vs L05 Lab 1 printout (zero parity cost "
    "at five strikes, 0 of 40 nonzero payoffs); c082 vs L06 A6; c092 vs L06 Definition 3.2 (V(n,k) recursion); "
    "c102 vs L07 Definition 1.3 and Section 4 ('not derived'); c112 algebra checked (d1 split is correct); c122 vs L08 "
    "Theorem 2.3.")
row("fc2d-cards-dups", "2.7-cards-duplicates", M + "cards.json (all 130 cards)", "PASS",
    "Full scan (" + S + "cards_check.py): 130 cards; no duplicate ids, no duplicate fronts, no duplicate backs; schema "
    "keys consistent (grade on 103, basis on 47).")
row("fc2d-cards-numbers", "2.7-cards-numbers", M + "cards.json (all cards vs lesson text)", "PASS",
    "Automated (cards_check.py): every number in every card's front and back appears in that card's lesson HTML text; "
    "every card's lesson label exists. Card labels cited (Definition 1.1, Example 2.4, Corollary 3.2, Proposition 3.3, "
    "Lemma 1.2, Remark 1.3, Remark 2.6, Example 2.5, Definition 1.2, Definition 3.1, 3.2, Definition 1.3, Proposition "
    "1.5, Theorem 2.3) were grep-confirmed in their lessons.")
row("fc2d-cards-grades", "2.7-cards-grade", M + "cards.json grade and basis fields", "PASS",
    "Grades: T 93, C 10, none 27. The one C-graded card read (c072) has a basis naming Lab 1 (SIMULATED price set). "
    "Lab-derived T cards (c021) name their lab in basis.")
row("fc2d-reading-theorem-locator", "2.1-attribution", M + "project.html #reading paragraph", "FAIL",
    "project.html says 'The parity relation and convexity in strike (Theorem 3.2 of Lesson 5) are proved in Lesson 5'. "
    "In L05 the parity relation is Theorem 1.2 (put-call parity, L05.html line ~63 of the text dump); Theorem 3.2 is "
    "convexity in strike only.",
    "Change to 'The parity relation (Theorem 1.2) and convexity in strike (Theorem 3.2) of Lesson 5 are proved there'.")
row("fc2d-references-no-locator", "2.1-attribution", M + "project.html #reading and data-cite items", "PASS",
    "The reading list says no chapter, page or equation is assigned; no locator or edition appears in project.html "
    "(grep for '11th', 'JF 24', 'JFE 7' returns 0).")
row("fc2d-notation", "2.4-notation", M + "project.html (all symbols)", "PASS",
    "grep for registered symbols (\\Phi, \\gamma, R^\\ast, \\tau, \\sigma, bare T) in project.html returns no hits; "
    "the project uses only C, P, S, K, df, r and the Lab variables, consistent with the plan's local letters.")
row("fc2d-simulated-label", "2.8-SIMULATED", M + "project.html, labs, instance.py", "PASS",
    "Every chain on the page and the grader instance carries SIMULATED (instance label; test_instance_is_labelled_simulated). "
    "No market data is embedded (architect default; plan section 7 B1).")
row("fc2d-process-banned", "2.9-prose", M + "project.html", "PASS",
    "grep for TODO, TBD, lorem, beyond the scope, for brevity, important to note, studies show, clearly, obviously, "
    "roughly, builder, verifier, planner, architect, agent: no hits. 'about 226' appears only inside Exemplar A (a "
    "deliberate level-2 example).")
row("fc2d-ladder-claims", "2.6-ladder", M + "project.html #ladder and rung text", "PASS",
    "Rung 1 fully solved (Lab 1), Rung 2 graded by its expected output (three blanks), Rung 3 is the scanner plus "
    "findings note, Rung 4 is open. Hub placement claim matches index.html lines 68 and 148.")
row("fc2d-curriculum-scope", "2.6-scope", "curriculum/02-economics-finance-core.yaml:425-431 vs project.html", "PASS",
    "Curriculum brief: detect parity and convexity violations net of a stated cost model, and explain each. The page "
    "covers exactly these. The embedded-snapshot wording is replaced by SIMULATED (architect default, plan section 7 B1); "
    "the substitution is disclosed on the page.")
row("fc2d-no-external", "2.9-page_smoke", M + "project.html and grader.js", "PASS",
    "No http(s) URL in project.html outside site-relative links; page_smoke reports no external requests (PASS). The "
    "only file read is the grader's own input element (course/assets/js/grader.js line 46, accept='.py').")

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
mutants = [
    {"id": "v01_convexity_zero_net_kept", "description": "Convexity finding kept at net exactly zero (>= 0 for convexity only)",
     "file": "ledgers/FC2/mutants/v01_convexity_zero_net_kept.py",
     "killed_by": "test_scan_matches_exhaustive_oracle_second_chain (seed 1 only; survives seed 0)"},
    {"id": "v02_parity_explanation_names_P1_only", "description": "Parity explanation names only P1",
     "file": "ledgers/FC2/mutants/v02_parity_explanation_names_P1_only.py", "killed_by": None},
    {"id": "v03_parity_gross_bankers_round", "description": "Parity gross via Python round() (half-even)",
     "file": "ledgers/FC2/mutants/v03_parity_gross_bankers_round.py",
     "killed_by": "test_half_cent_gross_rounds_once_up (seed 0)"},
    {"id": "v04_convexity_returns_one_based_index", "description": "Convexity indices returned one-based",
     "file": "ledgers/FC2/mutants/v04_convexity_returns_one_based_index.py",
     "killed_by": "test_unequal_grid_violation_is_found (seed 0)"},
    {"id": "v05_convexity_findings_before_parity", "description": "Convexity records before parity records",
     "file": "ledgers/FC2/mutants/v05_convexity_findings_before_parity.py",
     "killed_by": "test_findings_are_in_parity_then_convexity_order (seed 0)"},
    {"id": "v06_gross_rounds_signed_gap_then_abs", "description": "Gross = abs(half-up of signed gap)",
     "file": "ledgers/FC2/mutants/v06_gross_rounds_signed_gap_then_abs.py",
     "killed_by": "test_negative_half_cent_gross_rounds_once_up_in_magnitude (seed 0)"},
]
frag = {
    "unit": "FC2",
    "slice": "FC2-d",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 3 (did not build FC2)",
    "pin": "ccfdf4c",
    "base": "no round-2 fragment exists at /Users/billyribeiro/.fanout/frags/C-FC2-d.round2.json; the whole slice was re-verified, no PASS row was carried",
    "checkout": str(ROOT),
    "scratch": "/tmp/fc2d-r3.* (suite copies, removed after each run)",
    "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Read in full: project.html (672 lines), grader/instance.py, reference.py, starter.py, test_project.py (759 lines), "
        "cards.json (130 cards; full scan plus 13 sampled cards read against lessons), the three project lab twins. "
        "Commands run on the pin: check_projects, check_pages, check_dag, run_graders 0-49, run_labs, page_smoke, mutate_graders "
        "0-9 (36 mutants), verify_refs live, ruff, ruff format, mypy --no-incremental, pytest on the three lab/page test files. "
        "Five alternatives and six new mutants written and run; scripts under ledgers/FC2/scripts/FC2-d-r3/. "
        "Not checked: the full pytest suite (not in slice); render_curriculum/build_site --check (no input in slice changed "
        "by this verifier, the gate of other slices); the 19 cards not sampled were not read individually (automated full scans "
        "only); FC2 exemplar numbers are not pinned by any automated test; the explanation text's trade direction is not "
        "tested (noted, not a finding because the spec does not state the direction must appear in the explanation); "
        "the in-browser Pyodide run was taken from page_smoke's output rather than a manual browser session."
    ),
    "summary": (
        "FC2-d round 3: verdict FAIL. " + str(len(rows)) + " rows: " + str(sum(r["status"] == "PASS" for r in rows)) +
        " PASS, " + str(sum(r["status"] == "FAIL" for r in rows)) + " FAIL, 0 UNVERIFIABLE. Mutants: 6 new (5 of 6 killed; "
        "v02 survives; v01 killed only on seed 1). Principal FAILs: negative and below-bound quotes in generated 'clean' "
        "chains (instance.py), missing convexity net-zero boundary test, explanation-label test checks only P1, "
        "Exemplar B C2 calibration, and a wrong theorem locator for parity (Theorem 1.2, not 3.2)."
    ),
}
out = ROOT / "ledgers/FC2/FC2-d.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, verdict, len(rows))
