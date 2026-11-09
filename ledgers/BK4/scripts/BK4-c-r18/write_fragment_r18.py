"""Round 18 (BK4 slice c, verifier E18): writes ledgers/BK4/BK4-c.json from the outputs under out/.
Every row names the command, file, line or output that supports its status. Usage: python -I write_fragment_r18.py"""
import json
import pathlib
import re
import datetime

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE18-BK4-c")
OUT = ROOT / "ledgers/BK4/scripts/BK4-c-r18/out"

# ---- mutants: 97 pre-existing (mutate_graders run, seeds 0-9) + 4 round-18 (seeds 0-49)
mutants = []
for line in (OUT / "mutate_graders_r18.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    mutants.append({"name": name, "description": desc,
                    "killed_by": killed if status == "KILLED" else None,
                    "status": status, "seeds": "0-9"})
for line in (OUT / "r18_mutants.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    mutants.append({"name": name, "description": desc,
                    "killed_by": killed if status == "KILLED" else None,
                    "status": status, "seeds": "0-49"})
assert len(mutants) == 101, len(mutants)

P = "PASS"
F = "FAIL"
mut_group = ("ledgers/BK4/mutants/ (97 pre-existing mutants; every one KILLED in out/mutate_graders_r18.txt, "
             "mutate_graders BK4: PASS (97/97 killed) for the pre-existing set)")

