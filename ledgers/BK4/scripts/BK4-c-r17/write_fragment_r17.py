"""Round 17 (verifier E17, BK4 slice c): writes the fragment ledgers/BK4/BK4-c.json from the rows this round checked
(evidence strings cite the r17 scripts and outputs), the mutant list parsed from out/mutate_graders_r17.txt, and the
ids of the round-16 fragment (every previous row id must appear). Usage: write_fragment_r17.py <checkout-root>"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1])
S = "ledgers/BK4/scripts/BK4-c-r17"
OUT = ROOT / S / "out"
prev = json.loads(pathlib.Path("/Users/billyribeiro/.fanout/frags/E-BK4-c.round16.json").read_text(encoding="utf-8"))
prev_ids = [r["id"] for r in prev["rows"]]

MUT_RE = re.compile(r"^KILLED (\S+): (.*) -> (\S+) \(seed (\d+)\)$")
mutants = []
for line in (OUT / "mutate_graders_r17.txt").read_text(encoding="utf-8").splitlines():
    m = MUT_RE.match(line)
    if m:
        mutants.append({"id": m.group(1), "description": m.group(2), "killed_by": m.group(3) + f" (seed {m.group(4)})"})
assert len(mutants) == 97, len(mutants)

R = {}  # id -> (status, check, location, evidence)
def row(i, status, check, location, evidence):
    R[i] = (status, check, location, evidence)

GATE = "run_gates.sh on pin 700bf33f; exit codes out/_exit_codes.txt"
row("proj-check-tools", "PASS", "2.6 autograder (check tools)", "course/modules/BK/BK4/project.html",
    f"check_pages --unit BK4: 'check_pages BK4: PASS'; check_dag --unit BK4: 'check_dag BK4: PASS'; check_projects --unit BK4: 'check_projects BK4: PASS' (out/check_pages.txt, check_dag.txt, check_projects.txt; {GATE}).")
row("proj-ruff", "PASS", "2.6 autograder (ruff)", "tests/labs/BK4; course/modules/BK/BK4/grader",
    "ruff check tests/labs/BK4 course/modules/BK/BK4/grader: 'All checks passed!' exit 0 (out/ruff_check.txt); ruff format --check: '12 files already formatted' exit 0 (out/ruff_format.txt).")
row("proj-mypy-repo", "PASS", "2.6 autograder (mypy)", "pyproject.toml [tool.mypy]",
    "mypy --no-incremental (repo): 'Success: no issues found in 385 source files' exit 0 (out/mypy_repo.txt).")
row("proj-mypy-plan-command", "PASS", "2.6 autograder (mypy)", "course/modules/BK/BK4/grader/test_project.py:28,:30",
    "mypy --no-incremental tests/labs/BK4 course/modules/BK/BK4/grader: 'Success: no issues found in 12 source files' exit 0 (out/mypy_unit.txt).")
row("proj-pytest-labs", "PASS", "2.5 lab (pytest)", "tests/test_labs.py; tests/test_run_labs.py; tests/test_page_checks.py; tests/test_memo_exemplars.py",
    "pytest -q -k 'BK4 or bk4' over the four files: 8 tests, '........ [100%]', exit 0 (out/pytest_BK4.txt; _exit_codes.txt).")
row("proj-page-smoke", "PASS", "2.9 structure (page_smoke)", "course/modules/BK/BK4/project.html",
    "page_smoke.py --unit BK4 --pages project: 'lab lab-BK4-project-1..3' 0.0 s each; 'in-browser grader: All 88 tests pass on seed 2019964552'; 'page_smoke modules/BK/BK4/project.html: PASS' (out/page_smoke_project.txt).")
row("proj-refs", "PASS", "2.1 citations", "course/modules/BK/BK4/project.html:503-507 (data-cite duffie2011central, bisndcpmi)",
    "references/references.json entries exist for both keys (duffie2011central: DOI 10.1093/rapstu/rar001, verified_by crossref; bisndcpmi: BIS CPMI publications page, verified_by issuer). verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (out/verify_refs_offline.txt). verify_refs.py --unit BK4 (live, plain run): 'live re-verification of BK4: 3 of 560 entries, 0 problems', exit 0 (out/verify_refs_BK4_live.txt). The registry changed between pins only in generated_at and one used_by list of another key (git diff 56cc575a 700bf33f -- references/).")
row("proj-anchors-links", "PASS", "2.9 structure", "course/modules/BK/BK4/project.html",
    "anchors_imports_r17.py: every href='#...' target is an id on the page and every local file link resolves; the rubric criteria C1-C5, exemplar-a, exemplar-b and self-assessment ids exist (out/anchors_imports_r17.txt).")
row("proj-banned-and-process-words", "PASS", "2.9 structure", "project.html; grader/*.py; tests/labs/BK4/lab-BK4-project-*.py",
    "banned_scan_r17.py (ledgers/BK4/scripts/BK4-c-r17/banned_scan_r17.py; output out/banned_scan_r17.txt): BUILDER_RULES 1.3 strings (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more), filler (it is important to note, studies show, experts agree, well known, obviously, clearly, roughly, historically, it can be shown) and ellipses: no prose hit; the only '...' is Callable[..., None] typing in grader/test_project.py. Process words (round, verifier, builder, architect, ruling, fixer, ledger, mutant, agent, batch, slice): none in the page or the labs; 'round' occurs once, as arithmetic in the grader message at test_project.py:698.")
row("proj-dag-concepts", "PASS", "2.9 DAG", "course/modules/BK/BK4/project.html",
    "check_dag.py --unit BK4: PASS (out/check_dag.txt). project.html has no class='concept' link and no <dfn> (banned_scan_r17.py: no concept or dfn markup hit in project.html); the page defines in prose every term it uses (lede :38, :54, :58, :224).")
row("proj-notation-T", "PASS", "2.4 notation", "course/modules/BK/BK4/project.html (Conventions :220-225; Inputs :200; labs)",
    "notation/notation.json registers 8 symbols (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}); the page uses none of them (grep: no T as a symbol, no \\Phi, gamma, R_f, R^*, Q). Its letters S, L, M, K, R, D, DF_i, IM_d, k, t and the list name Lambda are local (notation.json 'about': only program-wide symbols are registered). R is defined at :38 and :220 and is not a registry symbol.")
row("proj-l03-crossref", "PASS", "2.9 DAG; 2.4 math", "course/modules/BK/BK4/project.html:224,:417,:54; course/modules/BK/BK4/L03.html",
    "L03.html: section 3 'Where the canon breaks' has 'No close-out period is modelled' (cited at :417 as Lesson 3 Section 3); '<dfn>scenarios</dfn>' in the why-it-matters block (cited at :54 'Lesson 3 defines the term scenario'); Proposition 2.3 (T) with assumptions A3, A4 states the k-th smallest order statistic (cited at :224 'Lesson 3 defines the cover and states the sizing rule with its proof under its own assumptions').")
row("proj-grade-scale-citation", "PASS", "2.1 citations", "course/modules/BK/BK4/project.html:421; course/modules/BK/BK4/L01.html:45-46",
    "L01.html:45 'B published, not settled'; :46 'C working paper, practitioner research or single sample'; project.html:421 quotes both descriptions correctly.")
row("proj-reading-list-no-claim", "PASS", "2.1 attribution", "course/modules/BK/BK4/project.html:503-507",
    "project.html:503 'This page attributes no statement to either'; the two list items are empty data-cite elements. The page makes no statement from either source (read in full).")
row("proj-atlas-studio", "PASS", "2.6 atlas; 2.6 studios", "course/modules/BK/BK4; plans/BK4-build-plan.md section 8",
    "check_projects.py --unit BK4: PASS (out/check_projects.txt). Plan section 8: 'None. The curriculum names no Atlas milestone for BK4'; no studio requirement applies to this module (plan section 8 and section 0).")
row("proj-lab1-numbers", "PASS", "2.5 lab; 2.2 numbers", "course/modules/BK/BK4/project.html:56-139; tests/labs/BK4/lab-BK4-project-1.py",
    "Recomputed independently (recompute_r17.py, out/recompute_r17.txt, all PASS): layers 50000/6000/20000, residual 4000; pool 12000; floored shares 1333/1666/1000, leftover 1, payments 1334/1666/1000; 9550 bps over 40 scenarios: exact position 191/5 = 38.2, k 39, margin 117088; cover 9750 at the margin, 9500 one cent below. The twin's stdout equals the page's expected block (recompute_r17.txt, last three lines).")
row("proj-lab2-numbers", "PASS", "2.5 lab; 2.2 numbers", "course/modules/BK/BK4/project.html:142-190; tests/labs/BK4/lab-BK4-project-2.py",
    "Page lines 169 and 182 are the only differences from the twin (shares = {m: ___}, index = ___), both blanks where the twin has the Conventions expressions (page-code vs twin diff, r17 strip_and_twin_check_r17.py). The completed twin's stdout equals the expected block: survivor shares 1334/1666/1000, k 39, margin 117088 (recompute_r17.txt).")
row("proj-lab3-numbers", "PASS", "2.5 lab; 2.2 numbers", "course/modules/BK/BK4/project.html:253-368; tests/labs/BK4/lab-BK4-project-3.py",
    "Recomputed (recompute_r17.txt): Part A rows 20000, 55000, 70000, 80000, 100000 (uncovered 12000); Part B k 36/38/39, margins 105154/111074/117088, covers 9000/9500/9750, one cent below 8750/9250/9500, largest loss 118151; Part C past margin 4 and 2, past default fund 2 and 2, past CCP capital 0 and 0. Twin stdout equals the expected block.")
row("proj-labs-simulated-stdlib", "PASS", "2.5 labs; 2.8 SIMULATED", "tests/labs/BK4/lab-BK4-project-1..3.py; project.html:54,:56-58",
    "Twin imports: fractions, random (twin 1); random (twins 2, 3) (out/anchors_imports_r17.txt). Page :54 labels every amount SIMULATED; the twins' MARGIN/FUND/CAPITAL comments say SIMULATED; no network or file read (grep).")
row("proj-lab2-learner-text", "PASS", "2.9 prose vs lab", "course/modules/BK/BK4/project.html:143-146,:190",
    "Hypothesis (:144) names the two expressions and the printed results (1334/1666/1000, index 39, margin 117088), all equal to the completed twin's output. Interpretation (:190): the instant check compares token by token; run_labs compare_output (tools/run_labs.py:13) allows tol*(1+|expected|) for numbers, tol 1e-6, i.e. about 0.117 cent at 117088, below one cent, so a wrong cent fails.")
row("proj-lab3-claim-checks-rules", "PASS", "2.9 prose vs lab", "course/modules/BK/BK4/project.html:255,:367",
    "Conservation column True in every Part A row; 100000 is the only row with uncovered (12000); brute-force agrees True for each target; Part C 9000 bps: past margin 4, past default fund 2, past capital 0, past survivors 0 (recompute_r17.txt). Each claim in :255 and :367 matches the printed output.")
row("proj-rung-ladder", "PASS", "2.6 ladder", "course/modules/BK/BK4/project.html:41-50",
    "Rung 1 worked example (Lab 1, annotated), Rung 2 completion (Lab 2, instant check), Rung 3 project (spec, autograder, memo with exemplars and self-assessment), Rung 4 stretch (not graded); order matches check_projects.py (PASS).")
row("proj-hours", "PASS", "2.6 hours; 2.9 structure", "course/modules/BK/BK4/project.html:36,:34,:374-386; course/modules/BK/BK4/index.html:29,:39,:42,:162-174",
    "Hours table rows 2+2+3+3+2+2+1 = 15 (:377-384); data-hours-project=15 (:34) and the lede (:36); hub: 35 lesson hours, 15 project hours, 30% of 50 (index.html:42), hub total row 15 (index.html:174).")
row("proj-hours-estimates", "PASS", "2.6 hours estimate", "course/modules/BK/BK4/project.html:377-383",
    "Verifier's estimate per component: Rung 1 read and annotate about 2 h; Rung 2 about 2 h; layers and survivor sharing (6 fixtures, remainder rule, named refusals) about 3-4 h; sizing and cover about 3 h; edge cases and local run about 2-3 h; memo about 2 h; self-assessment about 1 h. Total 15-17 h, within the 30% band of the declared 15 h.")
row("proj-named-conditions", "PASS", "2.6 spec (exception table)", "course/modules/BK/BK4/project.html:204-212; grader/test_project.py:467-609, 893-986",
    "Each named condition of :206-211 has a must_refuse test with the message naming the required input (naming= arguments) and an accepted-side must_accept test at the boundary: target 0/1/10000/10001, empty and one scenario, zero and negative loss, zero and negative margin, fund and capital, defaulter below/above/between/accepted. The must_refuse calls (grep) are exactly the named conditions; no other exception is required.")
row("proj-conventions-prose", "PASS", "2.4 math; 2.9 prose", "course/modules/BK/BK4/project.html:220-225",
    "Layer order a1, a2, a3, R, survivor rule (R>=D; R<D with floor and leftover), conservation, cover floor, sizing ceiling and money rules are implemented in grader/reference.py:57-100 and restated by the oracles in test_project.py:58-102; reference passes 50/50 seeds (run_graders). Read line by line against the page; no mismatch found.")
row("proj-fixture-tables", "PASS", "2.4 math; 2.9 fixtures", "course/modules/BK/BK4/project.html:230-251",
    "Layer table rows (11, :235-245) each match the test with the same loss in test_project.py:276-350; remainder fixture (:249) matches tests 378-415; sizing fixtures (:250) match tests 650-687; cover fixtures (:251) match tests 781-794 (cover 3333 and 6666 recomputed: 10000*1//3, 20000//3 in out/numeric_probes_r17.txt).")
row("proj-money-integer-claim", "PASS", "2.6 spec; method", "course/modules/BK/BK4/project.html:204,:225; grader/test_project.py:128-132, 186-194, 450-459",
    "reference.py uses // only (no '/' division, no float literal); checked_int rejects float and bool outputs; the 2**53 test forces exact integer floors (R*DF_1 = about 4.4e31 > 2**53, out/numeric_probes_r17.txt). Method is not graded beyond these outputs (project.html:215 says so).")
row("proj-large-cent-claim", "PASS", "2.6 autograder", "course/modules/BK/BK4/grader/test_project.py:450-459",
    "numeric_probes_r17.txt: D = 7278398114431529, R = 6585696953829388 < D; floored shares 6055950114045319 and 529746839784068; leftover 1 to member 1, giving 6055950114045320 and 529746839784068 as the test expects (line 'page test wants ... -> True').")
row("proj-sizing-duplicate-losses", "PASS", "2.6 autograder", "course/modules/BK/BK4/grader/test_project.py:703-717",
    "[5,5,10,20] at 5000: S=4, k=2, second smallest 5; [5,5,5,9,12] at 6000: S=5, k=3, third smallest 5; both expected 5 (hand computation, the reference passes, run_graders 50/50).")
row("proj-zero-loss-sizing", "PASS", "2.6 autograder", "course/modules/BK/BK4/grader/test_project.py:720-727",
    "[0,10,20,30] at 5000: S=4, k=2, second smallest 10, as expected (hand computation; reference passes).")
row("proj-zero-loss-cover", "PASS", "2.6 autograder", "course/modules/BK/BK4/grader/test_project.py:837-842",
    "[0,0,5,9] at margin 0: two of four covered, floor(10000*2/4) = 5000, as expected (hand computation; reference passes).")
row("proj-remainder-spec", "PASS", "2.4 math; 2.6 spec", "course/modules/BK/BK4/project.html:221; grader/test_project.py:378-438",
    "Page :221 (leftover one cent each to the first survivors in ascending id with DF_i>0; DF_i=0 pays zero). Tests 378-438 state the same cases: residual 1 to member 1, residual 2 to members 1 and 2, zero-fund member skipped, dictionary order ignored. reference.py:74-80 implements the rule.")
row("proj-survivor-leftover-order", "PASS", "2.6 autograder", "course/modules/BK/BK4/grader/test_project.py:428-437",
    "Dictionaries listed as 3,1,2,4 with residual 1: expected {1:1, 2:0, 3:0}; reference sorts the survivors (reference.py:62); mutants r4a and r14b killed (out/mutate_graders_r17.txt).")
row("proj-silence-named-refusals", "PASS", "2.6 autograder", "course/modules/BK/BK4/grader/test_project.py:1035-1084",
    "test_the_module_prints_nothing_on_valid_inputs (:1036) and test_refused_inputs_print_nothing_before_they_raise (:1047) use capsys; warnings are errors (pytestmark :32). Reference passes; mutants r4g, r4h (debug prints) and r14d (warning) killed (out/mutate_graders_r17.txt).")
row("proj-refusal-count-docstring", "PASS", "2.9 prose vs test", "course/modules/BK/BK4/grader/test_project.py:1047-1049, :1050-1081",
    "Docstring: 'Each named refusal in the list below raises ValueError and prints nothing on the way.' The list has 15 entries (counted in the source), each a named condition of project.html:206-211 (defaulter not a member: above, below, between).")
row("proj-grader-docstring-named-variables", "FAIL", "2.6 autograder docstring", "course/modules/BK/BK4/grader/test_project.py:9-15 (lines 12-14 state 'it never prints an expected value' and 'never the values it compared')",
    "The docstring's no-leak promise is contradicted by the assertion message at test_project.py:697-699, which prints the expected margin 14 on failure (out/P2_r12b_sizing_index_float.txt: 'E AssertionError: ... (2800 / 10000 * 50 is 14.000000000000002, not 14)'). The other sentence, '--assert=plain ... shows the source of the check', is accurate (P2, P3).")
row("proj-failure-leak", "FAIL", "2.6 autograder (failure messages)", "course/modules/BK/BK4/grader/test_project.py:697-699 (test_exact_position_is_an_integer_index_not_a_rounded_float)",
    "The message (added this round, lines 698-699) ends '(2800 / 10000 * 50 is 14.000000000000002, not 14)'. The fixture is losses 1..50 at 2800 bps, so the expected margin and index are both 14 (want = 14 at :694; sorted(range(1,51))[13] = 14, out/numeric_probes_r17.txt). The message therefore prints the expected value on every failing run. Observed: out/P2_r12b_sizing_index_float.txt (the float-index mutant fails with that message). Violates VERIFIER_RULES 2.6 item 4 and the page's own promise at test_project.py:12-13.")
row("proj-context-sentences", "PASS", "2.6 spec", "course/modules/BK/BK4/project.html:198",
    "'The autograder checks the cent results and the cover values, not the docstring or the imports.' True: the suite compares outputs only; no test reads source or docstrings (grep for inspect/ast/__doc__ in test_project.py: none).")
row("proj-spec-context-length", "PASS", "2.6 spec (context)", "course/modules/BK/BK4/project.html:198",
    "The context dd is one paragraph of four sentences plus the autograder sentence; it defines the terms it uses (clearing house, initial margin, default fund, CCP capital, survivors, cover) and needs no clarifying question.")
row("proj-spec-signatures", "PASS", "2.6 spec", "course/modules/BK/BK4/project.html:202; grader/starter.py:19-47",
    "Page names waterfall(loss_cents, defaulter_id, initial_margin_cents, default_fund_cents, ccp_capital_cents), margin_for_cover(losses_cents, target_bps), cover_bps(losses_cents, margin_cents) and the five Waterfall fields; starter.py has the same names, parameters and types (lines 19-47).")
row("proj-spec-inputs-instance", "PASS", "2.6 spec vs instance", "course/modules/BK/BK4/project.html:200; grader/instance.py",
    "Page :200: N members 1..N with N in 4..6; margins and funds per member (funds >= 1); capital; defaulter id; 40 to 80 losses; target in {9000, 9500, 9750}. instance.py:25-39 gives exactly these. Checked for seeds 0-49 (out/instance_sample_r17.txt: 50 valid, 0 invalid).")
row("proj-spec-questions", "PASS", "2.6 spec (no clarifying questions)", "course/modules/BK/BK4/project.html:196-216",
    "Read as a student: the layer order, survivor and leftover rules, cover floor, sizing ceiling, refusal list, return types and the memo content are all stated. No question was needed; the only open choice (a float or Fraction method) is stated as not graded (:215).")
row("proj-local-run", "FAIL", "2.6 autograder (local command)", "course/modules/BK/BK4/project.html:397-400",
    "The sentence at :400 says a failing check shows 'never the compared values'. That is contradicted by the test message that prints the expected 14 (test_project.py:698-699, see proj-failure-leak; out/P2_r12b_sizing_index_float.txt). The other claims hold: --assert=plain output shows the message and source only (P2); when the learner's code raises, pytest prints that exception and the learner function's arguments ('KeyError: probe-secret-12542' and 'loss_cents = 12542, defaulter_id = 5 ...', out/P3_raises_with_args.txt); must_accept prints the chained exception (P3 lines 507-531).")
row("proj-autograder-claims", "PASS", "2.6 autograder (panel)", "course/modules/BK/BK4/project.html:215; grader/test_project.py",
    "'runs 88 checks' (pytest --collect-only: '88 tests collected', out/P1_collect_only.txt); 'warnings as errors' (pytestmark :32); 'checks the cent results and the cover values, not the method' (no source inspection in any test); the second case INST2 (:36) is used in the conservation, oracle and sizing tests.")
row("proj-pyodide-empty-packages", "PASS", "2.6 autograder (Pyodide)", "course/modules/BK/BK4/project.html:393; grader/test_project.py:17-30",
    "The grader panel (:393) has no data-packages attribute (out/anchors_imports_r17.txt); the suite imports only the standard library and pytest, plus the learner module and instance.py. page_smoke runs the suite in the browser runner: 'All 88 tests pass' (out/page_smoke_project.txt).")
row("proj-round7-prose-delta", "PASS", "2.9 prose (delta)", "course/modules/BK/BK4/project.html:38,:45,:54,:58,:215",
    "Read in full this round: :38 lede defines margin, default fund, residual and cover (under Conventions); :45 Rung 1 link; :54 the rung inputs (all SIMULATED, integer cents, bps floored); :58 every number recomputed (out/recompute_r17.txt); :215 '88 checks' (P1).")
row("proj-exemplar-a-calibration", "PASS", "2.6 rubric calibration (blind)", "course/modules/BK/BK4/project.html:426-455 (exemplar A)",
    "Blind scoring from the annotation-stripped prose (out/blind_exemplars_r17.txt, script strip_and_twin_check_r17.py): C1 2 (all four layers named in order, no cents for any scenario); C2 2 (target 9500 stated, no value of k, no cover check); C3 1 (no sharing rule, no amount); C4 2 (a margin with no cover); C5 2 (two limits, no direction). Official 2,2,1,2,2: within one level on every criterion (0 differences).")
row("proj-exemplar-b-calibration", "PASS", "2.6 rubric calibration (blind)", "course/modules/BK/BK4/project.html:457-483 (exemplar B)",
    "Blind scoring (out/blind_exemplars_r17.txt): C1 4 (four layers in order, 80000 cents, 'used only after the one before it is exhausted'); C2 4 (9500 bps, k 38, 38th smallest, cover 9500 and 9250 one cent below); C3 4 (pro rata and leftover rules, 1334+1666+1000=4000); C4 4 (one margin 111074 with cover 9500, count past survivors and uncovered = 0, one alternative); C5 4 (four limits with directions; no B or C claim; no source). Official 4,4,4,4,4: 0 differences.")
row("proj-exemplar-b-numbers", "PASS", "2.2 numbers (exemplar B)", "course/modules/BK/BK4/project.html:459-471",
    "Each number traced: inputs (30000/50000/40000/20000; 4000/6000/5000/3000; 20000; 40 scenarios) from grader/instance.py and the lab code; Lab 1 printed values (80000, 6000, 1333/1666/1000, 1334, 4000); Lab 3 printed values (k 38, 111074, 9250, 105154, 117088, 9500 and the Part C counts 2, 0, 4); computed 12000 pool, 38.0 = 9500*40/10000 and 3999 = 1333+1666+1000 (recompute_r17.txt); differences 5920 and 500 of printed numbers. The 111074 convention is labelled in the memo.")
row("proj-rubric-c1-levels", "PASS", "2.6 rubric (observable)", "course/modules/BK/BK4/project.html:413",
    "C1 levels 4 to 1 name observable items: each layer named, cents for a stated scenario, the 'used only after' statement, count of layers named (at most one = level 1).")
row("proj-rubric-c2-levels", "PASS", "2.6 rubric (observable)", "course/modules/BK/BK4/project.html:414",
    "C2 levels name the target in bps, the value of k, the sorted position, the cover at the margin and one cent below, and the presence of a margin value or sizing rule; each is checkable in a memo.")
row("proj-rubric-c3-descriptors", "PASS", "2.6 rubric (observable)", "course/modules/BK/BK4/project.html:415",
    "C3 levels name the pro rata rule, the leftover rule, survivor amounts, and a sum that checks them; observable.")
row("proj-rubric-c4-descriptors", "PASS", "2.6 rubric (observable)", "course/modules/BK/BK4/project.html:416",
    "C4 levels name one margin, its cover, the count past survivors or uncovered, one alternative, and 'no margin'; observable.")
row("proj-rubric-c5-descriptor", "PASS", "2.6 rubric (observable)", "course/modules/BK/BK4/project.html:417 (hunk :414-417 changed this round)",
    "The level-4 cell now reads 'states the direction ... (a statement that the direction is not known counts as stating it)'. The same parenthetical is in the level-3 cell, so the levels agree. Observable: a memo either gives a direction, or says the direction is not known. Exemplar B meets it (blind scoring).")
row("proj-rubric-observable-wording", "PASS", "2.6 rubric (vague words)", "course/modules/BK/BK4/project.html:409-417",
    "All five criteria read in full; no unobservable adjective (good, clear, thorough, appropriate, sufficient); each level is a count or a named item.")
row("proj-exemplar-annotations-agree", "PASS", "2.6 rubric (annotations)", "course/modules/BK/BK4/project.html:444-481 (annotations, compared after blind scoring)",
    "Exemplar A annotations: C1 level 2, C2 level 2 (meets) and level 3 (misses), C3 level 1, C4 level 2, C5 level 2 — the blind scores. Exemplar B annotations: all level 4 — the blind scores.")
row("proj-rubric-self-form", "PASS", "2.6 rubric (form)", "course/modules/BK/BK4/project.html:485-489; course/assets/js (rubric form)",
    "section.rubric-self has data-rubric='rubric', data-exemplars='exemplar-a exemplar-b', data-store-key and data-summary-path (report/self_assessment.md); the no-JavaScript notice at :488 is present. The form itself was not run in a browser this round (see notes).")
row("proj-alternatives", "PASS", "2.6 autograder (alternatives)", "ledgers/BK4/alternatives/alt1..alt5 (+ alt6 from scripts/BK4-c-r16/alts)",
    "run_alts_r17.py: alt1_comprehensions, alt2_class_based, alt3_fraction, alt4_integer_two_pass, alt5_bisection, alt6_bisect_module and reference.py each pass the suite for seeds 0-49, 50/50 (out/alts_seeds0-49.txt). Styles differ (comprehensions, class, Fraction with floor/ceil, integer two-pass, bisection over margins, bisect module), so ruling 10 is met.")
row("proj-mutants-builder", "PASS", "2.6 mutation", "ledgers/BK4/mutants/ (m01-m10)",
    "tools/mutate_graders.py --unit BK4 --seeds 0-9 on the full mutant directory (out/mutate_graders_r17.txt, 97/97 killed, exit 0): m01..m10 each KILLED with its killer test (see mutants).")
row("proj-mutants-own", "PASS", "2.6 mutation", "ledgers/BK4/mutants/ (n1-n4)",
    "n1..n4 KILLED in out/mutate_graders_r17.txt (97/97 run).")
for i, label in [("proj-mutants-round7", "round-7 mutants"), ("proj-mutants-round8", "round-8 mutants"),
                 ("proj-mutants-round9", "round-9 mutants"), ("proj-mutants-round10", "round-10 mutants"),
                 ("proj-mutants-round11", "round-11 mutants"), ("proj-mutants-round12", "round-12 mutants"),
                 ("proj-mutants-round13", "round-13 mutants"), ("proj-mutants-round14", "round-14 mutants"),
                 ("proj-mutants-r15", "round-15 mutants"), ("proj-mutants-vc", "vc, t8, x10, y11 and s-series mutants")]:
    row(i, "PASS", "2.6 mutation", "ledgers/BK4/mutants/", f"All {label} in ledgers/BK4/mutants are KILLED in the 97/97 run of tools/mutate_graders.py --unit BK4 --seeds 0-9 (out/mutate_graders_r17.txt); each killer is listed in the mutants field.")
row("proj-mutant-float-index", "PASS", "2.6 mutation (float)", "ledgers/BK4/mutants/r12b_sizing_index_float.py",
    "Killed by test_exact_position_is_an_integer_index_not_a_rounded_float (out/mutate_graders_r17.txt; P2 shows the failure). The killer is the test whose message leaks, see proj-failure-leak: the kill is valid, the message is not.")
row("proj-mutant-float", "PASS", "2.6 mutation (float)", "ledgers/BK4/mutants/ (float mutants: vc10_float_arithmetic.py, r12b, and the 2**53 case)",
    "KILLED in the 97/97 run (out/mutate_graders_r17.txt).")
row("proj-mutant-argument", "PASS", "2.6 mutation (purity)", "ledgers/BK4/mutants/ (r4f, r16e, t8e)",
    "KILLED in the 97/97 run (out/mutate_graders_r17.txt).")
row("proj-mutant-fund-capped-at-pool", "PASS", "2.6 mutation", "ledgers/BK4/mutants/r13d_fund_layer_capped_at_survivor_pool.py",
    "KILLED in the 97/97 run (out/mutate_graders_r17.txt).")
row("proj-cap-layer-probes", "PASS", "2.6 mutation (probe, not counted)", "ledgers/BK4/scripts/BK4-c-r13/probes_r13.py",
    "Carried from round 16 (ledgers/BK4/scripts/BK4-c-r13/probes_r13.py byte-identical since the previous pin 56cc575a; not counted as a mutant).")
row("proj-direction-claims", "PASS", "2.7 directional claims", "course/modules/BK/BK4/project.html:469,:471",
    "Second default: a larger loss cannot lower the k-th smallest loss and cannot raise the count at or below a margin, so omitting it biases the sized margin down and the cover up (checked: order statistic is monotone in each loss). Close-out: losses growing gives a low margin and a high cover. Stress: margins rising gives a low simulated cover. All three directions are the stated ones.")
row("proj-scope-words", "PASS", "2.9 scope words (exemplar B)", "course/modules/BK/BK4/project.html:54,:139,:200,:215,:255,:367,:400",
    "Universal words (all, every, any, only, never, exactly, same) on the page are attached to a finite check (the 40 scenarios, the two seeded cases, the 50-seed run), a stated enumeration (the amounts of the lab, the five rows of Part A), or a disclaimer ('does not show that the rules are correct for any other set'). No unbounded universal claim found.")
row("proj-numbers-rounding", "PASS", "2.2 numbers (rounding)", "course/modules/BK/BK4/project.html:58,:112-113,:139,:251,:384",
    "Floored and ceiling rules stated; 38.2 taken up to 39; 95.00 % from 38/40 (exact); 6666.67 = 20000/3 to two places (exact 6666.666...); 9500 bps of 38 of 40 scenarios; all recomputed (recompute_r17.txt, numeric_probes_r17.txt).")
row("proj-page-prose-delta-ruling", "PASS", "2.9 rulings", "plans/BK4-build-plan.md:751; plans/FINAL-ARCHITECT-RULINGS.md",
    "The 2026-11-04 project ruling (plan :751) names the target set 9000/9500/9750, exemplar levels 2 and 4, the cover_bps empty condition and the struck period sentence; the page matches each (:200, :215, :205-208, :401-440). Ruling 9 (mutants) and 10 (alternatives) applied (see proj-mutants-*, proj-alternatives).")
row("proj-grader-reference-run", "PASS", "2.6 autograder (reference)", "course/modules/BK/BK4/grader/reference.py",
    "run_graders.py --unit BK4 --seeds 0-49: 'run_graders BK4: PASS (reference 50/50 seeds, slowest 0.3 s)' (out/run_graders.txt).")
row("proj-grader-starter-fails", "PASS", "2.6 autograder (starter)", "course/modules/BK/BK4/grader/starter.py",
    "Starter run under the page's local command (QF_SEED=0): '84 failed, 4 passed'; all 84 failures name the missing implementation ('the student module has no implementation for <name> yet', 84 occurrences, out/P4_starter_seed0.txt); the 4 passing tests do not call the student functions.")
row("proj-collect-count", "PASS", "2.6 autograder (count)", "course/modules/BK/BK4/project.html:215 (88 checks)",
    "pytest --collect-only -q on the reference copy: '88 tests collected' exit 0 (out/P1_collect_only.txt); the page's '88 checks' matches.")
row("proj-instances", "PASS", "2.6 autograder (instances)", "course/modules/BK/BK4/grader/instance.py",
    "instance_sample_r17.py over seeds 0-49: 50 valid, 0 invalid (N 4-6, ids 1..N, funds >= 1, 40-80 losses, targets in the set, three regions present); 50 distinct sizing margins at each seed's own target and 48 distinct total-uncovered values (out/instance_sample_r17.txt).")
row("proj-placement-claim", "PASS", "2.9 prose vs hub", "course/modules/BK/BK4/project.html:43; course/modules/BK/BK4/index.html:69,:160-174 (placement)",
    "Hub placement: eight questions, two skill checks 'marked as such' on rungs 1 and 2, mastery bar 80 percent; to skip rungs 1 and 2 a student must reach the bar and answer both skill checks (index.html quiz section). Project :43 says the same.")
row("proj-page-test-count-line", "PASS", "2.9 prose vs suite", "course/modules/BK/BK4/project.html:215",
    "'runs 88 checks' equals the collect-only count (88, P1) and the in-browser count (page_smoke: 'All 88 tests pass').")
row("proj-mutant-r15c-equivalent", "PASS", "2.6 mutation (equivalence proof)", "ledgers/BK4/scripts/BK4-c-r15/equivalent/r15c_cover_float_floor.py; ledgers/BK4/scripts/BK4-c-r15/out/equivalent_check_r15c.txt",
    "Carried from round 16 (ledgers/BK4/scripts/BK4-c-r15/equivalent/r15c_cover_float_floor.py and out/equivalent_check_r15c.txt are unchanged since the previous pin 56cc575a; not re-run this round): float cover floor equals integer floor for S <= 2000 exhaustively and for 200000 random pairs with S <= 10^7 (0 disagreements). Note: the proof lives under scripts/, not ledgers/BK4/equivalent/ (ruling 9 wording), see notes.")
row("proj-lab-page-twin", "PASS", "2.5 page code vs twin", "course/modules/BK/BK4/project.html lab blocks; tests/labs/BK4/lab-BK4-project-1..3.py",
    "Page code equals twin for lab 1 and lab 3 (after HTML unescape, trailing newline ignored); lab 2 differs only in the two blank lines 169 and 182 (rung-2 convention, FINAL-ARCHITECT-RULINGS 11). Expected blocks equal the twins' stdout (recompute_r17.txt).")
row("proj-twins-alone", "PASS", "2.5 labs (twins alone)", "tests/labs/BK4/lab-BK4-project-1..3.py",
    "Each twin run alone as python -I -W error: exit 0 and stdout equal to the page's expected block (recompute_r17.txt, three lines 'True').")
row("proj-r16-new-mutants", "PASS", "2.6 mutation (own mutants, round 16)", "ledgers/BK4/mutants/r16a..r16e",
    "The five round-16 mutants are KILLED in the 97/97 run (out/mutate_graders_r17.txt).")
row("proj-r16-alt6", "PASS", "2.6 autograder (alternatives)", "ledgers/BK4/scripts/BK4-c-r16/alts/alt6_bisect_module.py",
    "alt6 passes seeds 0-49 50/50 (out/alts_seeds0-49.txt, run_alts_r17.py).")
row("proj-r16-blind-prose", "PASS", "2.9 structure (rubric blind)", "course/modules/BK/BK4/project.html:424-489",
    "Blind prose extracted by a script that drops the annotation asides, verdict lines and data-score attributes (out/blind_exemplars_r17.txt); the scores from it match the official scores (see proj-exemplar-*-calibration).")
row("proj-r17-mutants-new", "PASS", "2.6 mutation (own mutants, round 17)", "ledgers/BK4/mutants/r17a..r17e",
    "Five new student-error mutants written from reference.py by make_mutants_r17.py (each change asserted to match once): r17a CCP capital ignores the margin already paid; r17b sizing drops the last loss; r17c margin layer reads the fund table; r17d a zero margin covers nothing; r17e uncovered subtracts the capital again. All KILLED in out/mutate_graders_r17.txt (killers named in mutants).")
row("proj-r17-assert-plain-exception-claim", "PASS", "2.6 autograder (local run, new sentence)", "course/modules/BK/BK4/project.html:400 (sentence on exceptions)",
    "'When your code raises an exception, pytest also prints that exception and the arguments of your function.' Verified by P3 (out/P3_raises_with_args.txt): the KeyError and the learner function's argument values are printed; the must_accept wrapper prints the chained exception. The clause is true as written.")
row("proj-r17-float-message-numbers", "PASS", "2.9 prose vs test (numbers in a message)", "course/modules/BK/BK4/grader/test_project.py:698-699",
    "The float claim in the message is true: (2800/10000)*50 = 14.000000000000002 and its ceiling is 15, while the exact ceiling index is 14 (out/numeric_probes_r17.txt). The claim is accurate; the printed expected value is the defect, see proj-failure-leak.")
row("proj-r17-stretch-wording", "PASS", "2.9 prose (stretch, not graded)", "course/modules/BK/BK4/project.html:497",
    "The new wording 'State which scenario the k-th smallest loss selects at each count, and whether that scenario changes, with the reason.' is open-ended, carries a stated check ('Each extension needs a stated rule and a check against a direct computation', :495) and is not graded (:494).")

all_ids = prev_ids + [i for i in R if i not in prev_ids]
missing = [i for i in prev_ids if i not in R]
assert not missing, missing
rows = []
for i in all_ids:
    status, check, location, evidence = R[i]
    entry = {"id": i, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        entry["fix"] = {
            "proj-failure-leak": "Change the message at test_project.py:697-699 so it contains no number equal to the expected margin or index, for example: '(in floating point, 2800 / 10000 * 50 is not exactly an integer, so its ceiling can come out one too high)'. Then re-run the r12b mutant under QF_SEED=0 and confirm the failure text contains no expected value.",
            "proj-grader-docstring-named-variables": "Fix proj-failure-leak. The docstring at lines 12-14 is then accurate as written.",
            "proj-local-run": "Fix proj-failure-leak. The sentence at project.html:400 is then accurate; its exception clause is already correct.",
        }[i]
    rows.append(entry)

fragment = {
    "unit": "BK4",
    "slice": "BK4-c",
    "round": 17,
    "verifier": "Claude Haiku 5.5, independent verifier E17 for BK4-c (round 17); did not build BK4",
    "pin": "700bf33f (detached; the checkout at /Users/billyribeiro/.fanout/wt/verifyE17-BK4-c)",
    "base": "56cc575a (round-16 pin; the previous fragment's pin). Slice delta, git diff 56cc575a 700bf33f: project.html hunks :397-400 (local-run sentence, now names the exception output), :414-417 (rubric C5 level-4 cell), :494-497 (stretch wording); grader/test_project.py hunks :10-13 (module docstring) and :698-699 (sizing message, adds the float example with the number 14). grader/reference.py, instance.py, starter.py, tests/labs/BK4/* and ledgers/BK4/alternatives/* byte-identical. ledgers/BK4/mutants gained r17a-r17e.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE17-BK4-c",
    "scratch": "temporary workspaces under /tmp/bk4c_r17_* (removed by their scripts); every kept output is under ledgers/BK4/scripts/BK4-c-r17/out/",
    "verified_at": "2026-11-08",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Blind-scoring deviation (disclosed): before running the strip script I read the full project.html, including the data-scores and verdict lines of both exemplars. The exemplar scores in proj-exemplar-a/b-calibration were then taken only from the stripped text (out/blind_exemplars_r17.txt, produced by strip_and_twin_check_r17.py), and the comparison with the official scores was made after that.",
        "The round-16 gate run (out/mutate_graders.txt, 92/92) ran before the five round-17 mutants were written; the 97/97 run (out/mutate_graders_r17.txt) is the one cited.",
        "Equivalence proof location: the round-15 equivalent mutant (r15c) is under scripts/BK4-c-r15/equivalent/, not ledgers/BK4/equivalent/ with a README (FINAL-ARCHITECT-RULINGS 9 wording). The proof is an exhaustive check for S <= 2000 and a random check up to S = 10^7; its argument (float error is far below 1/S for any list that fits in memory) is not written as a README. Not counted as a FAIL here because the page's 'no float appears' sentence (project.html:204) is not a grader-checked behaviour (project.html:215), but the location should be fixed by the owner.",
        "Not checked in this round: the autograder panel and the self-assessment form in a real browser (page_smoke runs the suite in Pyodide and reports PASS, but no screenshot or interaction was taken); the lesson pages L01-L05 and the hub beyond the cross-references used here; the cards (other slice); live network access beyond verify_refs --unit BK4.",
        "The five alternatives were run through the suite (seeds 0-49). They are correct by reading; a float-based alternative was not added.",
        "No PASS row was carried from round 16 except proj-cap-layer-probes and proj-mutant-r15c-equivalent (subjects byte-identical since the previous pin); every other PASS row was re-checked this round with evidence named in its row.",
    ],
    "summary": "BK4-c round 17: 0 blocking defects beyond one message leak. Three FAIL rows: proj-failure-leak (test_project.py:697-699 prints the expected margin 14 on failure, contradicting the page's and the docstring's no-leak promise), and the two rows whose claims it contradicts (proj-grader-docstring-named-variables, proj-local-run). Everything else PASS: gates exit 0, 88 checks collected, 97/97 mutants killed (5 new), 6/6 alternatives plus reference pass seeds 0-49, blind exemplar scores match the official scores, lab outputs and twins match the page, numbers recomputed.",
}
path = ROOT / "ledgers/BK4/BK4-c.json"
path.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "mutants", len(mutants), "FAIL", sum(1 for r in rows if r["status"] != "PASS"))
