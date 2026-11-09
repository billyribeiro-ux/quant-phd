"""Round 15, FC1-c: write ledgers/FC1/FC1-c.json from the rows and the mutation output of this round (python -I).

Usage: python -I build_fragment_r15.py <checkout>
Mutant rows are parsed from out/mutate_FC1_s0-9_final.out (tools/mutate_graders.py, seeds 0-9).
"""

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

checkout = Path(sys.argv[1])
scripts = "ledgers/FC1/scripts/FC1-c-r15"
out = f"{scripts}/out"

mutants = []
for line in (checkout / out / "mutate_FC1_s0-9_final.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, description, killed = m.groups()
    killed_by = None
    if status == "KILLED":
        killed_by = re.sub(r" \(seed \d+\)$", "", killed).strip()
    mutants.append({"id": name, "name": name, "description": description, "killed_by": killed_by})

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

R = []
R.append(row("proj-run-graders", "2.6-autograde-reference",
    "course/modules/FC/FC1/grader/reference.py; tools/run_graders.py",
    "PASS", f"`tools/run_graders.py --unit FC1 --seeds 0-49` -> 'run_graders FC1: PASS (reference 50/50 seeds, slowest 0.5 s)' ({out}/run_graders_s0-49.out)."))
R.append(row("proj-collect-count-65", "2.6-page-count",
    "course/modules/FC/FC1/project.html line 171; grader/test_project.py",
    "PASS", f"`pytest --collect-only` on a scratch copy (reference as instruments.py): '97 tests collected' ({out}/collect_count_r15.out). project.html line 171 says 'runs 97 checks'. The id keeps the historical text '65' for tracking only."))
R.append(row("proj-browser-suite", "2.6-autograder-both",
    "course/modules/FC/FC1/project.html line 302 (section#grader); course/assets/js/grader.js lines 53, 95; course/assets/js/py-worker.js line 111",
    "PASS", f"grader.js sends QF_SEED and runs the suite with pytest flags '--assert=plain -W error' (py-worker.js line 111), the same as the local command quoted at grader.js line 53. `page_smoke.py --unit FC1 --pages project` -> 'in-browser grader: All 97 tests pass on seed 1041238696' with the reference, labs 1-3 pass in Pyodide, 'page_smoke FC1: PASS' ({out}/page_smoke_FC1_project.out)."))
R.append(row("proj-alternatives-five", "2.6-alternatives",
    "ledgers/FC1/alternatives/a1..a5 (run against grader/test_project.py)",
    "PASS", f"`{scripts}/alt_run_r15.py` (seeds 0-49, browser flags): a1, a2, a3, a4, a5 each 'PASS ... failing seeds 0/50' ({out}/alternatives_and_reference_s0-49.out)."))
R.append(row("proj-alternatives-integer-only", "2.6-alternatives",
    "ledgers/FC1/scripts/FC1-c-r14/alt_integer_only_r14.py",
    "PASS", f"Same run: alt_integer_only_r14.py 'PASS ... failing seeds 0/50' ({out}/alternatives_and_reference_s0-49.out)."))
R.append(row("proj-alternatives-new-r15", "2.6-alternatives (new in round 15)",
    f"{scripts}/alternatives/alt_decimal_100_digits_r15.py; {scripts}/alternatives/alt_cached_lists_r15.py",
    "PASS", f"Two new correct styles, both 'PASS ... failing seeds 0/50' over seeds 0-49 ({out}/alt_new_r15_s0-49.out): (a) decimal.Decimal at 100 significant digits with ROUND_HALF_UP, type-checked; (b) events computed once in __init__ and returned as fresh lists of lists, Fraction price with half-away rounding."))
R.append(row("proj-instances-20", "2.6-instances",
    "course/modules/FC/FC1/grader/instance.py",
    "PASS", f"`{scripts}/check_instances_r15.py` (python -I): seeds 0-19 (and all of 0-49) lie in the stated ranges (face 100000-5000000, coupon 100-900 bps, periods 1-8, yield 50-900 bps, quantity 1-500, price 5000-150000, side +-1, settlement 1-5); 'range violations (seeds 0-49): []' ({out}/instances_r15.out)."))
R.append(row("proj-instances-50", "2.6-instances",
    "course/modules/FC/FC1/grader/instance.py; grader/reference.py",
    "PASS", f"Same script: over seeds 0-49 the reference gives 50 distinct bond prices, 50 distinct bond event lists, 50 distinct trade events and 50 distinct answer tuples ({out}/instances_r15.out). The answers change, not only the labels."))
R.append(row("proj-starter-vs-spec", "2.6-spec",
    "course/modules/FC/FC1/grader/starter.py; project.html line 161",
    "PASS", f"Signatures of Bond, Bond.events, bond_price_cents, CashTrade and CashTrade.events are identical in starter.py and reference.py ({out}/instances_r15.out). The starter run fails 50/50 seeds with property-naming messages and no traceback (grep -c traceback = 0)."))
R.append(row("proj-spec-questions", "2.6-spec",
    "course/modules/FC/FC1/project.html lines 153-172",
    "PASS", "The spec gives the names, signatures, sign convention (line 179), period indexing (line 177), rounding rule (line 176), the eight named conditions (lines 165-167) and the output types (line 163). The one unstated detail, whether a named refusal is raised at construction or at events(), does not block the student: test_project.py wraps both calls in must_raise (lines 215-274, 684-694)."))
R.append(row("proj-ladder", "2.6-ladder",
    "course/modules/FC/FC1/project.html lines 41-50; course/modules/FC/FC1/index.html lines 122-128",
    "PASS", "Four rungs in order (ol.ladder). Rung 1 is Lab 1, fully solved and annotated (lines 56-102). Rung 2 is Lab 2, the completion problem with blanks (lines 104-150). Rung 3 is the spec (lines 153-172). Rung 4 is the stretch (lines 312-318). The placement pass names two data-skill items, and index.html lines 122 and 127 mark exactly two."))
R.append(row("proj-stretch-scope", "2.6-scope",
    "course/modules/FC/FC1/project.html section#stretch lines 312-318",
    "PASS", "Line 314 states 'Not graded'. The limit-order-book extension refers to Lesson 4 (price-time priority, in FC1 L04.html), and the odd-first-period extension states its own coupon convention (line 317)."))
R.append(row("proj-local-command", "2.6-local-run",
    "course/modules/FC/FC1/project.html section#local lines 305-310; grader/starter.py docstring",
    "PASS", f"Ran `QF_SEED=0 pytest -q -p no:cacheprovider --assert=plain -W error test_project.py` in a scratch directory with the reference as instruments.py: '97 passed'. The command matches page line 308 and starter.py docstring."))
R.append(row("proj-lab1-twin", "2.5-lab",
    "course/modules/FC/FC1/project.html lab-FC1-project-1 (lines 56-102); tests/labs/FC1/lab-FC1-project-1.py",
    "PASS", f"`{scripts}/page_vs_twin_r15.py`: the page's run block 1 has 0 differing lines from the twin; `python -I -W error` exits 0 and its output equals the page's expected block ({out}/page_vs_twin_r15.out). run_labs FC1 8/8 PASS ({out}/run_labs_FC1.out)."))
R.append(row("proj-lab2-completion", "2.5-lab",
    "course/modules/FC/FC1/project.html lab-FC1-project-2 (lines 104-150); tests/labs/FC1/lab-FC1-project-2.py",
    "PASS", f"The page's run block differs from the twin only in the two blanks (`** ___` line 133, `(settlement_day, ___)` line 140), as {out}/page_vs_twin_r15.out shows; the twin's output equals the expected block there too. The completion tolerance is data-tolerance 1e-6 with |a-e| <= tol*(1+|e|) (course/assets/js/labs.js line 50; tools/coursekit.py line 329): 1e-6 * 102775 = about 0.10 cent, as the page says (line 149)."))
R.append(row("proj-lab2-docstring", "2.9-prose",
    "course/modules/FC/FC1/project.html line 107; tests/labs/FC1/lab-FC1-project-2.py line 1",
    "PASS", "Previous FAIL fixed. Both lines read 'Rung 2 completed solution: the worked example with its two blanks filled in.' (diff of the page block against the twin shows no docstring difference)."))
R.append(row("proj-lab3-fixtures", "2.5-lab",
    "course/modules/FC/FC1/project.html lab-FC1-project-3 (lines 196-276); tests/labs/FC1/lab-FC1-project-3.py",
    "PASS", f"Page run block equals the twin (0 differing lines) and the twin's output equals the expected block ({out}/page_vs_twin_r15.out). Every printed value re-derived in {out}/numbers_r15.out. Lab 3 interpretation (line 276) says which fixtures the autograder checks; grep of test_project.py: fixture G events [(1, 10001)] and the rounding case's events are never asserted as lists (fixture G price at lines 427-433; rounding price at lines 408-416, and the events are not compared), while fixtures A, C, D, F and E events are (lines 177, 192, 200, 245, 551)."))
R.append(row("proj-prose-numbers", "2.2-numbers",
    "course/modules/FC/FC1/project.html lines 54, 58, 101, 171, 176, 186-193, 198, 275, 290, 293",
    "PASS", f"`{scripts}/numbers_r15.py` (python -I) re-derives every number on the page: exact PV 102775.091033 and price 102775; 11052.6316 (210000/19) and 11053; fixture C 5001 and 15002; fixture D 2; fixture F 1/2 (round() gives 0, half-away 1); fixture G 5000.5 -> 5001; rounding case 10277.509103 -> 10278, terms 480.77/462.28/9334.46 -> 481+462+9334 = 10277; 97 checks; yield limits 150-100000 % and 10^16 % (10^18 bps); 'two sources'; 20 hours and 70 hours. Output in {out}/numbers_r15.out."))
R.append(row("proj-fixture-claims", "2.4-math",
    "course/modules/FC/FC1/project.html lines 183-194 and 276; grader/test_project.py lines 174-200, 245, 396-480",
    "PASS", f"Fixtures A-G and the rounding fixture re-derived in {out}/numbers_r15.out. The 'exact' claims: 496 bps case = 3305625/2 cents (test line 435); 13/1.04 = 12.5 exact and the float path gives 12.499999999999998 (line 460); just-under case equals 1/2 - 1/(2*1000300030001) (line 471)."))
R.append(row("proj-hours-arithmetic", "2.9-hours",
    "course/modules/FC/FC1/project.html section#budget lines 283-293; course/modules/FC/FC1/index.html lines 29-41",
    "PASS", "Budget rows 1+2+5+4+2+3+3 = 20 (lines 286-292), total 20 (line 293). Hub data-hours-lessons=50 and data-hours-project=20 (index.html line 29), 50 + 20 = 70 (line 31), 20/70 = 28.6 % (line 41). Five lessons of 10 h (index.html lines 137-143) = 50 h."))
R.append(row("proj-check-pages-dag", "2.9-structure",
    "course/modules/FC/FC1/ (project.html)",
    "PASS", f"`tools/check_pages.py --unit FC1`: 'check_pages FC1: PASS'; `tools/check_dag.py --unit FC1`: 'check_dag FC1: PASS'; `tools/check_projects.py --unit FC1`: 'check_projects FC1: PASS' ({out}/check_pages.out, check_dag.out, check_projects.out)."))
R.append(row("proj-dag-closure", "2.9-dag",
    "course/modules/FC/FC1/project.html lines 58, 178, 316; curriculum/curriculum.json (prerequisite closure)",
    "PASS", "Closure of FC1 computed from curriculum.json prereqs: {E1, FC1, M1, M2, P0.1}. present-value and discount-factor (links at lines 178, 58) are defined in M1 (course/modules/M/M1/L05.html lines 65, 70), inside the closure. Lesson 4 and Lesson 5 references are the unit's own. Out of slice: course/modules/FC/FC1/L05.html lines 397, 625 and 632 use 'settlement period' before this page's <dfn> (line 54); see notes."))
R.append(row("proj-notation", "2.4-notation",
    "course/modules/FC/FC1/project.html math (\\(y\\), \\(t\\), \\(1+y\\), \\(y = 400/10000\\)); notation/notation.json",
    "PASS", "The page's only symbols are y (per-period yield) and t (period). grep of `\\(...\\)` on the page returns \\(1+y\\), \\(t\\) (x3) and \\(y = 400/10000\\). notation.json registers T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} and macros \\E, \\Prob, ...; none collides, and the page uses no macro."))
R.append(row("proj-banned-phrases", "2.9-prose",
    "course/modules/FC/FC1/project.html; grader/*.py; tests/labs/FC1/lab-FC1-project-*.py",
    "PASS", "grep (case-insensitive) of BUILDER_RULES §1.3-1.4 and §8 strings (TODO, TBD, lorem, ellipsis, for brevity, beyond the scope, it is important to note, obviously, clearly, well known, about N %, roughly, historically, let us, we will, note that, simply, just, easy) on project.html, grader/*.py and the three twins: 0 hits (the only match is the type ellipsis in Callable[..., None] on line 797 of the grader, which is not learner text). Process words (verifier, ledger, round, builder, fixed): 0 hits; 'a reviewer reads it' (lines 163, 161) is about a human reviewer."))
R.append(row("proj-reading-list", "2.9-citations",
    "course/modules/FC/FC1/project.html lines 321-327; references/references.json (mishkin2021economics, harris2002trading)",
    "PASS", f"Carried from round 14 (project.html lines 321-327 and references/references.json byte-identical since the round-14 pin, per git diff): both keys exist in references/references.json (character offsets 309368 and 205026 in the JSON). `tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems' ({out}/verify_refs_offline_all.out). The live `verify_refs --unit FC1` run was not repeated in this round. The page states no year and attributes no statement to either source. The FC1 course pages cite exactly these two keys (grep of data-cite and registry keys in FC1 html)."))
R.append(row("proj-scope-ruling5", "2.6-scope",
    "course/modules/FC/FC1/project.html line 157; curriculum/02-economics-finance-core.yaml lines 388-395; plans/FINAL-ARCHITECT-RULINGS.md ruling 5 (lines 11-13)",
    "PASS", "The brief in the YAML ('Represent a fixed-rate bond and a trade that settles later ... Futures, swaps and options follow in FC2') matches page line 157, which excludes futures, swaps and options and names FC2. Ruling 5 is unchanged by the delta (rulings 26-29 appended)."))
R.append(row("proj-named-conditions", "2.6-autograde-mutation",
    "course/modules/FC/FC1/project.html lines 163-167; grader/test_project.py must_raise and must_accept call sites",
    "PASS", "The eight named conditions (lines 165-167) each have a refusal test and a boundary acceptance test. Bond: periods 0 (line 215) and -1 (220) refused, 1 accepted (225); face 0 (232) and -1 (237) refused, 1 accepted (242); coupon -1 refused (258), 0 accepted (263). bond_price_cents: yield -10000 (511) and -20000 (516) refused, -9999 accepted (521). CashTrade: quantity 0 (571) and -1 (576) refused, 1 accepted (581); price -1 refused (620), 0 accepted (625); side 0, 2, -2, 3, -3 refused (633-653), +1 and -1 accepted (658); settlement 0 (666) and -1 (671) refused, 1 accepted (676). Sell-side and zero-coupon refusals are at lines 268-278 and 684-694."))
R.append(row("proj-named-conditions-context", "2.6-autograde-mutation",
    "course/modules/FC/FC1/project.html lines 163 and 167; grader/test_project.py lines 268-278 (zero-coupon refusals) and 684-694 (sell-side refusals)",
    "PASS", f"Previous FAIL fixed. The five tests the previous round asked for are present: sale quantity 0 (line 684), sale price -1 (689), sale settlement 0 (694), zero-coupon periods 0 (268) and zero-coupon face 0 (274). With them, mutants r14n01 and r14n05 are KILLED (see {out}/mutate_FC1_s0-9_final.out)."))
R.append(row("proj-failure-messages", "2.6-messages",
    "course/modules/FC/FC1/grader/test_project.py (all assertions, must_raise, must_accept, checked_events, checked_int, _named_when_unimplemented)",
    "PASS", "All messages were read (grep of assert/pytest.fail messages). They name the property and give a concept hint, and none contains an answer value. The one run of --assert=plain showed only 'AssertionError: <message>' and no values (scratch run with mutant r15n02)."))
R.append(row("proj-test-docstring", "2.4-docstrings",
    "course/modules/FC/FC1/grader/test_project.py docstrings (e.g. lines 293-300, 408-413, 435-444, 446-452, 460-464, 527-531, 849-851, 866-869, 876-879, 908-912, 956-961, 996-1002)",
    "PASS", f"Every number in the docstrings was re-derived in {out}/numbers_r15.out: 1652812.4999999998 (float path, lines 435-444), 12.499999999999998 (lines 460-464), 10277.5091 and terms 480.77/462.28/9334.46 (lines 408-413), 100/(10**14+1) (lines 996-1002), 103.96 and 10.49 (lines 908-912, 956-961), 10500/21 = 500 (lines 876-879), 10500/2.5 = 4200 (lines 527-531), 2625 (lines 849-851). The docstring claim that a ten-significant-digit decimal context drops the half (lines 446-452) was checked: 5000000000.5 rounds to 5000000000. Nit: the name test_trade_settling_after_period_one_hundred_is_accepted (line 858) tests period 1000; the docstring is correct."))
R.append(row("proj-simulated-labels", "2.8-simulated",
    "course/modules/FC/FC1/project.html lines 54, 72, 120, 159; grader/instance.py label",
    "PASS", "Line 54 'both SIMULATED'; line 72 comment 'SIMULATED face of 1,000.00'; line 120 same; line 159 'The values are SIMULATED'; instance.py label 'SIMULATED bond and trade, seed N: not market data' (checked for seed 0)."))
R.append(row("proj-silence-coverage", "2.6-silence",
    "course/modules/FC/FC1/project.html line 163; grader/test_project.py lines 720-762",
    "PASS", "The page says no function prints or warns on the checked inputs. test_the_module_prints_nothing (720) lists 14 valid inputs and test_refused_inputs_print_nothing_before_they_raise (746) lists 8 refusals, each with capsys. pytestmark filterwarnings('error') (line 30) turns any warning into a failure."))
R.append(row("proj-privacy-claim", "2.9-privacy",
    "course/modules/FC/FC1/project.html line 341; course/assets/js/grader.js; course/assets/js/py-worker.js; course/assets/js/store.js",
    "PASS", "grader.js sends no request (only fetches the panel's own suite and support files from grader/, and writes the draft with store.put). Pyodide is loaded from ../vendor/pyodide (py-worker.js line 10 and 18). grep for http(s):// and fetch/XMLHttpRequest/sendBeacon in grader.js, py-worker.js and store.js: no external host. page_smoke reports zero requests to other hosts for the project page."))
R.append(row("proj-lint-types", "2.6-lint",
    "course/modules/FC/FC1/grader/*.py; tests/labs/FC1/*.py",
    "PASS", f"`ruff check` and `ruff format --check` on grader and tests/labs/FC1: 'All checks passed!', '12 files already formatted' ({out}/ruff_check.out). `mypy --no-incremental` on the repo: 'Success: no issues found in 385 source files' ({out}/mypy_repo.out)."))
R.append(row("proj-reference-deployment", "2.6-deployment",
    "course/modules/FC/FC1/grader/reference.py lines 3-4; BLUEPRINT.md lines 400-401",
    "PASS", "The docstring says BLUEPRINT requires that deployment exclude reference.py, and that no file enforces it. BLUEPRINT.md lines 400-401 state the exclusion, and ruling 4 records that no deploy step exists yet. The statement is accurate; the enforcement gap is a registry flag, not a slice defect."))
R.append(row("proj-exemplar-blind", "2.3-rubric",
    "course/modules/FC/FC1/project.html; curriculum grading for FC1 project",
    "PASS", "grep of project.html for rubric and exemplar: 0 matches. The FC1 project is graded 'autograder' only (curriculum.json), so no rubric or exemplar calibration applies."))
R.append(row("proj-mutant-set-earlier", "2.6-mutation",
    "ledgers/FC1/mutants/ (136 files that existed at the round-14 pin)",
    "PASS", f"All 136 earlier mutant files are KILLED in the final run ({out}/mutate_FC1_s0-9_final.out; see the mutants array)."))
R.append(row("proj-mutant-first-line", "2.6-mutation",
    "ledgers/FC1/mutants/*.py (every file's first docstring line)",
    "PASS", f"`tools/mutate_graders.py` printed a description for every mutant: 'no description' count = 0 ({out}/mutate_FC1_s0-9_final.out). Each first docstring line names the student error."))
R.append(row("proj-new-mutants-r10", "2.6-mutation",
    "ledgers/FC1/mutants/r10n01..r10n04; r10c_*", "PASS", f"All killed in the final run ({out}/mutate_FC1_s0-9_final.out)."))
R.append(row("proj-new-mutants-r11", "2.6-mutation",
    "ledgers/FC1/mutants/r11n01..r11n03; r11c_*", "PASS", f"All killed in the final run ({out}/mutate_FC1_s0-9_final.out)."))
R.append(row("proj-new-mutants-r12", "2.6-mutation",
    "ledgers/FC1/mutants/r12n01..r12n03; r12c_*", "PASS", f"All killed in the final run ({out}/mutate_FC1_s0-9_final.out)."))
R.append(row("proj-mutant-r13n01", "2.6-mutation",
    "ledgers/FC1/mutants/r13n01_coupon_computed_in_float.py; grader/test_project.py test_bond_coupon_is_exact_for_a_face_too_large_for_floats (line 178-189)",
    "PASS", f"KILLED by test_bond_coupon_is_exact_for_a_face_too_large_for_floats ({out}/mutate_FC1_s0-9_final.out)."))
R.append(row("proj-mutant-r13n02", "2.6-mutation",
    "ledgers/FC1/mutants/r13n02_trade_cash_flow_in_float.py; grader/test_project.py test_trade_cash_flow_is_exact_above_two_to_the_fifty_three",
    "PASS", f"KILLED by test_trade_cash_flow_is_exact_above_two_to_the_fifty_three ({out}/mutate_FC1_s0-9_final.out)."))
R.append(row("proj-mutant-r13n03", "2.6-mutation",
    "ledgers/FC1/mutants/r13n03_yield_rate_through_float.py; grader/test_project.py test_bond_price_exact_half_cent_at_400_bps_uses_the_exact_yield (line 460)",
    "PASS", f"KILLED by test_bond_price_exact_half_cent_at_400_bps_uses_the_exact_yield ({out}/mutate_FC1_s0-9_final.out)."))
R.append(row("proj-new-mutants-r14-killed", "2.6-mutation",
    "ledgers/FC1/mutants/r14n02, r14n03, r14n04", "PASS", f"All killed in the final run ({out}/mutate_FC1_s0-9_final.out)."))
R.append(row("proj-mutant-r14n01", "2.6-mutation",
    "ledgers/FC1/mutants/r14n01_sale_skips_quantity_and_settlement_checks.py; grader/test_project.py line 684",
    "PASS", f"Previous FAIL fixed: KILLED by test_sale_quantity_zero_is_refused ({out}/mutate_FC1_s0-9_final.out)."))
R.append(row("proj-mutant-r14n05", "2.6-mutation",
    "ledgers/FC1/mutants/r14n05_bond_periods_and_face_checked_only_with_a_coupon.py; grader/test_project.py line 268",
    "PASS", f"Previous FAIL fixed: KILLED by test_bond_zero_coupon_periods_zero_is_refused ({out}/mutate_FC1_s0-9_final.out)."))
R.append(row("proj-new-mutants-r15-killed", "2.6-mutation (new in round 15)",
    "ledgers/FC1/mutants/r15n01..r15n04",
    "PASS", f"Four new student-error mutants, all KILLED in the final run ({out}/mutate_FC1_s0-9_final.out): r15n01 decimal at default precision (killed by test_bond_price_exact_half_above_forty_significant_digits_is_exact, line 866); r15n02 face added again on each events() call (killed by test_repeated_events_calls_agree, line 764, and the 13-15 periods test); r15n03 yield refused only at -10000 (killed by test_yield_below_minus_one_is_refused, line 516); r15n04 zero-coupon periods skipped in discounting (killed by test_bond_price_just_under_a_half_cent_rounds_down, line 471)."))
R.append(row("proj-mutant-r15n05", "2.6-mutation (new in round 15)",
    "ledgers/FC1/mutants/r15n05_price_refused_above_one_million_cents.py; grader/test_project.py CashTrade tests (lines 571-699); project.html lines 163 and 167",
    "FAIL", f"SURVIVED seeds 0-9 and 0-49 ({out}/mutate_FC1_s0-9_final.out; ledgers/FC1/scripts/FC1-c-r15/alt_run_r15.py): CashTrade refuses price_cents above 1000000, which no test sees, because the largest price any test passes is the seeded price (at most 150000 over seeds 0-49, instance.py) or the literal 9851 (lines 609-615); no test checks a price above those. project.html line 163 says 'Each named condition below raises ValueError. Any other invalid input may raise any exception or return.' and line 167 names only 'price_cents negative' as refused for CashTrade. The plan (plans/FC1-build-plan.md line 252, section 5.2) says 'Valid input (exception table, section 5.4 only)'. A price of 10**7 is valid under those sentences and the grading text (line 171: accepted 'because the page names no upper limit'), so refusing it is a student error the suite must catch.",
    "Add to grader/test_project.py a must_accept check, for example `must_accept(lambda: sol.CashTrade(10, 10**9, 1, 2).events(), 'price_cents = 10**9')` with a rule that the event is (2, -10**10), and state the same case in the page's accepted list (line 171). Re-run tools/mutate_graders.py --unit FC1 --seeds 0-9: r15n05 must be KILLED."))
R.append(row("proj-mutant-r15n06", "2.6-mutation (new in round 15)",
    "ledgers/FC1/mutants/r15n06_coupon_refused_above_twenty_thousand_bps.py; grader/test_project.py test_bond_coupon_above_one_hundred_percent_is_accepted (line 344); project.html lines 163 and 165",
    "FAIL", f"SURVIVED seeds 0-9 and 0-49 ({out}/mutate_FC1_s0-9_final.out): Bond refuses coupon_bps above 20000. The suite's largest accepted coupon is 15000 (line 344-350). project.html line 165 names only 'coupon_bps negative' for Bond, and line 163 gives the same sentences as for r15n05; plans/FC1-build-plan.md section 5.2 says 'Valid input (exception table, section 5.4 only)'.",
    "Add a must_accept check such as `must_accept(lambda: sol.Bond(10_000, 20_001, 1).events(), 'coupon_bps = 20001')` with the event (1, 30001), and list it in the accepted-input text (line 171). Re-run tools/mutate_graders.py --unit FC1 --seeds 0-9: r15n06 must be KILLED."))
R.append(row("proj-mutants-killed", "2.6-mutation",
    "ledgers/FC1/mutants/ (147 files); grader/test_project.py",
    "FAIL", f"`tools/mutate_graders.py --unit FC1 --seeds 0-9` -> 'mutate_graders FC1: FAIL (145/147 killed)' ({out}/mutate_FC1_s0-9_final.out). Survivors: r15n05_price_refused_above_one_million_cents and r15n06_coupon_refused_above_twenty_thousand_bps (see their rows).",
    "Add the two accepted-input checks given in proj-mutant-r15n05 and proj-mutant-r15n06 to grader/test_project.py; then require 147/147 killed."))
R.append(row("proj-run-labs", "2.5-labs",
    "tests/labs/FC1 (all eight twins)",
    "PASS", f"`tools/run_labs.py --unit FC1`: 'run_labs FC1: PASS (8/8)' ({out}/run_labs_FC1.out). Each project twin run alone under `python -I -W error` exits 0 (rc=0 for project-1, -2 and -3)."))
R.append(row("proj-page-smoke", "2.9-page-smoke",
    "course/modules/FC/FC1/project.html",
    "PASS", f"`tools/page_smoke.py --unit FC1 --pages project` (the stem, not the file name: a first attempt with 'project.html' matched no page and is not evidence) -> 'page_smoke modules/FC/FC1/project.html: PASS', 'page_smoke FC1: PASS' ({out}/page_smoke_FC1_project.out). Labs 1-3 and the in-browser grader pass."))
R.append(row("proj-check-projects", "2.6-structure",
    "course/modules/FC/FC1/project.html; grader panel attributes",
    "PASS", f"`tools/check_projects.py --unit FC1`: 'check_projects FC1: PASS' ({out}/check_projects.out)."))
R.append(row("proj-pytest-targeted", "2.9-tests",
    "tests/test_curriculum.py; tests/test_labs.py; tests/test_page_checks.py; tests/test_run_labs.py (selected by -k 'FC1 or project or grader or FC')",
    "PASS", f"`pytest -q tests/test_curriculum.py tests/test_labs.py -k 'FC1 or project or grader'` and `pytest -q tests/test_page_checks.py tests/test_run_labs.py -k 'FC1 or project or grader or FC'`: both exit 0 ({out}/pytest_targeted_r15.out, pytest_page_run_labs_r15.out)."))

verified_at = datetime.now(UTC).replace(microsecond=0).isoformat()
fails = [r["id"] for r in R if r["status"] != "PASS"]
fragment = {
    "unit": "FC1",
    "slice": "c",
    "round": 15,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-c, round 15 (did not build FC1)",
    "pin": "dde0486beeb0312e4ac1cc03aaa02e56644adb24",
    "base": "1431aa1d842a5d2d05fd5953c098500bf78a4307 (round-14 pin). Delta 1431aa1d..dde0486b in the slice: course/modules/FC/FC1/project.html (8 lines), grader/test_project.py (+27 lines: five new tests), tests/labs/FC1/lab-FC1-project-2.py (docstring), ledgers/FC1/mutants/r14n01-r14n05 (added in this delta), plans/FINAL-ARCHITECT-RULINGS.md (rulings 26-29 appended), plans/KNOWN-ISSUES.md (new). Every row was re-verified from the pin; no round-14 PASS row was carried, except proj-reading-list (its cited lines and references/references.json are byte-identical since 1431aa1d).",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD15-FC1-c",
    "scratch": f"{scripts}/ (scripts, probes, alternatives and out/)",
    "verified_at": verified_at,
    "verdict": "FAIL",
    "rows": R,
    "mutants": mutants,
    "registry_flags": [
        "mishkin2021economics: registry year 2021 (Open Library record; curriculum sources say 13th ed. (2022)). The project page states no year; a published-version check was not done.",
        "harris2002trading: registry years [2002, 2023] (curriculum sources say Harris, Trading and Exchanges (2003)). The project page states no year.",
        "curriculum/02-economics-finance-core.yaml FC1 sources list McLeay, Radia & Thomas (2014); no FC1 course page cites it (outside this slice).",
        "grader/reference.py is git-tracked; the BLUEPRINT deployment exclusion is not enforced (ruling 4: recorded, not a slice defect).",
    ],
    "freshness_flags": [],
    "notes": (
        "Round 15, FC1-c, pin dde0486b (detached HEAD in the checkout). Delta 1431aa1d..dde0486b read in full for the slice: "
        "project.html (hunks at lines 46, 54, 107 and 171; the rest unchanged), grader/test_project.py (five new tests at lines 268-278 and 684-694), "
        "tests/labs/FC1/lab-FC1-project-2.py (docstring), mutants r14n01-r14n05 (new). Previous FAIL rows: proj-lab2-docstring, "
        "proj-named-conditions-context, proj-mutant-r14n01, proj-mutant-r14n05, proj-mutants-killed; all now PASS except proj-mutants-killed, "
        "which fails on two new survivors. Verdict FAIL: 3 rows (proj-mutant-r15n05, proj-mutant-r15n06, proj-mutants-killed). "
        "Results: run_graders 50/50; collect 97; page_smoke project PASS (labs and in-browser grader); run_labs 8/8; check_pages, check_dag, "
        "check_projects PASS; ruff and mypy PASS; mutate_graders 145/147; alternatives a1-a5, the round-14 integer-only alternative and two new "
        "alternatives (decimal at 100 digits; cached lists) all pass seeds 0-49; instances: 50 distinct answers. "
        "New student-error mutants written this round: r15n01-r15n04 (all killed). Two upper-limit mutants (r15n05, r15n06) survive and are FAILs. "
        "Scripts are under ledgers/FC1/scripts/FC1-c-r15/. Out-of-slice observations (not rows of this slice): "
        "course/modules/FC/FC1/L05.html lines 397, 625 and 632 use 'settlement period' before project.html line 54 defines it with <dfn>; "
        "the term is not in course/assets/data/glossary.json. Not checked: the live verify_refs --unit FC1 run (network), the cards, the lessons, "
        "the hub's placement quiz items other than the two skill checks, and Pyodide timing per test (page_smoke ran the whole suite in-browser in under 1 s)."
    ),
    "summary": (
        f"FC1-c round 15 at dde0486b: FAIL. Rows {len(R)}: PASS {sum(r['status']=='PASS' for r in R)}, FAIL {len(fails)}, UNVERIFIABLE 0. "
        f"Mutants {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed. Failing rows: {', '.join(fails)}."
    ),
}
target = checkout / "ledgers/FC1/FC1-c.json"
target.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", target, "rows", len(R), "mutants", len(mutants), "fails", fails)
