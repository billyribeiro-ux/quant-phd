"""Round-4 verifier fragment for FC2-d (pin b276325). Rows keep every round-3 id."""
import json
import pathlib
import re

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyC4-FC2-d")
S = "ledgers/FC2/scripts/FC2-d-r4/"
C = "Carried from round 3 (course/modules/FC/FC2/project.html byte-identical in this range since ccfdf4c; git diff ccfdf4c b276325 hunks are at lines 34, 52, 160, 279-323, 482, 522-531, 654 only):"

def row(i, check, loc, status, ev, fix=None):
    r = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if fix:
        r["fix"] = fix
    return r

rows = [
 row("fc2d-gate-check-projects", "2.6-gate", "tools/check_projects.py --all", "PASS", "Observed 'check_projects FC2: PASS', exit 0 (run on pin b276325)."),
 row("fc2d-gate-check-pages", "2.9-gate", "tools/check_pages.py --all", "PASS", "Observed 'check_pages FC2: PASS', exit 0."),
 row("fc2d-gate-check-dag", "2.9-DAG", "tools/check_dag.py --all", "PASS", "Observed 'check_dag FC2: PASS', exit 0; FC2 concept links unchanged by the delta."),
 row("fc2d-gate-run-labs", "2.5-labs", "tools/run_labs.py --unit FC2", "PASS", "Observed 'run_labs FC2: PASS (11/11)', exit 0."),
 row("fc2d-gate-page-smoke", "2.9-page_smoke", "tools/page_smoke.py --unit FC2", "PASS", "Observed 'page_smoke modules/FC/FC2/project.html: PASS', in-browser line 'All 87 tests pass on seed 304304175', 'page_smoke FC2: PASS', exit 0."),
 row("fc2d-gate-run-graders", "2.6-autograder-1", "tools/run_graders.py --unit FC2 --seeds 0-49", "PASS", "Observed 'run_graders FC2: PASS (reference 50/50 seeds)'. Independent: ledgers/FC2/scripts/FC2-d-r4/reference_0-49.out, 50 of 50 seeds '87 passed'."),
 row("fc2d-gate-ruff-mypy", "2.6-gate", "ruff check ., ruff format --check ., mypy --no-incremental", "PASS", "'All checks passed!'; '335 files already formatted'; 'Success: no issues found in 229 source files'."),
 row("fc2d-gate-pytest", "2.5-pytest", "tests/test_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py", "PASS", "pytest -q on the three files: all dots, exit 0."),
 row("fc2d-gate-verify-refs", "2.1-citations", "tools/verify_refs.py --unit FC2", "PASS", "'live re-verification of FC2: 3 of 560 entries, 0 problems', exit 0."),
 row("fc2d-collect-count", "2.6-autograder", "grader/test_project.py vs project.html line 320 'collects 87 checks'", "PASS", "Scratch dir with test_project.py, instance.py and reference.py as scanner.py: '87 tests collected'; page says 87 and 'the count is 87 for each of the seeds 0 to 49'."),
 row("fc2d-seeds-84", "2.6-autograder-1", "grader/test_project.py on reference.py, seeds 0-49", "PASS", "Row id kept from round 3 (the old count 84 is gone). Evidence: ledgers/FC2/scripts/FC2-d-r4/reference_0-49.out, 50 of 50 seeds '87 passed'; no seed differs."),
 row("fc2d-starter-fails", "2.6-autograder", "grader/starter.py", "PASS", "QF_SEED=0 on starter.py: '79 failed, 8 passed'. The suite fails on the starter, as the spec states."),
 row("fc2d-alternatives", "2.6-autograder-5", "ledgers/FC2/scripts/FC2-d-r3/alts/alt1..alt5 (five correct implementations)", "PASS", "run_suite.sh on seeds 0-49 per alternative: alt1 50/50, alt2 50/50, alt3 50/50, alt4 50/50, alt5 50/50 '87 passed' (ledgers/FC2/scripts/FC2-d-r4/alt*.out). Round-3 alternatives reused, unchanged."),
 row("fc2d-mutate-builder", "2.6-mutation", "tools/mutate_graders.py --unit FC2 --seeds 0-9", "PASS", "Observed 'mutate_graders FC2: PASS (36/36 killed)' (ledgers/FC2/scripts/FC2-d-r4/mutate_all_0-9.out). This covers the 30 builder mutants m01-m46 and the six verifier mutants v01-v06; all are killed in the window."),
 row("fc2d-mut-v03", "2.6-mutation", "ledgers/FC2/mutants/v03_parity_gross_bankers_round.py", "PASS", "KILLED: test_half_cent_gross_rounds_once_up (seed 0)."),
 row("fc2d-mut-v04", "2.6-mutation", "ledgers/FC2/mutants/v04_convexity_returns_one_based_index.py", "PASS", "KILLED: test_convexity_matches_exhaustive_oracle_second_chain (seed 0)."),
 row("fc2d-mut-v05", "2.6-mutation", "ledgers/FC2/mutants/v05_convexity_findings_before_parity.py", "PASS", "KILLED: test_findings_are_in_parity_then_convexity_order (seed 0)."),
 row("fc2d-mut-v06", "2.6-mutation", "ledgers/FC2/mutants/v06_gross_rounds_signed_gap_then_abs.py", "PASS", "KILLED: test_negative_half_cent_gross_rounds_once_up_in_magnitude (seed 0)."),
 row("fc2d-mut-v01-boundary", "2.6-mutation", "ledgers/FC2/mutants/v01_convexity_zero_net_kept.py; grader/test_project.py lines 669-683 (new convexity boundary tests)", "PASS", "Round-3 FAIL resolved. The new test_convexity_finding_with_net_exactly_zero_is_not_returned (chain [100,110,120], calls [50,75,10], puts [50,85,30], fee 10, spread 5: chord 30, call 75, gross 45 = 3 x 15, net 0) kills v01 on seed 0 (mutate output; run_suite v01 seeds 0-2: 1 failed on each). Kept-at-net-1 counterpart test_convexity_finding_with_net_one_cent_is_returned passes on reference."),
 row("fc2d-mut-v02-labels", "2.6-mutation", "ledgers/FC2/mutants/v02_parity_explanation_names_P1_only.py; grader/test_project.py PARITY_LABELS / CONVEXITY_LABELS (lines 38-41, 587-593)", "PASS", "Round-3 FAIL resolved. The per-kind label test kills v02 on seed 1 (mutate output 'KILLED ... (seed 1)'; run_suite seeds 0-2: fails only on seed 1). Seeds 0 and 2 have no parity finding, so the kill is seed-dependent; it is inside the 0-9 window, so it counts."),
 row("fc2d-grader-stdlib", "2.6-autograder", "course/modules/FC/FC2/grader/instance.py, reference.py, test_project.py", "PASS", "Imports: math, random, fractions, typing, itertools, copy, os, sys, re, pathlib, pytest, ast (instance and test). The new 're' import is stdlib. test_module_imports_standard_library_only still passes on the reference."),
 row("fc2d-grader-messages", "2.6-autograder-4", "course/modules/FC/FC2/grader/test_project.py (new asserts lines ~674-790)", "PASS", "Read every new assert message: 'a convexity finding whose net amount is exactly zero is not returned', 'a call is at most the spot', 'a put is at most the discounted strike', 'the explanation names each assumption its kind depends on'. None prints an expected value."),
 row("fc2d-grader-instance-validity", "2.8-instances / 2.6-autograder-2", "course/modules/FC/FC2/grader/instance.py lines 46-59 (_within_bounds) and 109-110; test_generated_chains_satisfy_the_model_free_bounds_of_theorem_2_2", "PASS", "Round-3 FAIL resolved. Theorem 2.2 (course/modules/FC/FC2/L05.html lines 84-91: 0<=C<=S, C>=max(S-DK,0), 0<=P<=DK, P>=max(DK-S,0)) re-checked on seeds 0-49 with a separate script: ledgers/FC2/scripts/FC2-d-r4/bounds_check.out gives 0 violations for the 17 none, 12 parity and 21 convexity chains (round 3 had 6 clean chains violating). The new test passes on the reference."),
 row("fc2d-grader-instance-diversity", "2.8-instances", "course/modules/FC/FC2/grader/instance.py", "PASS", "ledgers/FC2/scripts/FC2-d-r4/instance_check_r4.out: planted kinds none 17, convexity 21, parity 12; reference scan gives 0 findings for all 17 clean chains and finds every planted violation whose net is positive; 29 distinct finding lists; labels all SIMULATED. Only 0 or 1 finding per chain occurs over seeds 0-49 (coverage note: multi-finding ordering is tested by hand-built chains)."),
 row("fc2d-lab1", "2.5-labs", "course/modules/FC/FC2/project.html lab-FC2-project-1 (code, expected block, hypothesis lines 55, interpretation line 163)", "PASS", "check_labs.out: expected == stdout True; diff_labs.out: no code difference beyond the trailing newline. Interpretation numbers recomputed in prose_numbers.out: gaps 0,120,0,0,-20,0 at 9000..11500; chord-less-call at 10500 -75 (chord 625, call 700); gross 75 net 30; cost 45. The hypothesis's definitional claim about P6 is a separate FAIL row."),
 row("fc2d-lab2", "2.5-labs", "course/modules/FC/FC2/project.html lab-FC2-project-2", "PASS", "diff_labs.out: page differs from twin only at three blank lines (___ for gap, net, net); completion rule holds (0 non-blank differences). expected == stdout True. Output md5 equals Lab 1 (same chain)."),
 row("fc2d-lab3", "2.5-labs", "course/modules/FC/FC2/project.html lab-FC2-project-3 (hypothesis line 376, expected block, interpretation line 485)", "PASS", "check_labs.out: expected == stdout True. prose_numbers.out: strike 4500 gap -60 gross 60 net 0 (dropped); 6500 gap 226 net 166; 7000 gap 540 net 480; convex 5000 chord-less-call 470/3; convex 6000 -188/3, gross 63, net 3. Interpretation 'about minus 62.67 cents to two decimals' is consistent with -188/3."),
 row("fc2d-lab-twins-pure", "2.5-labs", "tests/labs/FC2/lab-FC2-project-{1,2,3}.py", "PASS", "python -I -W error: exit 0 and empty stderr for each (lab1.stderr, lab2.stderr, lab3.stderr); no random, network, file or __name__ guard."),
 row("fc2d-rubric-observable", "2.6-rubric-1", "course/modules/FC/FC2/project.html rubric table lines 503-514", "PASS", C + " the rubric level descriptors were re-read in this round and each names something a grader can see."),
 row("fc2d-rubric-calib-A", "2.6-rubric-2", "course/modules/FC/FC2/project.html article#exemplar-a lines 583-633 (data-scores 2,1,1,2,1)", "PASS", C + " blind scoring of Exemplar A by the rubric alone remains within one level of the official scores."),
 row("fc2d-rubric-calib-B", "2.6-rubric-2", "course/modules/FC/FC2/project.html article#exemplar-b, summary line 525 and annotation line 529 (data-scores 4,4,3,3,3)", "PASS", "Round-3 FAIL resolved. The passage now states 'Each finding trades three legs at a fee of 8 and a half-spread of 12 cents, a cost of 60 cents', and 'each net is its gross less that cost'. Blind C2 = 3 (cost model and survival stated; the net is stated, the 'gap between net and zero' is only implicit), official 4: within one level. The annotation's phrase 'its gap from zero' is a stretch, noted, not a fail."),
 row("fc2d-exemplar-numbers", "2.2-numbers", "course/modules/FC/FC2/project.html exemplar-a and exemplar-b passages", "PASS", "prose_numbers.out reproduces 6175 and 6650 (6500 and 7000 times 0.95); gaps 226 and 540; nets 166 and 480; chord 802/3 at 6000; chord-less-call -188/3; gross 63; net 3; cost 60. Exemplar A's 'about 226/540/63' are these values."),
 row("fc2d-exemplar-annotations", "2.6-rubric-2", "course/modules/FC/FC2/project.html annotations (lines 529-566, 589-620)", "PASS", "Each annotation was checked against its passage. B C2 annotation is consistent after the fix (see fc2d-rubric-calib-B). A annotations unchanged and consistent."),
 row("fc2d-spec-explanation-labels", "2.6-spec", "course/modules/FC/FC2/project.html Rung 3 scan bullet line 301; grader/test_project.py PARITY_LABELS and CONVEXITY_LABELS", "PASS", "Round-3 FAIL resolved. The spec states 'A parity finding names P1, P2, P3, P4 and P6, and a convexity finding names P1, P2, P5 and P6'. The grader sets the same two sets, and the reference explanations contain them (test_scan_explanations_are_nonempty_and_name_the_rule passes)."),
 row("fc2d-spec-errors-scope", "2.6-spec", "course/modules/FC/FC2/project.html 'Constraints' lines ~306-316", "PASS", C + " the exception list is unchanged; the ValueError tests pass on the reference."),
 row("fc2d-hours", "2.6-hours", "course/modules/FC/FC2/project.html #hours table lines 338-356; course/modules/FC/FC2/index.html lines 29-41", "PASS", "Table rows 2+3+5+9+3+5+3 = 30. Hub: 'data-hours-lessons=60, data-hours-project=30', '60 h lessons · 30 h project (33.3% of the 90 module hours)'. Project hours are consistent with the hub. The 30% band is a design target (ruling), not a fail."),
 row("fc2d-cards-sample", "2.7-cards-sample", "course/modules/FC/FC2/cards.json (all 137 cards read; every changed card and every L04-L08 card checked against lesson text)", "PASS", "Changed cards checked: c013 and c138 vs Lab 1 Part B output; c032 vs L02 Definition 1.1 and L02 line 290; c038, c133 vs Lab 3 Part A daily margins (39 31 34 -35 34 -13 -36 23 29 -22; balance 84; 4 losses on days 4,6,7,10); c045, c134 vs Lab 3 Part B (0.049026; 4902625; Solution E3 exists); c056, c057, c135 vs L04 Example 2.5 (9/10 factor; 6.561; 14.58; 18.00); c059, c071, c080 vs L05 Theorem 4.1 and Remark 4.2; c085 vs L06 Theorem 1.4(c); c086, c136 vs Example 1.5 (Delta 1/2, B -20, V0 30, q 3/4); c094, c137 vs Example 3.4 (45, 75; Lab 1 prints 45 and 75); c102, c103, c107, c122, c123 vs L07 A8, Prop 1.4, Thm 2.3 and L08 Thm 2.3, Prop 3.2 (2 halvings, bracket conditions match Def 3.1); c110 (-91.01 unrounded, -91 printed), c111, c116 (12.162285 -> 12.1623), c117 (-0.0049977 currency units) recomputed with a Python tree. c132 FAIL (separate row). Unchanged L01-L03 cards read in full; lab-derived ones (c008, c021-c027, c046, c050) recomputed from twin output. Cross-check: a Python recomputation of the L07 binomial values. Cards c012, c077 and c113 are T and mention Lab 1 without a basis; their T answer is a theorem or proposition, so not a fail (note)."),
 row("fc2d-cards-dups", "2.7-cards-duplicates", "course/modules/FC/FC2/cards.json (137 cards)", "PASS", "ledgers/FC2/scripts/FC2-d-r4/cards_check.out: no duplicate ids, fronts or backs; key sets consistent."),
 row("fc2d-cards-numbers", "2.7-cards-numbers", "course/modules/FC/FC2/cards.json (all cards vs own lesson text)", "PASS", "cards_check.out: 'cards with a number absent from their lesson: []'. This is a weak automated check (number present somewhere in the lesson); the semantic checks are in fc2d-cards-sample and fc2d-cards-c132."),
 row("fc2d-cards-grades", "2.7-cards-grade", "course/modules/FC/FC2/cards.json grade and basis fields", "PASS", "Grades: T 98, C 11, none 28 (definitions and formulas, no grade needed by BUILDER section 7). Every C card has a basis. The T cards FC2-c012, c077, c113 mention Lab 1 without a basis; their T answers are a theorem or proposition, so not a fail."),
 row("fc2d-cards-ids", "2.7-cards-ids", "course/modules/FC/FC2/cards.json ids", "PASS", "ids FC2-c001..c138 with FC2-c031 absent (no card at c031 in ccfdf4c either). BUILDER section 7 says ids run upward; a gap is not a violation (note)."),
 row("fc2d-reading-theorem-locator", "2.1-attribution", "course/modules/FC/FC2/project.html #reading line 657", "PASS", "Round-3 FAIL resolved. The page now says 'The parity relation (Theorem 1.2 of Lesson 5) and convexity in strike (Theorem 3.2 of Lesson 5)'. L05.html line 63 is 'Theorem 1.2 (put–call parity)'; line 115 is 'Theorem 3.2 (convexity in strike)'."),
 row("fc2d-references-no-locator", "2.1-attribution", "course/modules/FC/FC2/project.html #reading and data-cite items", "PASS", "No chapter, page, equation or edition in project.html (grep for 11th, JF 24, JFE 7, p., pp., chapter: no hits)."),
 row("fc2d-notation", "2.4-notation", "course/modules/FC/FC2/project.html (all symbols); notation/notation.json", "PASS", "project.html contains no math macros (no \\( \\) spans). Registered symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f and \\mathbb{Q} do not occur in project.html. Plain-text symbols C, P, S, K, df, r are local to the project."),
 row("fc2d-simulated-label", "2.8-SIMULATED", "course/modules/FC/FC2/project.html, labs, instance.py", "PASS", "Every chain on the page and in the instance carries SIMULATED; test_instance_is_labelled_simulated passes; instance labels over seeds 0-49 are all SIMULATED (instance_check_r4.out)."),
 row("fc2d-process-banned", "2.9-prose", "course/modules/FC/FC2/project.html and grader/*.py", "PASS", "grep for TODO, TBD, lorem, beyond the scope, for brevity, important to note, studies show, clearly, obviously, roughly, builder, verifier, planner, architect, agent, batch, round N: no hits."),
 row("fc2d-ladder-claims", "2.6-ladder", "course/modules/FC/FC2/project.html #ladder lines 41-50", "PASS", C + " the ladder section is outside every hunk."),
 row("fc2d-curriculum-scope", "2.6-scope", "curriculum/02-economics-finance-core.yaml:425-431 vs project.html", "PASS", "git diff ccfdf4c b276325 -- curriculum references tools/data_sources.yaml is empty; the brief is unchanged. The SIMULATED substitution is disclosed on the page."),
 row("fc2d-no-external", "2.9-page_smoke", "course/modules/FC/FC2/project.html and grader.js", "PASS", "grep -c 'https?://' project.html = 0; page_smoke reports no external requests (PASS)."),
 row("fc2d-new-tests", "2.6-autograder", "grader/test_project.py: test_convexity_finding_with_net_exactly_zero_is_not_returned, test_convexity_finding_with_net_one_cent_is_returned, test_generated_chains_satisfy_the_model_free_bounds_of_theorem_2_2", "PASS", "Re-derived by hand: chain [100,110,120], calls [50,75,10], puts [50,85,30], spot 100, df 1e6, fee 10, spread 5: chord at 110 = 30; second difference -45; gross 45 = 3 x 15; net 0, so not returned; parity gaps are 0 at all strikes. Calls 76 and puts 86 give gross 46, net 1, returned. The bounds test loops seeds 0-49 with the Theorem 2.2 inequalities. All three pass on reference.py."),
 row("fc2d-mut-new-student-errors", "2.6-mutation", "ledgers/FC2/mutants/n01..n05 (generated by ledgers/FC2/scripts/FC2-d-r4/gen_mutants.py from reference.py)", "PASS", "Five new student-error mutants, each one change to reference.py: n01 convexity explanation omits P6 (killed on 8 of seeds 0-9, first at seed 0); n02 parity strike divided by df (10/10 seeds); n03 negative parity gaps skipped (10/10); n04 convexity charged one leg less (10/10); n05 findings sorted by net, not by kind and strike (10/10). Outputs in ledgers/FC2/scripts/FC2-d-r4/mut_n0*.out."),
 row("fc2d-lab1-hypothesis-terms", "2.1-definitions / 2.6-spec", "course/modules/FC/FC2/project.html line 55 (lab-FC2-project-1 hypothesis: 'both terms are defined in assumption P6 below'); P6 at line 333", "FAIL", "The hypothesis says the fee and the half-spread are both defined in P6. P6 defines the half-spread (the bid-ask half-width) and says 'each leg pays the fee', but never says what the fee is. 'fee' is also used before any definition in the spec key list (line ~286). A learner cannot tell what a fee of 5 cents is, so the claim in line 55 is false for one of its two terms.", "In P6 (project.html line 333) add: 'The fee is the charge per contract that the trade pays on each leg, in cents (fee_cents_per_contract).' Or delete '(both terms are defined in assumption P6 below)' from line 55."),
 row("fc2d-cards-c132", "2.7-cards-correctness / 2.3-grades", "course/modules/FC/FC2/cards.json line 935 (FC2-c132, lesson L05, grade T); L05.html line 337 (Section 6 misconception) and line 311 (Remark 4.2)", "FAIL", "The card answers 'Should a deep in-the-money call be exercised early?' with 'No', graded T, and cites 'Section 6; Remark 4.2' for 'Depth in the money does not change this'. Remark 4.2 (L05.html ~line 311) says the opposite of an answer: 'The theorem concerns prices. It does not say how the buyer of an American call should behave on each path', and 'the date-t statement is a remark, not a proved result'. The comparison 'selling the European call does at least as well as exercising' for an American holder needs V_A(t) >= V_E(t) at date t, which Remark 4.2 says is not proved. The card therefore over-grades an unproved behaviour claim.", "Regrade FC2-c132 to C, or rewrite it to the proved statement only: 'Theorem 4.1 fixes the date-0 price; at date t the bound V_E(t) >= (S_t - K)^+ is proved, but equality at a later date is a remark (Remark 4.2).' Remove 'Depth in the money does not change this' from the card. The same overclaim is in the L05 Section 6 misconception (L05.html line 337), which belongs to the L05 slice: flag it to that verifier."),
]

