"""Round 19 (BK4 slice c): write the fragment ledgers/BK4/BK4-c.json from the round-19 outputs under out/.

Usage: python -I write_fragment_r19.py <checkout-root>. Every row's evidence names the output file or script that backs it.
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1])
S = "ledgers/BK4/scripts/BK4-c-r19"
O = f"{S}/out"
CARRY = "Carried from round 18 (files byte-identical since the previous pin 50559266): "

rows = {}


def row(rid, check, location, evidence, status="PASS", carried=False):
    rows[rid] = {
        "id": rid,
        "check": check,
        "location": location,
        "status": status,
        "evidence": (CARRY + evidence) if carried else evidence,
    }


# ---- gates (run this round, pin cd4dd7df)
row("proj-check-tools", "2.9/2.6 tools", "course/modules/BK/BK4/project.html",
    f"{O}/check_pages.txt 'check_pages BK4: PASS'; {O}/check_dag.txt 'check_dag BK4: PASS'; {O}/check_projects.txt 'check_projects BK4: PASS' (run_gates.sh, exit 0 each).")
row("proj-ruff", "ruff", "tests/labs/BK4; course/modules/BK/BK4/grader",
    f"{O}/ruff_check.txt 'All checks passed!'; {O}/ruff_format.txt '12 files already formatted'.")
row("proj-mypy-repo", "mypy strict", "pyproject.toml [tool.mypy]",
    f"{O}/mypy_repo.txt 'Success: no issues found in 385 source files' (mypy --no-incremental).")
row("proj-mypy-plan-command", "mypy on grader and labs", "course/modules/BK/BK4/grader/test_project.py:28,:30",
    f"{O}/mypy_unit.txt 'Success: no issues found in 12 source files' (tests/labs/BK4 and grader).")
row("proj-pytest-labs", "pytest -k BK4", "tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_memo_exemplars.py",
    f"{O}/pytest_BK4.txt: 8 passed (exit 0).")
row("proj-page-smoke", "page_smoke project", "course/modules/BK/BK4/project.html",
    f"{O}/page_smoke_project.txt: lab timings 0.0 s, 'in-browser grader: All 89 tests pass on seed 160286821. (0.9 s)', 'page_smoke BK4: PASS'.")
row("proj-refs", "citations resolve", "project.html:505-506",
    f"{O}/verify_refs_offline.txt 'offline integrity: 560 entries, 0 problems'; project.html:505-506 data-cite keys read (duffie2011central, bisndcpmi) and both are in the BK4 registry set (plans/BK4-build-plan.md section 7.1).")
row("proj-anchors-links", "anchors and links", "course/modules/BK/BK4/project.html",
    f"{O}/check_pages.txt PASS; grep of index.html shows id=\"placement\" at line 69 (the placement link target).")
row("proj-banned-and-process-words", "BUILDER_RULES 1.3-1.4 and process words", "project.html; grader/*.py; tests/labs/BK4/lab-BK4-project-*.py",
    "grep (this round) for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, roughly, historically, verifier, builder, agent, ruling, slice, fixer over the slice files: no hits. 'exemplar' is the rubric term (project.html:407-489); '...' occurs only as typing ellipses (test_project.py:38, :1128).")
row("proj-dag-concepts", "DAG", "course/modules/BK/BK4/project.html",
    f"{O}/check_dag.txt 'check_dag BK4: PASS' (run this round on cd4dd7df).")
row("proj-notation-T", "notation", "project.html:200,:220-225",
    "notation/notation.json (read this round) registers 8 symbols: T (S1), \\Phi, \\gamma_3, \\gamma_4 (M4), R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} (AP1). The page uses L, IM_d, DF_d, K, R, D, S, t, k, M, L_s, a1-a3, Lambda only. None collides with a registered symbol; no page symbol is T, Phi, gamma or R^ast.")
row("proj-l03-crossref", "cross-references to Lesson 3", "project.html:54,:224,:417; L03.html:55,:130,:134,:143,:178",
    "Re-read this round: L03.html:55 says Section 3 names the close-out limit; :134 defines margin cover level (def-margin-cover); :143 Assumption A3 (target); :178 Example 2.5 sizes the margin as the k-th smallest loss; :54 'Lesson 3 defines the term scenario' (L03 defines scenarios in its definitions). L03.html is byte-identical to the previous pin (git diff 50559266..cd4dd7df empty for course/modules/BK/BK4/L03.html).")
row("proj-grade-scale-citation", "grade scale matches Lesson 1", "project.html:421; L01.html:45-46",
    "project.html:421 read this round: 'B is published but not settled, and C is a working paper, practitioner research or a single sample.' L01.html is byte-identical to the previous pin.", carried=True)
row("proj-reading-list-no-claim", "reading list attributes no statement", "project.html:501-508",
    "Read this round: the section says 'This page attributes no statement to either.' and holds two empty data-cite list items.")
row("proj-atlas-studio", "no Atlas or studio requirement", "course/modules/BK/BK4; curriculum/curriculum.json atlas",
    "grep (this round): project.html has no 'atlas' or 'studio' text; curriculum/curriculum.json 'atlas' array has no BK4 entry (python check this round).")

# ---- labs (run this round)
row("proj-lab1-numbers", "Lab 1 prose numbers", "project.html:56-139; tests/labs/BK4/lab-BK4-project-1.py",
    "Recomputed independently in ledgers/BK4/scripts/BK4-c-r19/recompute_r19.py (out/recompute_r19.txt): shares 1333/1666/1000 with leftover 1, survivors 1334/1666/1000, 9550 bps: exact position 191/5, k 39, margin 117088, cover 9750, one cent below 9500. Lab output equals expected block (out/twin_vs_page_r19.txt 'project-1: run exit 0; output == expected block: True').")
row("proj-lab2-numbers", "Lab 2 completion blanks and expected output", "project.html:142-190; tests/labs/BK4/lab-BK4-project-2.py",
    "out/twin_vs_page_r19.txt: page code has 2 blanks, every line equals the twin or contains a blank (42 vs 42 lines), twin output equals the expected block; out/run_labs_unit.txt 'run_labs BK4: PASS (8/8)'.")
row("proj-lab3-numbers", "Lab 3 prose numbers", "project.html:253-368; tests/labs/BK4/lab-BK4-project-3.py",
    "recompute_r19.txt: largest loss 118151; margins 105154/111074/117088 for 9000/9500/9750 with k 36/38/39 and covers 9000/9500/9750, one cent below 8750/9250/9500; Part C past-counts 2/2/0/0 (9500) and 4/2/0/0 (9000); 111074-105154=5920; 9500-9000=500. Lab output equals expected block (twin_vs_page_r19.txt).")
row("proj-labs-simulated-stdlib", "SIMULATED, no file, standard library", "tests/labs/BK4/lab-BK4-project-1..3.py; project.html:54,:56-58",
    "grep of imports (this round): only 'random' and 'fractions' in the three twins; random.Random(1) seeds the losses; no open() or network call; project.html:54 and the lab hypotheses label the inputs SIMULATED.")
row("proj-lab2-learner-text", "Lab 2 hypothesis and interpretation", "project.html:143-146,:190",
    "Read this round. The completed lines print 1334, 1666, 1000, k 39, 117088 (out/twin_vs_page_r19.txt). data-tolerance 1e-6 times (1+size) is 0.117 cent at 117088, under one cent, so 'a wrong cent fails the check' holds.")
row("proj-lab3-claim-checks-rules", "Lab 3 claim-check sentences", "project.html:255,:367",
    "Read this round: 'conservation True in every row' (Part A output, all five rows True); 'the 100000-cent row is the only row with an uncovered loss' (12000 uncovered only there); 'three different sizing indices, 36, 38 and 39' (Part B); 'agrees True' three times; Part C 4 past the margin and 2 past the default fund at 9000 bps, none past capital.")

# ---- structure, spec, prose (this round)
row("proj-rung-ladder", "ladder", "project.html:41-50", "Read this round: four rungs (worked example, completion, independent project, stretch) with the content the plan states (plans/BK4-build-plan.md section 5.1).")
row("proj-hours", "hours split and project hours", "project.html:34,:36,:374-386; index.html data-hours-lessons=35, data-hours-project=15",
    "grep this round: index.html data-hours-lessons=\"35\" and data-hours-project=\"15\"; project.html:34 data-hours-project=\"15\"; :384 '15 of the module's 50 hours, or 30 %' (15/50 = 30 %).")
row("proj-hours-estimates", "time budget sums", "project.html:377-383",
    "Rows 2+2+3+3+2+2+1 = 15, equal to the total in :384. The verifier's component estimates (waterfall and sizing 6 h, rungs 1-2 4 h, suite 2-3 h, memo 2-3 h, self-assessment 1 h) bracket the stated 15 h within 30 %.")
row("proj-named-conditions", "named conditions, both sides", "project.html:204-212; grader/test_project.py:468-617, 903-996",
    "Read this round. margin_for_cover: empty refused (:903) and one scenario accepted (:913); target 0 refused (:919), 1 accepted (:929), 10001 refused (:935), 10000 accepted (:945); negative refused (:951), zero accepted (:961). cover_bps: empty refused (:967), one accepted (:977); negative refused (:983), zero accepted (:993). waterfall: loss, margin, fund, capital each refused with the named input and accepted at zero (:468-556); defaulter below, above, between and absent refused, lowest and highest accepted (:558-617). The 15-entry refusal list (test_project.py:1060-1091) is also run for ValueError and for no output (:1092-1095).")
row("proj-conventions-prose", "Conventions match the tests", "project.html:220-225; grader/test_project.py:59-103, 225-261",
    "Read this round: layer formulas a1..a3 and R, the survivor rule and leftover rule, cover floor, and sizing ceiling match oracle_waterfall (test_project.py:59-77), oracle_sorted_margin (:80-84) and oracle_cover (:102-103). Reference passes 89/89 (out/collect_count_r19.txt).")
row("proj-fixture-tables", "hand-computed fixtures", "project.html:230-251; grader/test_project.py:277-351, 379-438, 651-711, 791-804",
    "recompute_r19.txt recomputes every layer-table row (80..300), the remainder rows (1, 2, 3, 4 cents), the sizing fixtures (8000 -> 40, 8001 -> 50, 10000 -> 50, 5000 on four losses -> 20) and the cover fixtures (3333, 6666); each equals the page table and the test expectation.")
row("proj-money-integer-claim", "money outputs int", "project.html:204,:225; grader/test_project.py:128-132, 186-196, 451-460",
    "checked_int rejects float and bool (:129-133); the waterfall and sizing tests check every money field; 89/89 pass on the reference.")
row("proj-large-cent-claim", "large-cent fixture", "grader/test_project.py:451-460",
    "recompute_r19.txt: loss*fund_1 exceeds 2^53 (True); floored share 6055950114045319 for member 1, 529746839784068 for member 2, leftover 1 goes to member 1, giving 6055950114045320 as expected.")
row("proj-sizing-duplicate-losses", "repeated losses count per occurrence", "grader/test_project.py:713-727",
    "[5,5,10,20] at 5000 bps: k=2, margin 5; [5,5,5,9,12] at 6000 bps: k=3, margin 5 (hand-computed from k = ceil(target*S/10000): k = 2 and k = 3, giving 5 and 5; the reference passes the test).")
row("proj-zero-loss-sizing", "zero loss is a scenario in sizing", "grader/test_project.py:730-737",
    "[0,10,20,30] at 5000 bps: k = 2, margin 10 (hand-computed; the test expects 10).")
row("proj-zero-loss-cover", "zero loss in cover denominator", "grader/test_project.py:847-852",
    "[0,0,5,9] at margin 0: 10000*2//4 = 5000, as the test expects.")
row("proj-remainder-spec", "remainder rule text matches tests", "project.html:221; grader/test_project.py:379-438",
    "project.html:221 states the leftover rule; recompute_r19.txt remainder rows give {1:1,2:0,3:0} for 1 cent, {1:1,2:1,3:0} for 2 cents, and 1 uncovered at 4 cents, as the tests state.")
row("proj-survivor-leftover-order", "leftover by ascending id, not dict order", "grader/test_project.py:419-438",
    "The out-of-order dictionary test expects member 1 to receive the leftover cent; the reference passes it; mutant r14b (dictionary order) is killed (mutate_graders_0_9_after_new.txt).")
row("proj-silence-named-refusals", "no print or warning", "grader/test_project.py:1046-1096",
    "Read this round. capsys checks valid calls and each of the 15 refusals; filterwarnings('error') (:33) turns any warning into an exception; the reference passes; debug-print mutants r4g and r4h are killed.")
row("proj-refusal-count-docstring", "refusal list sentence", "grader/test_project.py:1057-1059",
    "The docstring says 'Each named refusal in the list below raises ValueError' and states no count; the list has 15 entries, and the test passes on the reference.")
row("proj-grader-docstring-named-variables", "grader docstring claims", "grader/test_project.py:9-16",
    "FIXED since round 18: the docstring now says --assert=plain keeps compared values out of the report and each test hides its own traceback. Observed (out/probe_failure_output_r19.txt): probe B (wrong sizing value) prints only 'AssertionError: the margin must be ...' and 'All traceback entries are hidden'; ledgers/BK4/scripts/BK4-c-r19/tracebackhide_check.py finds 89 of 89 test functions with __tracebackhide__ = True.")
row("proj-failure-leak", "failing check prints no expected value", "grader/test_project.py:9-16, 106-158",
    "out/probe_failure_output_r19.txt: wrong survivors (probe C, leftover dropped) prints 'the survivors' payments differ from the fixture' with no values; the starter prints only the named message. No failure message contains a compared value.")
row("proj-context-sentences", "context paragraph claims", "project.html:198",
    "Read this round: the context paragraph's order (margin, default fund, capital, then survivors) matches the test_project.py oracle and instance.py; 'autograder checks the cent results and the cover values, not the docstring or the imports' matches the suite (no docstring or import test).")
row("proj-spec-context-length", "context paragraph accuracy", "project.html:198", "Read this round; the paragraph states only rules the suite and the reference implement (see proj-conventions-prose).")
row("proj-spec-signatures", "required names and signatures", "project.html:202; grader/starter.py:15-47",
    "starter.py defines Waterfall (frozen, five fields) and the three function signatures named on the page (waterfall, margin_for_cover, cover_bps); the page's Required outputs match these names and parameter names.")
row("proj-spec-inputs-instance", "inputs match instance.py", "project.html:200; grader/instance.py:22-50",
    "instance.py generates 4-6 members (randint 4..6), margins 10000-60000, default funds 1000-8000 (>= 1 cent), capital 0-50000, 40-80 losses, targets from (9000, 9500, 9750): all within the page's ranges. Validity asserted on seeds 0-49 (recompute_r19.txt).")
row("proj-spec-questions", "no clarifying questions needed", "project.html:196-216; grader/test_project.py",
    "Read this round. Every required message substring the suite checks (at least one scenario is needed; target_bps; losses cannot be negative; the input name, e.g. default_fund_cents; defaulter_id) is named on the page. No input or convention is left for the student to guess.")
row("proj-local-run", "local command and exception sentence", "project.html:397-400; grader/test_project.py:5",
    "The command at project.html:399 equals test_project.py:5 and starter.py:6. Probes A and D (out/probe_failure_output_r19.txt) show the student's exception with the function arguments, as project.html:400 states.")
row("proj-autograder-claims", "autograder claims", "project.html:215; grader/test_project.py",
    "collect-only count 89 (out/collect_count_r19.txt); warnings as errors (test_project.py:33); the listed checks (conservation, layer order, remainder, named conditions, order statistic and brute force, cover floor, monotonicity, silence, purity, two cases) are present; reference 89 passed.")
row("proj-pyodide-empty-packages", "in-browser run needs no packages", "project.html:393; grader/test_project.py:17-31",
    "The grader panel declares no data-packages; page_smoke ran the 89 tests in the browser (out/page_smoke_project.txt). The suite imports only the standard library, pytest and the student module (test_project.py:20-31).")
row("proj-round7-prose-delta", "prose changed since round 7 is correct", "project.html:38,:45,:54,:58,:215",
    "Read this round. The only change since the round-18 pin is :215 (88 -> 89), which equals the collect-only count. The other lines were recomputed (lab rows above).")

# ---- exemplars (scored by the dedicated blind scorer; verifier does not score)
row("proj-exemplar-a-calibration", "exemplar A official scores equal blind scores", "project.html:426 data-scores; :428 official scoring",
    "Blind scorer output ~/.fanout/blind/BK4-c.json: A = [2,2,1,2,2] (its notes say the prose was read through a stripper that drops the annotations and verdicts). Official data-scores=\"2,2,1,2,2\" (project.html:426) and official scoring C1 2, C2 2, C3 1, C4 2, C5 2 (:428). Equal on every criterion. The verifier did not score exemplars (ruling 23).")
row("proj-exemplar-b-calibration", "exemplar B official scores equal blind scores", "project.html:457 data-scores; :459 official scoring",
    "Blind scorer output ~/.fanout/blind/BK4-c.json: B = [4,4,4,4,4]. Official data-scores=\"4,4,4,4,4\" (project.html:457) and official 4 on all five (:459). Equal. Not scored by the verifier (ruling 23).")
row("proj-exemplar-b-numbers", "exemplar B numbers", "project.html:459-471",
    "Each number is printed by Lab 1 or Lab 3, is an input of the instance, is computed from them by the rules (38.0 = 9500*40/10000), or is a difference of printed numbers (5920, 500). Recomputed in recompute_r19.txt.")
row("proj-rubric-c1-levels", "rubric C1 observable", "project.html:413",
    "Read this round. Each level counts the named layers, the cents for a stated scenario, or the order statement, so each is observable. Note (not a defect): level 2 says 'names all four', where the page's own convention is three layers and then the survivors (project.html:220).")
row("proj-rubric-c2-levels", "rubric C2 observable", "project.html:414", "Read this round: target in bps, value of k, sorted position, cover check at the margin and one cent below, each a checkable item.")
row("proj-rubric-c3-descriptors", "rubric C3 observable", "project.html:415", "Read this round: pro rata rule, leftover rule, and a sum checking the residual are each checkable.")
row("proj-rubric-c4-descriptors", "rubric C4 observable", "project.html:416", "Read this round: one recommended margin, its cover, a count of scenarios past the survivors or uncovered, one compared alternative are each checkable.")
row("proj-rubric-c5-descriptor", "rubric C5 observable", "project.html:417", "Read this round: limits named, direction stated (a 'not known' statement counts), counter-evidence or 'cites none' stated.")
row("proj-rubric-observable-wording", "rubric wording observable", "project.html:409-417", "Read this round: no vague descriptor; each level names an item a reader can check.")
row("proj-exemplar-annotations-agree", "annotations agree with scores", "project.html:426-489 (annotations 446-451, 475-479)",
    "Read this round: exemplar A annotations (C1 2, C2 2 met and 3 missed, C3 1, C4 2, C5 2) and exemplar B annotations (4 on all five) are consistent with the blind scores and official scores.")
row("proj-rubric-self-form", "self-assessment wiring", "project.html:485-489; course/assets/js/site.js:163; rubric.js:223",
    "Asset files are byte-identical since the previous pin (git diff 50559266..cd4dd7df empty for course/assets); project.html:485-489 data attributes unchanged.", carried=True)
row("proj-alternatives", "five alternatives and the reference pass seeds 0-49", "ledgers/BK4/alternatives/alt1..alt5; scripts/BK4-c-r16/alts/alt6_bisect_module.py",
    f"{O}/alternatives_r19.txt: alt1..alt6 and reference each 50/50 seeds (scratch copies, run_alts_r19.py). Styles: comprehensions and sorted (alt1); ClearingHouse class returning Waterfall (alt2); Fraction with math.floor and math.ceil (alt3); integer two-pass (alt4); bisection with no sort (alt5). Note (not a defect): alt4 and alt1 use the integer ceiling (x+9999)//10000 instead of -((-x)//y); both are exact integer ceilings for x >= 0 and both pass.")
row("proj-r16-alt6", "alternative 6", "ledgers/BK4/scripts/BK4-c-r16/alts/alt6_bisect_module.py", f"{O}/alternatives_r19.txt: alt6_bisect_module.py 50/50 seeds pass (re-run this round).")
row("proj-r16-new-mutants", "round-16 mutants r16a-r16e killed", "ledgers/BK4/mutants/r16a..r16e",
    f"{O}/mutate_graders_0_9_after_new.txt: r16a_target_message_omits_target_bps, r16b_defaulter_margin_read_at_zero_based_index, r16c_default_fund_ignores_the_margin_already_paid, r16d_loss_refusal_message_omits_loss_cents, r16e_cover_sorts_the_callers_list_in_place: all KILLED.")
row("proj-r17-mutants-new", "round-17 mutants r17a-r17e killed", "ledgers/BK4/mutants/r17a..r17e",
    f"{O}/mutate_graders_0_9_after_new.txt: r17a_capital_layer_ignores_margin_paid, r17b_sizing_drops_the_last_loss, r17c_margin_layer_reads_the_fund_table, r17d_zero_margin_covers_nothing, r17e_uncovered_subtracts_the_capital_again: all KILLED.")

# ---- mutants (re-run this round, all 106)
row("proj-mutants-builder", "builder mutants m01-m10 killed", "ledgers/BK4/mutants/m01..m10",
    f"{O}/mutate_graders_0_9_after_new.txt: each of m01-m10 KILLED (seeds 0-9); mutate_graders BK4: PASS (106/106 killed).")
row("proj-mutants-own", "own mutants n1-n4 killed", "ledgers/BK4/mutants/n1..n4", f"{O}/mutate_graders_0_9_after_new.txt: n1-n4 KILLED.")
for rid, label in [("proj-mutants-round7", "round-7"), ("proj-mutants-round8", "round-8"), ("proj-mutants-round9", "round-9"),
                   ("proj-mutants-round10", "round-10"), ("proj-mutants-round11", "round-11"), ("proj-mutants-round12", "round-12"),
                   ("proj-mutants-vc", "vc-series"), ("proj-mutants-round13", "round-13"), ("proj-mutants-round14", "round-14"),
                   ("proj-mutants-r15", "round-15")]:
    row(rid, f"{label} mutants killed", "ledgers/BK4/mutants/",
        f"{O}/mutate_graders_0_9_after_new.txt: every {label} mutant file present in ledgers/BK4/mutants is KILLED (106/106 in this run).")
row("proj-mutant-float-index", "float index mutant killed", "ledgers/BK4/mutants/r12b_sizing_index_float.py",
    f"{O}/mutate_graders_0_9_after_new.txt: r12b_sizing_index_float.py KILLED.")
row("proj-mutant-float", "float arithmetic mutants killed", "ledgers/BK4/mutants/vc10_float_arithmetic.py; r12b_sizing_index_float.py",
    f"{O}/mutate_graders_0_9_after_new.txt: vc10_float_arithmetic.py and r12b KILLED.")
row("proj-mutant-argument", "argument-changing mutants killed", "ledgers/BK4/mutants/r4f, r16e, t8e",
    f"{O}/mutate_graders_0_9_after_new.txt: r4f_sizing_sorts_caller_list_in_place.py, r16e_cover_sorts_the_callers_list_in_place.py, t8e_waterfall_pops_defaulter_from_argument.py KILLED.")
row("proj-mutant-r15c-equivalent", "equivalent float-floor mutant", "ledgers/BK4/equivalent/r15c_cover_float_floor.py; ledgers/BK4/equivalent/README.md",
    f"{O}/equivalent_r15c_r19.txt reproduces the README's check: exhaustive S<=2000 2003000 pairs, 0 disagreements; random S<=10^7 200000 pairs, 0 disagreements. The README's argument covers S up to 9e11 (2^53/10000 bound; 9e11 < 9.007e11). Judgment for the architect: project.html:204 says 'no float appears' (a method constraint) while project.html:215 says the grader checks 'not the method'; no output of the grader can differ (math.floor returns an int in both versions), so the mutant is output-identical on every list that fits in memory and is kept in equivalent/ per ruling 9's output-equivalence reading. Not a FAIL.")
row("proj-mutant-fund-capped-at-pool", "fund-capped-at-pool mutant killed", "ledgers/BK4/mutants/r13d_fund_layer_capped_at_survivor_pool.py",
    f"{O}/mutate_graders_0_9_after_new.txt: r13d KILLED.")
row("proj-cap-layer-probes", "capital-layer probes", "ledgers/BK4/scripts/BK4-c-r13/probes_r13.py",
    "Script byte-identical since the previous pin; its probes are not counted as mutants.", carried=True)
row("proj-direction-claims", "bias-direction claims", "project.html:469,:471",
    "Checked by argument this round: the sized margin is the k-th smallest loss, which cannot fall when a loss rises (so one default at a time biases the margin down and the cover up); a close-out that grows losses biases the margin low and the cover high; margins held fixed in stress bias the simulated cover low when margins rise and high when they fall.")
row("proj-scope-words", "scope words backed", "project.html:54,:139,:200,:215,:255,:367,:400",
    "Read this round: 'every' and 'all' statements are backed by a loop in the suite (every scenario, every seed in 0-49), a computed list (the 40 scenarios), or the stated hypothesis of the lab.")
row("proj-numbers-rounding", "rounded numbers state their rule", "project.html:58,:112-113,:139,:251,:384",
    "38.2 = 191/5 (:58), 95.00 % = 38/40 (:139), 6666.67 = 20000/3 (:251), 15/50 = 30 % (:384): each computed and stated with its base.")
row("proj-page-prose-delta-ruling", "page follows binding plan and rulings", "plans/BK4-build-plan.md:751; plans/FINAL-ARCHITECT-RULINGS.md:9, :10, :22",
    "Plan ruling (line 751): target set 9000/9500/9750; exemplars A level 2 and B level 4; the empty-losses condition on cover_bps is on the page (project.html:209); no period-convention sentence in project.html (grep 'period' shows only close-out wording, :417 and :471). Rulings 9, 10, 22 are unchanged since the previous pin.", carried=True)
row("proj-grader-reference-run", "reference passes seeds 0-49", "course/modules/BK/BK4/grader/reference.py",
    f"{O}/run_graders.txt: 'run_graders BK4: PASS (reference 50/50 seeds)'; and the 89-test collect run on reference (out/collect_count_r19.txt: 89 passed).")
row("proj-grader-starter-fails", "starter fails with named messages", "course/modules/BK/BK4/grader/starter.py",
    f"{O}/collect_count_r19.txt: starter gives 85 failed, 4 passed; the 4 are the frozen-dataclass test (starter defines Waterfall) and three instance-only tests. The failure lines name the property, e.g. 'the student module has no implementation for waterfall yet; write it in clearing_house.py.' with no traceback.")
row("proj-collect-count", "collect-only count equals page", "course/modules/BK/BK4/grader/test_project.py; project.html:215",
    f"{O}/collect_count_r19.txt: '89 tests collected' (run in a scratch workspace with reference.py as clearing_house.py; the in-repo collect fails with ImportError because clearing_house.py is not in the repository, as expected). project.html:215 says 89.")
row("proj-instances", "instance.py valid cases", "course/modules/BK/BK4/grader/instance.py",
    "recompute_r19.txt: seeds 0-49 each valid (ids 1..N with N 4-6, funds >= 1000, 40-80 losses, targets in the set); 50 distinct sizing answers across seeds 0-49; the 9000/9500/9750 answers differ for all 50 seeds (the answers change, not only labels).")
row("proj-placement-claim", "hub placement claim", "project.html:43; index.html:69-71,:150",
    "index.html:69 id=\"placement\" (mastery 0.8), :71 'to skip them, reach the bar and answer both skill checks'; project.html:43 states the same rule. Re-read this round.")
row("proj-page-test-count-line", "page test-count sentence", "project.html:215", "'runs 89 checks' equals the collect-only count of 89 (out/collect_count_r19.txt).")
row("proj-lab-page-twin", "page lab code equals twin; expected equals output", "project.html lab blocks; tests/labs/BK4/lab-BK4-project-1..3.py",
    f"{O}/twin_vs_page_r19.txt: project-1 and project-3 page code equals the twin after the one trailing newline that HTML does not carry (the tools/run_labs.py rule: twin.rstrip('\\n')); project-2 differs only at the two blanks. Expected blocks equal fresh output for 1 and 3; the project-2 twin's output equals its expected block.")
row("proj-twins-alone", "each twin runs alone under -I -W error", "tests/labs/BK4/lab-BK4-project-1..3.py",
    f"{O}/twin_vs_page_r19.txt: each twin run as python -I -W error exits 0; {O}/run_labs_unit.txt 'run_labs BK4: PASS (8/8)'.")
row("proj-r16-blind-prose", "exemplar prose consistent with rubric", "project.html:424-489",
    "Exemplar prose is byte-identical to the state the blind scorer read (the last change to project.html before the scorer's file, 700bf33f at 22:57, precedes the scorer's 23:27; cd4dd7df changes only :215).")
row("proj-r17-assert-plain-exception-claim", "--assert=plain exception sentence", "project.html:400",
    "Probes A and D (out/probe_failure_output_r19.txt) show the exception, its message and the student function's arguments, and no comparison details; the sentence is accurate.")
row("proj-r17-float-message-numbers", "float example in message", "grader/test_project.py:696-710",
    "recompute_r19.txt: repr(2800/10000*50) = 14.000000000000002 and its ceiling is 15, so 'can come out one too high' is correct; the test's expected 14 is the exact integer ceiling of 2800*50/10000.")
row("proj-r17-stretch-wording", "stretch section wording", "project.html:492-499", "Read this round: 'Not graded' and the two extensions state a rule and a check.")

# ---- round-18 rows that this round re-verified
row("proj-r18-mutate-all", "every mutant killed (ruling 9)", "ledgers/BK4/mutants/r18a_full_cover_margin_is_last_loss_given.py; grader/test_project.py:682-688; project.html",
    f"Round-18 FAIL re-verified and now PASS: {O}/mutate_graders_0_9_after_new.txt 'mutate_graders BK4: PASS (106/106 killed)'; r18a now KILLED by test_full_target_margin_is_the_largest_loss_in_any_order (seed 0). The reference passes that test (89/89), and page lines 202 and 207 state the least-margin rule and the 1..10000 range.")
row("proj-r18-new-mutants", "round-18 mutants r18b-r18d killed", "ledgers/BK4/mutants/r18b, r18c, r18d",
    f"{O}/mutate_graders_0_9_after_new.txt: r18b KILLED by test_each_scenario_matches_the_oracle_on_both_instances; r18c KILLED by test_layers_and_survivor_payments_add_to_the_loss_on_every_scenario; r18d KILLED by test_waterfall_is_a_frozen_dataclass_with_the_named_fields.")
row("proj-r18-delta-read", "every hunk since the round-17 pin is read", "git diff 700bf33f 50559266 for course/modules/BK/BK4",
    "Re-read this round: the only BK4 hunk in that range is test_project.py:698-699 (the float message, now accurate; see proj-r17-float-message-numbers) and the new mutant and script files. project.html has no hunk in that range.")

# ---- round-19 delta and new work
row("proj-r19-delta-read", "every hunk since the round-18 pin is read", "git diff 50559266 cd4dd7df for course/modules/BK/BK4, tests/labs/BK4, ledgers/BK4",
    "Read in full: project.html:215 (88 -> 89); grader/test_project.py:9-16 (docstring) and :682-688 (new test); ledgers/BK4/mutants/r18a..r18d (new mutant files); ledgers/BK4/scripts/BK4-c-r18/* (archived round-18 scripts). tests/labs/BK4, grader/reference.py, instance.py, starter.py, alternatives/ and equivalent/ are byte-identical to the previous pin (git diff empty).")
row("proj-r19-tracebackhide-claim", "docstring claim: each test hides its own traceback", "grader/test_project.py:13-15",
    f"{S}/tracebackhide_check.py: 89 test functions, 0 without '__tracebackhide__ = True'. Probes B and C (out/probe_failure_output_r19.txt) show a failing check prints only its message and 'All traceback entries are hidden'. Student-raised exceptions (probes A, D) are not 'failing checks' and show the student's frames and arguments, which project.html:400 states.")
row("proj-r19-full-target-test", "new test expects the rule the page states", "grader/test_project.py:682-688; project.html:202,:207",
    "losses [30,50,10,20] at 10000 bps: k = 4, sorted position 4 = 50. The page states the least margin whose cover is at least target_bps (:202) and the 1..10000 range (:207). The reference passes; mutant r18a is killed by this test.")
row("proj-r19-new-mutants", "five new student-error mutants r19a-r19e", "ledgers/BK4/mutants/r19a..r19e; ledgers/BK4/scripts/BK4-c-r19/make_mutants_r19.py",
    f"Written from grader/reference.py by make_mutants_r19.py (each search text occurs exactly once). {O}/mutate_graders_0_9_after_new.txt: r19a leftover to every positive survivor KILLED (test_layers_and_survivor_payments_add_to_the_loss_on_every_scenario); r19b pro rata denominator includes the defaulter's fund KILLED (same test); r19c negative check looks only at the first loss KILLED (test_negative_loss_is_refused_in_margin_for_cover); r19d sizing memo keyed by target KILLED (test_margin_matches_the_order_statistic_on_both_instances); r19e index floor plus one KILLED (test_fixture_five_losses_at_8000_bps_uses_the_ceiling_index).")
row("proj-r19-probe-fund-cap", "three further probes killed", "scratch probes (recorded in this row, not a mutant)",
    "Probes (run in scratch, seed 0, listed in out/probe_failure_output_r19.txt and the notes): fund capped by the defaulter's margin (9 failed), sizing strict above target (5 failed), residual strictly above the total (equivalent: the output is identical at residual = total; passes 89/89).")
row("proj-r19-starter-instance-only", "starter passes only frozen-class and instance tests", "grader/starter.py; grader/test_project.py",
    f"{O}/collect_count_r19.txt and the -rA run: the four passing starter tests are test_waterfall_is_a_frozen_dataclass_with_the_named_fields (the starter defines Waterfall) and three instance-only tests. All other 85 tests fail with a named message.")
row("proj-r19-equivalence-recheck", "equivalent-mutant proof re-run", "ledgers/BK4/equivalent/README.md",
    f"{O}/equivalent_r15c_r19.txt: reran the check script (exhaustive and random counts as in the README).")
row("proj-r19-blind-scorer-source", "exemplar scoring source", "~/.fanout/blind/BK4-c.json",
    "Read this round: A [2,2,1,2,2], B [4,4,4,4,4], notes state the stripper output was used (annotations and verdict lines dropped). Used as the exemplar calibration evidence (ruling 23); the verifier did not score the exemplars.")

# ---- mutants list from the run
mutants = []
pat = re.compile(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (\S+) \(seed (\d+)\)$")
for line in (ROOT / O / "mutate_graders_0_9_after_new.txt").read_text(encoding="utf-8").splitlines():
    m = pat.match(line)
    if not m:
        continue
    status, name, desc, killed, seed = m.groups()
    mutants.append({
        "name": name,
        "description": desc.replace("Student error: ", "", 1),
        "killed_by": f"{killed} (seed {seed})" if status == "KILLED" else None,
        "status": status,
        "seeds": "0-9",
    })

rows_list = [rows[k] for k in sorted(rows, key=lambda x: list(rows).index(x))]
sha = "cd4dd7dfc2bbe0fc16b672329daa408d1d8a268b"
fragment = {
    "unit": "BK4",
    "slice": "c",
    "round": 19,
    "verifier": "E19 (Haiku 5.5, independent verifier)",
    "pin": sha,
    "base": "50559266 (round-18 pin; the round-18 fragment is /Users/billyribeiro/.fanout/frags/E-BK4-c.round18.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE19-BK4-c",
    "scratch": "/tmp/bk4r19-ws and /tmp/bk4r19-probe (scratch; the scripts that back the rows are under ledgers/BK4/scripts/BK4-c-r19/)",
    "verified_at": "2026-11-09T05:53:37Z",
    "verdict": "PASS",
    "rows": rows_list,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta 50559266..cd4dd7df read in full: project.html:215 count 88->89; grader/test_project.py docstring (9-16) and a new test (682-688); mutants r18a-d added; no other slice file changed. "
        "Round-18 FAIL rows proj-grader-docstring-named-variables and proj-r18-mutate-all are re-verified PASS. "
        "All 106 mutants (101 prior + 5 new r19a-r19e) are killed at seeds 0-9 by tools/mutate_graders.py --unit BK4. The five alternatives and the reference pass seeds 0-49. "
        "Exemplar calibration comes from the dedicated blind scorer (~/.fanout/blind/BK4-c.json), not from this verifier (ruling 23). "
        "Judgment calls, recorded for the architect and not failed: (1) the r15c float-floor mutant stays in equivalent/ (proj-mutant-r15c-equivalent); (2) alternatives alt1 and alt4 use the integer ceiling (x+9999)//10000 rather than the -((-x)//y) form that the plan names for style 4 (proj-alternatives); (3) rubric C1 level 2 says 'names all four' where the page counts three layers and then the survivors. "
        "Gate exit codes: check_pages, check_dag, check_projects, run_labs (project and unit), run_graders 0-49, mutate_graders, page_smoke, ruff check and format, mypy (unit and repo), verify_refs --offline, pytest -k BK4 all exit 0 (out/_exit_codes.txt). collect_only_grader exit 2 is expected: the grader imports clearing_house, which the repository does not hold; the 89 count comes from a scratch workspace (out/collect_count_r19.txt)."
    ),
    "summary": (
        "BK4 slice c, round 19: PASS. Rows: all re-verified or carried with the byte-identical prefix; every round-18 FAIL re-verified PASS. Mutants: 106/106 killed at seeds 0-9, including 5 new student-error mutants. "
        "Alternatives: 6 of 6 pass 50/50 seeds, reference 50/50. Labs: 3/3 project labs and 8/8 unit labs pass; page code equals twins modulo the trailing newline. Collect count 89 matches the page."
    ),
}

out = ROOT / "ledgers/BK4/BK4-c.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows_list), "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