rows = [
 ("proj-check-tools", "check_pages, check_dag, check_projects exit 0 for BK4", "course/modules/BK/BK4/project.html", P,
  "out/check_pages.txt 'check_pages BK4: PASS'; out/check_dag.txt 'check_dag BK4: PASS'; out/check_projects.txt 'check_projects BK4: PASS'; _exit_codes.txt exit=0 for each"),
 ("proj-ruff", "ruff check and ruff format --check on tests/labs/BK4 and grader", "tests/labs/BK4; course/modules/BK/BK4/grader", P,
  "out/ruff_check.txt 'All checks passed!'; out/ruff_format.txt '12 files already formatted'"),
 ("proj-mypy-repo", "mypy --no-incremental over the repository (strict config)", "pyproject.toml [tool.mypy]", P,
  "out/mypy_repo.txt 'Success: no issues found in 385 source files'"),
 ("proj-mypy-plan-command", "mypy on the grader and labs", "course/modules/BK/BK4/grader/test_project.py:28,:30", P,
  "out/mypy_unit.txt 'Success: no issues found in 12 source files'; test_project.py:28 and :30 carry the type-ignore lines"),
 ("proj-pytest-labs", "pytest -k BK4 over tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_memo_exemplars.py", "tests/", P,
  "out/pytest_BK4.txt: 8 passed, exit 0"),
 ("proj-page-smoke", "page_smoke --pages project (in-browser grader run in Pyodide)", "course/modules/BK/BK4/project.html", P,
  "out/page_smoke_project.txt: 'page_smoke BK4: PASS', 'in-browser grader: All 88 tests pass on seed 1794260670'"),
 ("proj-refs", "data-cite keys resolve to admitted registry records used by BK4", "project.html:505-506", P,
  "references/references.json entries 'duffie2011central' (used_by ['BK4']) and 'bisndcpmi' (used_by ['BK4'], url https://www.bis.org/committees/cpmi/publications); out/verify_refs_offline.txt 'offline integrity: 560 entries, 0 problems'"),
 ("proj-anchors-links", "every in-page anchor and cross-file link resolves", "course/modules/BK/BK4/project.html", P,
  "every href target exists: #conventions, #rubric-heading, #self-assessment, #spec, #grader-section, #report, #stretch (each id appears once); index.html#placement (index.html:69); L01.html, L03.html, L05.html, grader/*.py exist"),
 ("proj-banned-and-process-words", "no process or banned words in learner-facing text", "project.html; grader/*.py; tests/labs/BK4/lab-BK4-project-*.py", P,
  "grep -i for builder|verifier|fixer|round N|slice|todo|draft|placeholder over those files: no match"),
 ("proj-dag-concepts", "concepts used in project.html are in the prerequisite closure", "course/modules/BK/BK4/project.html", P,
  "out/check_dag.txt 'check_dag BK4: PASS'; project.html contains no <dfn> and no data-concept link"),
 ("proj-notation-T", "every symbol on the page agrees with notation/notation.json", "project.html:200,:220-225", P,
  "notation/notation.json holds 8 symbols (T, \\\\Phi, \\\\gamma_3, \\\\gamma_4, R^\\\\ast, R^{e\\\\ast}, R_f, \\\\mathbb{Q}); the project uses S, t, k, K, R, D, DF_i, IM_d, a1-a3 and none of the registered symbols"),
 ("proj-l03-crossref", "Lesson 3 supports the page's cover, sizing and close-out cross-references", "project.html:224,:417,:54; L03.html:134,:152,:419", P,
  "L03.html:134 defines the margin cover floored in basis points; L03.html:152 gives k = ceil(tS/10000) under A3, A4; L03.html:419 'No close-out period is modelled' (Section 3 spans L03.html:415-426); project.html:417 cites Section 3 correctly"),
 ("proj-grade-scale-citation", "the B and C grade scale on the page matches Lesson 1", "project.html:421; L01.html:45-46", P,
  "L01.html:45 'B ... published, not settled'; L01.html:46 'C ... working paper, practitioner research or single sample'; project.html:421 paraphrases both"),
 ("proj-reading-list-no-claim", "the reading list attributes no statement", "project.html:501-508", P,
  "the reading section lists two data-cite entries and states 'This page attributes no statement to either'; no finding is attributed"),
 ("proj-atlas-studio", "no Atlas entry or studio requirement is stated for BK4", "course/modules/BK/BK4; curriculum/curriculum.json atlas", P,
  "python: 'atlas BK4: 0' of 20 atlas entries mention BK4; the page names no studio"),
 ("proj-lab1-numbers", "every number in Lab 1 prose and hypothesis matches the printed output", "project.html:56-139; tests/labs/BK4/lab-BK4-project-1.py", P,
  "out/lab_page_twin_check.txt: page code == twin, output == expected; recompute_r18.txt re-derives layers 50000/6000/20000, residual 4000, floors 1333/1666/1000, leftover 1, k=39 (191/5 = 38.2), margin 117088, covers 9750 and 9500"),
 ("proj-lab2-numbers", "Lab 2 completion blanks and expected output match the completed twin", "project.html:142-190; tests/labs/BK4/lab-BK4-project-2.py", P,
  "out/lab_page_twin_check.txt: output == expected; diff of page code vs twin differs only at the two blanks (shares and index lines)"),
 ("proj-lab3-numbers", "Lab 3 prose numbers (margins, covers, counts) match the printed output", "project.html:253-368; tests/labs/BK4/lab-BK4-project-3.py", P,
  "out/lab_page_twin_check.txt: page code == twin; output == expected; recompute_r18.txt: margins 105154, 111074, 117088; covers 9000/9500/9750; one-cent-below 8750/9250/9500; largest loss 118151"),
 ("proj-labs-simulated-stdlib", "labs use SIMULATED inputs, read no file, and import only the standard library", "tests/labs/BK4/lab-BK4-project-1..3.py; project.html:54,:56-58", P,
  "imports: lab-1 random, fractions; lab-2 random; lab-3 random; grep for open(, urllib, socket, http: none; project.html:54 'all of its amounts are SIMULATED ... no file is read'"),
 ("proj-lab2-learner-text", "Lab 2 hypothesis and interpretation describe the code and output", "project.html:143-146,:190", P,
  "the completed expressions give shares 1334/1666/1000 and index 39 (out/lab_page_twin_check.txt); the 1e-6 tolerance is labs.js:50 'tol*(1 + |expected|)', under one cent for 117088"),
 ("proj-lab3-claim-checks-rules", "Lab 3 claim-check sentences match the code and output", "project.html:255,:367", P,
  "Part A conservation column True in all five rows (out); only the 100000 row has uncovered 12000; Part C 9000 row past margin 4, past fund 2, capital 0 (out)"),
 ("proj-rung-ladder", "the ladder lists four rungs with the stated content", "project.html:41-50", P,
  "four li rungs in order; rung 1 = Lab 1, rung 2 = Lab 2 (instant check), rung 3 = spec/grader/memo, rung 4 = stretch, not graded (project.html:494)"),
 ("proj-hours", "hub hours split and project hours agree", "project.html:34,:36,:374-386; index.html:29,:39,:42,:162-174", P,
  "project.html:34 data-hours-project=15; index.html:29 data-hours-lessons=35, data-hours-project=15; 35 + 15 = 50; rubric table rows 2+2+3+3+2+2+1 = 15 (project.html:377-384)"),
 ("proj-hours-estimates", "the time-budget rows sum to the stated total", "project.html:377-383", P,
  "2+2+3+3+2+2+1 = 15, matching the Total row (project.html:384) and 15 of 50 hours = 30 %"),
 ("proj-named-conditions", "each named condition on the page has a test on both sides of its limit", "project.html:204-212; grader/test_project.py:467-609, 893-986", P,
  "page list (6 items) mapped to tests: negative loss, margin, fund, capital refused and zero accepted; defaulter below/above/between refused and lowest/highest accepted; target 0 and 10001 refused, 1 and 10000 accepted; empty losses refused and one scenario accepted; negative loss refused in both functions"),
 ("proj-conventions-prose", "Conventions formulas match the rules the tests check", "project.html:220-225", P,
  "a1, a2, a3, R, share_i = (R*DF_i)//D, leftover rule, cover = (10000*#{L<=M})//S and k = -((-t*S)//10000) are the formulas in reference.py:57-100 and oracles in test_project.py:58-102"),
 ("proj-fixture-tables", "the hand-computed fixtures are right and each is tested", "project.html:230-251; grader/test_project.py:276-350, 378-438, 650-687, 781-794", P,
  "re-derived in recompute_r18.txt: layer table rows 80..300, remainder 1/2/4 cents, sizing 8000->40, 8001->50, 10000->50, 5000 of 4 ->20, cover 3333 and 6666; all 11 layer rows, 3 remainder rows and 4 sizing rows have a test"),
 ("proj-money-integer-claim", "money outputs are ints in cents and computed in integers (grader-checked part)", "project.html:204,:225; grader/test_project.py:128-132, 186-194, 450-459", P,
  "checked_int rejects floats and bools (test_project.py:128-132); test_large_cent_shares_are_floored_in_integers covers products above 2**53 (recompute: product 4.4e31 > 2**53); page line 204's 'no float appears' is a method constraint the page excludes from grading (project.html:215)"),
 ("proj-large-cent-claim", "the large-cent test expects the values the rules give", "grader/test_project.py:450-459", P,
  "recompute_r18.txt: floors 6055950114045319 and 529746839784068, leftover 1 to member 1 (first survivor with a positive fund) gives 6055950114045320, the expected value; the sum equals the loss"),
 ("proj-sizing-duplicate-losses", "repeated losses count once per occurrence", "grader/test_project.py:703-717", P,
  "[5,5,10,20] at 5000 -> k=2 -> 5; [5,5,5,9,12] at 6000 -> k=3 -> 5; both match the test and the rule"),
 ("proj-zero-loss-sizing", "a zero loss is a scenario in the sizing", "grader/test_project.py:720-727", P,
  "[0,10,20,30] at 5000 -> k=2 -> 10, matching the test"),
 ("proj-zero-loss-cover", "a zero loss is in the cover denominator", "grader/test_project.py:837-842", P,
  "[0,0,5,9] at margin 0 -> 2 of 4 covered -> 5000 bps, matching the test"),
 ("proj-remainder-spec", "the remainder rule text matches the tests", "project.html:221; grader/test_project.py:378-438", P,
  "remainder 1 -> {1:1,2:0,3:0}; 2 -> {1:1,2:1,3:0}; 3 -> pays in full; 4 -> uncovered 1 (recompute_r18.txt 'remainder')"),
 ("proj-survivor-leftover-order", "leftover cents go to the first survivors by ascending id, not by dictionary order", "grader/test_project.py:428-437", P,
  "the dictionaries list members 3,1,2,4; the one leftover cent goes to member 1 (test_project.py:434, exact dictionary)"),
 ("proj-silence-named-refusals", "no function prints or warns on a valid call or a named refusal", "grader/test_project.py:1035-1084", P,
  "capsys checks stdout and stderr empty for 4 valid calls and 15 named refusals; pytestmark filterwarnings('error') makes any warning an exception that must_refuse does not swallow"),
 ("proj-refusal-count-docstring", "the refusal-count sentence matches the list", "grader/test_project.py:1047-1049, :1050-1081", P,
  "the docstring says 'each named refusal in the list below' and the list has 15 entries, each a ValueError condition from project.html:205-211"),
 ("proj-grader-docstring-named-variables", "module docstring: failing checks never print an expected value and the failing line shows the source of the check", "grader/test_project.py:9-15 (line 13-14 claims; the 'source of the check' clause at :14)", F,
  "the 'never prints an expected value' claim holds: failure messages name properties and inputs only (grep of pytest.fail/assert messages; probe r12b output shows no expected value). The clause 'a failing line shows the source of the check' is contradicted by observed output: with --assert=plain every test frame is hidden and the output is only the message line ('All traceback entries are hidden. Pass --full-trace to see hidden and internal frames.'), see the probe run in out/ and /tmp/bk4c_r18_floor.txt"),
 ("proj-failure-leak", "a failing check does not print the expected value", "grader/test_project.py:690-700", P,
  "the round-17 leak (the message named 14) is gone: test_project.py:696-700 names no expected value; probe with a float-index mutant (r12b) prints the message only, and '14' does not occur in its output (checked this round)"),
 ("proj-context-sentences", "the context paragraph's claims match the grader and the instance", "project.html:198", P,
  "'The autograder checks the cent results and the cover values, not the docstring or the imports' matches test_project.py (no docstring or import test)"),
 ("proj-spec-context-length", "the context paragraph is accurate on the rules it states", "project.html:198", P,
  "the layer order and the three named outputs match conventions (project.html:220-225) and reference.py"),
 ("proj-spec-signatures", "the required names and signatures match the starter", "project.html:202; grader/starter.py:19-47", P,
  "starter.py: Waterfall fields margin_cents, default_fund_cents, ccp_capital_cents, survivor_cents, uncovered_cents; waterfall(loss_cents, defaulter_id, initial_margin_cents, default_fund_cents, ccp_capital_cents); margin_for_cover(losses_cents, target_bps); cover_bps(losses_cents, margin_cents): all as page line 202"),
 ("proj-spec-inputs-instance", "the stated inputs match what instance.py generates", "project.html:200; grader/instance.py:22-50", P,
  "instance.py: N = randint(4,6) members with ids 1..N; default funds >= 1000 cents; scenarios randint(40,80); targets (9000, 9500, 9750); label 'SIMULATED ... not market data'; checked on seeds 0-49 by run_graders"),
 ("proj-spec-questions", "the spec asks no clarifying questions and names every input", "project.html:196-216", P,
  "read in full; no question to the learner; the required outputs are named in page line 202"),
 ("proj-local-run", "the local command and the exception sentence match what pytest prints", "project.html:397-400", P,
  "ran the page's command verbatim on the reference copy: 'QF_SEED=0 pytest -q -p no:cacheprovider --assert=plain -W error test_project.py' -> 88 passed; the seed note matches grader.js:53 ('Locally: QF_SEED=... pytest -q -p no:cacheprovider --assert=plain -W error ...'); an uncaught exception from a student function prints the exception and its arguments (loss_cents = 181, defaulter_id = 3, ... in the probe output /tmp/bk4c_r18_raise.txt)"),
 ("proj-autograder-claims", "the autograder claims (88 checks, warnings as errors, monotonicity, silence, purity, two cases)", "project.html:215; grader/test_project.py", P,
  "pytest --collect-only: 88 tests; monotonicity tests at test_project.py:759-767 and 857-865; silence 1036-1085; purity 253-260, 1088-1096; two cases INST and INST2 (lines 35-36)"),
 ("proj-pyodide-empty-packages", "the in-browser run needs no extra packages and matches the local run", "project.html:393; grader/test_project.py:17-30", P,
  "page_smoke ran the suite in the in-browser grader: All 88 tests pass; the local pytest run with the same flags gives 88 passed"),
 ("proj-round7-prose-delta", "prose numbers and statements changed since round 7 are correct", "project.html:38,:45,:54,:58,:215", P,
  "re-derived: 9550 bps -> 191/5 = 38.2 -> k 39; 2 scenario-count facts; 'pro rata' and 'floored' defined at :54; 88 checks at :215 = collect-only count"),
 ("proj-exemplar-a-calibration", "exemplar A official scores (data-scores) are the blind scorer's scores", "project.html:426 data-scores=\"2,2,1,2,2\"; :428 official scoring", P,
  "delegated to the blind scorer per ruling 23; its result (A = [2,2,1,2,2]) equals the page's data-scores and the official text at :428; exemplar scores not scored by this verifier"),
 ("proj-exemplar-b-calibration", "exemplar B official scores (data-scores) are the blind scorer's scores", "project.html:457 data-scores=\"4,4,4,4,4\"; :459 official scoring", P,
  "delegated to the blind scorer per ruling 23; its result (B = [4,4,4,4,4]) equals data-scores and the official text at :459"),
 ("proj-exemplar-b-numbers", "exemplar B numbers are printed by Lab 1/3 or are rule computations or differences of printed numbers", "project.html:459-471", P,
  "111074 (Part B and C), 105154, 117088, 9250 (one cent below 9500 target), 4 and 2 scenario counts (Part C), 80000 layer sum, 1334+1666+1000 = 4000, 5920 = 111074-105154, 500 = 9500-9000; each matches out/ or recompute_r18.txt"),
 ("proj-rubric-c1-levels", "rubric C1 levels are observable", "project.html:413", P,
  "four descriptors name layers, amounts for a stated scenario and the 'used only after' statement; observable"),
 ("proj-rubric-c2-levels", "rubric C2 levels are observable", "project.html:414", P,
  "descriptors name target in bps, k, sorted position, cover at margin and one cent below"),
 ("proj-rubric-c3-descriptors", "rubric C3 descriptors are observable", "project.html:415", P,
  "descriptors name the pro rata and leftover rules and the sum check"),
 ("proj-rubric-c4-descriptors", "rubric C4 descriptors are observable", "project.html:416", P,
  "descriptors name the recommended margin, its cover, the count past the survivors and one alternative"),
 ("proj-rubric-c5-descriptor", "rubric C5 descriptors are observable", "project.html:417", P,
  "descriptors name the four limits, direction of bias and counter-evidence statement; Lesson 3 Section 3 cross-reference correct (L03.html:419)"),
 ("proj-rubric-observable-wording", "rubric wording is observable, not vague", "project.html:409-417", P,
  "the descriptors name countable items (layers, cents, k, cover, counts, limits); no 'good' or 'clear' descriptor"),
 ("proj-exemplar-annotations-agree", "exemplar annotations agree with the data-scores and the official text", "project.html:426-489 (annotations 446-451 and 475-479)", P,
  "A: annotations give C1 2, C2 2 (and miss level 3), C3 1, C4 2, C5 2 = data-scores 2,2,1,2,2; B: annotations all level 4 = data-scores 4,4,4,4,4"),
 ("proj-rubric-self-form", "the self-assessment form is wired to the rubric and exemplars", "project.html:485-489; course/assets/js/site.js:163; rubric.js:223", P,
  "site.js:163 selects section.rubric-self[data-rubric]; rubric.js:223 uses [data-rubric-form]; the form itself was not exercised in a browser (see notes)"),
 ("proj-alternatives", "five different correct alternatives and the reference pass seeds 0-49", "ledgers/BK4/alternatives/alt1..alt5; scripts/BK4-c-r16/alts/alt6_bisect_module.py", P,
  "out/alts_seeds0-49.txt: alt1 50/50, alt2 50/50, alt3 (Fraction) 50/50, alt4 50/50, alt5 (bisection) 50/50, alt6 50/50, reference 50/50"),
 ("proj-mutants-builder", "the builder's mutants m01-m10 are killed", "ledgers/BK4/mutants/m01-m10", P,
  "out/mutate_graders_r18.txt: m01-m10 all KILLED"),
 ("proj-mutants-own", "the own mutants n1-n4 are killed", "ledgers/BK4/mutants/n1-n4", P,
  "out/mutate_graders_r18.txt: all four KILLED"),
 ("proj-mutants-round7", "round-7 mutants are killed", mut_group, P, "out/mutate_graders_r18.txt: s01-s05 KILLED (5/5)"),
 ("proj-mutants-round8", "round-8 mutants are killed", mut_group, P, "out/mutate_graders_r18.txt: t8a-t8e KILLED (5/5)"),
 ("proj-mutants-round9", "round-9 mutants are killed", mut_group, P, "out/mutate_graders_r18.txt: v9a-v9e KILLED (5/5)"),
 ("proj-mutants-round10", "round-10 mutants are killed", mut_group, P, "out/mutate_graders_r18.txt: x10a-x10d KILLED (4/4)"),
 ("proj-mutants-round11", "round-11 mutants are killed", mut_group, P, "out/mutate_graders_r18.txt: y11a-y11d KILLED (4/4)"),
 ("proj-mutants-round12", "round-12 mutants are killed", mut_group, P, "out/mutate_graders_r18.txt: r12a-r12d KILLED (4/4)"),
 ("proj-mutants-vc", "vc-series mutants are killed", mut_group, P, "out/mutate_graders_r18.txt: vc01-vc10 and vc12-vc15 KILLED (14 files; vc11 does not exist)"),
 ("proj-mutant-float-index", "the float index mutant is killed", "ledgers/BK4/mutants/r12b_sizing_index_float.py", P,
  "out/mutate_graders_r18.txt: r12b KILLED; probe output /tmp/bk4c_r18_r12b.txt: 1 failed, test_exact_position_is_an_integer_index_not_a_rounded_float"),
 ("proj-mutant-float", "float-arithmetic mutants are killed", "ledgers/BK4/mutants/vc10_float_arithmetic.py; r12b", P,
  "out/mutate_graders_r18.txt: vc10 KILLED by test_large_cent_shares_are_floored_in_integers (seed 0)"),
 ("proj-mutant-argument", "mutants that change arguments are killed", "ledgers/BK4/mutants/r4f, r16e, t8e", P,
  "out/mutate_graders_r18.txt: r4f, r16e, t8e KILLED"),
 ("proj-mutants-round13", "round-13 mutants are killed", mut_group, P, "out/mutate_graders_r18.txt: r13a-r13d KILLED (4/4)"),
 ("proj-mutant-fund-capped-at-pool", "the fund-capped-at-pool mutant is killed", "ledgers/BK4/mutants/r13d_fund_layer_capped_at_survivor_pool.py", P,
  "out/mutate_graders_r18.txt: r13d KILLED"),
 ("proj-cap-layer-probes", "capital-layer probes (not counted)", "ledgers/BK4/scripts/BK4-c-r13/probes_r13.py", P,
  "Carried from round 17 (ledgers/BK4/scripts/BK4-c-r13/ byte-identical since the previous pin): git diff 700bf33f 50559266 lists no change under that path"),
 ("proj-direction-claims", "directional claims about bias are correct", "project.html:469,:471", P,
  "one default at a time: a larger loss cannot lower the k-th smallest and cannot raise the count at or below a margin, so the sized margin is biased low and the cover high (correct); stress: margins held fixed so rising margins bias the simulated cover low (correct)"),
 ("proj-scope-words", "scope words (every, all, any, never) are backed by a computation or a stated hypothesis", "project.html:54,:139,:200,:215,:255,:367,:400", P,
  "'every amount', 'every cover', 'all of its amounts' are definitional for the simulator; 'every scenario' (:215) is the test loop; 'every one of them' (:229) matches all fixtures tested"),
 ("proj-numbers-rounding", "rounded numbers state their rule", "project.html:58,:112-113,:139,:251,:384", P,
  "6666.67 to two places (:251) = 20000/3; 38.2 (:58, :139) exact; 30 % = 15/50; floors stated where used"),
 ("proj-page-prose-delta-ruling", "the page follows the binding plan and rulings", "plans/BK4-build-plan.md:751; plans/FINAL-ARCHITECT-RULINGS.md:9, :10, :22", P,
  "ruling 9 (survivor in mutants must be killed) is violated by r18a (new row proj-r18-mutate-all); ruling 22 (equivalents in ledgers/BK4/equivalent with README) now met; ruling 10 (five alternatives) met"),
 ("proj-grader-reference-run", "the reference passes the suite on seeds 0-49", "course/modules/BK/BK4/grader/reference.py", P,
  "out/run_graders.txt: 'run_graders BK4: PASS (reference 50/50 seeds)'; local runs seeds 0-2 each 88 passed"),
 ("proj-grader-starter-fails", "the starter fails with a named message and no traceback", "course/modules/BK/BK4/grader/starter.py", P,
  "starter run: 84 failed, 4 passed (the 4 do not call the student module), 0 'Traceback' lines, each failure names the test and 'has no implementation for waterfall/margin_for_cover/cover_bps'"),
 ("proj-collect-count", "the collect-only count equals the page's 88", "course/modules/BK/BK4/grader/test_project.py; project.html:215", P,
  "pytest --collect-only -q: '88 tests collected'"),
 ("proj-instances", "instance.py produces valid cases", "course/modules/BK/BK4/grader/instance.py", P,
  "test_seeded_cases_are_valid and test_each_seeded_case_has_a_loss_in_each_region pass for seeds 0-49 (run_graders); the case shape matches project.html:200"),
 ("proj-placement-claim", "the hub placement claim matches the page", "project.html:43; index.html:69-71,:160-174", P,
  "index.html:69 placement section (data-mastery 0.8, eight items, two skill checks on rungs 1 and 2); project.html:43 says skip rungs 1 and 2 with the mastery bar and both skill checks, which matches"),
 ("proj-mutants-round14", "round-14 mutants are killed", mut_group, P, "out/mutate_graders_r18.txt: r14a-r14d KILLED (4/4)"),
 ("proj-page-test-count-line", "the page's test-count sentence equals the collect-only count", "project.html:215", P,
  "'runs 88 checks' = 88 collected (proj-collect-count)"),
 ("proj-mutants-r15", "round-15 mutants are killed", mut_group, P, "out/mutate_graders_r18.txt: r15a, r15b, r15d, r15e KILLED (r15c is equivalent and lives in ledgers/BK4/equivalent)"),
 ("proj-mutant-r15c-equivalent", "the equivalent float-floor mutant is proven equivalent and filed under equivalent/", "ledgers/BK4/equivalent/r15c_cover_float_floor.py; ledgers/BK4/equivalent/README.md", P,
  "ruling 22: the file and README now live in ledgers/BK4/equivalent/; re-ran ledgers/BK4/scripts/BK4-c-r15/equivalent_check_r15c.py: 'exhaustive S<=2000: 2003000 pairs, disagreements 0' and 'random S<=10^7: 200000 pairs, disagreements 0' (out/equivalent_check_r18.txt); the README proof's arithmetic checked (2^53/10000 = 9.007e11 > 9e11)"),
 ("proj-lab-page-twin", "page lab code equals the twin; expected block equals output", "project.html lab blocks; tests/labs/BK4/lab-BK4-project-1..3.py", P,
  "out/lab_page_twin_check.txt: lab-1 and lab-3 page code == twin; lab-2 differs only at the two blanks; all three expected blocks == output"),
 ("proj-twins-alone", "each twin runs alone under python -I -W error", "tests/labs/BK4/lab-BK4-project-1..3.py", P,
  "out/lab_page_twin_check.txt: exit 0 and empty stderr for lab-1, lab-2, lab-3; out/run_labs_project.txt 'run_labs BK4: PASS (3/3)'"),
 ("proj-r16-new-mutants", "round-16 mutants r16a-r16e are killed", "ledgers/BK4/mutants/r16a..r16e", P,
  "out/mutate_graders_r18.txt: r16a-r16e KILLED"),
 ("proj-r16-alt6", "alternative 6 passes seeds 0-49", "ledgers/BK4/scripts/BK4-c-r16/alts/alt6_bisect_module.py", P,
  "out/alts_seeds0-49.txt: alt6_bisect_module.py 50/50"),
 ("proj-r16-blind-prose", "rubric blind prose (exemplar text) is consistent with the rubric", "project.html:424-489", P,
  "exemplar A and B prose read in full; each quoted number is from Lab 1/3 or a rule computation; no process words"),
 ("proj-r17-mutants-new", "round-17 mutants r17a-r17e are killed", "ledgers/BK4/mutants/r17a..r17e", P,
  "out/mutate_graders_r18.txt: r17a-r17e KILLED"),
 ("proj-r17-assert-plain-exception-claim", "the --assert=plain exception sentence is accurate", "project.html:400", P,
  "observed: with --assert=plain, a raised exception shows the exception and the function's arguments (probe /tmp/bk4c_r18_raise.txt); a failing check shows only its message"),
 ("proj-r17-float-message-numbers", "the float example in the message uses numbers the page supports", "grader/test_project.py:696-700", P,
  "message text now: '(in floating point, 2800 / 10000 * 50 is not exactly an integer, so its ceiling can come out one too high)'; 2800/10000*50 = 14.000000000000002 (Python, recompute_r18.txt); the message names no expected number"),
 ("proj-r17-stretch-wording", "the stretch section is not graded and its wording is accurate", "project.html:492-499", P,
  "'Not graded.' at :494; each extension names a rule and a check"),
 ("proj-r18-mutate-all", "every mutant in ledgers/BK4/mutants is killed (ruling 9)", "ledgers/BK4/mutants/r18a_full_cover_margin_is_last_loss_given.py; grader/test_project.py:672-678; project.html:202", F,
  "tools/mutate_graders.py --unit BK4 (seeds 0-9): 100 of 101 KILLED; r18a SURVIVED on seeds 0-49 (out/r18_mutants.txt). r18a returns losses_cents[-1] at target 10000. page line 202 states 'returns the least margin in cents whose cover is at least target_bps'; for 10000 bps the least margin is the largest loss. The only 10000-bps test (test_project.py:672-678) uses the sorted list [10,20,30,40,50], so it cannot tell last from largest. A probe test with [30,50,10,20] -> 50 kills r18a and the reference still passes 89/89 (scripts/BK4-c-r18/probe_r18a_fix.py; out/probe_r18a_fix.txt: r18a exit 1, reference exit 0)",
  "add a grader test with an unsorted list at full cover, e.g. def test_full_target_margin_is_the_largest_loss_in_any_order(): assert sol.margin_for_cover([30, 50, 10, 20], 10_000) == 50 (place it after test_fixture_five_losses_at_10000_bps_gives_the_largest_loss); re-run mutate_graders --unit BK4 and require 101/101 killed"),
 ("proj-r18-new-mutants", "round-18 mutants r18b-r18d are killed", "ledgers/BK4/mutants/r18b, r18c, r18d", P,
  "out/r18_mutants.txt: r18b KILLED by test_each_scenario_matches_the_oracle_on_both_instances; r18c KILLED by test_layers_and_survivor_payments_add_to_the_loss_on_every_scenario; r18d KILLED by test_waterfall_is_a_frozen_dataclass_with_the_named_fields (seeds 0-49)"),
 ("proj-r18-delta-read", "every hunk changed since the round-17 pin is read and re-verified", "git diff 700bf33f 50559266 for course/modules/BK/BK4, tests/labs/BK4, ledgers/BK4", P,
  "changed: grader/test_project.py:698-699 (message only, re-verified in full); ledgers/BK4/equivalent/ (README + r15c, re-verified); ledgers/BK4/mutants r17a-r17e (killed); cards.json (outside this slice, BK4-c107 added; not verified here); plans/FINAL-ARCHITECT-RULINGS.md rulings 21-23 read"),
]
seen = set()
row_objs = []
for rid, check, loc, status, ev, *rest in rows:
    assert rid not in seen, rid
    seen.add(rid)
    r = {"id": rid, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != P:
        r["fix"] = rest[0] if rest else ""
    row_objs.append(r)
# fix the two FAIL rows that carry their own fix text
for r in row_objs:
    if r["id"] == "proj-grader-docstring-named-variables" and not r.get("fix"):
        r["fix"] = "reword test_project.py:14 to 'so a failing check shows only its message, and never the values it compared'"

round17 = json.loads((pathlib.Path("/Users/billyribeiro/.fanout/frags/E-BK4-c.round17.json")).read_text(encoding="utf-8"))
missing = [r["id"] for r in round17["rows"] if r["id"] not in seen]
assert not missing, missing

verdict = "PASS" if all(r["status"] == P for r in row_objs) and all(m["killed_by"] for m in mutants) else "FAIL"
fragment = {
    "unit": "BK4",
    "slice": "BK4-c",
    "round": 18,
    "verifier": "Claude Haiku 5.5, independent verifier E18 for BK4-c (round 18); did not build BK4",
    "pin": "50559266 (detached; checkout /Users/billyribeiro/.fanout/wt/verifyE18-BK4-c)",
    "base": "700bf33f (round-17 pin, from /Users/billyribeiro/.fanout/frags/E-BK4-c.round17.json). Slice delta 700bf33f..50559266: grader/test_project.py:698-699 (message only); ledgers/BK4/equivalent/ (README and r15c, moved from scripts per ruling 22); ledgers/BK4/mutants r17a-r17e. project.html, grader/reference.py, instance.py, starter.py, tests/labs/BK4/*, ledgers/BK4/alternatives/* byte-identical to the base.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE18-BK4-c",
    "scratch": "scratch workspaces removed by their scripts; scripts/BK4-c-r18/probe_r18a_fix.py (probe; output out/probe_r18a_fix.txt), /tmp/bk4c_r18_*.txt (probe outputs); kept outputs under ledgers/BK4/scripts/BK4-c-r18/out/",
    "verified_at": "2026-11-08",
    "verdict": verdict,
    "rows": row_objs,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [
        "grader/test_project.py changed at 50559266 (message at :698-699): whole file re-read and re-run this round",
        "ledgers/BK4/equivalent/ is new since the base (ruling 22): README and r15c re-checked",
        "plans/FINAL-ARCHITECT-RULINGS.md gained rulings 21-23 at 50559266: read; ruling 23 applied (exemplar scores by the blind scorer)",
    ],
    "notes": [
        "Exemplar scoring is not done here (ruling 23). The blind scorer's result (~/.fanout/blind/BK4-c.json, score arrays A=[2,2,1,2,2], B=[4,4,4,4,4]) equals the page's data-scores (project.html:426, :457). Only the score arrays were read; no competitor content was opened.",
        "Surviving mutant: r18a (ledgers/BK4/mutants/r18a_full_cover_margin_is_last_loss_given.py) is a new student-error mutant that survives 50/50 seeds. Ruling 9 forbids survivors in mutants/. The fix is a grader test, not a move to equivalent/, because page line 202 states the behaviour it violates.",
        "Mutation count: 101 files in ledgers/BK4/mutants (97 pre-existing, all KILLED; 4 new: r18a SURVIVED, r18b-d KILLED). The mutate_graders run on seeds 0-9 covers the 97; the four new ones were run on seeds 0-49 with the same workspace logic (scripts/BK4-c-r18/run_r18_mutants.py).",
        "Alternatives: six alternatives (alt1-alt5, alt6 archived under scripts/BK4-c-r16) and the reference each pass seeds 0-49 (out/alts_seeds0-49.txt). No new alternative was added.",
        "Equivalent README claim checked: scripts/BK4-c-r15/equivalent_check_r15c.py re-run, output as the README states. The README's pointer to fragment row proj-mutant-r15c-equivalent is stale in its script docstring (cosmetic; not a row).",
        "The blocking item for this slice is r18a. The docstring clause at test_project.py:14 is a second, minor FAIL. All other rows PASS.",
        "Not checked: the autograder panel and the self-assessment form in a real browser (page_smoke ran the suite in Pyodide, no screenshot); the live verify_refs run (offline only, as the gate lists); the cards (cards.json is another slice; it changed at 50559266 with BK4-c107); Duffie and Zhu (2011) and the CPMI pages (not read; the page attributes no statement to them); the grader.js save-as-you-type behaviour beyond the input listener at grader.js:59-62.",
    ],
    "summary": ("BK4-c round 18: FAIL. 2 FAIL rows: proj-r18-mutate-all (mutant r18a survives 50/50 seeds: margin_for_cover at 10000 bps returns the last loss; page line 202 states the least-margin behaviour; the fix is an unsorted full-cover test, verified to kill r18a with the reference still at 89/89) and proj-grader-docstring-named-variables (test_project.py:14 says a failing line shows the source; observed output hides all test frames). Round-17 FAILs proj-failure-leak and proj-local-run now PASS. Gates exit 0: check_pages, check_dag, check_projects, run_labs, run_graders (50 seeds), page_smoke, ruff, mypy, verify_refs --offline, pytest BK4; 88 collected; alternatives 50/50 each."),
}
out = ROOT / "ledgers/BK4/BK4-c.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(row_objs), "mutants", len(mutants), "verdict", verdict)