mutants = []
mut_out = (ROOT / S / "mutate_all_0-9.out").read_text(encoding="utf-8").splitlines()
pat = re.compile(r"^KILLED (\S+)\.py: (.*?) -> (.*)$")
for line in mut_out:
    m = pat.match(line)
    if m:
        mutants.append({"id": m.group(1), "description": m.group(2), "killed_by": m.group(3),
                        "file": f"ledgers/FC2/mutants/{m.group(1)}.py"})
for name, desc in [
    ("n01_convexity_explanation_omits_P6", "Convexity explanation omits the cost label P6"),
    ("n02_parity_strike_divided_by_df", "Parity gap divides the strike by df instead of multiplying"),
    ("n03_negative_parity_gaps_skipped", "Negative parity gaps skipped, so only rich calls reported"),
    ("n04_convexity_charged_one_leg_less", "Convexity net charges two legs instead of three"),
    ("n05_findings_sorted_by_net_descending", "Findings sorted by net amount instead of kind and strike order"),
]:
    mutants.append({"id": name, "description": desc, "killed_by": f"run_suite.sh seeds 0-9 (ledgers/FC2/scripts/FC2-d-r4/mut_{name}.out): killed on every seed except n01 on 2 of 10 seeds",
                    "file": f"ledgers/FC2/mutants/{name}.py"})
for m in mutants:
    if m["id"].startswith("n0"):
        pass

fragment = {
    "unit": "FC2",
    "slice": "FC2-d",
    "round": 4,
    "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 4 (did not build FC2)",
    "pin": "b276325",
    "base": "ccfdf4c (round-3 pin). Delta reviewed: project.html hunks at lines 34, 52, 160, 279-323, 482, 522-531, 654; grader/instance.py and test_project.py (new bounds check and convexity boundary tests, label sets); cards.json (c013-c138, 19 changed and 7 new); L04-L08 lesson hunks read for card dependencies; lab-FC2-L04-1 twin outside this slice.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC4-FC2-d",
    "scratch": "/tmp/fc2d-r4.* (per-seed suite copies, removed after each run)",
    "verified_at": "2026-10-29T02:31:03+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Read in full: project.html (672 lines), grader/instance.py (141), reference.py (145), starter.py (29), test_project.py (800), "
        "cards.json (137 cards: all L04-L08 cards and all changed cards read against lesson text; unchanged L01-L03 cards read and "
        "the lab-derived ones recomputed), the three project lab twins and the page code. Commands run on b276325: check_projects, "
        "check_pages, check_dag, run_labs, run_graders 0-49, page_smoke, verify_refs (live), ruff check, ruff format --check, "
        "mypy --no-incremental, pytest on the three files, mutate_graders 0-9, run_suite over the reference, five alternatives, "
        "the starter, all 41 mutants at seeds 0-9 (5 new), bounds_check, instance_check_r4, check_labs, diff_labs, prose_numbers, "
        "cards_check, L01/L02/L03/L06/L07/L08 lab twins for card numbers. Not checked: the full pytest suite and render_curriculum/build_site "
        "--check (no input of this slice changed); the lesson-side defects in L04-L08 beyond the cards that depend on them (other slices; "
        "the L05 Section 6 sentence is flagged in fc2d-cards-c132); the in-browser Pyodide run beyond page_smoke's output; "
        "Exemplar blind scores are my own judgment, not an independent rater's; the hours band is a design target and not re-judged. "
        "Observed (not rows): every generated chain has at most one finding, so multi-finding ordering is covered only by hand-built tests; "
        "the 'gap from zero' phrase in Exemplar B's C2 annotation is implicit in the passage; FC2-c031 is absent from the id sequence (also absent at ccfdf4c)."
    ),
    "summary": "",
}
n_rows = len(rows)
n_fail = sum(1 for r in rows if r["status"] != "PASS")
fragment["summary"] = (
    f"FC2-d round 4: verdict FAIL. {n_rows} rows: {n_rows - n_fail} PASS, {n_fail} FAIL, 0 UNVERIFIABLE. "
    f"Mutants: {len(mutants)} (all killed in seeds 0-9; 5 new student-error mutants n01-n05 killed). "
    "Non-PASS: fc2d-lab1-hypothesis-terms (P6 does not define 'fee'), fc2d-cards-c132 (T-graded card answers an exercise-behaviour question that Remark 4.2 disclaims). "
    "Round-3 FAILs resolved: fc2d-mut-v01-boundary, fc2d-mut-v02-labels, fc2d-grader-instance-validity, fc2d-rubric-calib-B, fc2d-spec-explanation-labels, fc2d-reading-theorem-locator."
)
out = ROOT / "ledgers/FC2/FC2-d.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", out, "rows", n_rows, "fail", n_fail, "mutants", len(mutants))
